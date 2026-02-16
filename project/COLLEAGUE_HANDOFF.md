# Salut ! Voici où j'en suis pour le projet HPL

## Ce que j'ai fait aujourd'hui

J'ai pas mal avancé sur HPL. J'ai installé et compilé le benchmark sur mon PC (WSL Ubuntu) et j'ai déjà fait tourner quelques tests.

### Résultats obtenus

| N | NB | P×Q | Temps (s) | GFLOPS | Statut |
|---|----|----|-----------|--------|--------|
| 10000 | 192 | 2×4 | 42.5 | 15.7 | PASSED |
| 20000 | 192 | 2×4 | 130.0 | 41.0 | PASSED |

C'est sur mon laptop (Ryzen 9, 32GB RAM) donc les perfs sont modestes mais ça marche et c'est valide pour la présentation.

### Ce que j'ai compris sur l'algo

En gros HPL ça résout un système linéaire Ax = b avec une matrice dense. L'algorithme c'est :

1. **Décomposition LU** : on factorise A = L × U (triangulaire inférieure × triangulaire supérieure)
2. **Pivotage partiel** : on échange les lignes pour mettre les plus grandes valeurs en pivot (stabilité numérique)
3. **Distribution 2D block-cyclic** : la matrice est répartie sur les processus en blocs qui "cyclent" sur une grille P×Q

Le but c'est de mesurer les GFLOPS max que la machine peut atteindre. C'est ce benchmark qui est utilisé pour le classement TOP500.

---

## Pour la répartition du travail

On a 15 minutes de présentation. Je te propose plusieurs options, dis-moi ce qui te convient :

### Option A : Moi algo, toi résultats
- **Moi (slides 1-8, ~8 min)** : Intro, c'est quoi HPL, l'algorithme LU, la parallélisation
- **Toi (slides 9-14, ~7 min)** : Setup expérimental, résultats, graphes, analyse, conclusion

### Option B : Toi algo, moi résultats
- **Toi (slides 1-8, ~8 min)** : Intro, c'est quoi HPL, l'algorithme, parallélisation
- **Moi (slides 9-14, ~7 min)** : Setup, résultats, graphes, conclusion

Je peux te filer toutes mes notes sur l'algo si tu préfères cette partie.

### Option C : On fait les slides ensemble
On se retrouve demain et on fait tout ensemble, chacun prend la moitié à présenter à l'oral.

---

## Ce qu'il reste à faire

### Expériences
- [ ] N = 30000 (~10-15 min de calcul)
- [ ] N = 40000 (~20-30 min de calcul)
- [ ] Tester NB = 128 et NB = 256 (pour comparer)

Je peux les lancer ce soir ou demain matin.

### Slides à créer
1. **Titre** : HPL Benchmark - Projet MPNA
2. **Agenda**
3-4. **C'est quoi HPL ?** : Objectif, TOP500, problème mathématique Ax=b
5-6. **L'algorithme** : Décomposition LU, pivotage, schéma
7-8. **Parallélisation** : Distribution 2D block-cyclic, paramètres N/NB/P×Q
9. **Setup expérimental** : Specs de la machine, logiciels utilisés
10-12. **Résultats** : Tableau + graphe GFLOPS vs N
13. **Analyse** : Observations, efficacité
14. **Conclusion**

### Infos sur notre plateforme (pour slide 9)
```
Machine : ASUS Zephyrus G14 (2020) via WSL2
CPU : AMD Ryzen 9 4900HS (8 cœurs, 16 threads)
RAM : 32 Go
OS : Ubuntu (WSL2)
MPI : OpenMPI
BLAS : OpenBLAS
```

---

## Questions qu'on pourrait nous poser

J'ai préparé quelques réponses au cas où :

**Pourquoi LU et pas une autre méthode ?**
> LU est efficace pour les systèmes denses, complexité O(n³), et se parallélise bien.

**C'est quoi le pivotage partiel ?**
> On sélectionne le plus grand élément de la colonne comme pivot pour éviter les divisions par des petits nombres (erreurs numériques).

**Pourquoi distribution cyclique ?**
> Pour l'équilibrage de charge. Comme on traite la matrice colonne par colonne, la partie restante rétrécit. Avec le cyclique, tous les processus continuent à avoir du travail.

**C'est quoi un bon score d'efficacité ?**
> 70-80% c'est bien, >80% c'est excellent. L'efficacité = GFLOPS obtenus / GFLOPS théoriques max.

---

## Demain

Faut qu'on se sync pour :
1. Décider qui fait quoi (Option A, B ou C ?)
2. Finir les slides
3. Répéter au moins 2 fois (timing !)

La soutenance c'est le 28, donc on a la journée de demain pour tout boucler.

---

Dis-moi ce que tu préfères et si t'as des questions !
