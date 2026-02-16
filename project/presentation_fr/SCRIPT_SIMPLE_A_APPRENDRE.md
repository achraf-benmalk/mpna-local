# Script Simple à Apprendre - Présentation HPL
## Ta partie: ~6-7 minutes

---

# SLIDE 9: Configuration (45 sec)

**Ce que tu dis:**

> "Pour nos expériences, on a utilisé mon laptop ASUS Zephyrus avec un Ryzen 9 à 8 coeurs et 32 Go de RAM.
>
> On tourne sous Ubuntu via WSL2. Pour HPL, on utilise OpenMPI pour la communication et OpenBLAS pour les maths.
>
> On a testé avec 8 processus MPI, arrangés en grille 2 par 4."

---

# SLIDE 10: Résultats (1 min 30)

**Ce que tu dis:**

> "Voici nos résultats principaux.
>
> Avec N égal 10 000, on obtient 15.7 GFLOPS en 42 secondes.
>
> En doublant à N égal 20 000, on monte à 41 GFLOPS. C'est presque 3 fois mieux!
>
> À N égal 30 000, avec NB=192, on observe une baisse à 38.2 GFLOPS. C'est dû au thermal throttling - le CPU a chauffé après 8 minutes.
>
> MAIS en changeant NB de 192 à 128, on remonte à 44.2 GFLOPS. C'est une amélioration de 15.6%!
>
> Tous les tests sont validés numériquement - ils affichent PASSED."

---

# SLIDE 11: Évolution (1 min)

**Ce que tu dis:**

> "Ce graphique montre l'évolution des GFLOPS.
>
> On voit clairement que la performance augmente avec N. C'est logique : plus le problème est grand, plus on passe de temps à calculer plutôt qu'à communiquer entre processus.
>
> La baisse à N=30K avec NB=192 c'est le throttling thermique. Mais le point vert montre qu'avec NB=128, on récupère et dépasse même les 41 GFLOPS."

---

# SLIDE 12: Efficacité (1 min)

**Ce que tu dis:**

> "En termes d'efficacité, le pic théorique du Ryzen 9 est environ 400 GFLOPS.
>
> Notre meilleur résultat de 44.2 GFLOPS donne une efficacité d'environ 11%.
>
> Pourquoi c'est bas? Trois raisons:
> - WSL2 ajoute de l'overhead de virtualisation
> - OpenBLAS n'est pas aussi optimisé qu'Intel MKL
> - Un laptop a des limites thermiques qu'un serveur HPC n'a pas
>
> Sur un vrai cluster HPC, on attendrait 70 à 85% d'efficacité."

---

# SLIDE 13: Limites (1 min)

**Ce que tu dis:**

> "Ce qui marche bien: la performance scale avec N, tous les tests sont validés, et le tuning de NB améliore vraiment les perfs.
>
> Les limites: WSL c'est pas natif, le laptop chauffe, et OpenBLAS n'est pas optimisé pour AMD.
>
> Pour faire mieux, il faudrait un cluster HPC dédié avec des bibliothèques optimisées."

---

# SLIDE 14: Conclusion (30 sec)

**Ce que tu dis:**

> "En conclusion: HPL mesure les GFLOPS en résolvant Ax=b par décomposition LU.
>
> Notre meilleur résultat c'est 44.2 GFLOPS avec NB=128.
>
> On retient que les GFLOPS augmentent avec N, et que le tuning est important - on a gagné 15.6% en changeant juste NB.
>
> Merci, je suis disponible pour vos questions."

---

# QUESTIONS PROBABLES

## Q: Pourquoi l'efficacité est si basse?
> "WSL ajoute de l'overhead, OpenBLAS n'est pas optimisé, et le laptop a des limites thermiques."

## Q: C'est quoi le thermal throttling?
> "Quand le CPU chauffe trop, il réduit sa fréquence automatiquement pour se refroidir. Ça baisse les performances."

## Q: Pourquoi NB=128 est mieux que NB=192?
> "NB=128 utilise mieux le cache du CPU. C'est plus petit donc ça tient mieux en mémoire rapide."

## Q: Comment tu sais que les résultats sont corrects?
> "HPL vérifie le résidu ||Ax-b||. Si c'est petit, le test passe. Tous nos tests affichent PASSED."

## Q: Pourquoi les GFLOPS augmentent avec N?
> "Plus grand N = plus de calcul par rapport à la communication. Le ratio calcul/comm s'améliore."

## Q: C'est quoi P×Q = 2×4?
> "C'est la grille de processus. 2 lignes, 4 colonnes, donc 8 processus au total."

---

# CHIFFRES À RETENIR

- **Meilleur GFLOPS**: 44.2 (N=30K, NB=128)
- **Efficacité**: ~11%
- **Amélioration NB**: +15.6%
- **Processus**: 8 (grille 2×4)
- **CPU**: Ryzen 9, 8 coeurs
- **RAM**: 32 Go

---

# TIMING

| Slide | Durée |
|-------|-------|
| 9 - Config | 45s |
| 10 - Résultats | 1m30 |
| 11 - Évolution | 1m |
| 12 - Efficacité | 1m |
| 13 - Limites | 1m |
| 14 - Conclusion | 30s |
| **TOTAL** | **~6 min** |

---

**BON COURAGE POUR DEMAIN!**
