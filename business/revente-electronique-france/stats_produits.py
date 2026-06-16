"""
Générateur du fichier d'analyse produits — opportunités d'achat/revente.
Basé sur données de marché Vinted, Le Bon Coin, Anibis (2025-2026).
"""
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.formatting.rule import ColorScaleRule, DataBarRule, CellIsRule, FormulaRule
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter
from openpyxl.chart import BarChart, Reference
from openpyxl.chart.label import DataLabelList

# ── Palette ───────────────────────────────────────────────────────────────────
C_DARK      = "1F3864"
C_BLUE      = "2E75B6"
C_GREEN     = "375623"
C_GREEN_BG  = "E2EFDA"
C_GREEN_HL  = "70AD47"
C_ORANGE    = "ED7D31"
C_ORANGE_BG = "FCE4D6"
C_RED       = "C00000"
C_RED_BG    = "FFE0E0"
C_YELLOW_BG = "FFF2CC"
C_ALT       = "DCE6F1"
C_WHITE     = "FFFFFF"
C_GREY      = "F2F2F2"
C_BORDER    = "B8CCE4"

EUR   = '#,##0.00 "€"'
PCT   = '0.0"%"'
NB    = '#,##0'
NB1   = '#,##0.0'

def side(c=C_BORDER): return Side(style="thin", color=c)
def brd(c=C_BORDER):  return Border(left=side(c), right=side(c), top=side(c), bottom=side(c))

def cell(ws, r, c, v=None, fmt=None, bold=False, bg=None, fg="000000",
         align="left", wrap=False, size=10, italic=False, border=True):
    cl = ws.cell(row=r, column=c, value=v)
    cl.font = Font(name="Calibri", bold=bold, color=fg, size=size, italic=italic)
    cl.alignment = Alignment(horizontal=align, vertical="center", wrap_text=wrap)
    if fmt:   cl.number_format = fmt
    if bg:    cl.fill = PatternFill("solid", fgColor=bg)
    if border: cl.border = brd()
    return cl

def hcell(ws, r, c, v, bg=C_DARK, fg=C_WHITE, size=10, align="center", wrap=True):
    cl = cell(ws, r, c, v, bold=True, bg=bg, fg=fg, align=align, size=size, wrap=wrap)
    return cl

def merge_hdr(ws, r, c1, c2, v, bg=C_DARK, fg=C_WHITE, size=12):
    cl = ws.cell(row=r, column=c1, value=v)
    cl.font = Font(name="Calibri", bold=True, color=fg, size=size)
    cl.fill = PatternFill("solid", fgColor=bg)
    cl.alignment = Alignment(horizontal="center", vertical="center")
    cl.border = brd()
    ws.merge_cells(start_row=r, start_column=c1, end_row=r, end_column=c2)
    ws.row_dimensions[r].height = 28

# ══════════════════════════════════════════════════════════════════════════════
# DONNÉES PRODUITS
# ══════════════════════════════════════════════════════════════════════════════
# Colonnes:
#   categorie, produit, plateforme_cible, demande_hebdo, prix_achat_1688,
#   frais_transport_unitaire, cout_douane_unitaire, cout_total_unitaire,
#   prix_revente_bas, prix_revente_moyen, prix_revente_haut,
#   frais_plateforme_pct, marge_nette_moy, rotation_semaine,
#   risque, legalite, commentaire
#
# Frais transport estimés: 3-6€/unité selon volume commande
# Droits douane France: ~3.7% sur valeur + TVA 20% sur valeur+transport
#   (applicable si envoi >150€ total, souvent <150€ pour petits lots)
# Droits douane Suisse (Anibis): TVA 8.1%
# ══════════════════════════════════════════════════════════════════════════════

PRODUCTS = [
    # cat                  produit                            plateformes        dem/sem  p_ach   fret  dou   p_rev_b  p_rev_m  p_rev_h  frais%  rot/sem  risque  note
    ("🎧 Audio",           "Écouteurs TWS sans fil",          "Vinted / LBC / Anibis",  45, 4.50,  2.50, 0.00,  18,     28,      45,     5,     12,   "Faible", "Top 1 Anibis 2025. Très léger, frais port mini. Pas de marque = légal."),
    ("🎧 Audio",           "Haut-parleur Bluetooth compact",  "LBC / Anibis",           30, 9.00,  3.00, 0.00,  28,     42,      60,     0,      8,   "Faible", "Forte demande fêtes + été. Saisonnier. Stock léger."),
    ("🏠 Petit électro",   "Air Fryer 4-5L (générique)",      "LBC / Anibis / Vinted",  35,28.50,  4.50, 0.00,  65,     85,     110,     0,      6,   "Moyen",  "Votre produit actuel. Ninja-like sans la marque. Légal si pas logo Ninja."),
    ("🏠 Petit électro",   "Machine à café capsules",         "LBC / Vinted",           22,18.00,  5.00, 2.00,  45,     65,      85,     0,      5,   "Moyen",  "Demande stable. Compatibles Nespresso génériques."),
    ("🏠 Petit électro",   "Robot aspirateur mini",           "LBC / Anibis",           18,32.00,  6.00, 3.00,  80,    110,     149,     0,      4,   "Moyen",  "Marché en hausse. Différencier par autonomie et silencieux."),
    ("⌚ Wearables",       "Montre connectée (smartwatch)",   "Vinted / LBC / Anibis",  40, 9.00,  2.00, 0.00,  30,     49,      75,     5,     10,   "Faible", "Très forte demande. Éviter de simuler Apple Watch."),
    ("⌚ Wearables",       "Bracelet fitness tracker",        "Vinted / Anibis",         28, 5.00,  2.00, 0.00,  18,     29,      45,     5,      7,   "Faible", "Marché stable. Axer sur sport/santé."),
    ("🔋 Accessoires",    "Batterie externe 20000mAh",        "LBC / Vinted / Anibis",  35, 6.50,  2.50, 0.00,  22,     32,      45,     5,      8,   "Faible", "Produit permanent. Différencier par charge rapide 65W."),
    ("🔋 Accessoires",    "Câbles et chargeurs USB-C lot",    "Vinted / LBC",           50, 1.50,  1.50, 0.00,   8,     14,      20,     5,     15,   "Faible", "Vendre en lot de 3. Marge énorme. Volume clé."),
    ("💡 Maison",          "Guirlandes LED USB/solaire",      "LBC / Vinted / Anibis",  40, 2.00,  1.50, 0.00,  12,     18,      28,     5,     12,   "Faible", "Pic déc + été. Commander 3 mois avant saison."),
    ("💡 Maison",          "Lampe de bureau LED tactile",     "LBC / Anibis",           25, 7.00,  3.00, 0.00,  22,     35,      50,     0,      6,   "Faible", "Tendance télétravail. Photos soignées = +30% prix."),
    ("🎮 Gaming",          "Console retro portable 10k jeux", "LBC / Anibis / Vinted",  28,15.00,  3.50, 0.00,  45,     65,      90,     0,      6,   "Faible", "Nostalgie Gen-X. Cadeau idéal Noël. Éviter logos Nintendo."),
    ("🎮 Gaming",          "Manette sans fil PC/Android",     "LBC / Vinted",           20, 8.00,  2.50, 0.00,  25,     38,      55,     5,      5,   "Faible", "Boom gaming mobile. Compatible PC+Android."),
    ("👶 Puériculture",    "Moniteur bébé vidéo",             "LBC / Anibis",           15,22.00,  5.00, 2.00,  55,     80,     110,     0,      4,   "Moyen",  "Forte valeur perçue. Parents exigeants = SAV important."),
    ("🧴 Beauté/Bien-être","Épilateur lumière pulsée IPL",    "Vinted / LBC",           20,18.00,  4.00, 0.00,  55,     79,     110,     5,      5,   "Moyen",  "Très forte marge. Produit phare Vinted femmes 25-45 ans."),
    ("🧴 Beauté/Bien-être","Brosse nettoyante visage sonic",  "Vinted / LBC / Anibis",  25, 6.00,  2.50, 0.00,  22,     35,      55,     5,      7,   "Faible", "Tendance skin care. Léger, facile à expédier."),
    ("🏋️ Sport",           "Corde à sauter connectée",        "LBC / Vinted",           18, 8.00,  2.50, 0.00,  25,     38,      55,     5,      5,   "Faible", "Pic janv (bonnes résolutions) + été. Saisonnier."),
    ("🏋️ Sport",           "Tapis de yoga + sangle lot",      "Vinted / LBC",           22, 5.00,  4.00, 0.00,  18,     28,      40,     5,      6,   "Faible", "Produit poids = frais port plus élevés. Vendre local."),
    ("📷 Photo/Vidéo",     "Mini caméra sport type GoPro",    "LBC / Anibis",           15,18.00,  4.00, 0.00,  45,     65,      95,     0,      4,   "Moyen",  "Prix 1688 vs GoPro : x5 moins cher. Bien photographier."),
    ("🧹 Maison",          "Balai vapeur électrique",         "LBC / Anibis",           12,22.00,  6.00, 2.00,  55,     79,     100,     0,      3,   "Moyen",  "Encombrant = retirer localement ou remise en main propre."),
]

# ══════════════════════════════════════════════════════════════════════════════
def compute_margins(p):
    """Calcule les métriques financières pour un produit."""
    (cat, nom, plat, dem, p_ach, fret, dou, p_rev_b, p_rev_m, p_rev_h,
     frais_pct, rot, risque, note) = (
        p[0], p[1], p[2], p[3], p[4], p[5], p[6],
        p[7], p[8], p[9], p[10], p[11], p[12], p[13]
    )
    cout_total = p_ach + fret + dou
    frais_vente_moy = p_rev_m * frais_pct / 100
    marge_brute_moy = p_rev_m - frais_vente_moy - cout_total
    marge_pct_moy   = marge_brute_moy / p_rev_m * 100 if p_rev_m else 0
    ca_semaine      = rot * p_rev_m
    marge_semaine   = rot * marge_brute_moy
    roi             = marge_brute_moy / cout_total * 100 if cout_total else 0
    return {
        "cat": cat, "nom": nom, "plat": plat, "dem": dem,
        "p_ach": p_ach, "fret": fret, "dou": dou,
        "cout": cout_total,
        "p_rev_b": p_rev_b, "p_rev_m": p_rev_m, "p_rev_h": p_rev_h,
        "frais_pct": frais_pct, "frais_vente": frais_vente_moy,
        "marge_eu": marge_brute_moy, "marge_pct": marge_pct_moy,
        "rot": rot, "ca_sem": ca_semaine, "marge_sem": marge_semaine,
        "roi": roi, "risque": risque, "note": note,
    }

DATA = sorted([compute_margins(p) for p in PRODUCTS],
              key=lambda x: x["marge_pct"], reverse=True)

RISQUE_COLOR = {"Faible": C_GREEN_BG, "Moyen": C_YELLOW_BG, "Élevé": C_RED_BG}

# ══════════════════════════════════════════════════════════════════════════════
# FEUILLE 1 — CLASSEMENT GLOBAL
# ══════════════════════════════════════════════════════════════════════════════
def make_ranking(wb):
    ws = wb.create_sheet("🏆 CLASSEMENT")
    ws.sheet_view.showGridLines = False

    # Titre
    merge_hdr(ws, 1, 1, 16,
              "🏆  TOP PRODUITS ACHAT/REVENTE — VINTED · LE BON COIN · ANIBIS  |  Juin 2026",
              bg=C_DARK, fg=C_WHITE, size=14)

    # Sous-titre
    ws.merge_cells("A2:P2")
    st = ws.cell(row=2, column=1,
                 value="Classé par marge nette % · Prix d'achat source : 1688.com · Frais de port estimés inclus")
    st.font = Font(name="Calibri", italic=True, color="666666", size=10)
    st.alignment = Alignment(horizontal="center")
    ws.row_dimensions[2].height = 18

    headers = [
        ("A",  "#",                     5,  "center"),
        ("B",  "Catégorie",            18,  "left"),
        ("C",  "Produit",              32,  "left"),
        ("D",  "Plateformes cibles",   22,  "left"),
        ("E",  "Demande\n/sem",        10,  "center"),
        ("F",  "Prix achat\n1688 (€)", 13,  "center"),
        ("G",  "Coût total\nunitaire", 13,  "center"),
        ("H",  "Prix revente\nmoyen",  13,  "center"),
        ("I",  "Frais plat.\n(%)",     10,  "center"),
        ("J",  "Marge\nnette (€)",     12,  "center"),
        ("K",  "Marge\nnette (%)",     12,  "center"),
        ("L",  "ROI\n(%)",             10,  "center"),
        ("M",  "Rot.\n/sem",           10,  "center"),
        ("N",  "CA est.\n/sem (€)",    14,  "center"),
        ("O",  "Marge est.\n/sem (€)", 14,  "center"),
        ("P",  "Risque",               10,  "center"),
    ]

    for col_letter, label, w, al in headers:
        col = ord(col_letter) - ord("A") + 1
        hcell(ws, 3, col, label)
        ws.column_dimensions[col_letter].width = w
    ws.row_dimensions[3].height = 30

    for r_offset, d in enumerate(DATA):
        r = r_offset + 4
        alt = C_ALT if r_offset % 2 == 0 else C_WHITE

        # Couleur marge
        if d["marge_pct"] >= 60:   marge_bg = C_GREEN_BG
        elif d["marge_pct"] >= 40: marge_bg = C_YELLOW_BG
        else:                       marge_bg = C_ORANGE_BG

        risque_bg = RISQUE_COLOR.get(d["risque"], C_WHITE)

        cell(ws, r,  1, r_offset + 1, align="center", bold=True, bg=alt, fg=C_DARK)
        cell(ws, r,  2, d["cat"],   bg=alt)
        cell(ws, r,  3, d["nom"],   bg=alt, bold=True)
        cell(ws, r,  4, d["plat"],  bg=alt, size=9)
        cell(ws, r,  5, d["dem"],   fmt=NB,  align="center", bg=alt)
        cell(ws, r,  6, d["p_ach"], fmt=EUR, align="center", bg=alt)
        cell(ws, r,  7, d["cout"],  fmt=EUR, align="center", bg=alt, bold=True)
        cell(ws, r,  8, d["p_rev_m"], fmt=EUR, align="center", bg=alt)
        cell(ws, r,  9, d["frais_pct"], fmt='0"%"', align="center", bg=alt)
        cell(ws, r, 10, d["marge_eu"],  fmt=EUR, align="center",
             bg=marge_bg, bold=True, fg=C_GREEN if d["marge_pct"] >= 40 else "000000")
        cell(ws, r, 11, d["marge_pct"], fmt=PCT, align="center",
             bg=marge_bg, bold=True, fg=C_GREEN if d["marge_pct"] >= 40 else "000000")
        cell(ws, r, 12, d["roi"], fmt=PCT, align="center", bg=alt)
        cell(ws, r, 13, d["rot"], fmt=NB, align="center", bg=alt)
        cell(ws, r, 14, d["ca_sem"],    fmt=EUR, align="center", bg=alt, bold=True)
        cell(ws, r, 15, d["marge_sem"], fmt=EUR, align="center",
             bg=marge_bg, bold=True, fg=C_GREEN)
        cell(ws, r, 16, d["risque"], align="center", bold=True,
             bg=risque_bg,
             fg=C_GREEN if d["risque"] == "Faible" else (C_ORANGE if d["risque"] == "Moyen" else C_RED))

    ws.freeze_panes = "A4"
    ws.auto_filter.ref = f"A3:P{len(DATA)+3}"

    # Note légale
    r_note = len(DATA) + 5
    ws.merge_cells(f"A{r_note}:P{r_note}")
    n = ws.cell(row=r_note, column=1,
                value="⚠️  LÉGAL : Ne jamais vendre des contrefaçons (copies de marques Nike, Apple, Louis Vuitton...). "
                      "Les produits listés ici sont des génériques sans marque protégée. "
                      "Déclaration fiscale obligatoire si revenus > 3000€/an ou > 20 transactions (plateformes déclarent au fisc).")
    n.font = Font(name="Calibri", italic=True, color=C_RED, size=9, bold=True)
    n.alignment = Alignment(wrap_text=True)
    n.fill = PatternFill("solid", fgColor="FFE0E0")
    n.border = brd(C_RED)
    ws.row_dimensions[r_note].height = 30


# ══════════════════════════════════════════════════════════════════════════════
# FEUILLE 2 — PAR PLATEFORME
# ══════════════════════════════════════════════════════════════════════════════
def make_by_platform(wb):
    ws = wb.create_sheet("🛒 PAR PLATEFORME")
    ws.sheet_view.showGridLines = False

    platforms = {
        "🟣 VINTED":       ("Vinted",  C_DARK,   "Mode, lifestyle, électro compact. Frais vendeur ~5%."),
        "🟠 LE BON COIN":  ("LBC",     C_ORANGE, "Électro, électroménager, mobilier. Gratuit pour particuliers."),
        "🔵 ANIBIS (CH)":  ("Anibis",  C_BLUE,   "Marché suisse. Prix ~20-30% plus élevés qu'en France. TVA CH 8.1%."),
    }

    current_row = 1
    col_start = 1

    headers_plat = [
        ("Produit", 30, "left"),
        ("Coût\nunitaire", 12, "center"),
        ("Prix\nrevente", 12, "center"),
        ("Marge €", 11, "center"),
        ("Marge %", 10, "center"),
        ("Rot/sem", 9, "center"),
        ("Marge\n/sem", 12, "center"),
    ]

    for plat_label, (plat_key, color, description) in platforms.items():
        # Titre plateforme
        merge_hdr(ws, current_row, col_start, col_start + len(headers_plat) - 1,
                  plat_label, bg=color)
        current_row += 1

        # Description
        ws.merge_cells(
            start_row=current_row, start_column=col_start,
            end_row=current_row, end_column=col_start + len(headers_plat) - 1
        )
        desc_cell = ws.cell(row=current_row, column=col_start, value=description)
        desc_cell.font = Font(name="Calibri", italic=True, color="444444", size=9)
        desc_cell.fill = PatternFill("solid", fgColor=C_GREY)
        desc_cell.alignment = Alignment(horizontal="left", vertical="center")
        ws.row_dimensions[current_row].height = 16
        current_row += 1

        # Headers
        for c_off, (h, w, al) in enumerate(headers_plat):
            col = col_start + c_off
            hcell(ws, current_row, col, h, bg=color)
            col_letter = get_column_letter(col)
            ws.column_dimensions[col_letter].width = w
        ws.row_dimensions[current_row].height = 28
        current_row += 1

        # Produits filtrés
        plat_data = [d for d in DATA if plat_key in d["plat"]]
        plat_data_sorted = sorted(plat_data, key=lambda x: x["marge_pct"], reverse=True)

        for r_off, d in enumerate(plat_data_sorted):
            r = current_row + r_off
            alt = C_ALT if r_off % 2 == 0 else C_WHITE
            marge_bg = C_GREEN_BG if d["marge_pct"] >= 60 else (C_YELLOW_BG if d["marge_pct"] >= 40 else C_ORANGE_BG)

            cell(ws, r, col_start,     d["nom"],        bold=True, bg=alt)
            cell(ws, r, col_start + 1, d["cout"],       fmt=EUR, align="center", bg=alt)
            cell(ws, r, col_start + 2, d["p_rev_m"],    fmt=EUR, align="center", bg=alt)
            cell(ws, r, col_start + 3, d["marge_eu"],   fmt=EUR, align="center", bg=marge_bg, bold=True)
            cell(ws, r, col_start + 4, d["marge_pct"],  fmt=PCT, align="center", bg=marge_bg, bold=True)
            cell(ws, r, col_start + 5, d["rot"],        fmt=NB,  align="center", bg=alt)
            cell(ws, r, col_start + 6, d["marge_sem"],  fmt=EUR, align="center", bg=marge_bg, bold=True)

        current_row += len(plat_data_sorted) + 2


# ══════════════════════════════════════════════════════════════════════════════
# FEUILLE 3 — SIMULATEUR DE MARGE
# ══════════════════════════════════════════════════════════════════════════════
def make_simulator(wb):
    ws = wb.create_sheet("🧮 SIMULATEUR")
    ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 3
    ws.column_dimensions["B"].width = 32
    ws.column_dimensions["C"].width = 20
    ws.column_dimensions["D"].width = 20
    ws.column_dimensions["E"].width = 3

    merge_hdr(ws, 1, 1, 4, "🧮  SIMULATEUR DE MARGE — PERSONNALISEZ VOS CALCULS", bg=C_DARK)

    ws.merge_cells("B2:D2")
    t = ws.cell(row=2, column=2,
                value="Modifiez les cellules en orange · Les résultats se calculent automatiquement")
    t.font = Font(name="Calibri", italic=True, color="666666", size=10)
    t.alignment = Alignment(horizontal="center")

    def section(r, label):
        ws.merge_cells(f"B{r}:D{r}")
        c = ws.cell(row=r, column=2, value=label)
        c.font = Font(name="Calibri", bold=True, color=C_WHITE, size=11)
        c.fill = PatternFill("solid", fgColor=C_BLUE)
        c.alignment = Alignment(horizontal="left", vertical="center", indent=1)
        c.border = brd()
        ws.row_dimensions[r].height = 22

    def input_row(ws, r, label, value, fmt=EUR, note=""):
        c_label = ws.cell(row=r, column=2, value=label)
        c_label.font = Font(name="Calibri", size=10)
        c_label.alignment = Alignment(vertical="center")
        c_label.border = brd()
        c_label.fill = PatternFill("solid", fgColor=C_GREY)

        c_val = ws.cell(row=r, column=3, value=value)
        c_val.font = Font(name="Calibri", bold=True, color=C_DARK, size=11)
        c_val.alignment = Alignment(horizontal="center", vertical="center")
        c_val.fill = PatternFill("solid", fgColor=C_YELLOW_BG)
        c_val.border = brd(C_ORANGE)
        c_val.number_format = fmt

        if note:
            c_note = ws.cell(row=r, column=4, value=note)
            c_note.font = Font(name="Calibri", italic=True, color="888888", size=9)
            c_note.alignment = Alignment(vertical="center")
            c_note.border = brd()
            c_note.fill = PatternFill("solid", fgColor=C_GREY)
        ws.row_dimensions[r].height = 20

    def result_row(ws, r, label, formula, fmt=EUR, highlight=False):
        c_label = ws.cell(row=r, column=2, value=label)
        c_label.font = Font(name="Calibri", bold=highlight, size=10)
        c_label.border = brd()
        c_label.fill = PatternFill("solid", fgColor=C_GREEN_BG if highlight else C_GREY)
        c_label.alignment = Alignment(vertical="center")

        c_val = ws.cell(row=r, column=3, value=formula)
        c_val.number_format = fmt
        c_val.font = Font(name="Calibri", bold=True, color=C_GREEN if highlight else C_DARK, size=12 if highlight else 11)
        c_val.alignment = Alignment(horizontal="center", vertical="center")
        c_val.border = brd()
        c_val.fill = PatternFill("solid", fgColor=C_GREEN_BG if highlight else C_WHITE)

        ws.merge_cells(f"C{r}:D{r}") if not highlight else None
        ws.row_dimensions[r].height = 22 if highlight else 20

    # ── Inputs
    section(3, "  📦  ACHAT (1688.com)")
    input_row(ws, 4,  "Prix achat unitaire (€)",           28.50, EUR, "Prix sur 1688 converti en €")
    input_row(ws, 5,  "Frais de transport total (€)",       45.00, EUR, "Pour toute la commande")
    input_row(ws, 6,  "Quantité commandée (unités)",         10,   "#,##0", "Nombre d'unités dans le lot")
    input_row(ws, 7,  "Droits de douane estimés (€ total)",  0,   EUR, "0€ si commande <150€")

    section(8, "  🛒  VENTE")
    input_row(ws, 9,  "Prix de vente moyen (€)",            85.00, EUR, "Prix affiché sur la plateforme")
    input_row(ws, 10, "Frais plateforme (%)",                5,   '0"%"', "Vinted=5%, LBC=0%, Anibis=0%")
    input_row(ws, 11, "Frais d'envoi payé par vous (€)",    6.00, EUR, "Si vous payez la livraison")
    input_row(ws, 12, "Unités vendues par semaine",          5,   "#,##0", "Estimation réaliste")

    section(13, "  📊  RÉSULTATS CALCULÉS")
    result_row(ws, 14, "Coût unitaire total (€)",
               "=C4+(C5+C7)/C6", EUR)
    result_row(ws, 15, "Frais plateforme unitaires (€)",
               "=C9*C10/100", EUR)
    result_row(ws, 16, "Prix net reçu après frais (€)",
               "=C9-C15-C11", EUR)
    result_row(ws, 17, "Marge nette par unité (€)",
               "=C16-C14", EUR, highlight=True)
    result_row(ws, 18, "Marge nette (%)",
               "=IF(C9=0,0,(C17/C9)*100)", PCT, highlight=True)
    result_row(ws, 19, "ROI — retour sur investissement (%)",
               "=IF(C14=0,0,(C17/C14)*100)", PCT)
    result_row(ws, 20, "CA hebdomadaire estimé (€)",
               "=C9*C12", EUR)
    result_row(ws, 21, "Marge hebdomadaire estimée (€)",
               "=C17*C12", EUR, highlight=True)
    result_row(ws, 22, "Marge mensuelle estimée (€)",
               "=C21*4", EUR, highlight=True)
    result_row(ws, 23, "Seuil de rentabilité (unités à vendre)",
               "=CEILING((C5+C7)/(C9-C4-C15-C11),1)", "#,##0")

    # Séparateur visuel colonne E = vide
    ws.column_dimensions["E"].width = 3

    # Note sur la TVA suisse
    ws.merge_cells("B25:D25")
    note_ch = ws.cell(row=25, column=2,
                      value="🇨🇭 Vente sur ANIBIS (Suisse) : appliquez +20-30% sur votre prix de vente moyen "
                            "vs France. La TVA suisse (8.1%) est à la charge de l'acheteur si vous êtes vendeur particulier français.")
    note_ch.font = Font(name="Calibri", italic=True, color=C_BLUE, size=9)
    note_ch.alignment = Alignment(wrap_text=True, vertical="center")
    note_ch.fill = PatternFill("solid", fgColor=C_ALT)
    note_ch.border = brd(C_BLUE)
    ws.row_dimensions[25].height = 32


# ══════════════════════════════════════════════════════════════════════════════
# FEUILLE 4 — TOP 5 RECOMMANDÉS
# ══════════════════════════════════════════════════════════════════════════════
def make_top5(wb):
    ws = wb.create_sheet("⭐ TOP 5 RECOMMANDÉS")
    ws.sheet_view.showGridLines = False

    merge_hdr(ws, 1, 1, 6,
              "⭐  TOP 5 PRODUITS RECOMMANDÉS POUR DÉMARRER",
              bg=C_DARK, size=14)

    ws.merge_cells("A2:F2")
    st = ws.cell(row=2, column=1,
                 value="Sélection basée sur : marge ≥ 60%, risque faible, demande forte, facile à expédier")
    st.font = Font(name="Calibri", italic=True, color="555555", size=10)
    st.alignment = Alignment(horizontal="center")
    ws.row_dimensions[2].height = 18

    top5 = [d for d in DATA if d["risque"] == "Faible" and d["marge_pct"] >= 55][:5]

    col_widths = [5, 32, 22, 16, 16, 50]
    for i, w in enumerate(col_widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w

    for rank, d in enumerate(top5):
        base_row = 3 + rank * 9

        # Header produit
        medal = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"][rank]
        ws.merge_cells(f"A{base_row}:F{base_row}")
        h = ws.cell(row=base_row, column=1,
                    value=f"{medal}  {d['nom']}  —  {d['cat']}")
        h.font = Font(name="Calibri", bold=True, color=C_WHITE, size=12)
        h.fill = PatternFill("solid", fgColor=[C_DARK, C_BLUE, C_GREEN_HL, C_ORANGE, "8E44AD"][rank])
        h.alignment = Alignment(horizontal="left", vertical="center", indent=1)
        h.border = brd()
        ws.row_dimensions[base_row].height = 26

        # KPIs en grille 2x3
        kpi_data = [
            ("Prix achat 1688",  f"{d['p_ach']:.2f} €",  "Coût total unitaire",  f"{d['cout']:.2f} €"),
            ("Prix revente moy", f"{d['p_rev_m']:.0f} €", "Marge nette / unité",  f"{d['marge_eu']:.2f} €"),
            ("Marge nette %",    f"{d['marge_pct']:.1f}%", "Rotation estimée/sem", f"{d['rot']} unités"),
            ("Marge / semaine",  f"{d['marge_sem']:.0f} €", "Plateformes cibles",   d["plat"]),
        ]

        for ki, (l1, v1, l2, v2) in enumerate(kpi_data):
            r = base_row + 1 + ki
            alt_bg = C_ALT if ki % 2 == 0 else C_WHITE

            # Col 1: label
            lc = ws.cell(row=r, column=2, value=l1)
            lc.font = Font(name="Calibri", bold=True, color="555555", size=9)
            lc.fill = PatternFill("solid", fgColor=C_GREY)
            lc.border = brd(); lc.alignment = Alignment(vertical="center")
            ws.row_dimensions[r].height = 18

            # Col 2: valeur
            vc = ws.cell(row=r, column=3, value=v1)
            vc.font = Font(name="Calibri", bold=True, color=C_DARK, size=11)
            vc.fill = PatternFill("solid", fgColor=alt_bg)
            vc.border = brd(); vc.alignment = Alignment(horizontal="center", vertical="center")

            # Col 3: label2
            lc2 = ws.cell(row=r, column=4, value=l2)
            lc2.font = Font(name="Calibri", bold=True, color="555555", size=9)
            lc2.fill = PatternFill("solid", fgColor=C_GREY)
            lc2.border = brd(); lc2.alignment = Alignment(vertical="center")

            # Col 4: valeur2
            vc2 = ws.cell(row=r, column=5, value=v2)
            vc2.font = Font(name="Calibri", bold=True,
                            color=C_GREEN if "€" in v2 and float(v2.replace("€","").replace(" ","").replace(",","")) > 20
                                  else C_DARK, size=11)
            vc2.fill = PatternFill("solid", fgColor=C_GREEN_BG if "Marge" in l2 else alt_bg)
            vc2.border = brd(); vc2.alignment = Alignment(horizontal="center", vertical="center")

        # Conseil
        r_conseil = base_row + 5
        ws.merge_cells(f"B{r_conseil}:F{r_conseil}")
        conseil = ws.cell(row=r_conseil, column=2, value=f"💡  {d['note']}")
        conseil.font = Font(name="Calibri", italic=True, color=C_DARK, size=9)
        conseil.fill = PatternFill("solid", fgColor=C_YELLOW_BG)
        conseil.border = brd(C_ORANGE)
        conseil.alignment = Alignment(vertical="center", wrap_text=True)
        ws.row_dimensions[r_conseil].height = 28

        # Séparateur
        ws.row_dimensions[base_row + 6].height = 6


# ══════════════════════════════════════════════════════════════════════════════
# FEUILLE 5 — CALENDRIER SAISONNIER
# ══════════════════════════════════════════════════════════════════════════════
def make_calendar(wb):
    ws = wb.create_sheet("📅 SAISONNIER")
    ws.sheet_view.showGridLines = False

    merge_hdr(ws, 1, 1, 13, "📅  CALENDRIER SAISONNIER — QUAND COMMANDER ET VENDRE", bg=C_DARK)

    mois = ["Jan", "Fév", "Mar", "Avr", "Mai", "Jun",
            "Jul", "Aoû", "Sep", "Oct", "Nov", "Déc"]
    hcell(ws, 2, 1, "Produit", bg=C_BLUE)
    for i, m in enumerate(mois):
        hcell(ws, 2, i + 2, m, bg=C_BLUE)
    ws.column_dimensions["A"].width = 32
    for i in range(2, 14):
        ws.column_dimensions[get_column_letter(i)].width = 6

    # Matrice saisonnalité: 0=creux, 1=normal, 2=fort, 3=peak
    SAISONNAL = {
        "Écouteurs TWS sans fil":          [1,1,1,1,1,1,1,1,1,1,3,3],
        "Haut-parleur Bluetooth compact":  [1,1,1,1,2,3,3,2,1,1,2,3],
        "Air Fryer 4-5L":                  [1,1,1,1,1,1,1,1,1,2,3,3],
        "Montre connectée":                [3,1,1,1,1,1,1,1,2,2,3,3],
        "Batterie externe 20000mAh":       [1,1,1,1,2,2,2,2,1,1,2,2],
        "Guirlandes LED USB/solaire":      [0,0,1,1,2,2,2,2,1,2,3,3],
        "Console retro portable":          [1,1,1,1,1,1,1,1,1,2,3,3],
        "Corde à sauter connectée":        [3,3,1,1,1,2,2,1,2,1,1,1],
        "Épilateur lumière pulsée IPL":    [1,1,2,3,3,3,1,1,1,1,2,2],
        "Câbles et chargeurs USB-C lot":   [1,1,1,1,1,1,1,1,1,1,3,3],
    }

    COLORS = {0: "BFBFBF", 1: "D9E1F2", 2: "70AD47", 3: "C00000"}
    LABELS = {0: "—", 1: "●", 2: "▲▲", 3: "🔥"}

    for r_off, (prod, sais) in enumerate(SAISONNAL.items()):
        r = r_off + 3
        alt = C_ALT if r_off % 2 == 0 else C_WHITE
        c = ws.cell(row=r, column=1, value=prod)
        c.font = Font(name="Calibri", size=9, bold=True)
        c.fill = PatternFill("solid", fgColor=alt)
        c.border = brd(); c.alignment = Alignment(vertical="center")
        ws.row_dimensions[r].height = 18

        for m_off, niveau in enumerate(sais):
            mc = ws.cell(row=r, column=m_off + 2, value=LABELS[niveau])
            mc.fill = PatternFill("solid", fgColor=COLORS[niveau])
            mc.font = Font(name="Calibri", size=9, color=C_WHITE if niveau == 3 else C_DARK, bold=niveau >= 2)
            mc.alignment = Alignment(horizontal="center", vertical="center")
            mc.border = brd()

    # Légende
    r_leg = len(SAISONNAL) + 4
    ws.merge_cells(f"A{r_leg}:M{r_leg}")
    leg = ws.cell(row=r_leg, column=1,
                  value="Légende : — = saison creuse (commander peu) | ● = demande normale | ▲▲ = forte demande | 🔥 = pic / commander 4-6 sem à l'avance")
    leg.font = Font(name="Calibri", italic=True, size=9, color="444444")
    leg.fill = PatternFill("solid", fgColor=C_GREY)
    leg.border = brd()
    leg.alignment = Alignment(vertical="center")
    ws.row_dimensions[r_leg].height = 20

    r_tip = r_leg + 1
    ws.merge_cells(f"A{r_tip}:M{r_tip}")
    tip = ws.cell(row=r_tip, column=1,
                  value="⏰  DÉLAI 1688 → réception : comptez 15-25 jours ouvrés. Commandez TOUJOURS 4 semaines avant un pic. Exemple : commander pour Noël avant début novembre.")
    tip.font = Font(name="Calibri", italic=True, size=9, color=C_DARK, bold=True)
    tip.fill = PatternFill("solid", fgColor=C_YELLOW_BG)
    tip.border = brd(C_ORANGE)
    tip.alignment = Alignment(vertical="center", wrap_text=True)
    ws.row_dimensions[r_tip].height = 26


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════
def main():
    wb = openpyxl.Workbook()
    wb.remove(wb.active)

    make_top5(wb)
    make_ranking(wb)
    make_by_platform(wb)
    make_simulator(wb)
    make_calendar(wb)

    wb.active = wb["⭐ TOP 5 RECOMMANDÉS"]

    out = "/home/user/Stats_Produits_Revente_2026.xlsx"
    wb.save(out)
    print(f"✅  Fichier créé : {out}")

if __name__ == "__main__":
    main()
