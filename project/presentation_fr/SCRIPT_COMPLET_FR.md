# Présentation HPL - Script Complet et Guide d'Apprentissage
## Partie 2 : Résultats (Slides 9-14) - ~7 minutes
### Présentation MPNA - 28 janvier 2026

---

# PARTIE A : TOUT CE QUE TU DOIS COMPRENDRE

## A.1 C'est Quoi HPL ? (Les Bases)

### Définition Simple
**HPL = High Performance Linpack = Un test de vitesse pour ordinateurs**

C'est comme un chronomètre qui mesure combien de calculs mathématiques un ordinateur peut faire par seconde.

### Le Problème Mathématique
HPL résout cette équation :
```
A × x = b

Où :
- A = un tableau de nombres (matrice), taille N×N
- x = les nombres qu'on cherche (vecteur inconnu)
- b = des nombres connus (vecteur)
```

**Exemple concret (petit) :**
```
[ 2  1 ]   [ x₁ ]   [ 5 ]
[ 1  3 ] × [ x₂ ] = [ 7 ]

On cherche x₁ et x₂ tels que :
2×x₁ + 1×x₂ = 5
1×x₁ + 3×x₂ = 7

Solution : x₁ = 1.6, x₂ = 1.8
```

### Pourquoi Ce Problème ?
1. C'est un problème **standard** que tous les ordinateurs peuvent résoudre
2. Plus N est grand, plus il y a de travail → meilleur test de vitesse
3. Utilisé pour classer les **TOP500** supercalculateurs du monde

---

## A.2 Les Termes Clés à Connaître

### GFLOPS (Giga FLOPS)
- **G** = Giga = milliard (10⁹)
- **FLOPS** = Floating-Point Operations Per Second = Opérations à virgule flottante par seconde
- **GFLOPS** = Milliards d'opérations mathématiques par seconde

**Tes résultats :**
- 15.7 GFLOPS = ton laptop a fait 15.7 milliards de calculs par seconde
- 41.0 GFLOPS = 41 milliards de calculs par seconde (ton meilleur score)

### N (Taille du Problème)
- N = dimension de la matrice
- N = 10 000 signifie un tableau de 10 000 × 10 000 = **100 millions de nombres**
- **Plus N est grand = plus de travail = généralement meilleurs GFLOPS**

### NB (Taille de Bloc)
- La grande matrice est découpée en petits blocs carrés
- NB = taille de chaque bloc (NB × NB)
- Tu as utilisé NB = 192 → blocs de 192×192 nombres = 36 864 nombres par bloc
- **Valeur idéale : 64-256** (dépend du cache CPU)

### P×Q (Grille de Processus)
- Comment les travailleurs (processus CPU) sont organisés
- P = nombre de lignes de travailleurs
- Q = nombre de colonnes de travailleurs
- Tu as utilisé P×Q = 2×4 = **8 travailleurs au total**

### Efficacité
```
Efficacité = (GFLOPS obtenus / GFLOPS théoriques max) × 100%
```
- Pic théorique de ton laptop ≈ 400 GFLOPS (estimation)
- Tu as obtenu 41 GFLOPS max
- Efficacité ≈ 10%
- **Pourquoi si bas ?** WSL, OpenBLAS pas optimisé, limites thermiques du laptop

---

## A.3 L'Algorithme (Décomposition LU)

### Qu'est-ce que la Décomposition LU ?
Au lieu de résoudre A×x=b directement, on décompose la matrice A en deux matrices plus simples :

```
A = L × U

L = Triangulaire inférieure    U = Triangulaire supérieure
┌─────────┐                    ┌─────────┐
│ X 0 0 0 │                    │ X X X X │
│ X X 0 0 │                    │ 0 X X X │
│ X X X 0 │                    │ 0 0 X X │
│ X X X X │                    │ 0 0 0 X │
└─────────┘                    └─────────┘
(zéros au-dessus)              (zéros en-dessous)
```

### Pourquoi ?
Les matrices triangulaires sont **triviales à résoudre** :
1. Résoudre L×y = b (de haut en bas, substitution avant)
2. Résoudre U×x = y (de bas en haut, substitution arrière)

**Analogie :** C'est comme transformer un problème compliqué en deux problèmes faciles.

### Les Étapes (pour chaque colonne k) :
1. **Pivotage** : Trouver le plus grand nombre dans la colonne k, échanger les lignes
2. **Factorisation du panneau** : Calculer les valeurs de L pour la colonne k
3. **Mise à jour de la matrice restante** : Mettre à jour la sous-matrice (90% du travail!)

### Pourquoi le Pivotage ?
Si on divise par un petit nombre, les erreurs explosent :
```
Mauvais : 1 ÷ 0.0001 = 10 000 → petites erreurs deviennent énormes
Bon : 1 ÷ 500 = 0.002 → erreurs restent petites
```
Le pivotage garantit qu'on divise toujours par le plus grand nombre → **stabilité numérique**.

---

## A.4 La Parallélisation (Distribution 2D Block-Cyclic)

### Le Problème
La matrice est ÉNORME (N=30 000 → 900 millions de nombres). Un seul CPU ne peut pas tout stocker ni tout calculer assez vite.

### La Solution
Distribuer les blocs sur plusieurs travailleurs de manière **cyclique** :

```
8 travailleurs dans une grille 2×4 :

Les blocs sont distribués comme des cartes :
┌────┬────┬────┬────┬────┬────┐
│ T1 │ T2 │ T3 │ T4 │ T1 │ T2 │ ...
├────┼────┼────┼────┼────┼────┤
│ T5 │ T6 │ T7 │ T8 │ T5 │ T6 │ ...
├────┼────┼────┼────┼────┼────┤
│ T1 │ T2 │ T3 │ T4 │ T1 │ T2 │ ...
└────┴────┴────┴────┴────┴────┘

Chaque travailleur reçoit des blocs éparpillés partout dans la matrice !
```

### Pourquoi Cyclique ?
L'algorithme traite la matrice de gauche à droite. Si le Travailleur 1 n'avait que la partie gauche :
- Travailleur 1 finit tôt → reste inactif
- Travailleur 8 travaille encore → gaspillage de ressources

Avec la distribution cyclique :
- Tout le monde a des blocs partout
- Tout le monde reste occupé jusqu'à la fin
- **Équilibrage de charge !**

---

## A.5 Pourquoi les GFLOPS Changent avec N

### Tes Résultats
| N | GFLOPS | Observation |
|---|--------|-------------|
| 10 000 | 15.7 | Baseline |
| 20 000 | 41.0 | **+161%** ↑ |
| 30 000 | 38.2 | -7% ↓ (throttling) |

### Pourquoi ça MONTE de 10K à 20K ?

**Le calcul croît en N³, la communication en N²**

Quand N double :
- Travail de calcul : **8× plus** (2³)
- Communication : **4× plus** (2²)

Le calcul croît PLUS VITE que la communication !

**Petit N** → les travailleurs passent plus de temps à se parler qu'à calculer
**Grand N** → les travailleurs passent plus de temps à calculer qu'à se parler

**Analogie :**
- Petit dîner (N=10K) : Plus de temps à se passer les plats qu'à manger
- Grand banquet (N=20K) : Surtout en train de manger, passer les plats c'est mineur

### Pourquoi ça DESCEND à 30K ?

Ton laptop a tourné pendant **8 minutes** à pleine puissance :
- Le CPU a **chauffé**
- Le **thermal throttling** s'est activé (le CPU ralentit pour se refroidir)
- Les GFLOPS ont baissé

**C'est normal sur un laptop !** Un vrai cluster HPC avec un bon refroidissement n'aurait pas ce problème.

---

## A.6 Mémoire et Complexité

### Formule Mémoire
```
Mémoire = N² × 8 octets (pour la double précision)

N = 10 000 → 10 000² × 8 = 800 Mo
N = 30 000 → 30 000² × 8 = 7.2 Go
N = 50 000 → 50 000² × 8 = 20 Go
```

### Formule de Complexité
```
FLOPS = (2/3) × N³

N = 10 000 → ~667 milliards d'opérations
N = 20 000 → ~5 333 milliards d'opérations (8× plus!)
N = 30 000 → ~18 000 milliards d'opérations
```

---

# PARTIE B : TON SCRIPT DE PRÉSENTATION (Mot à Mot)

## Slide 9 : Configuration Expérimentale (~1 min)

**[AFFICHER SLIDE 9]**

> "Pour nos expériences, nous avons utilisé un laptop ASUS Zephyrus G14 équipé d'un processeur AMD Ryzen 9 4900HS à 8 cœurs et 32 gigaoctets de RAM.
>
> Le système tourne sous Ubuntu via WSL2, la couche de compatibilité Linux de Windows. Pour la parallélisation, nous utilisons OpenMPI, et pour les opérations d'algèbre linéaire, la bibliothèque OpenBLAS.
>
> Côté paramètres HPL, nous avons configuré une taille de bloc NB de 192 et une grille de processus de 2 par 4, ce qui nous donne 8 processus MPI au total."

**Temps : ~45 secondes**

---

## Slide 10 : Résultats des Expériences (~1.5 min)

**[AFFICHER SLIDE 10 - Tableau des Résultats]**

> "Voici le tableau récapitulatif de nos trois expériences.
>
> Pour N égal à 10 000, nous obtenons 15.7 GFLOPS en environ 42 secondes. C'est notre point de référence.
>
> En doublant la taille du problème à N égal 20 000, la performance fait un bond significatif à 41 GFLOPS - c'est presque trois fois mieux. Le temps d'exécution passe à environ 2 minutes.
>
> Pour N égal 30 000, on observe une légère baisse à 38.2 GFLOPS, malgré un temps d'exécution de près de 8 minutes.
>
> Point important : tous les tests ont passé la vérification du résidu, ce qui confirme la validité numérique de nos résultats. Le benchmark affiche 'PASSED' pour les trois cas."

**Temps : ~1 minute 15 secondes**

---

## Slide 11 : Graphique de Performance (~1 min)

**[AFFICHER SLIDE 11 - Graphique GFLOPS]**

> "Ce graphique illustre l'évolution des GFLOPS en fonction de la taille du problème N.
>
> On observe clairement deux tendances. D'abord, une augmentation significative entre N égal 10K et 20K. C'est le comportement attendu : avec un problème plus grand, le ratio calcul sur communication s'améliore. Les processus passent plus de temps à calculer qu'à échanger des données.
>
> Ensuite, une légère baisse à N égal 30K. Cette diminution s'explique par le thermal throttling. Le CPU du laptop a réduit automatiquement sa fréquence après 8 minutes de calcul intensif pour éviter la surchauffe. C'est une limitation physique de notre plateforme de test."

**Temps : ~1 minute**

---

## Slide 12 : Analyse de l'Efficacité (~1 min)

**[AFFICHER SLIDE 12]**

> "Analysons maintenant l'efficacité de notre benchmark.
>
> Le pic théorique de notre processeur Ryzen 9 est estimé à environ 400 GFLOPS. Notre meilleure performance de 41 GFLOPS représente donc une efficacité d'environ 10%.
>
> Cette efficacité relativement faible s'explique par plusieurs facteurs :
>
> Premièrement, WSL2 ajoute une couche de virtualisation qui introduit de l'overhead.
>
> Deuxièmement, OpenBLAS n'est pas aussi optimisé qu'Intel MKL pour ce type de processeur.
>
> Troisièmement, un laptop a des limitations thermiques importantes comparé à un serveur HPC correctement refroidi.
>
> Pour référence, sur un vrai cluster HPC, on attend généralement une efficacité entre 70 et 85%."

**Temps : ~1 minute**

---

## Slide 13 : Observations et Limites (~1 min)

**[AFFICHER SLIDE 13]**

> "Résumons nos principales observations.
>
> Ce qui fonctionne bien : la performance scale correctement avec la taille du problème, jusqu'aux limites thermiques. Tous nos tests passent la validation numérique, les résultats sont donc fiables. Et nos expériences sont reproductibles.
>
> Les limites de notre configuration incluent : la virtualisation WSL qui ajoute de l'overhead, le refroidissement limité d'un laptop qui cause du throttling après quelques minutes, et l'utilisation d'OpenBLAS qui n'est pas optimisé pour notre processeur AMD.
>
> Pour améliorer ces résultats, il faudrait utiliser un cluster HPC dédié avec un refroidissement adapté, et des bibliothèques optimisées comme Intel MKL ou AMD BLIS."

**Temps : ~1 minute**

---

## Slide 14 : Conclusion (~30 sec)

**[AFFICHER SLIDE 14]**

> "En conclusion, nous avons démontré que HPL mesure efficacement la performance de calcul d'un système en termes de GFLOPS.
>
> Nous avons validé le benchmark sur notre plateforme avec des résultats cohérents et vérifiés numériquement.
>
> La tendance des GFLOPS avec N confirme la théorie : un meilleur ratio calcul-communication avec des problèmes plus grands, jusqu'aux limites thermiques du matériel.
>
> Merci de votre attention. Je suis disponible pour répondre à vos questions."

**Temps : ~30-40 secondes**

---

# PARTIE C : QUESTIONS-RÉPONSES ANTICIPÉES

## Questions sur Tes Résultats

**Q : Pourquoi l'efficacité est si basse (10%) ?**
> "Trois facteurs principaux : premièrement, WSL2 ajoute une couche de virtualisation qui consomme des ressources. Deuxièmement, OpenBLAS n'est pas optimisé comme Intel MKL. Troisièmement, un laptop a des limites thermiques qu'un cluster HPC n'a pas."

**Q : Pourquoi les GFLOPS baissent à N=30K alors qu'ils devraient augmenter ?**
> "C'est le thermal throttling. Le test a duré 8 minutes à pleine charge. Le CPU a chauffé et a automatiquement réduit sa fréquence pour éviter la surchauffe. C'est un comportement normal sur un laptop."

**Q : C'est quoi un bon score de GFLOPS ?**
> "Ça dépend du matériel. Ce qui compte c'est l'efficacité. Sur un cluster HPC bien optimisé, on attend 70 à 85% d'efficacité. Notre 10% est faible mais explicable par les limitations de notre plateforme."

**Q : Pourquoi avoir choisi NB=192 ?**
> "C'est une valeur standard qui équilibre l'utilisation du cache CPU et l'overhead de communication. Trop petit, on a trop de communications. Trop grand, le cache est mal utilisé. 192 est dans la plage optimale de 128 à 256."

**Q : Comment savoir que le résultat est correct ?**
> "HPL calcule le résidu, c'est-à-dire ||Ax-b|| normalisé. Si cette valeur est inférieure à un seuil (16.0), le test est validé. Tous nos tests affichent PASSED, ce qui confirme la validité numérique."

---

## Questions sur l'Algorithme

**Q : Pourquoi utiliser la décomposition LU ?**
> "Parce que les matrices triangulaires sont triviales à résoudre. On transforme un problème difficile A×x=b en deux problèmes faciles : d'abord L×y=b par substitution avant, puis U×x=y par substitution arrière."

**Q : C'est quoi le pivotage partiel ?**
> "On échange les lignes de la matrice pour mettre le plus grand élément de la colonne comme pivot. Ça évite de diviser par des petits nombres, ce qui causerait une amplification des erreurs d'arrondi."

**Q : Pourquoi la distribution 2D block-cyclic ?**
> "Pour l'équilibrage de charge. L'algorithme LU traite la matrice de gauche à droite, donc la zone de travail rétrécit. Avec une distribution cyclique, tous les processus ont des blocs répartis dans toute la matrice, donc ils restent tous occupés jusqu'à la fin."

**Q : Quelle est la complexité de HPL ?**
> "La complexité est de (2/3)×N³ opérations flottantes. Quand N double, le nombre d'opérations est multiplié par 8. C'est pour ça qu'on préfère de grands N pour avoir de meilleures performances."

**Q : Pourquoi P ≤ Q est recommandé ?**
> "La factorisation du panneau se fait sur une colonne de processus. Avec un P plus petit, cette phase critique implique moins de processus, ce qui réduit la communication."

---

## Questions sur HPL en Général

**Q : À quoi sert HPL ?**
> "HPL mesure la performance maximale en GFLOPS d'un système de calcul. C'est le benchmark officiel utilisé pour établir le classement TOP500 des supercalculateurs mondiaux depuis 1993."

**Q : Est-ce que HPL est représentatif des vraies applications ?**
> "Partiellement. HPL est très orienté calcul dense, notamment la multiplication de matrices (DGEMM). Beaucoup d'applications réelles sont plus limitées par la mémoire. C'est pourquoi le benchmark HPCG a été introduit comme complément pour mesurer les performances sur des opérations mémoire-intensives."

**Q : Qu'est-ce qui limite la performance sur un vrai cluster HPC ?**
> "Principalement la bande passante du réseau pour la communication entre nœuds, et la bande passante mémoire. L'optimisation des bibliothèques BLAS est aussi cruciale."

---

# PARTIE D : CHIFFRES CLÉS À MÉMORISER

```
Complexité :           (2/3) × N³ FLOPS
Mémoire :              N² × 8 octets
Ton meilleur GFLOPS :  41.0 (à N=20K)
Ton efficacité :       ~10%
Taille de bloc :       NB = 192
Grille de processus :  P×Q = 2×4 = 8 processus
Bonne efficacité :     70-85% (sur vrai HPC)
Processeur :           Ryzen 9 4900HS (8 cœurs)
RAM :                  32 Go
```

---

# PARTIE E : RÉSUMÉ EN 1 MINUTE (si on te demande)

> "HPL mesure la performance d'un système en résolvant un système linéaire dense Ax=b par décomposition LU parallélisée avec distribution 2D block-cyclic.
>
> Nous avons testé sur un laptop avec 8 processus MPI. Les résultats montrent que les GFLOPS augmentent avec la taille du problème grâce à un meilleur ratio calcul/communication - on passe de 15.7 à 41 GFLOPS entre N=10K et N=20K.
>
> La baisse à N=30K s'explique par le thermal throttling du laptop après 8 minutes de calcul.
>
> Notre efficacité de 10% est faible à cause de WSL et des limites thermiques, mais tous les résultats sont validés numériquement et cohérents avec la théorie."

---

# PARTIE F : TIMING DE TA PRÉSENTATION

| Slide | Contenu | Durée | Temps cumulé |
|-------|---------|-------|--------------|
| 9 | Configuration | 45s | 0:45 |
| 10 | Résultats | 1m15s | 2:00 |
| 11 | Graphique | 1m00s | 3:00 |
| 12 | Efficacité | 1m00s | 4:00 |
| 13 | Observations | 1m00s | 5:00 |
| 14 | Conclusion | 40s | 5:40 |

**Total : ~6 minutes** (laisse de la marge pour les transitions et imprévus)

---

*Document créé pour la Présentation MPNA HPL - 28 janvier 2026*
