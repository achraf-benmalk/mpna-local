#!/usr/bin/env python3
"""
HPL Benchmark - Génération des Graphiques (Français)
Exécuter pour créer les graphiques de la présentation
"""

import matplotlib.pyplot as plt
import numpy as np

# Résultats
N_values = [10000, 20000, 30000]
GFLOPS = [15.7, 41.0, 38.2]
Time_seconds = [42.5, 130.0, 471.2]

# Configuration du style
plt.rcParams['font.size'] = 12
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 0.3

# ============================================
# GRAPHIQUE 1: GFLOPS vs Taille du Problème
# ============================================
fig1, ax1 = plt.subplots(figsize=(10, 6))

colors = ['#3498db', '#2ecc71', '#e74c3c']
bars = ax1.bar(range(len(N_values)), GFLOPS, color=colors,
               edgecolor='black', linewidth=1.5, width=0.6)

ax1.set_xticks(range(len(N_values)))
ax1.set_xticklabels([f'N = {n:,}'.replace(',', ' ') for n in N_values], fontsize=14)
ax1.set_ylabel('GFLOPS', fontsize=14, fontweight='bold')
ax1.set_xlabel('Taille du Problème (N)', fontsize=14, fontweight='bold')
ax1.set_title('Performance HPL en Fonction de la Taille du Problème', fontsize=16, fontweight='bold')

# Annotations sur les barres
for bar, gflop in zip(bars, GFLOPS):
    height = bar.get_height()
    ax1.annotate(f'{gflop:.1f}',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 5),
                textcoords="offset points",
                ha='center', va='bottom', fontsize=16, fontweight='bold')

ax1.set_ylim(0, max(GFLOPS) * 1.25)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('/home/user/mpna-local/project/presentation_fr/graphique1_gflops.png', dpi=150, bbox_inches='tight')
plt.close()

# ============================================
# GRAPHIQUE 2: Temps d'Exécution
# ============================================
fig2, ax2 = plt.subplots(figsize=(10, 6))

bars2 = ax2.bar(range(len(N_values)), Time_seconds, color='#9b59b6',
                edgecolor='black', linewidth=1.5, width=0.6)

ax2.set_xticks(range(len(N_values)))
ax2.set_xticklabels([f'N = {n:,}'.replace(',', ' ') for n in N_values], fontsize=14)
ax2.set_ylabel('Temps (secondes)', fontsize=14, fontweight='bold')
ax2.set_xlabel('Taille du Problème (N)', fontsize=14, fontweight='bold')
ax2.set_title('Temps d\'Exécution en Fonction de N', fontsize=16, fontweight='bold')

for bar, t in zip(bars2, Time_seconds):
    height = bar.get_height()
    minutes = int(t // 60)
    seconds = int(t % 60)
    if minutes > 0:
        label = f'{minutes}m {seconds}s'
    else:
        label = f'{t:.0f}s'
    ax2.annotate(label,
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 5),
                textcoords="offset points",
                ha='center', va='bottom', fontsize=14, fontweight='bold')

ax2.set_ylim(0, max(Time_seconds) * 1.2)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('/home/user/mpna-local/project/presentation_fr/graphique2_temps.png', dpi=150, bbox_inches='tight')
plt.close()

# ============================================
# GRAPHIQUE 3: Évolution GFLOPS (courbe)
# ============================================
fig3, ax3 = plt.subplots(figsize=(10, 6))

ax3.plot(N_values, GFLOPS, 'o-', markersize=14, linewidth=3, color='#2c3e50',
         markerfacecolor='#e74c3c', markeredgewidth=2, markeredgecolor='#2c3e50')

for n, g in zip(N_values, GFLOPS):
    offset = (15, 10) if n != 30000 else (-50, -25)
    ax3.annotate(f'{g:.1f} GFLOPS', (n, g), textcoords="offset points",
                xytext=offset, fontsize=12, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))

ax3.set_xlabel('Taille du Problème (N)', fontsize=14, fontweight='bold')
ax3.set_ylabel('GFLOPS', fontsize=14, fontweight='bold')
ax3.set_title('Évolution de la Performance avec la Taille du Problème', fontsize=16, fontweight='bold')
ax3.set_xticks(N_values)
ax3.set_xticklabels(['10K', '20K', '30K'], fontsize=14)

# Annotation pour le throttling
ax3.annotate('← Thermal\n    Throttling', xy=(30000, 38.2), xytext=(32000, 42),
            fontsize=11, ha='left', color='#c0392b', fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='#c0392b', lw=2))

# Zone d'augmentation
ax3.annotate('Augmentation\n(meilleur ratio\ncalcul/comm.)', xy=(15000, 28),
            fontsize=10, ha='center', color='#27ae60', fontweight='bold')

ax3.set_ylim(0, 55)
ax3.set_xlim(5000, 38000)
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('/home/user/mpna-local/project/presentation_fr/graphique3_evolution.png', dpi=150, bbox_inches='tight')
plt.close()

# ============================================
# GRAPHIQUE 4: Tableau des Résultats
# ============================================
fig4, ax4 = plt.subplots(figsize=(12, 4))
ax4.axis('off')

table_data = [
    ['N', 'NB', 'P×Q', 'Temps', 'GFLOPS', 'Statut'],
    ['10 000', '192', '2×4', '42.5 s', '15.7', '✓ VALIDÉ'],
    ['20 000', '192', '2×4', '2 min 10 s', '41.0', '✓ VALIDÉ'],
    ['30 000', '192', '2×4', '7 min 51 s', '38.2', '✓ VALIDÉ'],
]

table = ax4.table(cellText=table_data, loc='center', cellLoc='center',
                  colWidths=[0.12, 0.1, 0.1, 0.15, 0.12, 0.14])
table.auto_set_font_size(False)
table.set_fontsize(14)
table.scale(1.3, 2.2)

# Style header
for j in range(6):
    table[(0, j)].set_facecolor('#2c3e50')
    table[(0, j)].set_text_props(color='white', fontweight='bold', fontsize=14)

# Alternate row colors and style
for i in range(1, 4):
    for j in range(6):
        if i % 2 == 0:
            table[(i, j)].set_facecolor('#ecf0f1')
        else:
            table[(i, j)].set_facecolor('#ffffff')
        # Color the status column green
        if j == 5:
            table[(i, j)].set_text_props(color='#27ae60', fontweight='bold')
        # Highlight best GFLOPS
        if j == 4 and i == 2:
            table[(i, j)].set_text_props(fontweight='bold', color='#e74c3c')
            table[(i, j)].set_facecolor('#ffeaa7')

plt.title('Tableau Récapitulatif des Résultats HPL', fontsize=18, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('/home/user/mpna-local/project/presentation_fr/graphique4_tableau.png', dpi=150, bbox_inches='tight')
plt.close()

# ============================================
# GRAPHIQUE 5: Comparaison Efficacité
# ============================================
fig5, ax5 = plt.subplots(figsize=(10, 6))

categories = ['Notre Setup\n(Laptop WSL)', 'Cluster HPC\n(Typique)', 'TOP500\n(Meilleurs)']
efficiencies = [10, 75, 85]
colors = ['#e74c3c', '#3498db', '#2ecc71']

bars = ax5.barh(categories, efficiencies, color=colors, edgecolor='black', linewidth=1.5, height=0.5)

ax5.set_xlim(0, 100)
ax5.set_xlabel('Efficacité (%)', fontsize=14, fontweight='bold')
ax5.set_title('Comparaison de l\'Efficacité HPL', fontsize=16, fontweight='bold')

for bar, eff in zip(bars, efficiencies):
    width = bar.get_width()
    ax5.annotate(f'{eff}%',
                xy=(width + 2, bar.get_y() + bar.get_height()/2),
                va='center', fontsize=14, fontweight='bold')

ax5.axvline(x=70, color='gray', linestyle='--', alpha=0.5, label='Seuil "Bon"')
ax5.spines['top'].set_visible(False)
ax5.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('/home/user/mpna-local/project/presentation_fr/graphique5_efficacite.png', dpi=150, bbox_inches='tight')
plt.close()

print("✓ Graphiques créés avec succès!")
print("  - graphique1_gflops.png")
print("  - graphique2_temps.png")
print("  - graphique3_evolution.png")
print("  - graphique4_tableau.png")
print("  - graphique5_efficacite.png")
print("\nFichiers dans: /home/user/mpna-local/project/presentation_fr/")
