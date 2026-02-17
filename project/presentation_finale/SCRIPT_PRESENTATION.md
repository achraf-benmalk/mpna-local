# Script de Présentation — Partie 2 : Résultats et Analyse HPL

## Vue d'ensemble de tes slides

| Slide | Titre | Durée |
|-------|-------|-------|
| 1 | Titre (HPL Benchmark GPU) | 10s |
| 2 | Plateforme d'exécution | 1m30 |
| 3 | Étapes d'exécution | 1m |
| 4 | Résultats A100 | 1m30 |
| 5 | Résultats H100 | 1m30 |
| 6 | Anomalie multi-GPU N=20K | 1m |
| 7 | Comparaison A100 vs H100 | 1m30 |
| 8 | Synthèse de l'efficacité | 1m |
| 9 | Conclusion | 1m |
| **Total** | | **~10 min** |

---

## PARTIE A : Tout ce que tu dois comprendre

### A1. C'est quoi les GFLOPS ?

GFLOPS = milliards d'opérations mathématiques par seconde. C'est la vitesse du GPU.
- Plus le chiffre est haut, plus le GPU est rapide
- HPL mesure cette vitesse en résolvant Ax = b

### A2. C'est quoi le pic théorique ?

C'est la vitesse maximale que le GPU POURRAIT atteindre si tout est parfait. En pratique, on n'atteint jamais 100%.

- **A100** : pic = **19,5 TFLOPS** (19 500 GFLOPS)
- **H100 PCIe** : pic = **51 TFLOPS** (51 000 GFLOPS)

### A3. Comment on calcule le pic ? (Question fréquente !)

**Pour l'A100 :**
```
3 456 cœurs FP64 × 2 (opération FMA) × 1,41 GHz = 9,7 TFLOPS (cœurs CUDA seuls)
Avec Tensor Cores (×2) : 9,7 × 2 = 19,5 TFLOPS
```
- 3 456 = nombre de cœurs capables de faire du calcul en double précision (FP64)
- FMA = Fused Multiply-Add → chaque opération compte pour 2 (une multiplication + une addition)
- 1,41 GHz = vitesse d'horloge du GPU
- Tensor Cores = unités spéciales qui doublent le débit FP64 pour les opérations DGEMM (produits de matrices)

**Pour le H100 PCIe :**
- 7 296 cœurs FP64, Tensor Cores 4e génération
- Pic officiel NVIDIA : **51 TFLOPS**
- La variante SXM (plus puissante) atteint 67 TFLOPS

### A4. C'est quoi l'efficacité ?

```
Efficacité = (GFLOPS mesurés / Pic théorique) × 100%
```

Exemples :
- A100 : 17 860 / 19 500 = **91,6%** → excellent
- H100 : 45 110 / 51 000 = **88,5%** → très bon
- A100 a meilleure efficacité car plus facile à saturer (moins de cœurs)

### A5. C'est quoi le speedup multi-GPU ?

```
Speedup = GFLOPS avec 2 GPUs / GFLOPS avec 1 GPU
```

- A100 : 34 720 / 17 860 = **1,94x** → efficacité parallèle 97% (quasi parfait)
- H100 : 81 970 / 45 110 = **1,82x** → efficacité parallèle 91% (bon mais pas parfait)
- Idéal = 2,0x (doublement parfait), jamais atteint en pratique à cause de la communication

### A6. Pourquoi GFLOPS augmente avec N ?

Le calcul de HPL (factorisation LU) a deux composantes :
- **Calcul** : croît en O(N³) → cubique
- **Communication** : croît en O(N²) → quadratique

Quand N est grand, le calcul domine. Quand N est petit, le GPU passe trop de temps à communiquer par rapport au calcul.

### A7. Pourquoi 2 GPUs sont plus LENTS à N=20K ?

Avec un petit problème, chaque GPU reçoit la moitié de la matrice. Cette moitié est trop petite pour occuper tous les cœurs. En plus, les 2 GPUs doivent communiquer entre eux (via NVLink/PCIe). Le coût de cette communication est plus élevé que le gain de calcul.

Sur H100 c'est pire (-28,6% vs -6,4% sur A100) car le H100 a plus de cœurs à occuper (7 296 vs 3 456).

### A8. Pourquoi H100 a moins bonne efficacité parallèle ?

Le H100 calcule plus vite → il finit sa partie de calcul plus vite → il passe un pourcentage plus élevé de son temps à attendre la communication. La latence de communication (NVLink) est à peu près la même sur A100 et H100, mais le H100 calcule ~2,5x plus vite, donc la communication pèse proportionnellement plus.

### A9. NB=576, c'est quoi et pourquoi ?

NB = taille des blocs de la matrice distribuée.
- Sur CPU : NB = 128-256 (blocs qui tiennent dans le cache L2)
- Sur GPU : NB = 576 (blocs beaucoup plus grands)

Pourquoi plus grand sur GPU ? Les GPUs ont des milliers de cœurs. Il faut de grands blocs pour les occuper tous. Avec des petits blocs, les cœurs n'auraient pas assez de travail.

### A10. Tensor Cores, c'est quoi ?

Des unités de calcul spéciales dans les GPUs NVIDIA, conçues pour accélérer les multiplications de matrices. Sur HPL, elles doublent la performance FP64 par rapport aux cœurs CUDA classiques.
- A100 : 3e génération → ×2 en FP64
- H100 : 4e génération → ×2 en FP64

Sans Tensor Cores, le pic FP64 de l'A100 serait 9,7 TFLOPS au lieu de 19,5.

---

## PARTIE B : Script mot à mot

### Slide 1 — Titre (10s)

> "Je vais maintenant vous présenter les résultats de notre implémentation HPL sur GPU, avec une comparaison entre les architectures A100 et H100."

### Slide 2 — Plateforme d'exécution (1m30)

> "Nous avons exécuté HPL sur un cluster HPC équipé de deux types de GPUs NVIDIA."
>
> "Le premier est l'A100, architecture Ampere, avec 3 456 cœurs FP64 et un pic théorique de 19,5 TFLOPS en FP64 avec Tensor Cores."
>
> "Le second est le H100 en variante PCIe, architecture Hopper, avec 7 296 cœurs FP64 et un pic de 51 TFLOPS — soit 2,6 fois plus puissant."
>
> "HPL a été déployé via le conteneur NVIDIA HPC-Benchmarks 23.10, avec Singularity. Ce conteneur utilise les Tensor Cores pour les opérations DGEMM, ce qui double le débit FP64."
>
> "Pour la configuration HPL, nous avons utilisé NB = 576. C'est nettement plus grand que les valeurs CPU typiques de 128 à 256, car les GPUs ont besoin de grands blocs pour alimenter leurs milliers de cœurs."

### Slide 3 — Étapes d'exécution (1m)

> "L'exécution se déroule en 4 étapes."
>
> "D'abord, on crée le fichier HPL.dat avec les paramètres : taille N, taille de bloc NB, grille de processus."
>
> "Ensuite, on lance le conteneur Singularity en bindant notre répertoire de travail."
>
> "Puis on alloue les ressources GPU via Slurm avec la commande salloc."
>
> "Enfin, on lance le benchmark avec mpirun. Pour 1 GPU, on utilise -np 1. Pour 2 GPUs, -np 2."

### Slide 4 — Résultats A100 (1m30)

> "Voici les résultats sur A100. On voit que les GFLOPS augmentent avec N, passant de 9 700 à 17 860 GFLOPS pour 1 GPU."
>
> "Le pic théorique est de 19 500 GFLOPS. À N = 100 000, on atteint 17 860, soit une efficacité de 91,6%. C'est excellent."
>
> "Avec 2 GPUs, on obtient 34 720 GFLOPS, soit un speedup de 1,94x. L'efficacité parallèle est de 97%, ce qui est quasi-linéaire."
>
> "On remarque toutefois qu'à N = 20 000, les 2 GPUs sont légèrement plus lents que 1 seul. On y reviendra."

### Slide 5 — Résultats H100 (1m30)

> "Sur H100, les performances sont nettement supérieures. 1 GPU atteint 45 110 GFLOPS à N = 100 000, soit une efficacité de 88,5% par rapport au pic de 51 TFLOPS."
>
> "Avec 2 GPUs, on monte à 81 970 GFLOPS, un speedup de 1,82x — soit 91% d'efficacité parallèle."
>
> "Mais l'anomalie à N = 20 000 est beaucoup plus marquée ici : 2 GPUs H100 sont 28,6% PLUS LENTS qu'un seul."

### Slide 6 — Anomalie N=20K (1m)

> "Pourquoi 2 GPUs peuvent être plus lents qu'un seul ?"
>
> "À N = 20 000, le problème est trop petit. Chaque GPU reçoit une portion de matrice insuffisante pour saturer ses cœurs."
>
> "Le coût de communication entre les 2 GPUs dépasse le gain de calcul supplémentaire."
>
> "C'est plus prononcé sur H100 car il a plus de cœurs à alimenter : 7 296 contre 3 456 pour l'A100."
>
> "Il existe donc un seuil de rentabilité : entre N = 20 000 et 40 000. En dessous, ajouter un GPU est contre-productif."
>
> "Fondamentalement, c'est parce que le calcul croît en N cube, mais la communication en N carré. Pour les grands N, le calcul domine."

### Slide 7 — Comparaison A100 vs H100 (1m30)

> "Si on compare les deux architectures, le H100 surpasse l'A100 sur toutes les tailles de problème."
>
> "Le ratio d'accélération varie : 1,66x à N = 20 000, et converge vers 2,53x à N = 100 000."
>
> "Le ratio théorique entre les pics est 51 divisé par 19,5, soit 2,62x."
>
> "Le ratio mesuré de 2,53x est très proche, avec un écart de seulement 3%. Cela confirme que HPL exploite efficacement les deux architectures."
>
> "À N = 20 000, le ratio est seulement de 1,66x car les deux GPUs sont sous-utilisés."

### Slide 8 — Synthèse de l'efficacité (1m)

> "Ce tableau résume l'efficacité de chaque configuration."
>
> "On observe une tendance claire : plus la configuration est puissante, plus l'efficacité baisse. De 91,6% pour l'A100 1 GPU jusqu'à 80,4% pour le H100 2 GPUs."
>
> "Mais toutes les configurations dépassent 80%, ce qui confirme la nature compute-bound de HPL."
>
> "La conclusion : plus un GPU est puissant, plus il est difficile d'exploiter 100% de sa capacité. Le dimensionnement du problème et le tuning des paramètres restent essentiels."

### Slide 9 — Conclusion (1m)

> "Pour résumer nos 5 enseignements principaux :"
>
> "Un : HPL est compute-bound — les efficacités de 88 à 92% le confirment."
>
> "Deux : la taille du problème est déterminante — N cube versus N carré."
>
> "Trois : le multi-GPU a un seuil de rentabilité autour de N = 20 à 40 000."
>
> "Quatre : le H100 offre un gain de 2,5x sur l'A100, cohérent avec les specs."
>
> "Cinq : l'efficacité parallèle diminue avec la puissance — 97% sur A100 contre 91% sur H100."
>
> "Merci, des questions ?"

---

## PARTIE C : Questions-Réponses anticipées

### Q1 : "Pourquoi avoir choisi NB = 576 ?"
> "NB = 576 est la valeur recommandée par NVIDIA pour les GPUs dans le conteneur HPC-Benchmarks. Les GPUs ont des milliers de cœurs — il leur faut des blocs plus grands que les CPUs pour maintenir un taux d'occupation élevé. Sur CPU, on utilise 128 à 256 pour tenir dans le cache L2."

### Q2 : "Pourquoi l'efficacité du H100 est inférieure à celle de l'A100 ?"
> "Le H100 a 2,1 fois plus de cœurs FP64 que l'A100. Avec le même problème de taille N, il est plus difficile de tous les occuper. Il faudrait un N encore plus grand pour atteindre la même efficacité. C'est un compromis classique en HPC entre puissance brute et utilisation."

### Q3 : "Comment calculez-vous le pic théorique ?"
> "Pour l'A100 : 3 456 cœurs FP64, multipliés par 2 pour le FMA, multipliés par 1,41 GHz — ce qui donne 9,7 TFLOPS pour les cœurs CUDA. Avec les Tensor Cores qui doublent le débit FP64, on arrive à 19,5 TFLOPS. C'est le chiffre officiel NVIDIA. Pour le H100 PCIe, le pic officiel est 51 TFLOPS."

### Q4 : "Pourquoi P×Q = 2×1 et pas 1×2 ?"
> "Sur GPU avec HPL, on utilise 1 processus MPI par GPU. Pour 2 GPUs, P×Q = 2×1 signifie 2 processus en colonne. La distribution des données dans HPL favorise cette configuration pour minimiser la communication pendant la factorisation de panel."

### Q5 : "C'est quoi les Tensor Cores ?"
> "Ce sont des unités de calcul spécialisées dans les GPUs NVIDIA, optimisées pour les multiplications de matrices. HPL les utilise pour les opérations DGEMM — c'est pour ça qu'on atteint presque 2× le débit des cœurs CUDA classiques en FP64."

### Q6 : "Avez-vous vérifié la correction des résultats ?"
> "Oui, tous les tests ont passé la vérification du résidu. HPL vérifie que la norme ||Ax-b|| est inférieure à un seuil de 16,0 par rapport à la précision machine. Tous nos résultats affichent PASSED."

### Q7 : "Pourquoi le ratio mesuré (2,53x) ne correspond pas exactement au ratio théorique (2,62x) ?"
> "L'écart est de seulement 3%, ce qui est très faible. La différence vient du fait que le H100 est légèrement plus difficile à saturer — son efficacité est 88,5% vs 91,6% pour l'A100. En pratique, la bande passante mémoire, les latences internes et le scheduler GPU expliquent ce petit écart."

### Q8 : "Pourquoi Singularity et pas Docker ?"
> "Singularity est le standard en HPC car il fonctionne sans privilèges root, contrairement à Docker. Sur un cluster partagé, la sécurité impose Singularity. Le conteneur NVIDIA HPC-Benchmarks est fourni au format Singularity/Docker sur NGC."

### Q9 : "Quelle est la différence entre H100 SXM et PCIe ?"
> "Le SXM a plus de SM actifs (132 vs 114), une fréquence boost plus élevée (1 830 vs 1 620 MHz) et utilise NVLink pour la connexion inter-GPU, ce qui est plus rapide que le PCIe. Son pic FP64 Tensor Core est 67 TFLOPS contre 51 pour le PCIe."

### Q10 : "Qu'est-ce qu'on pourrait améliorer ?"
> "Tester des valeurs de N encore plus grandes pour voir si l'efficacité du H100 converge vers celle de l'A100. Aussi, tester avec plus de GPUs (4, 8) pour étudier le passage à l'échelle. Et comparer NB = 576 avec d'autres valeurs de bloc."

---

## PARTIE D : Chiffres à mémoriser

| Quoi | Valeur |
|------|--------|
| A100 pic FP64 TC | 19,5 TFLOPS |
| H100 PCIe pic FP64 TC | 51 TFLOPS |
| A100 meilleur résultat | 17 860 GFLOPS (91,6%) |
| H100 meilleur résultat | 45 110 GFLOPS (88,5%) |
| A100 2-GPU speedup | 1,94x (97% eff. parallèle) |
| H100 2-GPU speedup | 1,82x (91% eff. parallèle) |
| H100/A100 ratio mesuré | 2,53x (théorique : 2,62x) |
| Anomalie N=20K H100 | -28,6% (2 GPUs plus lents) |
| NB GPU | 576 |
| NB CPU typique | 128-256 |
