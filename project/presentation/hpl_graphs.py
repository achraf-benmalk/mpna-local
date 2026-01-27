#!/usr/bin/env python3
"""
HPL Benchmark Results - Graph Generation
Run this to create graphs for your presentation
"""

import matplotlib.pyplot as plt
import numpy as np

# Your results
N_values = [10000, 20000, 30000]
GFLOPS = [15.7, 41.0, 38.2]
Time_seconds = [42.5, 130.0, 471.2]

# Theoretical FLOPS calculation
def theoretical_flops(N):
    return (2/3) * (N ** 3)

theoretical = [theoretical_flops(n) / 1e9 for n in N_values]  # in GFLOPS-seconds
actual_flops = [theoretical_flops(n) / 1e9 for n in N_values]

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.size'] = 12
plt.rcParams['figure.figsize'] = (10, 6)

# ============================================
# GRAPH 1: GFLOPS vs Problem Size N
# ============================================
fig1, ax1 = plt.subplots(figsize=(10, 6))

bars = ax1.bar(range(len(N_values)), GFLOPS, color=['#3498db', '#2ecc71', '#e74c3c'],
               edgecolor='black', linewidth=1.5)

ax1.set_xticks(range(len(N_values)))
ax1.set_xticklabels([f'N = {n:,}' for n in N_values], fontsize=14)
ax1.set_ylabel('GFLOPS (milliards d\'opérations/seconde)', fontsize=14)
ax1.set_xlabel('Taille du problème (N)', fontsize=14)
ax1.set_title('Performance HPL vs Taille du Problème', fontsize=16, fontweight='bold')

# Add value labels on bars
for bar, gflop in zip(bars, GFLOPS):
    height = bar.get_height()
    ax1.annotate(f'{gflop:.1f}',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3),
                textcoords="offset points",
                ha='center', va='bottom', fontsize=14, fontweight='bold')

ax1.set_ylim(0, max(GFLOPS) * 1.2)
plt.tight_layout()
plt.savefig('/home/user/mpna-local/project/presentation/graph1_gflops_vs_n.png', dpi=150, bbox_inches='tight')
plt.close()

# ============================================
# GRAPH 2: Execution Time vs Problem Size
# ============================================
fig2, ax2 = plt.subplots(figsize=(10, 6))

bars2 = ax2.bar(range(len(N_values)), Time_seconds, color=['#9b59b6', '#9b59b6', '#9b59b6'],
                edgecolor='black', linewidth=1.5)

ax2.set_xticks(range(len(N_values)))
ax2.set_xticklabels([f'N = {n:,}' for n in N_values], fontsize=14)
ax2.set_ylabel('Temps d\'exécution (secondes)', fontsize=14)
ax2.set_xlabel('Taille du problème (N)', fontsize=14)
ax2.set_title('Temps d\'Exécution vs Taille du Problème', fontsize=16, fontweight='bold')

for bar, t in zip(bars2, Time_seconds):
    height = bar.get_height()
    ax2.annotate(f'{t:.1f}s',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3),
                textcoords="offset points",
                ha='center', va='bottom', fontsize=14, fontweight='bold')

ax2.set_ylim(0, max(Time_seconds) * 1.2)
plt.tight_layout()
plt.savefig('/home/user/mpna-local/project/presentation/graph2_time_vs_n.png', dpi=150, bbox_inches='tight')
plt.close()

# ============================================
# GRAPH 3: GFLOPS Line Chart (trend)
# ============================================
fig3, ax3 = plt.subplots(figsize=(10, 6))

ax3.plot(N_values, GFLOPS, 'o-', markersize=12, linewidth=3, color='#e74c3c',
         markerfacecolor='white', markeredgewidth=3)

for n, g in zip(N_values, GFLOPS):
    ax3.annotate(f'{g:.1f}', (n, g), textcoords="offset points",
                xytext=(10, 10), fontsize=12, fontweight='bold')

ax3.set_xlabel('Taille du problème (N)', fontsize=14)
ax3.set_ylabel('GFLOPS', fontsize=14)
ax3.set_title('Évolution des GFLOPS avec N', fontsize=16, fontweight='bold')
ax3.set_xticks(N_values)
ax3.set_xticklabels([f'{n//1000}K' for n in N_values])

# Add annotation for the drop
ax3.annotate('Throttling\nthermique?', xy=(30000, 38.2), xytext=(27000, 30),
            fontsize=11, ha='center',
            arrowprops=dict(arrowstyle='->', color='gray'))

plt.tight_layout()
plt.savefig('/home/user/mpna-local/project/presentation/graph3_gflops_trend.png', dpi=150, bbox_inches='tight')
plt.close()

# ============================================
# GRAPH 4: Results Summary Table as Image
# ============================================
fig4, ax4 = plt.subplots(figsize=(10, 4))
ax4.axis('off')

table_data = [
    ['N', 'NB', 'P×Q', 'Temps (s)', 'GFLOPS', 'Statut'],
    ['10 000', '192', '2×4', '42.5', '15.7', 'PASSED'],
    ['20 000', '192', '2×4', '130.0', '41.0', 'PASSED'],
    ['30 000', '192', '2×4', '471.2', '38.2', 'PASSED'],
]

colors = [['#3498db']*6] + [['white']*6]*3
table = ax4.table(cellText=table_data, loc='center', cellLoc='center',
                  colWidths=[0.15]*6)
table.auto_set_font_size(False)
table.set_fontsize(14)
table.scale(1.2, 2)

# Style header
for j in range(6):
    table[(0, j)].set_facecolor('#2c3e50')
    table[(0, j)].set_text_props(color='white', fontweight='bold')

# Alternate row colors
for i in range(1, 4):
    for j in range(6):
        if i % 2 == 0:
            table[(i, j)].set_facecolor('#ecf0f1')

plt.title('Résultats des Expériences HPL', fontsize=16, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('/home/user/mpna-local/project/presentation/graph4_results_table.png', dpi=150, bbox_inches='tight')
plt.close()

print("✓ Graphs created successfully!")
print("  - graph1_gflops_vs_n.png")
print("  - graph2_time_vs_n.png")
print("  - graph3_gflops_trend.png")
print("  - graph4_results_table.png")
print("\nFiles saved in: /home/user/mpna-local/project/presentation/")
