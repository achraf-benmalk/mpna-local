#!/usr/bin/env python3
"""Generate the HPL presentation slides (Part 2: Execution, Results, Analysis)."""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import os

IMG_DIR = os.path.join(os.path.dirname(__file__), '..', 'latex report', 'images')
OUT_DIR = os.path.join(os.path.dirname(__file__), 'presentation_finale')
os.makedirs(OUT_DIR, exist_ok=True)

# Colors
DARK_BLUE = RGBColor(0x1B, 0x3A, 0x5C)
ACCENT_BLUE = RGBColor(0x2E, 0x86, 0xC1)
ACCENT_GREEN = RGBColor(0x27, 0xAE, 0x60)
ACCENT_RED = RGBColor(0xE7, 0x4C, 0x3C)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT_GRAY = RGBColor(0xF2, 0xF3, 0xF4)
DARK_GRAY = RGBColor(0x2C, 0x3E, 0x50)
BLACK = RGBColor(0x00, 0x00, 0x00)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

def add_bg(slide, color=WHITE):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_title_bar(slide, text, subtitle=None):
    """Add a colored top bar with title."""
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(1.3))
    shape.fill.solid()
    shape.fill.fore_color.rgb = DARK_BLUE
    shape.line.fill.background()
    tf = shape.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.alignment = PP_ALIGN.LEFT
    tf.margin_left = Inches(0.8)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    if subtitle:
        p2 = tf.add_paragraph()
        p2.text = subtitle
        p2.font.size = Pt(18)
        p2.font.color.rgb = RGBColor(0xAE, 0xD6, 0xF1)
        p2.alignment = PP_ALIGN.LEFT

def add_text_box(slide, left, top, width, height, text, font_size=18, bold=False, color=DARK_GRAY, alignment=PP_ALIGN.LEFT):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.bold = bold
    p.font.color.rgb = color
    p.alignment = alignment
    return tf

def add_bullet_list(slide, left, top, width, height, items, font_size=18, color=DARK_GRAY):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.text = item
        p.font.size = Pt(font_size)
        p.font.color.rgb = color
        p.space_after = Pt(8)
        p.level = 0
    return tf

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
                paragraph.font.size = Pt(14)
                paragraph.alignment = PP_ALIGN.CENTER
                if r == 0:
                    paragraph.font.bold = True
                    paragraph.font.color.rgb = WHITE
            if r == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = DARK_BLUE
            elif r % 2 == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = LIGHT_GRAY
    return table

# ============================================================
# SLIDE 1: Title
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank
add_bg(slide, DARK_BLUE)
add_text_box(slide, Inches(1), Inches(1.5), Inches(11), Inches(1.5),
             "HPL Benchmark : Implémentation GPU", 44, True, WHITE, PP_ALIGN.CENTER)
add_text_box(slide, Inches(1), Inches(3.2), Inches(11), Inches(1),
             "Résultats et Analyse Comparative A100 vs H100", 28, False, RGBColor(0xAE, 0xD6, 0xF1), PP_ALIGN.CENTER)
add_text_box(slide, Inches(1), Inches(5), Inches(11), Inches(0.5),
             "Partie 2 : Exécution, Résultats, Analyse", 20, False, RGBColor(0xD5, 0xDB, 0xDB), PP_ALIGN.CENTER)
add_text_box(slide, Inches(1), Inches(6), Inches(11), Inches(0.5),
             "BENMALK Achraf  |  Projet MPNA  |  2026", 18, False, RGBColor(0x85, 0x92, 0x9E), PP_ALIGN.CENTER)

# ============================================================
# SLIDE 2: Plateforme d'exécution
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "Plateforme d'exécution")

add_text_box(slide, Inches(0.8), Inches(1.6), Inches(5.5), Inches(0.5),
             "Environnement", 22, True, DARK_BLUE)
add_bullet_list(slide, Inches(0.8), Inches(2.2), Inches(5.5), Inches(2.5), [
    "Cluster HPC avec nœuds GPU NVIDIA",
    "Conteneur : NVIDIA HPC-Benchmarks 23.10 (Singularity)",
    "Bibliothèques : cuBLAS + NCCL",
    "Ordonnanceur : Slurm",
    "HPL utilise les Tensor Cores FP64 pour DGEMM",
], 17)

add_text_box(slide, Inches(7), Inches(1.6), Inches(5.5), Inches(0.5),
             "GPUs testés", 22, True, DARK_BLUE)

data = [
    ["", "A100 (Ampere)", "H100 (Hopper)"],
    ["Partition", "gpu", "gpu_h100"],
    ["Variante", "SXM / 80 Go HBM2e", "PCIe / 80 Go HBM3"],
    ["Cœurs FP64", "3 456", "7 296"],
    ["Tensor Cores", "3e gén.", "4e gén."],
    ["Peak FP64 TC", "19,5 TFLOPS", "51 TFLOPS"],
]
add_table(slide, Inches(7), Inches(2.2), Inches(5.5), Inches(3), data)

add_text_box(slide, Inches(0.8), Inches(5.2), Inches(11), Inches(0.5),
             "Configuration HPL", 22, True, DARK_BLUE)
add_bullet_list(slide, Inches(0.8), Inches(5.8), Inches(11), Inches(1.5), [
    "NB = 576 (blocs larges pour saturer les cœurs GPU — vs NB = 128-256 sur CPU)",
    "P × Q = 2 × 1  (1 processus MPI par GPU)   |   BCAST = 6 (broadcast MPI)",
], 17)

# ============================================================
# SLIDE 3: Étapes d'exécution
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "Étapes d'exécution sur GPU")

steps = [
    ("1. HPL.dat", "Création du fichier de\nconfiguration (N, NB, P×Q)", "Step1.png"),
    ("2. Singularity", "Lancement du conteneur\navec bind du répertoire", "Step2.png"),
    ("3. Slurm", "Allocation GPU via salloc\n(--gres=gpu:1 ou gpu:2)", "Step3.png"),
    ("4. Exécution", "mpirun -np <X> ./hpl.sh\n--dat /mnt/HPL.dat", "Step4.png"),
]

for i, (title, desc, img) in enumerate(steps):
    x = Inches(0.5 + i * 3.2)
    # Step box
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.6), Inches(2.8), Inches(5.2))
    shape.fill.solid()
    shape.fill.fore_color.rgb = LIGHT_GRAY
    shape.line.color.rgb = ACCENT_BLUE
    shape.line.width = Pt(1.5)

    add_text_box(slide, x + Inches(0.1), Inches(1.7), Inches(2.6), Inches(0.5),
                 title, 20, True, DARK_BLUE, PP_ALIGN.CENTER)
    add_text_box(slide, x + Inches(0.1), Inches(2.3), Inches(2.6), Inches(1),
                 desc, 14, False, DARK_GRAY, PP_ALIGN.CENTER)

    img_path = os.path.join(IMG_DIR, img)
    if os.path.exists(img_path):
        slide.shapes.add_picture(img_path, x + Inches(0.15), Inches(3.4), Inches(2.5))

# ============================================================
# SLIDE 4: Résultats A100
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "Résultats : GPU A100 (Ampere)")

data_a100 = [
    ["N", "1 GPU (GFLOPS)", "2 GPUs (GFLOPS)", "Speedup"],
    ["20 000", "9 731", "9 106", "0,94x"],
    ["40 000", "15 890", "25 230", "1,59x"],
    ["60 000", "17 150", "31 430", "1,83x"],
    ["80 000", "17 600", "33 560", "1,91x"],
    ["100 000", "17 860", "34 720", "1,94x"],
]
add_table(slide, Inches(0.5), Inches(1.6), Inches(6), Inches(3.5), data_a100)

img_path = os.path.join(IMG_DIR, 'hpl-a100.png')
if os.path.exists(img_path):
    slide.shapes.add_picture(img_path, Inches(6.8), Inches(1.6), Inches(6))

# Key metrics box
shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(5.5), Inches(12), Inches(1.5))
shape.fill.solid()
shape.fill.fore_color.rgb = RGBColor(0xEB, 0xF5, 0xFB)
shape.line.color.rgb = ACCENT_BLUE
tf = add_text_box(slide, Inches(0.8), Inches(5.6), Inches(11.5), Inches(1.3),
    "", 16)
p = tf.paragraphs[0]
p.text = "Peak théorique : 19,5 TFLOPS (FP64 Tensor Core)  |  Meilleur résultat : 17 860 GFLOPS  |  Efficacité : 91,6%"
p.font.size = Pt(17)
p.font.bold = True
p.font.color.rgb = DARK_BLUE
p2 = tf.add_paragraph()
p2.text = "Speedup 2 GPUs : 1,94x (efficacité parallèle 97%)  |  Tous les tests : PASSED"
p2.font.size = Pt(16)
p2.font.color.rgb = ACCENT_GREEN

# ============================================================
# SLIDE 5: Résultats H100
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "Résultats : GPU H100 (Hopper)")

data_h100 = [
    ["N", "1 GPU (GFLOPS)", "2 GPUs (GFLOPS)", "Speedup"],
    ["20 000", "16 130", "11 510", "0,71x"],
    ["40 000", "35 760", "41 460", "1,16x"],
    ["60 000", "41 760", "64 700", "1,55x"],
    ["80 000", "44 130", "76 730", "1,74x"],
    ["100 000", "45 110", "81 970", "1,82x"],
]
add_table(slide, Inches(0.5), Inches(1.6), Inches(6), Inches(3.5), data_h100)

img_path = os.path.join(IMG_DIR, 'hpl-h100.png')
if os.path.exists(img_path):
    slide.shapes.add_picture(img_path, Inches(6.8), Inches(1.6), Inches(6))

shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(5.5), Inches(12), Inches(1.5))
shape.fill.solid()
shape.fill.fore_color.rgb = RGBColor(0xFD, 0xED, 0xEC)
shape.line.color.rgb = ACCENT_RED
tf = add_text_box(slide, Inches(0.8), Inches(5.6), Inches(11.5), Inches(1.3),
    "", 16)
p = tf.paragraphs[0]
p.text = "Peak théorique : 51 TFLOPS (FP64 Tensor Core PCIe)  |  Meilleur résultat : 45 110 GFLOPS  |  Efficacité : 88,5%"
p.font.size = Pt(17)
p.font.bold = True
p.font.color.rgb = DARK_BLUE
p2 = tf.add_paragraph()
p2.text = "Speedup 2 GPUs : 1,82x (efficacité parallèle 91%)  |  Anomalie N=20K : 2 GPUs 28,6% plus lents que 1 !"
p2.font.size = Pt(16)
p2.font.color.rgb = ACCENT_RED

# ============================================================
# SLIDE 6: Anomalie multi-GPU à N=20K
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "Anomalie : 2 GPUs plus lents qu'un seul (N = 20 000)")

data_anomaly = [
    ["GPU", "1 GPU (GFLOPS)", "2 GPUs (GFLOPS)", "Dégradation"],
    ["A100", "9 731", "9 106", "-6,4%"],
    ["H100", "16 130", "11 510", "-28,6%"],
]
add_table(slide, Inches(0.5), Inches(1.8), Inches(5.5), Inches(1.5), data_anomaly)

add_text_box(slide, Inches(0.5), Inches(3.6), Inches(5.5), Inches(0.5),
             "Pourquoi ?", 22, True, ACCENT_RED)
add_bullet_list(slide, Inches(0.5), Inches(4.2), Inches(5.8), Inches(3), [
    "N = 20 000 est trop petit pour 2 GPUs",
    "Chaque GPU reçoit une portion de matrice insuffisante",
    "Le coût de communication inter-GPU > le gain de calcul",
    "Plus prononcé sur H100 (-28,6%) : plus de cœurs à alimenter",
    "Seuil de rentabilité : entre N = 20K et N = 40K",
], 17)

# Right side: visual explanation
shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.8), Inches(5.8), Inches(5))
shape.fill.solid()
shape.fill.fore_color.rgb = LIGHT_GRAY
shape.line.color.rgb = DARK_BLUE

add_text_box(slide, Inches(7), Inches(2), Inches(5.4), Inches(0.5),
             "Analogie", 20, True, DARK_BLUE, PP_ALIGN.CENTER)
add_text_box(slide, Inches(7.2), Inches(2.6), Inches(5), Inches(4),
             "Petit problème (N=20K) :\n"
             "  2 cuisiniers pour 1 petit plat\n"
             "  = plus de temps à se coordonner\n"
             "    qu'à cuisiner\n\n"
             "Grand problème (N=100K) :\n"
             "  2 cuisiniers pour un banquet\n"
             "  = chacun est occupé à cuisiner,\n"
             "    la coordination est négligeable\n\n"
             "Calcul : O(N³)    Communication : O(N²)\n"
             "Grand N → calcul domine → meilleure efficacité",
             15, False, DARK_GRAY)

# ============================================================
# SLIDE 7: Comparaison A100 vs H100
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "Comparaison architecturale : A100 vs H100")

img_path = os.path.join(IMG_DIR, 'a100-h100-hpl.png')
if os.path.exists(img_path):
    slide.shapes.add_picture(img_path, Inches(0.3), Inches(1.5), Inches(6.5))

data_ratio = [
    ["N", "A100", "H100", "Ratio"],
    ["20K", "9 731", "16 130", "1,66x"],
    ["40K", "15 890", "35 760", "2,25x"],
    ["60K", "17 150", "41 760", "2,43x"],
    ["80K", "17 600", "44 130", "2,51x"],
    ["100K", "17 860", "45 110", "2,53x"],
]
add_table(slide, Inches(7), Inches(1.5), Inches(5.8), Inches(3.2), data_ratio)

shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7), Inches(5), Inches(5.8), Inches(2))
shape.fill.solid()
shape.fill.fore_color.rgb = RGBColor(0xEB, 0xF5, 0xFB)
shape.line.color.rgb = ACCENT_BLUE

add_text_box(slide, Inches(7.2), Inches(5.1), Inches(5.4), Inches(1.8),
             "Ratio théorique : Peak H100 / Peak A100\n"
             "= 51 / 19,5 = 2,62x\n\n"
             "Ratio mesuré (N=100K) : 2,53x\n"
             "Écart : seulement 3% → HPL exploite bien les 2 architectures",
             16, False, DARK_BLUE)

# ============================================================
# SLIDE 8: Synthèse de l'efficacité
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "Synthèse de l'efficacité")

data_eff = [
    ["Configuration", "Peak TC (TFLOPS)", "Meilleur (GFLOPS)", "Efficacité"],
    ["A100 (1 GPU)", "19,5", "17 860", "91,6%"],
    ["H100 (1 GPU)", "51,0", "45 110", "88,5%"],
    ["A100 (2 GPUs)", "39,0", "34 720", "89,0%"],
    ["H100 (2 GPUs)", "102,0", "81 970", "80,4%"],
]
add_table(slide, Inches(0.5), Inches(1.6), Inches(7), Inches(3), data_eff)

add_text_box(slide, Inches(8), Inches(1.6), Inches(4.8), Inches(0.5),
             "Observations clés", 22, True, DARK_BLUE)
add_bullet_list(slide, Inches(8), Inches(2.3), Inches(4.8), Inches(4.5), [
    "Toutes les configs > 80% d'efficacité",
    "HPL est compute-bound : le calcul domine",
    "L'efficacité diminue avec la puissance",
    "A100 : meilleure efficacité (plus facile à saturer)",
    "H100 : performance brute supérieure",
    "Compromis puissance vs. efficacité",
], 17)

# Bottom key takeaway
shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(5.2), Inches(12), Inches(1.8))
shape.fill.solid()
shape.fill.fore_color.rgb = DARK_BLUE
shape.line.fill.background()
add_text_box(slide, Inches(0.8), Inches(5.3), Inches(11.5), Inches(1.5),
             "Conclusion : Plus un GPU est puissant, plus il est difficile d'exploiter 100% de sa capacité.\n"
             "La taille du problème (N) et les paramètres de tuning (NB, P×Q) sont déterminants.",
             20, True, WHITE, PP_ALIGN.CENTER)

# ============================================================
# SLIDE 9: Conclusion
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_title_bar(slide, "Conclusion et enseignements")

points = [
    ("HPL est compute-bound", "Efficacités de 88-92% confirment que le calcul (DGEMM) domine", ACCENT_GREEN),
    ("La taille du problème est clé", "GFLOPS augmente avec N  (O(N³) calcul vs O(N²) communication)", ACCENT_BLUE),
    ("Le multi-GPU a un seuil", "En dessous de N ≈ 20-40K, 2 GPUs sont contre-productifs", ACCENT_RED),
    ("H100 ≈ 2,5x l'A100", "Ratio mesuré (2,53x) cohérent avec le ratio théorique (2,62x)", ACCENT_BLUE),
    ("Efficacité vs puissance", "A100 : 97% eff. parallèle / H100 : 91% — communication plus coûteuse sur GPU rapide", ACCENT_RED),
]

for i, (title, desc, color) in enumerate(points):
    y = Inches(1.6 + i * 1.1)
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), y, Inches(12), Inches(0.95))
    shape.fill.solid()
    shape.fill.fore_color.rgb = LIGHT_GRAY
    shape.line.color.rgb = color
    shape.line.width = Pt(2)

    # Number circle
    num_shape = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(0.7), y + Inches(0.15), Inches(0.65), Inches(0.65))
    num_shape.fill.solid()
    num_shape.fill.fore_color.rgb = color
    num_shape.line.fill.background()
    tf = num_shape.text_frame
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.text = str(i + 1)
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.alignment = PP_ALIGN.CENTER

    add_text_box(slide, Inches(1.6), y + Inches(0.05), Inches(10.5), Inches(0.45),
                 title, 19, True, DARK_BLUE)
    add_text_box(slide, Inches(1.6), y + Inches(0.5), Inches(10.5), Inches(0.4),
                 desc, 15, False, DARK_GRAY)

# Save
output_path = os.path.join(OUT_DIR, 'HPL_Resultats_Analyse.pptx')
prs.save(output_path)
print(f"Presentation saved to: {output_path}")
