/*
 * Mini-HPL - Version corrigée
 *
 * Corrections appliquées :
 *   1. find_global_pivot() supprimée (placeholder inutilisable)
 *   2. MPI_2DOUBLE_PRECISION remplacé par MPI_DOUBLE_INT (standard C)
 *   3. Pivot quasi-nul : arrêt propre via MPI_Abort (plus de division par ~0)
 *   4. Contrainte N % (NB*size) == 0 conservée mais clairement documentée
 *   5. GFLOPS renommés "approximatifs (modèle 2/3 N^3)"
 *
 * Compilation : mpicc -O2 -Wall -o mini_hpl mini_hpl.c -lm
 * Exécution   : mpirun -np 4 ./mini_hpl 1024
 *               mpirun -np 4 ./mini_hpl 1024 128   (NB=128)
 *
 * Contrainte  : N doit être divisible par (NB * nb_processus).
 *               Simplification pédagogique : les blocs partiels
 *               ne sont pas gérés (voir ScaLAPACK pour le cas général).
 */

#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

/* Accès à l'élément (i,j) d'une matrice de largeur N stockée en row-major */
#define IDX(i, j, N) ((i) * (N) + (j))

/* Distribution bloc-cyclique 1D :
 *   OWNER(gi)    = processus propriétaire de la ligne globale gi
 *   LOCAL_LI(gi) = indice local de gi sur son propriétaire
 * Ces macros supposent que NB et size sont visibles dans la portée. */
#define OWNER(gi)    (((gi) / NB) % size)
#define LOCAL_LI(gi) ((((gi) / NB) / size) * NB + (gi) % NB)

/* ------------------------------------------------------------------ */
/* Initialisation de la matrice augmentée [A | b]                      */
/* Chaque processus initialise uniquement ses lignes locales.           */
/* La matrice est rendue diagonalement dominante pour garantir          */
/* l'inversibilité et éviter les pivots nuls lors des tests.           */
/* ------------------------------------------------------------------ */
void initialize_matrix(double *A, double *b,
                        int N, int NB,
                        int local_rows, int rank, int size)
{
    for (int li = 0; li < local_rows; li++) {
        int panel_local  = li / NB;
        int within_panel = li % NB;
        int global_i     = (panel_local * size + rank) * NB + within_panel;

        for (int j = 0; j < N; j++) {
            if (j == global_i)
                A[IDX(li, j, N)] = (double)N + (double)(global_i + j + 1) / N;
            else
                A[IDX(li, j, N)] = (double)(global_i + j + 1) / N;
        }
        b[li] = 1.0;
    }
}

/* ================================================================== */
/* PROGRAMME PRINCIPAL                                                  */
/* ================================================================== */
int main(int argc, char **argv)
{
    MPI_Init(&argc, &argv);
    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    if (argc < 2) {
        if (rank == 0) printf("Usage: %s N [NB]\n", argv[0]);
        MPI_Finalize();
        return 0;
    }
    int N  = atoi(argv[1]);
    int NB = (argc >= 3) ? atoi(argv[2]) : 64;

    /*
     * Contrainte simplificatrice (pédagogique) :
     * N doit être divisible par NB*size pour que chaque processus
     * possède exactement le même nombre de lignes entières.
     * Dans ScaLAPACK, les blocs partiels sont gérés mais complexifient
     * significativement le code.
     */
    if (N % (NB * size) != 0) {
        if (rank == 0)
            fprintf(stderr,
                "ERREUR : N (%d) doit etre divisible par NB*size = %d*%d = %d\n"
                "Simplification pedagogique : blocs partiels non geres.\n",
                N, NB, size, NB * size);
        MPI_Finalize();
        return 1;
    }

    int num_panels_local = (N / NB) / size;
    int local_rows       = num_panels_local * NB;

    double *A         = malloc((size_t)local_rows * N * sizeof(double));
    double *b_vec     = malloc((size_t)local_rows     * sizeof(double));
    double *pivot_row = malloc((size_t)(N + 1)        * sizeof(double));
    double *tmp_row   = malloc((size_t)(N + 1)        * sizeof(double));

    if (!A || !b_vec || !pivot_row || !tmp_row) {
        fprintf(stderr, "[rank %d] Echec malloc\n", rank);
        MPI_Abort(MPI_COMM_WORLD, 1);
    }

    initialize_matrix(A, b_vec, N, NB, local_rows, rank, size);

    MPI_Barrier(MPI_COMM_WORLD);
    double t_start = MPI_Wtime();

    /* ================================================================ */
    /* ÉLIMINATION DE GAUSS AVEC PIVOTAGE PARTIEL                       */
    /* ================================================================ */
    for (int k = 0; k < N; k++) {

        int k_owner = OWNER(k);
        int k_li    = LOCAL_LI(k);

        /* ---- Étape 1 : recherche du pivot maximal (MPI_DOUBLE_INT) -- */
        /*
         * MPI_DOUBLE_INT est le type MPI standard C pour les paires
         * {double, int}. MPI_MAXLOC retourne la paire dont le double
         * est maximal. Tous les processus reçoivent le résultat.
         *
         * ATTENTION : MPI_2DOUBLE_PRECISION est un type Fortran,
         * non garanti en C — on utilise MPI_DOUBLE_INT à la place.
         */
        struct { double val; int idx; } local_cand, global_cand;
        local_cand.val = 0.0;
        local_cand.idx = -1;

        for (int li = 0; li < local_rows; li++) {
            int panel_local  = li / NB;
            int within_panel = li % NB;
            int gi = (panel_local * size + rank) * NB + within_panel;
            if (gi < k) continue;
            double v = fabs(A[IDX(li, k, N)]);
            if (v > local_cand.val) {
                local_cand.val = v;
                local_cand.idx = gi;
            }
        }

        MPI_Allreduce(&local_cand, &global_cand, 1,
                      MPI_DOUBLE_INT, MPI_MAXLOC, MPI_COMM_WORLD);

        int pivot_gi    = global_cand.idx;
        int pivot_owner = OWNER(pivot_gi);
        int pivot_li    = LOCAL_LI(pivot_gi);

        /* ---- Étape 2 : échange de lignes (swap) -------------------- */
        if (pivot_gi != k) {
            if (rank == k_owner && rank == pivot_owner) {
                for (int j = 0; j < N; j++) {
                    double tmp             = A[IDX(k_li,     j, N)];
                    A[IDX(k_li,     j, N)] = A[IDX(pivot_li, j, N)];
                    A[IDX(pivot_li, j, N)] = tmp;
                }
                double tmp      = b_vec[k_li];
                b_vec[k_li]     = b_vec[pivot_li];
                b_vec[pivot_li] = tmp;

            } else if (rank == k_owner) {
                memcpy(tmp_row, &A[IDX(k_li, 0, N)], N * sizeof(double));
                tmp_row[N] = b_vec[k_li];
                MPI_Sendrecv(tmp_row,  N + 1, MPI_DOUBLE, pivot_owner, 0,
                             pivot_row, N + 1, MPI_DOUBLE, pivot_owner, 0,
                             MPI_COMM_WORLD, MPI_STATUS_IGNORE);
                memcpy(&A[IDX(k_li, 0, N)], pivot_row, N * sizeof(double));
                b_vec[k_li] = pivot_row[N];

            } else if (rank == pivot_owner) {
                memcpy(tmp_row, &A[IDX(pivot_li, 0, N)], N * sizeof(double));
                tmp_row[N] = b_vec[pivot_li];
                MPI_Sendrecv(tmp_row,  N + 1, MPI_DOUBLE, k_owner, 0,
                             pivot_row, N + 1, MPI_DOUBLE, k_owner, 0,
                             MPI_COMM_WORLD, MPI_STATUS_IGNORE);
                memcpy(&A[IDX(pivot_li, 0, N)], pivot_row, N * sizeof(double));
                b_vec[pivot_li] = pivot_row[N];
            }
        }

        /* ---- Étape 3 : broadcast de la ligne pivot ----------------- */
        if (rank == k_owner) {
            memcpy(pivot_row, &A[IDX(k_li, 0, N)], N * sizeof(double));
            pivot_row[N] = b_vec[k_li];
        }
        MPI_Bcast(pivot_row, N + 1, MPI_DOUBLE, k_owner, MPI_COMM_WORLD);

        /*
         * Vérification du pivot APRÈS le broadcast : tous les processus
         * ont la même valeur, donc la décision d'abort est cohérente.
         * On n'appelle PAS MPI_Abort uniquement depuis rank==0 car
         * MPI_Abort doit être appelé collectivement (ou depuis n'importe
         * quel rang, MPI le propage à tous).
         */
        double pivot_val = pivot_row[k];
        if (fabs(pivot_val) < 1e-14) {
            if (rank == 0)
                fprintf(stderr,
                    "ERREUR : pivot quasi-nul a k=%d (|pivot|=%.2e).\n"
                    "Matrice singuliere ou mal conditionnee. Arret.\n",
                    k, fabs(pivot_val));
            MPI_Abort(MPI_COMM_WORLD, 2);
        }

        /* ---- Étape 4 : mise à jour SAXPY --------------------------- */
        for (int li = 0; li < local_rows; li++) {
            int panel_local  = li / NB;
            int within_panel = li % NB;
            int gi = (panel_local * size + rank) * NB + within_panel;
            if (gi <= k) continue;

            double factor = A[IDX(li, k, N)] / pivot_val;
            for (int j = k; j < N; j++)
                A[IDX(li, j, N)] -= factor * pivot_row[j];
            b_vec[li]        -= factor * pivot_row[N];
            A[IDX(li, k, N)]  = factor;   /* L stocké in-place */
        }
    }

    MPI_Barrier(MPI_COMM_WORLD);
    double t_elim = MPI_Wtime() - t_start;

    /* ================================================================ */
    /* BACK-SUBSTITUTION : résolution de Ux = b (de k = N-1 à 0)       */
    /* ================================================================ */
    double *x_global = calloc(N, sizeof(double));

    for (int k = N - 1; k >= 0; k--) {
        int k_owner = OWNER(k);
        int k_li    = LOCAL_LI(k);

        double x_k = 0.0;
        if (rank == k_owner) {
            double s = b_vec[k_li];
            for (int j = k + 1; j < N; j++)
                s -= A[IDX(k_li, j, N)] * x_global[j];
            x_k = s / A[IDX(k_li, k, N)];
        }
        MPI_Bcast(&x_k, 1, MPI_DOUBLE, k_owner, MPI_COMM_WORLD);
        x_global[k] = x_k;
    }

    double t_solve = MPI_Wtime() - t_start;

    /* ================================================================ */
    /* VÉRIFICATION DE LA RÉSIDUELLE NORMÉE HPL                         */
    /* r = ||Ax-b||_inf / (||A||_inf * ||x||_inf * N * eps)            */
    /* PASSED si r < 16                                                  */
    /* ================================================================ */
    double *A_orig = malloc((size_t)local_rows * N * sizeof(double));
    double *b_orig = malloc((size_t)local_rows     * sizeof(double));
    if (!A_orig || !b_orig) {
        fprintf(stderr, "[rank %d] Echec malloc residuelle\n", rank);
        MPI_Abort(MPI_COMM_WORLD, 1);
    }
    initialize_matrix(A_orig, b_orig, N, NB, local_rows, rank, size);

    double local_res_norm = 0.0;
    double local_A_norm   = 0.0;

    for (int li = 0; li < local_rows; li++) {
        double row_sum = 0.0, Ax_i = 0.0;
        for (int j = 0; j < N; j++) {
            row_sum += fabs(A_orig[IDX(li, j, N)]);
            Ax_i    += A_orig[IDX(li, j, N)] * x_global[j];
        }
        local_res_norm = fmax(local_res_norm, fabs(Ax_i - b_orig[li]));
        local_A_norm   = fmax(local_A_norm,   row_sum);
    }

    double x_norm = 0.0;
    for (int j = 0; j < N; j++)
        x_norm = fmax(x_norm, fabs(x_global[j]));

    double global_res_norm, global_A_norm;
    MPI_Reduce(&local_res_norm, &global_res_norm, 1,
               MPI_DOUBLE, MPI_MAX, 0, MPI_COMM_WORLD);
    MPI_Reduce(&local_A_norm,   &global_A_norm,   1,
               MPI_DOUBLE, MPI_MAX, 0, MPI_COMM_WORLD);

    /* ================================================================ */
    /* AFFICHAGE DES RÉSULTATS                                           */
    /* ================================================================ */
    if (rank == 0) {
        const double eps = 2.22e-16;
        double residual  = global_res_norm /
                           (global_A_norm * x_norm * N * eps);

        /*
         * GFLOPS approximatifs : modèle 2/3 * N^3 (standard HPL).
         * Ignore swaps, communications et back-substitution,
         * négligeables devant l'élimination pour les grands N.
         */
        double gflops = (2.0 / 3.0 * (double)N * N * N) / (t_elim * 1e9);

        printf("\n");
        printf("========================================\n");
        printf("  Mini-HPL -- Resultats                \n");
        printf("========================================\n");
        printf("  N              = %d\n",    N);
        printf("  NB (bloc)      = %d\n",    NB);
        printf("  Processus MPI  = %d\n",    size);
        printf("  Lignes/proc    = %d\n",    local_rows);
        printf("----------------------------------------\n");
        printf("  Temps elimination = %.4f s\n",  t_elim);
        printf("  Temps total       = %.4f s\n",  t_solve);
        printf("  GFLOPS approx.    = %.4f\n",    gflops);
        printf("  (modele 2/3 * N^3, hors comms)\n");
        printf("----------------------------------------\n");
        printf("  ||Ax-b||_inf      = %.2e\n",  global_res_norm);
        printf("  ||A||_inf         = %.2e\n",  global_A_norm);
        printf("  ||x||_inf         = %.2e\n",  x_norm);
        printf("  Residuelle normee = %.2e\n",  residual);
        if (residual < 16.0)
            printf("  Statut : PASSED (r < 16)\n");
        else
            printf("  Statut : FAILED (r >= 16)\n");
        printf("========================================\n\n");
    }

    free(A);       free(b_vec);    free(pivot_row);
    free(tmp_row); free(x_global);
    free(A_orig);  free(b_orig);

    MPI_Finalize();
    return 0;
}
