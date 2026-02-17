#!/usr/bin/env python3
"""Generate the HPL presentation slides (Part 2: Execution, Results, Analysis).
Styled to match the binome's template (hpl_karim_versionfinale.pptx)."""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import os

IMG_DIR = os.path.join(os.path.dirname(__file__), '..', 'latex report', 'images')
OUT_DIR = os.path.join(os.path.dirname(__file__), 'presentation_finale')
os.makedirs(OUT_DIR, exist_ok=True)

# Template color palette
DARK_TEAL = RGBColor(0x14, 0x34, 0x40)
OFF_WHITE = RGBColor(0xFA, 0xF8, 0xF5)
ORANGE = RGBColor(0xFF, 0x6B, 0x35)
NEAR_BLACK = RGBColor(0x28, 0x28, 0x28)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)

SLIDE_W = Inches(10)
SLIDE_H = Inches(7.5)

prs = Presentation()
prs.slide_width = SLIDE_W
prs.slide_height = SLIDE_H


def add_content_bg(slide):
    """Off-white background + thin orange left stripe (template pattern)."""
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SLIDE_W, SLIDE_H)
    bg.fill.solid()
    bg.fill.fore_color.rgb = OFF_WHITE
    bg.line.fill.background()
    stripe = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(0.08), SLIDE_H)
    stripe.fill.solid()
    stripe.fill.fore_color.rgb = ORANGE
    stripe.line.fill.background()


def add_slide_title(slide, text):
    """Title text + orange accent bar below (template pattern)."""
    tf = add_text(slide, Inches(0.60), Inches(0.15), Inches(8.5), Inches(0.7),
                  text, 42, True, DARK_TEAL)
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, Inches(0.95), Inches(2.5), Inches(0.15))
    bar.fill.solid()
    bar.fill.fore_color.rgb = ORANGE
    bar.line.fill.background()
    return tf


def add_text(slide, left, top, width, height, text, size=20, bold=False,
             color=NEAR_BLACK, align=PP_ALIGN.LEFT):
    """Add a text box and return the text frame."""
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(size)
    p.font.bold = bold
    p.font.color.rgb = color
    p.alignment = align
    return tf


def add_orange_bullet(slide, left, top):
    """Small orange rounded-rectangle bullet marker (template pattern)."""
    dot = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(0.12), Inches(0.12))
    dot.fill.solid()
    dot.fill.fore_color.rgb = ORANGE
    dot.line.fill.background()


def add_bullet_items(slide, left, top, width, items, size=16, color=NEAR_BLACK, spacing=0.40):
    """Add bullet items with orange dot markers."""
    for i, item in enumerate(items):
        y = top + Inches(i * spacing)
        add_orange_bullet(slide, left, y + Inches(0.05))
        add_text(slide, left + Inches(0.25), y, width - Inches(0.25), Inches(0.35),
                 item, size, False, color)


def add_sub_heading(slide, left, top, text):
    """Orange sub-heading (template pattern)."""
    add_text(slide, left, top, Inches(8), Inches(0.45), text, 24, True, ORANGE)


def add_table(slide, left, top, width, height, data, col_widths=None):
    rows, cols = len(data), len(data[0])
    table_shape = slide.shapes.add_table(rows, cols, left, top, width, height)
    table = table_shape.table
    if col_widths:
        for i, w in enumerate(col_widths):
            table.columns[i].width = w
    for r, row_data in enumerate(data):
        for c, val in enumerate(row_data):
            cell = table.cell(r, c)
            cell.text = str(val)
            for paragraph in cell.text_frame.paragraphs:
                paragraph.font.size = Pt(13)
                paragraph.alignment = PP_ALIGN.CENTER
                if r == 0:
                    paragraph.font.bold = True
                    paragraph.font.color.rgb = WHITE
                else:
                    paragraph.font.color.rgb = NEAR_BLACK
            if r == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = DARK_TEAL
            elif r % 2 == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor(0xF0, 0xEE, 0xEB)
    return table


# ============================================================
# SLIDE 1: Title (dark teal background, matching template slide 1)
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank
bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SLIDE_W, SLIDE_H)
bg.fill.solid()
bg.fill.fore_color.rgb = DARK_TEAL
bg.line.fill.background()

add_text(slide, Inches(0.6), Inches(1.5), Inches(8.5), Inches(1),
         "HPL Benchmark : Résultats GPU", 48, True, WHITE)
# Orange accent bar
bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, Inches(2.7), Inches(5.5), Inches(0.15))
bar.fill.solid()
bar.fill.fore_color.rgb = ORANGE
bar.line.fill.background()
add_text(slide, Inches(0.6), Inches(3.1), Inches(8.5), Inches(0.8),
         "Analyse comparative A100 vs H100", 30, False, WHITE)
add_text(slide, Inches(0.6), Inches(4.2), Inches(8.5), Inches(0.5),
         "Partie 2 : Exécution, Résultats, Analyse", 20, False, RGBColor(0xCC, 0xCC, 0xCC))
add_text(slide, Inches(0.6), Inches(5.2), Inches(8.5), Inches(0.5),
         "BENMALK Achraf  |  Projet MPNA  |  2026", 18, False, RGBColor(0x99, 0x99, 0x99))

# ============================================================
# SLIDE 2: Plateforme d'exécution
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_content_bg(slide)
add_slide_title(slide, "Plateforme d'exécution")

add_sub_heading(slide, Inches(0.6), Inches(1.25), "Environnement")
add_bullet_items(slide, Inches(0.6), Inches(1.75), Inches(4.5), [
    "Cluster HPC avec nœuds GPU NVIDIA",
    "Conteneur NVIDIA HPC-Benchmarks 23.10",
    "Déploiement via Singularity",
    "Ordonnanceur Slurm",
], 15, spacing=0.35)

add_sub_heading(slide, Inches(5.3), Inches(1.25), "GPUs testés")
data = [
    ["", "A100", "H100"],
    ["Architecture", "Ampere", "Hopper"],
    ["Partition", "gpu", "gpu_h100"],
    ["Mémoire", "80 Go HBM2e", "80 Go HBM3"],
    ["Cœurs CUDA", "6 912", "16 896"],
    ["Peak FP64", "19,5 TFLOPS", "54 TFLOPS"],
]
add_table(slide, Inches(5.3), Inches(1.75), Inches(4.3), Inches(2.5), data)

add_sub_heading(slide, Inches(0.6), Inches(4.65), "Configuration HPL")
add_bullet_items(slide, Inches(0.6), Inches(5.15), Inches(8.5), [
    "NB = 576 (blocs larges pour saturer les cœurs GPU)",
    "P × Q = 2 × 1 (1 processus MPI par GPU)",
    "BCAST = 6 (broadcast MPI)",
], 15, spacing=0.35)

# ============================================================
# SLIDE 3: Étapes d'exécution (2x2 grid for 4:3)
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_content_bg(slide)
add_slide_title(slide, "Étapes d'exécution sur GPU")

steps = [
    ("1. HPL.dat", "Création du fichier de configuration\n(N, NB, P×Q)", "Step1.png"),
    ("2. Singularity", "Lancement du conteneur avec\nbind du répertoire", "Step2.png"),
    ("3. Slurm", "Allocation GPU via salloc\n(--gres=gpu:1 ou gpu:2)", "Step3.png"),
    ("4. Exécution", "mpirun -np <X> ./hpl.sh\n--dat /mnt/HPL.dat", "Step4.png"),
]

positions = [
    (Inches(0.4), Inches(1.3)),   # top-left
    (Inches(4.9), Inches(1.3)),   # top-right
    (Inches(0.4), Inches(4.3)),   # bottom-left
    (Inches(4.9), Inches(4.3)),   # bottom-right
]

for i, (title, desc, img) in enumerate(steps):
    x, y = positions[i]
    box_w, box_h = Inches(4.4), Inches(2.8)
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, box_w, box_h)
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor(0xF0, 0xEE, 0xEB)
    shape.line.color.rgb = ORANGE
    shape.line.width = Pt(1.5)

    add_text(slide, x + Inches(0.15), y + Inches(0.1), Inches(2), Inches(0.4),
             title, 18, True, DARK_TEAL)
    add_text(slide, x + Inches(0.15), y + Inches(0.5), Inches(2), Inches(0.7),
             desc, 12, False, NEAR_BLACK)

    img_path = os.path.join(IMG_DIR, img)
    if os.path.exists(img_path):
        slide.shapes.add_picture(img_path, x + Inches(2.2), y + Inches(0.15), Inches(2.0))

# ============================================================
# SLIDE 4: Résultats A100
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_content_bg(slide)
add_slide_title(slide, "Résultats : GPU A100")

data_a100 = [
    ["N", "1 GPU (GFLOPS)", "2 GPUs (GFLOPS)", "Speedup"],
    ["20 000", "9 731", "9 106", "0,94x"],
    ["40 000", "15 890", "25 230", "1,59x"],
    ["60 000", "17 150", "31 430", "1,83x"],
    ["80 000", "17 600", "33 560", "1,91x"],
    ["100 000", "17 860", "34 720", "1,95x"],
]
add_table(slide, Inches(0.4), Inches(1.25), Inches(4.5), Inches(2.8), data_a100)

img_path = os.path.join(IMG_DIR, 'hpl-a100.png')
if os.path.exists(img_path):
    slide.shapes.add_picture(img_path, Inches(5.1), Inches(1.25), Inches(4.6))

# Key metrics
add_sub_heading(slide, Inches(0.6), Inches(4.3), "Métriques clés")
add_bullet_items(slide, Inches(0.6), Inches(4.85), Inches(8.5), [
    "Peak théorique : 19,5 TFLOPS  →  Efficacité : 91,7%",
    "Speedup 2 GPUs : 1,95x  →  Efficacité parallèle : 97%",
    "Anomalie à N=20K : 2 GPUs légèrement plus lents que 1",
    "Tous les tests : résidu PASSED",
], 15, spacing=0.38)

# ============================================================
# SLIDE 5: Résultats H100
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_content_bg(slide)
add_slide_title(slide, "Résultats : GPU H100")

data_h100 = [
    ["N", "1 GPU (GFLOPS)", "2 GPUs (GFLOPS)", "Speedup"],
    ["20 000", "16 130", "11 510", "0,71x"],
    ["40 000", "35 760", "41 460", "1,16x"],
    ["60 000", "41 760", "64 700", "1,55x"],
    ["80 000", "44 130", "76 730", "1,74x"],
    ["100 000", "45 110", "81 970", "1,82x"],
]
add_table(slide, Inches(0.4), Inches(1.25), Inches(4.5), Inches(2.8), data_h100)

img_path = os.path.join(IMG_DIR, 'hpl-h100.png')
if os.path.exists(img_path):
    slide.shapes.add_picture(img_path, Inches(5.1), Inches(1.25), Inches(4.6))

add_sub_heading(slide, Inches(0.6), Inches(4.3), "Métriques clés")
add_bullet_items(slide, Inches(0.6), Inches(4.85), Inches(8.5), [
    "Peak théorique : 54 TFLOPS  →  Efficacité : 83,4%",
    "Speedup 2 GPUs : 1,82x  →  Efficacité parallèle : 91%",
    "Anomalie à N=20K : 2 GPUs 28,6% PLUS LENTS que 1 !",
    "Tous les tests : résidu PASSED",
], 15, spacing=0.38)

# ============================================================
# SLIDE 6: Anomalie multi-GPU à N=20K
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_content_bg(slide)
add_slide_title(slide, "Anomalie multi-GPU (N = 20 000)")

data_anomaly = [
    ["GPU", "1 GPU (GFLOPS)", "2 GPUs (GFLOPS)", "Dégradation"],
    ["A100", "9 731", "9 106", "-6,4%"],
    ["H100", "16 130", "11 510", "-28,6%"],
]
add_table(slide, Inches(0.4), Inches(1.35), Inches(5), Inches(1.3), data_anomaly)

add_sub_heading(slide, Inches(0.6), Inches(2.9), "Pourquoi ?")
add_bullet_items(slide, Inches(0.6), Inches(3.4), Inches(5), [
    "N = 20 000 est trop petit pour 2 GPUs",
    "Portion de matrice insuffisante par GPU",
    "Coût de communication > gain de calcul",
    "Plus prononcé sur H100 : plus de cœurs",
    "Seuil de rentabilité : N entre 20K et 40K",
], 14, spacing=0.35)

# Right side: explanation box
box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                              Inches(5.6), Inches(1.35), Inches(4.1), Inches(4.3))
box.fill.solid()
box.fill.fore_color.rgb = RGBColor(0xF0, 0xEE, 0xEB)
box.line.color.rgb = ORANGE
box.line.width = Pt(1.5)

add_text(slide, Inches(5.8), Inches(1.5), Inches(3.7), Inches(0.4),
         "Explication", 20, True, DARK_TEAL, PP_ALIGN.CENTER)

add_text(slide, Inches(5.8), Inches(2.0), Inches(3.7), Inches(3.5),
         "Petit problème (N=20K) :\n"
         "  2 cuisiniers pour 1 petit plat\n"
         "  = coordination > cuisine\n\n"
         "Grand problème (N=100K) :\n"
         "  2 cuisiniers pour un banquet\n"
         "  = coordination négligeable\n\n"
         "Calcul : O(N³)\n"
         "Communication : O(N²)\n"
         "Grand N → calcul domine",
         13, False, NEAR_BLACK)

# ============================================================
# SLIDE 7: Comparaison A100 vs H100
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_content_bg(slide)
add_slide_title(slide, "Comparaison A100 vs H100")

img_path = os.path.join(IMG_DIR, 'a100-h100-hpl.png')
if os.path.exists(img_path):
    slide.shapes.add_picture(img_path, Inches(0.3), Inches(1.25), Inches(5.2))

data_ratio = [
    ["N", "A100", "H100", "Ratio"],
    ["20K", "9 731", "16 130", "1,66x"],
    ["40K", "15 890", "35 760", "2,25x"],
    ["60K", "17 150", "41 760", "2,43x"],
    ["80K", "17 600", "44 130", "2,51x"],
    ["100K", "17 860", "45 110", "2,53x"],
]
add_table(slide, Inches(5.6), Inches(1.25), Inches(4.1), Inches(2.8), data_ratio)

# Ratio explanation box
box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                              Inches(5.6), Inches(4.3), Inches(4.1), Inches(2.5))
box.fill.solid()
box.fill.fore_color.rgb = RGBColor(0xF0, 0xEE, 0xEB)
box.line.color.rgb = ORANGE
box.line.width = Pt(1.5)

add_text(slide, Inches(5.8), Inches(4.45), Inches(3.7), Inches(2.2),
         "Ratio théorique :\n"
         "  54 / 19,5 = 2,77x\n\n"
         "Ratio mesuré (N=100K) :\n"
         "  2,53x\n\n"
         "Écart ~9% → dû à la différence\n"
         "d'efficacité (83% vs 92%)",
         14, False, DARK_TEAL)

# ============================================================
# SLIDE 8: Synthèse de l'efficacité
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_content_bg(slide)
add_slide_title(slide, "Synthèse de l'efficacité")

data_eff = [
    ["Configuration", "Peak (TFLOPS)", "Meilleur (GFLOPS)", "Efficacité"],
    ["A100 (1 GPU)", "19,5", "17 860", "91,7%"],
    ["H100 (1 GPU)", "54,0", "45 110", "83,4%"],
    ["A100 (2 GPUs)", "39,0", "34 720", "89,0%"],
    ["H100 (2 GPUs)", "108,0", "81 970", "75,8%"],
]
add_table(slide, Inches(0.4), Inches(1.25), Inches(9.2), Inches(2.5), data_eff)

add_sub_heading(slide, Inches(0.6), Inches(4.0), "Observations")
add_bullet_items(slide, Inches(0.6), Inches(4.55), Inches(8.5), [
    "L'efficacité diminue avec la puissance de la configuration",
    "HPL est compute-bound : le calcul (DGEMM) domine le temps d'exécution",
    "A100 : plus facile à saturer → meilleure efficacité",
    "H100 : performance brute supérieure mais utilisation plus difficile",
], 15, spacing=0.38)

# Bottom takeaway bar
bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, Inches(6.3), SLIDE_W, Inches(0.9))
bar.fill.solid()
bar.fill.fore_color.rgb = DARK_TEAL
bar.line.fill.background()
add_text(slide, Inches(0.6), Inches(6.4), Inches(8.8), Inches(0.7),
         "Plus un GPU est puissant, plus il est difficile d'exploiter 100% de sa capacité.",
         18, True, WHITE, PP_ALIGN.CENTER)

# ============================================================
# SLIDE 9: Conclusion
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_content_bg(slide)
add_slide_title(slide, "Conclusion")

points = [
    "HPL est compute-bound — efficacités de 83 à 92%",
    "La taille du problème est déterminante — O(N³) calcul vs O(N²) communication",
    "Le multi-GPU a un seuil de rentabilité — N entre 20K et 40K",
    "H100 offre un gain de ≈2,5x sur l'A100 — ratio mesuré 2,53x vs théorique 2,77x",
    "L'efficacité parallèle diminue avec la puissance — 97% A100 vs 91% H100",
]

for i, point in enumerate(points):
    y = Inches(1.4 + i * 1.05)
    add_orange_bullet(slide, Inches(0.6), y + Inches(0.06))
    add_text(slide, Inches(0.9), y, Inches(8.5), Inches(0.3),
             point, 18, True, NEAR_BLACK)

# Takeaway
add_text(slide, Inches(0.6), Inches(6.5), Inches(8.8), Inches(0.5),
         "Puissance brute, passage à l'échelle et dimensionnement du problème sont étroitement liés.",
         16, False, DARK_TEAL, PP_ALIGN.CENTER)

# Save
output_path = os.path.join(OUT_DIR, 'HPL_Resultats_Analyse.pptx')
prs.save(output_path)
print(f"Presentation saved to: {output_path}")
