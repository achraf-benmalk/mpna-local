# HPL Presentation - Complete Script & Learning Guide
## Part 2: Results (Slides 9-14) - ~7 minutes

---

# SECTION A: EVERYTHING YOU NEED TO UNDERSTAND

## A.1 What is HPL? (Basics)

### Simple Definition
HPL = High Performance Linpack = **A speed test for computers**

It measures how fast a computer can do math calculations, specifically solving a big equation.

### The Math Problem
```
A × x = b

- A = a table of numbers (matrix), size N×N
- x = the answer we're looking for (vector)
- b = known values (vector)
```

**Example (tiny):**
```
[ 2  1 ]   [ x₁ ]   [ 5 ]
[ 1  3 ] × [ x₂ ] = [ 7 ]

Find x₁ and x₂ such that:
2×x₁ + 1×x₂ = 5
1×x₁ + 3×x₂ = 7
```

### Why This Problem?
- It's a standard problem that all computers can solve
- The bigger N, the more work → better test of speed
- Used to rank the TOP500 fastest supercomputers in the world

---

## A.2 Key Terms You MUST Know

### GFLOPS
- **G** = Giga = billion (10⁹)
- **FLOPS** = Floating-Point Operations Per Second
- **GFLOPS** = Billions of math operations per second

**Your results:**
- 15.7 GFLOPS = your laptop did 15.7 billion calculations per second
- 41.0 GFLOPS = 41 billion calculations per second

### N (Problem Size)
- N = dimension of the matrix
- N = 10,000 means a 10,000 × 10,000 table = 100 million numbers
- **Bigger N = more work = usually better GFLOPS**

### NB (Block Size)
- The matrix is cut into smaller blocks
- NB = size of each block (NB×NB)
- You used NB = 192 → blocks of 192×192 numbers
- **Sweet spot: 64-256** (depends on CPU cache)

### P×Q (Process Grid)
- How the workers (CPU processes) are organized
- P = rows of workers
- Q = columns of workers
- You used P×Q = 2×4 = 8 workers total

### Efficiency
```
Efficiency = (Achieved GFLOPS / Theoretical Peak) × 100%
```
- Your laptop theoretical peak ≈ 400 GFLOPS (rough estimate)
- You achieved 41 GFLOPS max
- Efficiency ≈ 10%
- **Why so low?** WSL overhead, OpenBLAS not optimized, laptop thermal limits

---

## A.3 The Algorithm (LU Decomposition)

### What is LU Decomposition?
Instead of solving A×x=b directly, we split matrix A into two simpler matrices:

```
A = L × U

L = Lower triangular    U = Upper triangular
┌─────────┐             ┌─────────┐
│ X 0 0 0 │             │ X X X X │
│ X X 0 0 │             │ 0 X X X │
│ X X X 0 │             │ 0 0 X X │
│ X X X X │             │ 0 0 0 X │
└─────────┘             └─────────┘
(zeros above diagonal)   (zeros below diagonal)
```

### Why?
Triangular matrices are **easy to solve**:
1. Solve L×y = b (go top to bottom)
2. Solve U×x = y (go bottom to top)

### The Steps (for each column k):
1. **Pivoting**: Find the biggest number in column k, swap rows
2. **Panel factorization**: Calculate the L values for column k
3. **Trailing update**: Update the remaining matrix (this is 90% of the work!)

### Why Pivoting?
If you divide by a small number, errors explode:
```
Bad:  1/0.0001 = 10,000 → tiny errors become huge
Good: 1/500 = 0.002 → errors stay small
```
Pivoting ensures we always divide by the biggest number → numerical stability.

---

## A.4 Parallelization (2D Block-Cyclic Distribution)

### The Problem
Matrix is HUGE (N=30,000 → 900 million numbers). Can't fit on one CPU.

### The Solution
Distribute blocks across multiple workers in a cyclic pattern:

```
8 workers in 2×4 grid:

Matrix blocks assigned like dealing cards:
┌────┬────┬────┬────┬────┬────┐
│ W1 │ W2 │ W3 │ W4 │ W1 │ W2 │ ...
├────┼────┼────┼────┼────┼────┤
│ W5 │ W6 │ W7 │ W8 │ W5 │ W6 │ ...
├────┼────┼────┼────┼────┼────┤
│ W1 │ W2 │ W3 │ W4 │ W1 │ W2 │ ...
└────┴────┴────┴────┴────┴────┘

Each worker gets blocks scattered across the whole matrix!
```

### Why Cyclic?
The algorithm processes left-to-right. If Worker 1 only had the left part:
- Worker 1 finishes early → sits idle
- Worker 8 still working → waste of resources

With cyclic distribution:
- Everyone has blocks everywhere
- Everyone stays busy until the end
- **Load balancing!**

---

## A.5 Why GFLOPS Changes with N

### Your Results
| N | GFLOPS |
|---|--------|
| 10,000 | 15.7 |
| 20,000 | 41.0 |
| 30,000 | 38.2 |

### Why UP from 10K to 20K?

**Math grows as N³, Communication grows as N²**

When N doubles:
- Math work: 8× more (2³)
- Communication: 4× more (2²)

Small N → workers spend more time talking than working
Big N → workers spend more time working than talking

**Analogy:**
- Small dinner party (N=10K): More time passing dishes than eating
- Big banquet (N=20K): Mostly eating, passing dishes is minor

### Why DOWN at 30K?

Your laptop ran for **8 minutes** at full power:
- CPU got HOT
- Thermal throttling kicked in (CPU slows down to cool off)
- GFLOPS dropped

**This is expected on laptops!** A real HPC cluster with proper cooling wouldn't have this issue.

---

## A.6 Memory and Complexity

### Memory Formula
```
Memory = N² × 8 bytes (for double precision)

N = 10,000 → 10,000² × 8 = 800 MB
N = 30,000 → 30,000² × 8 = 7.2 GB
N = 50,000 → 50,000² × 8 = 20 GB
```

### Complexity Formula
```
FLOPS = (2/3) × N³

N = 10,000 → ~667 billion operations
N = 20,000 → ~5,333 billion operations (8× more!)
N = 30,000 → ~18,000 billion operations
```

---

# SECTION B: YOUR PRESENTATION SCRIPT (Word for word)

## Slide 9: Configuration Expérimentale (~1 min)

**[SHOW SLIDE 9]**

> "Pour nos expériences, nous avons utilisé un laptop ASUS Zephyrus G14 avec un processeur AMD Ryzen 9 à 8 cœurs et 32 Go de RAM.
>
> Le système tourne sous Ubuntu via WSL2, avec OpenMPI pour la parallélisation et OpenBLAS comme bibliothèque BLAS.
>
> Pour HPL, nous avons configuré une taille de bloc NB de 192 et une grille de processus de 2 par 4, soit 8 processus au total."

---

## Slide 10: Résultats (~1.5 min)

**[SHOW SLIDE 10 - Results Table]**

> "Voici nos résultats pour trois tailles de problème différentes.
>
> Avec N égal à 10 000, nous obtenons 15.7 GFLOPS en environ 42 secondes.
>
> En doublant la taille à N égal 20 000, la performance augmente significativement à 41 GFLOPS - presque trois fois plus.
>
> Pour N égal 30 000, nous observons une légère baisse à 38.2 GFLOPS, malgré un temps d'exécution de près de 8 minutes.
>
> Tous les tests ont passé la vérification de résidu, ce qui confirme la validité numérique de nos résultats."

---

## Slide 11: Graphique de Performance (~1 min)

**[SHOW SLIDE 11 - GFLOPS Graph]**

> "Ce graphique montre l'évolution des GFLOPS en fonction de la taille du problème.
>
> On observe une augmentation significative entre N=10K et N=20K. C'est le comportement attendu : avec un problème plus grand, le ratio calcul sur communication s'améliore.
>
> La légère baisse à N=30K s'explique par le thermal throttling - le CPU du laptop a réduit sa fréquence après 8 minutes de calcul intensif pour éviter la surchauffe."

---

## Slide 12: Analyse de l'Efficacité (~1 min)

**[SHOW SLIDE 12]**

> "En termes d'efficacité, notre pic théorique est estimé à environ 400 GFLOPS pour ce processeur.
>
> Notre meilleure performance de 41 GFLOPS représente donc une efficacité d'environ 10%.
>
> Cette efficacité relativement faible s'explique par plusieurs facteurs :
> - L'overhead de WSL2 qui ajoute une couche de virtualisation
> - OpenBLAS qui n'est pas aussi optimisé qu'Intel MKL
> - Les limitations thermiques d'un laptop par rapport à un serveur HPC refroidi
>
> Sur un vrai cluster HPC, on attendrait une efficacité de 70 à 85%."

---

## Slide 13: Observations et Limites (~1 min)

**[SHOW SLIDE 13]**

> "Nos principales observations sont :
>
> Premièrement, la performance scale bien avec la taille du problème, jusqu'aux limites thermiques.
>
> Deuxièmement, le benchmark HPL est validé - tous nos tests passent la vérification de résidu.
>
> Les limites de notre setup incluent :
> - La virtualisation WSL qui ajoute de l'overhead
> - Le refroidissement limité d'un laptop
> - L'utilisation d'OpenBLAS au lieu de bibliothèques optimisées
>
> Pour améliorer, il faudrait utiliser un cluster HPC dédié avec Intel MKL."

---

## Slide 14: Conclusion (~30 sec)

**[SHOW SLIDE 14]**

> "En conclusion, nous avons démontré que HPL mesure efficacement la performance de calcul d'un système.
>
> Nous avons validé le benchmark sur notre plateforme avec des résultats cohérents.
>
> La tendance des GFLOPS avec N confirme la théorie : un meilleur ratio calcul-communication avec des problèmes plus grands.
>
> Merci, je suis disponible pour vos questions."

---

# SECTION C: ANTICIPATED Q&A

## Questions About Your Results

**Q: Pourquoi l'efficacité est si basse (10%) ?**
> "Trois raisons : WSL2 ajoute de l'overhead de virtualisation, OpenBLAS n'est pas optimisé comme Intel MKL, et un laptop a des limites thermiques qu'un cluster HPC n'a pas."

**Q: Pourquoi les GFLOPS baissent à N=30K ?**
> "Thermal throttling. Le test a duré 8 minutes, le CPU a chauffé et a réduit sa fréquence pour se refroidir. C'est typique sur un laptop."

**Q: C'est quoi un bon score de GFLOPS ?**
> "Ça dépend du matériel. Sur un cluster HPC, on attend 70-85% d'efficacité. Notre 10% est faible mais explicable par les limitations du laptop et WSL."

**Q: Pourquoi NB=192 ?**
> "C'est une valeur standard qui équilibre l'utilisation du cache CPU et l'overhead de communication. Trop petit = trop de communication, trop grand = mauvaise utilisation du cache."

## Questions About the Algorithm

**Q: Pourquoi la décomposition LU ?**
> "Parce que les matrices triangulaires sont triviales à résoudre. On transforme un problème difficile (A×x=b) en deux problèmes faciles (L×y=b puis U×x=y)."

**Q: C'est quoi le pivotage partiel ?**
> "On échange les lignes pour mettre le plus grand élément comme pivot. Ça évite de diviser par des petits nombres, ce qui causerait des erreurs numériques."

**Q: Pourquoi 2D block-cyclic ?**
> "Pour l'équilibrage de charge. L'algorithme traite la matrice de gauche à droite, donc le travail diminue. Avec la distribution cyclique, tous les processus gardent du travail jusqu'à la fin."

**Q: C'est quoi la complexité de HPL ?**
> "(2/3)×N³ opérations. Quand N double, le travail est multiplié par 8."

## Questions About HPL in General

**Q: À quoi sert HPL ?**
> "À mesurer la performance maximale en GFLOPS d'un système. C'est le benchmark utilisé pour le classement TOP500 des supercalculateurs."

**Q: Comment on vérifie que le résultat est correct ?**
> "HPL calcule le résidu ||Ax-b||. Si c'est inférieur à un seuil (16.0), le test passe. Tous nos tests affichent PASSED."

**Q: HPL est-il représentatif des vraies applications ?**
> "Partiellement. HPL est très orienté calcul (DGEMM), alors que beaucoup d'applications réelles sont limitées par la mémoire. C'est pourquoi le benchmark HPCG a été introduit comme complément."

---

# SECTION D: KEY NUMBERS TO MEMORIZE

```
Complexity:        (2/3) × N³ FLOPS
Memory:            N² × 8 bytes
Your best GFLOPS:  41.0 (at N=20K)
Your efficiency:   ~10%
Block size used:   NB = 192
Process grid:      P×Q = 2×4 = 8 processes
Good efficiency:   70-85% (on real HPC)
```

---

# SECTION E: 1-MINUTE SUMMARY (if asked to summarize)

> "HPL mesure la performance d'un système en résolvant un système linéaire Ax=b par décomposition LU parallélisée.
>
> Nous avons testé sur un laptop avec 8 processus. Les résultats montrent que les GFLOPS augmentent avec la taille du problème grâce à un meilleur ratio calcul/communication, jusqu'à ce que le thermal throttling limite la performance.
>
> Notre efficacité de 10% est faible à cause de WSL et du laptop, mais les résultats sont valides et cohérents avec la théorie."

---

*Document created for MPNA HPL Presentation - January 27, 2026*
