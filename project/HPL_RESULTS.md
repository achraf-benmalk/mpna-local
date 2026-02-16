# Résultats du Benchmark HPL
## Plateforme : ASUS Zephyrus G14 (2020) via WSL2

### Configuration
- **CPU** : AMD Ryzen 9 4900HS (8 cœurs / 16 threads)
- **RAM** : 32 Go
- **OS** : Ubuntu (WSL2)
- **MPI** : OpenMPI
- **BLAS** : OpenBLAS
- **Version HPL** : 2.3

### Paramètres Fixes
- **P × Q** : 2 × 4 (grille de processus)
- **Processus** : 8

---

## Tableau des Résultats

| N | NB | Temps (s) | GFLOPS | Efficacité* | Statut |
|-------|-----|---------|--------|-------------|--------|
| 10 000 | 192 | 42.5 | 15.7 | ~4% | ✓ VALIDÉ |
| 20 000 | 192 | 130.0 | 41.0 | ~10% | ✓ VALIDÉ |
| 30 000 | 192 | 471.2 | 38.2 | ~10% | ✓ VALIDÉ |
| 30 000 | **128** | 407.5 | **44.2** ⭐ | ~11% | ✓ VALIDÉ |

*Efficacité estimée par rapport au pic théorique de ~400 GFLOPS (estimation pour Ryzen 9 4900HS)

**Meilleur résultat : 44.2 GFLOPS avec NB=128 (+15.6% vs NB=192)**

---

## Observations Clés

### 1. Scaling avec N (NB=192)
- **N=10K → N=20K** : GFLOPS ×2.6 (15.7 → 41.0)
- **Explication** : Meilleur ratio calcul/communication avec N plus grand

### 2. Baisse à N=30K (NB=192)
- **N=20K → N=30K** : GFLOPS -7% (41.0 → 38.2)
- **Explication** : Thermal throttling après 8 minutes de calcul intensif

### 3. Impact de la Taille de Bloc (N=30K)
- **NB=192** : 38.2 GFLOPS
- **NB=128** : 44.2 GFLOPS (+15.6%)
- **Explication** : NB=128 meilleure utilisation du cache L2/L3

---

## Extraits des Sorties HPL

### N = 10 000, NB = 192
```
WR11C2R4       10000   192     2     4              42.47             1.5699e+01
||Ax-b||_oo/(eps*(||A||_oo*||x||_oo+||b||_oo)*N)=   2.37915829e-03 ...... PASSED
```

### N = 20 000, NB = 192
```
WR11C2R4       20000   192     2     4             130.04             4.1016e+01
||Ax-b||_oo/(eps*(||A||_oo*||x||_oo+||b||_oo)*N)=   1.60720421e-03 ...... PASSED
```

### N = 30 000, NB = 192
```
WR11C2R4       30000   192     2     4             471.19             3.8204e+01
||Ax-b||_oo/(eps*(||A||_oo*||x||_oo+||b||_oo)*N)=   1.74252722e-03 ...... PASSED
```

### N = 30 000, NB = 128 (Meilleur résultat)
```
WR11C2R4       30000   128     2     4             407.50             4.4175e+01
||Ax-b||_oo/(eps*(||A||_oo*||x||_oo+||b||_oo)*N)=   ... ...... PASSED
```

---

*Résultats collectés : 27 janvier 2026*
