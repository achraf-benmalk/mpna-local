# Présentation HPL - Contenu des Slides (Copier dans PowerPoint)
## Ta Partie : Slides 9-14
### Présentation MPNA - 28 janvier 2026

---

# SLIDE 9 : Configuration Expérimentale

## Titre
**Configuration Expérimentale**

## Contenu (utiliser des puces)

### 🖥️ Plateforme de Test
- **Machine** : ASUS Zephyrus G14 (2020)
- **CPU** : AMD Ryzen 9 4900HS (8 cœurs / 16 threads)
- **RAM** : 32 Go
- **OS** : Ubuntu 22.04 via WSL2

### 📦 Logiciels
- HPL version 2.3
- OpenMPI (communication inter-processus)
- OpenBLAS (bibliothèque BLAS)

### ⚙️ Paramètres HPL
- **NB** = 192 (taille de bloc)
- **P × Q** = 2 × 4 (grille de 8 processus)
- **8 processus MPI** au total

---

# SLIDE 10 : Résultats des Expériences

## Titre
**Résultats des Expériences**

## Contenu (TABLEAU)

| N | NB | P×Q | Temps | GFLOPS | Statut |
|---|---|---|---|---|---|
| 10 000 | 192 | 2×4 | 42 s | 15.7 | ✓ VALIDÉ |
| 20 000 | 192 | 2×4 | 2 min 10 s | **41.0** | ✓ VALIDÉ |
| 30 000 | 192 | 2×4 | 7 min 51 s | 38.2 | ✓ VALIDÉ |

### Observation Clé (texte en dessous du tableau)
📈 **Tendance** : GFLOPS augmente avec N, puis diminue à N=30K (thermal throttling)

---

# SLIDE 11 : Évolution de la Performance

## Titre
**Évolution des GFLOPS**

## Contenu
[INSÉRER : graphique1_gflops.png OU graphique3_evolution.png]

### Points Clés (à côté du graphique)
- **N=10K** → 15.7 GFLOPS (référence)
- **N=20K** → 41.0 GFLOPS (**+161%** 📈)
- **N=30K** → 38.2 GFLOPS (-7%, throttling 🌡️)

### Explication
> "Plus N est grand, meilleur est le ratio calcul/communication"
>
> "La baisse à N=30K est due au thermal throttling du CPU"

---

# SLIDE 12 : Analyse de l'Efficacité

## Titre
**Analyse de l'Efficacité**

## Contenu

### 📊 Calcul de l'Efficacité
```
Efficacité = GFLOPS obtenus / GFLOPS théoriques × 100%

Pic théorique (Ryzen 9) : ~400 GFLOPS
Meilleur résultat : 41.0 GFLOPS

→ Efficacité : ~10%
```

### ❓ Pourquoi Seulement 10% ?

| Facteur | Impact |
|---------|--------|
| 🖥️ WSL2 | Overhead de virtualisation |
| 📚 OpenBLAS | Moins optimisé qu'Intel MKL |
| 🌡️ Laptop | Limites thermiques vs serveur HPC |

### 📌 Référence
> Sur cluster HPC réel : **70-85%** d'efficacité attendue

---

# SLIDE 13 : Observations et Limites

## Titre
**Observations et Limites**

## Contenu

### ✅ Ce Qui Fonctionne
- Performance scale avec N (jusqu'aux limites thermiques)
- Tous les tests passent la validation numérique (PASSED)
- Résultats reproductibles et cohérents

### ⚠️ Limites de Notre Setup
- **WSL2** : couche de virtualisation = overhead
- **Laptop** : refroidissement limité → throttling après ~5 min
- **OpenBLAS** : pas optimisé pour AMD Ryzen

### 🔧 Pour Améliorer
- Cluster HPC dédié avec refroidissement adapté
- Intel MKL ou AMD BLIS (bibliothèques optimisées)
- Plus de RAM → N plus grand → meilleure efficacité

---

# SLIDE 14 : Conclusion

## Titre
**Conclusion**

## Contenu

### 📝 Ce Qu'on Retient

✓ **HPL mesure les GFLOPS** via résolution de Ax = b

✓ **Algorithme** : Décomposition LU avec pivotage partiel

✓ **Parallélisation** : Distribution 2D block-cyclic

✓ **Nos résultats** : Validés, cohérents avec la théorie

### 📈 Tendance Observée
> GFLOPS ↑ avec N (meilleur ratio calcul/communication)
> jusqu'aux limites thermiques du matériel

---

### Au centre en bas :
# **Merci - Questions ?**

---

# CONSEILS DE DESIGN

## Couleurs à Utiliser
- Titres : Bleu foncé (#2C3E50)
- Résultats positifs : Vert (#27AE60)
- Avertissements/limites : Orange (#E67E22)
- Statut VALIDÉ : Vert
- Chiffres importants : **Gras**

## Tailles de Police
- Titre de slide : 36-44pt
- Sous-titres : 24-28pt
- Texte normal : 18-22pt
- Texte tableau : 16-18pt

## Mise en Page
- Ne pas surcharger les slides
- Maximum 6 puces par slide
- Laisser de l'espace blanc
- Un graphique par slide

---

# FICHIERS À INSÉRER

Les graphiques sont dans le dossier `presentation_fr/` :

1. **graphique1_gflops.png** - Barres GFLOPS vs N
2. **graphique2_temps.png** - Barres Temps vs N
3. **graphique3_evolution.png** - Courbe avec annotation throttling
4. **graphique4_tableau.png** - Tableau formaté (alternative)
5. **graphique5_efficacite.png** - Comparaison efficacité

**Recommandé pour Slide 11** : graphique3_evolution.png (le plus parlant)

---

# COMMENT CRÉER LA PRÉSENTATION

1. Ouvrir PowerPoint
2. Créer 6 slides (numérotés 9-14 si partie 2)
3. Copier le contenu ci-dessus
4. Insérer les graphiques du dossier `presentation_fr/`
5. Appliquer un formatage cohérent
6. Sauvegarder en `.pptx`

---

*Contenu des slides pour Présentation MPNA HPL - 28 janvier 2026*
