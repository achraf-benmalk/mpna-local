#!/usr/bin/env python3
"""
HPL Benchmark - Graphiques Mis à Jour (Français)
Inclut les résultats de tuning NB
"""

import matplotlib.pyplot as plt
import numpy as np

# Résultats - Scaling N (NB=192)
N_values = [10000, 20000, 30000]
GFLOPS_NB192 = [15.7, 41.0, 38.2]
Time_NB192 = [42.5, 130.0, 471.2]

# Résultats - Tuning NB (N=30000)
NB_values = [128, 192]
GFLOPS_NB = [44.2, 38.2]
Time_NB = [407.5, 471.2]

# Configuration du style
plt.rcParams['font.size'] = 12
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 0.3

# ============================================
# GRAPHIQUE 1: GFLOPS vs N (NB=192)
# ============================================
fig1, ax1 = plt.subplots(figsize=(10, 6))

colors = ['#3498db', '#2ecc71', '#e74c3c']
bars = ax1.bar(range(len(N_values)), GFLOPS_NB192, color=colors,
               edgecolor='black', linewidth=1.5, width=0.6)

ax1.set_xticks(range(len(N_values)))
ax1.set_xticklabels([f'N = {n:,}'.replace(',', ' ') for n in N_values], fontsize=14)
ax1.set_ylabel('GFLOPS', fontsize=14, fontweight='bold')
ax1.set_xlabel('Taille du Problème (N)', fontsize=14, fontweight='bold')
ax1.set_title('Performance HPL vs Taille du Problème (NB=192)', fontsize=16, fontweight='bold')

for bar, gflop in zip(bars, GFLOPS_NB192):
    height = bar.get_height()
    ax1.annotate(f'{gflop:.1f}',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 5),
                textcoords="offset points",
                ha='center', va='bottom', fontsize=16, fontweight='bold')

ax1.set_ylim(0, max(GFLOPS_NB192) * 1.25)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('/home/user/mpna-local/project/presentation_fr/graphique1_gflops.png', dpi=150, bbox_inches='tight')
plt.close()

# ============================================
# GRAPHIQUE 2: Comparaison NB (N=30000) - NOUVEAU!
# ============================================
fig2, ax2 = plt.subplots(figsize=(10, 6))

colors_nb = ['#27ae60', '#e74c3c']  # Vert pour meilleur, rouge pour moins bon
bars2 = ax2.bar(range(len(NB_values)), GFLOPS_NB, color=colors_nb,
                edgecolor='black', linewidth=1.5, width=0.5)

ax2.set_xticks(range(len(NB_values)))
ax2.set_xticklabels([f'NB = {nb}' for nb in NB_values], fontsize=16)
ax2.set_ylabel('GFLOPS', fontsize=14, fontweight='bold')
ax2.set_xlabel('Taille de Bloc (NB)', fontsize=14, fontweight='bold')
ax2.set_title('Impact de la Taille de Bloc sur la Performance (N=30 000)', fontsize=16, fontweight='bold')

for bar, gflop in zip(bars2, GFLOPS_NB):
    height = bar.get_height()
    ax2.annotate(f'{gflop:.1f}',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 5),
                textcoords="offset points",
                ha='center', va='bottom', fontsize=18, fontweight='bold')

# Annotation pour le meilleur
ax2.annotate('+15.6%', xy=(0, 44.2), xytext=(0.3, 48),
            fontsize=14, fontweight='bold', color='#27ae60',
            arrowprops=dict(arrowstyle='->', color='#27ae60', lw=2))

ax2.set_ylim(0, 55)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('/home/user/mpna-local/project/presentation_fr/graphique2_tuning_nb.png', dpi=150, bbox_inches='tight')
plt.close()

# ============================================
# GRAPHIQUE 3: Évolution GFLOPS (courbe avec meilleur résultat)
# ============================================
fig3, ax3 = plt.subplots(figsize=(11, 6))

# Courbe NB=192
ax3.plot(N_values, GFLOPS_NB192, 'o-', markersize=12, linewidth=3, color='#3498db',
         markerfacecolor='white', markeredgewidth=2, label='NB=192')

# Point optimisé NB=128
ax3.plot(30000, 44.2, 's', markersize=14, color='#27ae60',
         markeredgecolor='black', markeredgewidth=2, label='NB=128 (optimisé)')

for n, g in zip(N_values, GFLOPS_NB192):
    offset = (10, 10) if n != 30000 else (10, -25)
    ax3.annotate(f'{g:.1f}', (n, g), textcoords="offset points",
                xytext=offset, fontsize=11, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#3498db', alpha=0.3))

# Annotation meilleur résultat
ax3.annotate(f'44.2 GFLOPS\n(NB=128)', (30000, 44.2), textcoords="offset points",
            xytext=(-80, 15), fontsize=11, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#27ae60', alpha=0.5),
            arrowprops=dict(arrowstyle='->', color='#27ae60', lw=2))

ax3.set_xlabel('Taille du Problème (N)', fontsize=14, fontweight='bold')
ax3.set_ylabel('GFLOPS', fontsize=14, fontweight='bold')
ax3.set_title('Évolution de la Performance avec Tuning', fontsize=16, fontweight='bold')
ax3.set_xticks(N_values)
ax3.set_xticklabels(['10K', '20K', '30K'], fontsize=14)
ax3.legend(loc='upper left', fontsize=12)

ax3.set_ylim(0, 55)
ax3.set_xlim(5000, 35000)
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('/home/user/mpna-local/project/presentation_fr/graphique3_evolution.png', dpi=150, bbox_inches='tight')
plt.close()

# ============================================
# GRAPHIQUE 4: Tableau Complet des Résultats
# ============================================
fig4, ax4 = plt.subplots(figsize=(14, 5))
ax4.axis('off')

table_data = [
    ['N', 'NB', 'P×Q', 'Temps', 'GFLOPS', 'Statut'],
    ['10 000', '192', '2×4', '42 s', '15.7', '✓ VALIDÉ'],
    ['20 000', '192', '2×4', '2 min 10 s', '41.0', '✓ VALIDÉ'],
    ['30 000', '192', '2×4', '7 min 51 s', '38.2', '✓ VALIDÉ'],
    ['30 000', '128', '2×4', '6 min 48 s', '44.2 ⭐', '✓ VALIDÉ'],
]

table = ax4.table(cellText=table_data, loc='center', cellLoc='center',
                  colWidths=[0.12, 0.08, 0.08, 0.14, 0.12, 0.12])
table.auto_set_font_size(False)
table.set_fontsize(13)
table.scale(1.3, 2.2)

# Style header
for j in range(6):
    table[(0, j)].set_facecolor('#2c3e50')
    table[(0, j)].set_text_props(color='white', fontweight='bold', fontsize=13)

# Alternate row colors and highlight best
for i in range(1, 5):
    for j in range(6):
        if i % 2 == 0:
            table[(i, j)].set_facecolor('#ecf0f1')
        else:
            table[(i, j)].set_facecolor('#ffffff')
        # Color the status column green
        if j == 5:
            table[(i, j)].set_text_props(color='#27ae60', fontweight='bold')
        # Highlight best result row
        if i == 4:
            table[(i, j)].set_facecolor('#d5f5e3')
            if j == 4:
                table[(i, j)].set_text_props(fontweight='bold', color='#27ae60', fontsize=14)

plt.title('Tableau Récapitulatif des Résultats HPL', fontsize=18, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('/home/user/mpna-local/project/presentation_fr/graphique4_tableau.png', dpi=150, bbox_inches='tight')
plt.close()

# ============================================
# GRAPHIQUE 5: Comparaison Efficacité
# ============================================
fig5, ax5 = plt.subplots(figsize=(10, 6))

categories = ['Notre Laptop\n(NB=192)', 'Notre Laptop\n(NB=128, optimisé)', 'Cluster HPC\n(Typique)']
efficiencies = [10, 11, 75]
colors = ['#e74c3c', '#27ae60', '#3498db']

bars = ax5.barh(categories, efficiencies, color=colors, edgecolor='black', linewidth=1.5, height=0.5)

ax5.set_xlim(0, 100)
ax5.set_xlabel('Efficacité (%)', fontsize=14, fontweight='bold')
ax5.set_title('Comparaison de l\'Efficacité HPL', fontsize=16, fontweight='bold')

for bar, eff in zip(bars, efficiencies):
    width = bar.get_width()
    ax5.annotate(f'{eff}%',
                xy=(width + 2, bar.get_y() + bar.get_height()/2),
                va='center', fontsize=14, fontweight='bold')

ax5.axvline(x=70, color='gray', linestyle='--', alpha=0.5)
ax5.text(72, 2.3, 'Seuil "Bon"', fontsize=10, color='gray')
ax5.spines['top'].set_visible(False)
ax5.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('/home/user/mpna-local/project/presentation_fr/graphique5_efficacite.png', dpi=150, bbox_inches='tight')
plt.close()

# ============================================
# GRAPHIQUE 6: Temps d'exécution
# ============================================
fig6, ax6 = plt.subplots(figsize=(10, 6))

bars6 = ax6.bar(range(len(N_values)), Time_NB192, color='#9b59b6',
                edgecolor='black', linewidth=1.5, width=0.6)

ax6.set_xticks(range(len(N_values)))
ax6.set_xticklabels([f'N = {n:,}'.replace(',', ' ') for n in N_values], fontsize=14)
ax6.set_ylabel('Temps (secondes)', fontsize=14, fontweight='bold')
ax6.set_xlabel('Taille du Problème (N)', fontsize=14, fontweight='bold')
ax6.set_title('Temps d\'Exécution vs Taille du Problème', fontsize=16, fontweight='bold')

for bar, t in zip(bars6, Time_NB192):
    height = bar.get_height()
    minutes = int(t // 60)
    seconds = int(t % 60)
    if minutes > 0:
        label = f'{minutes}m {seconds}s'
    else:
        label = f'{t:.0f}s'
    ax6.annotate(label,
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 5),
                textcoords="offset points",
                ha='center', va='bottom', fontsize=14, fontweight='bold')

ax6.set_ylim(0, max(Time_NB192) * 1.2)
ax6.spines['top'].set_visible(False)
ax6.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('/home/user/mpna-local/project/presentation_fr/graphique6_temps.png', dpi=150, bbox_inches='tight')
plt.close()

print("✓ Graphiques mis à jour avec succès!")
print("\nFichiers créés:")
print("  - graphique1_gflops.png (GFLOPS vs N)")
print("  - graphique2_tuning_nb.png (Comparaison NB) ← NOUVEAU!")
print("  - graphique3_evolution.png (Courbe avec point optimisé)")
print("  - graphique4_tableau.png (Tableau complet avec 4 résultats)")
print("  - graphique5_efficacite.png (Efficacité)")
print("  - graphique6_temps.png (Temps d'exécution)")
print("\nMeilleur résultat: 44.2 GFLOPS (N=30000, NB=128)")
