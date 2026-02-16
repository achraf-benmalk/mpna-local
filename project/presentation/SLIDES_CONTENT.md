# HPL Presentation - Slides Content (Copy to PowerPoint)
## Your Part: Slides 9-14

---

# SLIDE 9: Configuration Expérimentale

## Title
**Configuration Expérimentale**

## Content (use bullet points)

### Plateforme de Test
- Machine : ASUS Zephyrus G14 (2020)
- CPU : AMD Ryzen 9 4900HS (8 cœurs / 16 threads)
- RAM : 32 Go
- OS : Ubuntu 22.04 via WSL2

### Logiciels
- HPL version 2.3
- OpenMPI (communication inter-processus)
- OpenBLAS (bibliothèque d'algèbre linéaire)

### Paramètres HPL
- NB = 192 (taille de bloc)
- P × Q = 2 × 4 (grille de 8 processus)

---

# SLIDE 10: Résultats des Expériences

## Title
**Résultats des Expériences**

## Content (TABLE - create this in PowerPoint)

| N | NB | P×Q | Temps (s) | GFLOPS | Statut |
|---|---|---|---|---|---|
| 10 000 | 192 | 2×4 | 42.5 | 15.7 | ✓ PASSED |
| 20 000 | 192 | 2×4 | 130.0 | 41.0 | ✓ PASSED |
| 30 000 | 192 | 2×4 | 471.2 | 38.2 | ✓ PASSED |

### Key Observation (add as text below table)
→ GFLOPS augmente avec N, puis diminue à N=30K (thermal throttling)

---

# SLIDE 11: Performance - Graphique

## Title
**Évolution des GFLOPS**

## Content
[INSERT: graph1_gflops_vs_n.png OR graph3_gflops_trend.png]

### Points Clés (bullet points next to graph)
- N=10K → 15.7 GFLOPS (baseline)
- N=20K → 41.0 GFLOPS (+161%)
- N=30K → 38.2 GFLOPS (-7%, throttling)

### Explication
"Plus N est grand, meilleur est le ratio calcul/communication"

---

# SLIDE 12: Analyse de l'Efficacité

## Title
**Analyse de l'Efficacité**

## Content

### Calcul
```
Efficacité = GFLOPS obtenus / GFLOPS théoriques × 100%

Peak théorique (estimé) : ~400 GFLOPS
Meilleur résultat : 41.0 GFLOPS
Efficacité : ~10%
```

### Pourquoi 10% seulement ?

| Facteur | Impact |
|---------|--------|
| WSL2 | Overhead de virtualisation |
| OpenBLAS | Moins optimisé qu'Intel MKL |
| Laptop | Limites thermiques vs serveur HPC |

### Référence
Sur cluster HPC réel : 70-85% d'efficacité attendue

---

# SLIDE 13: Observations et Limites

## Title
**Observations et Limites**

## Content

### ✓ Ce qui fonctionne
- Performance scale avec N (jusqu'aux limites thermiques)
- Tous les tests passent la validation numérique (PASSED)
- Résultats reproductibles et cohérents

### ✗ Limites de notre setup
- WSL2 : couche de virtualisation = overhead
- Laptop : refroidissement limité → throttling après ~5 min
- OpenBLAS : pas optimisé pour AMD Ryzen

### → Pour améliorer
- Cluster HPC dédié avec refroidissement adapté
- Intel MKL ou AMD BLIS (bibliothèques optimisées)
- Plus de RAM → N plus grand → meilleure efficacité

---

# SLIDE 14: Conclusion

## Title
**Conclusion**

## Content

### Ce qu'on retient

✓ **HPL mesure les GFLOPS** via résolution de Ax = b

✓ **Algorithme** : Décomposition LU avec pivotage partiel

✓ **Parallélisation** : Distribution 2D block-cyclic

✓ **Nos résultats** : Validés, cohérents avec la théorie

### Tendance observée
GFLOPS ↑ avec N (meilleur ratio calcul/communication)
jusqu'aux limites thermiques du matériel

---

## Center this at bottom:
**Merci - Questions ?**

---

# SLIDE DESIGN TIPS

## Colors to Use
- Title: Dark blue (#2C3E50)
- Positive results: Green (#27AE60)
- Warnings/limits: Orange (#E67E22)
- PASSED status: Green
- Important numbers: Bold

## Font Sizes
- Slide title: 36-44pt
- Section headers: 24-28pt
- Body text: 18-22pt
- Table text: 16-18pt

## Layout
- Don't overcrowd slides
- Max 6 bullet points per slide
- Leave white space
- One graph per slide

---

# HOW TO CREATE THE PRESENTATION

1. Open PowerPoint
2. Create 6 slides (9-14)
3. Copy content from above
4. Insert graphs from `presentation/` folder
5. Apply consistent formatting
6. Save as HPL_Presentation_Part2.pptx

---

*Slides content for MPNA HPL Presentation*
