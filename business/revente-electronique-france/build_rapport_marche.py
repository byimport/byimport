"""
Rapport d'analyse concurrentielle basé sur données de marché réelles.
Sources: LeBonCoin, Anibis, Vinted — Juin 2026
"""
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.formatting.rule import ColorScaleRule, DataBarRule
from datetime import datetime

# ── Styles ─────────────────────────────────────────────────────────────────
C_DARK  = "1F3864"; C_BLUE = "2E75B6"; C_TEAL = "1F7391"
C_GREEN = "375623"; C_GHL  = "70AD47"; C_GBG  = "E2EFDA"
C_ORG   = "C55A11"; C_OBG  = "FCE4D6"
C_RED   = "C00000"; C_RBG  = "FFE0E0"
C_YEL   = "7F6000"; C_YBG  = "FFF2CC"
C_ALT   = "DCE6F1"; C_GRY  = "F2F2F2"; C_WHT  = "FFFFFF"
C_BDR   = "B8CCE4"; C_CHF  = "2D6A9F"

EUR = '#,##0.00 "€"'
CHF = '#,##0.00 " CHF"'
PCT = '0.0"%"'
NB  = '#,##0'

def brd(c=C_BDR):
    s = Side(style="thin", color=c)
    return Border(left=s, right=s, top=s, bottom=s)

def C(ws, r, col, v=None, fmt=None, bold=False, bg=None, fg="000000",
      al="left", wrap=False, sz=10):
    cl = ws.cell(row=r, column=col, value=v)
    cl.font = Font(name="Calibri", bold=bold, color=fg, size=sz)
    cl.alignment = Alignment(horizontal=al, vertical="center", wrap_text=wrap)
    cl.border = brd()
    if fmt: cl.number_format = fmt
    if bg:  cl.fill = PatternFill("solid", fgColor=bg)
    return cl

def H(ws, r, col, v, bg=C_DARK, fg=C_WHT, sz=10, wrap=True):
    return C(ws, r, col, v, bold=True, bg=bg, fg=fg, al="center", sz=sz, wrap=wrap)

def MH(ws, r, c1, c2, v, bg=C_DARK, fg=C_WHT, sz=13, h=28):
    cl = ws.cell(row=r, column=c1, value=v)
    cl.font = Font(name="Calibri", bold=True, color=fg, size=sz)
    cl.fill = PatternFill("solid", fgColor=bg)
    cl.alignment = Alignment(horizontal="center", vertical="center")
    cl.border = brd()
    ws.merge_cells(start_row=r, start_column=c1, end_row=r, end_column=c2)
    ws.row_dimensions[r].height = h

def marge_style(m):
    if m >= 55: return C_GBG, C_GREEN
    if m >= 35: return C_YBG, C_YEL
    if m >= 20: return C_OBG, C_ORG
    return C_RBG, C_RED

# ══════════════════════════════════════════════════════════════════════════════
# DONNÉES DE MARCHÉ — collectées juin 2026
# Colonnes: produit, cout_1688, frais_port_unitaire,
#   lbc_min, lbc_med, lbc_max, lbc_nb_ann,
#   vinted_min, vinted_med, vinted_max,
#   anibis_min_chf, anibis_med_chf, anibis_max_chf,
#   frais_lbc%, frais_vinted%, frais_anibis%,
#   segment, notes_strategie
# ══════════════════════════════════════════════════════════════════════════════
MARKET_DATA = [
    {
        "cat":     "🎧 Audio",
        "produit": "Écouteurs TWS sans fil (générique)",
        "cout_1688":        4.50,
        "frais_port":       2.50,
        # LeBonCoin
        "lbc_min": 8,   "lbc_med": 18,  "lbc_max": 45,  "lbc_nb": 120,
        # Vinted
        "vt_min":  5,   "vt_med":  22,  "vt_max":  55,
        # Anibis CHF (×1.08 pour €)
        "an_min":  12,  "an_med":  28,  "an_max":  60,
        "frais_lbc": 0, "frais_vt": 5,  "frais_an": 0,
        "rot_sem": 14,
        "strat": "Lot de 2 = prix perçu élevé. Photo fond blanc. Axer sur sport/gaming.",
    },
    {
        "cat":     "🎧 Audio",
        "produit": "Haut-parleur Bluetooth compact",
        "cout_1688":        9.00,
        "frais_port":       3.50,
        "lbc_min": 12, "lbc_med": 32,  "lbc_max": 90,  "lbc_nb": 80,
        "vt_min":  10,  "vt_med": 28,  "vt_max":  70,
        "an_min":  18,  "an_med": 42,  "an_max":  95,
        "frais_lbc": 0, "frais_vt": 5, "frais_an": 0,
        "rot_sem": 8,
        "strat": "Pic d'été et Noël. Mettre en valeur l'autonomie (heures). Vendre sur Anibis = +30% vs LBC.",
    },
    {
        "cat":     "🏠 Électroménager",
        "produit": "Air Fryer 4-5L (générique, sans marque)",
        "cout_1688":        28.50,
        "frais_port":       4.50,
        "lbc_min": 25, "lbc_med": 55,  "lbc_max": 130, "lbc_nb": 300,
        "vt_min":  20,  "vt_med": 42,  "vt_max":  90,
        "an_min":  40,  "an_med": 70,  "an_max":  150,
        "frais_lbc": 0, "frais_vt": 5, "frais_an": 0,
        "rot_sem": 6,
        "strat": "Éviter Vinted (trop de concurrence à bas prix). LBC + Anibis. Mettre en avant wattage et capacité litres.",
    },
    {
        "cat":     "⌚ Wearables",
        "produit": "Montre connectée (smartwatch générique)",
        "cout_1688":        9.00,
        "frais_port":       2.00,
        "lbc_min": 10, "lbc_med": 30,  "lbc_max": 80,  "lbc_nb": 200,
        "vt_min":  8,   "vt_med": 22,  "vt_max":  60,
        "an_min":  15,  "an_med": 38,  "an_max":  85,
        "frais_lbc": 0, "frais_vt": 5, "frais_an": 0,
        "rot_sem": 10,
        "strat": "Cibler segment sport + santé (fréquence cardiaque, GPS). Anibis = meilleur prix. Éviter de simuler Apple Watch.",
    },
    {
        "cat":     "⌚ Wearables",
        "produit": "Bracelet fitness tracker",
        "cout_1688":        5.00,
        "frais_port":       2.00,
        "lbc_min": 5,  "lbc_med": 18,  "lbc_max": 50,  "lbc_nb": 90,
        "vt_min":  5,   "vt_med": 15,  "vt_max":  40,
        "an_min":  10,  "an_med": 22,  "an_max":  55,
        "frais_lbc": 0, "frais_vt": 5, "frais_an": 0,
        "rot_sem": 8,
        "strat": "Vendre en lot avec montre. Volume élevé = avantage. Marché saturé bas de gamme sur Vinted.",
    },
    {
        "cat":     "🔋 Accessoires",
        "produit": "Batterie externe 20000 mAh (charge rapide)",
        "cout_1688":        6.50,
        "frais_port":       2.50,
        "lbc_min": 8,  "lbc_med": 22,  "lbc_max": 50,  "lbc_nb": 180,
        "vt_min":  5,   "vt_med": 18,  "vt_max":  40,
        "an_min":  12,  "an_med": 28,  "an_max":  60,
        "frais_lbc": 0, "frais_vt": 5, "frais_an": 0,
        "rot_sem": 10,
        "strat": "Mettre en avant wattage (65W). Lot câble inclus = prix +5€ pour +0.5€ coût. Permanent toute l'année.",
    },
    {
        "cat":     "🔋 Accessoires",
        "produit": "Câbles USB-C + adaptateurs (lot 3 pcs)",
        "cout_1688":        1.80,
        "frais_port":       1.50,
        "lbc_min": 3,  "lbc_med": 10,  "lbc_max": 22,  "lbc_nb": 60,
        "vt_min":  3,   "vt_med": 12,  "vt_max":  28,
        "an_min":  6,   "an_med": 15,  "an_max":  32,
        "frais_lbc": 0, "frais_vt": 5, "frais_an": 0,
        "rot_sem": 18,
        "strat": "Volume. Lot 3 pièces = perçu utile. Ajouter comme article additionnel aux autres ventes (vente croisée).",
    },
    {
        "cat":     "💡 Maison",
        "produit": "Lampe LED bureau tactile dimmable",
        "cout_1688":        7.00,
        "frais_port":       3.00,
        "lbc_min": 8,  "lbc_med": 28,  "lbc_max": 65,  "lbc_nb": 70,
        "vt_min":  6,   "vt_med": 20,  "vt_max":  50,
        "an_min":  12,  "an_med": 36,  "an_max":  80,
        "frais_lbc": 0, "frais_vt": 5, "frais_an": 0,
        "rot_sem": 6,
        "strat": "Axer télétravail. Photo lifestyle bureau propre. Mettre en avant 3 modes de couleur.",
    },
    {
        "cat":     "💡 Maison",
        "produit": "Guirlandes LED USB / solaire (5m)",
        "cout_1688":        2.00,
        "frais_port":       1.50,
        "lbc_min": 3,  "lbc_med": 15,  "lbc_max": 35,  "lbc_nb": 55,
        "vt_min":  3,   "vt_med": 12,  "vt_max":  28,
        "an_min":  6,   "an_med": 18,  "an_max":  40,
        "frais_lbc": 0, "frais_vt": 5, "frais_an": 0,
        "rot_sem": 14,
        "strat": "TRÈS saisonnier : nov-déc et juin-août. Commander 5 semaines avant. Vendre lot 2 guirlandes.",
    },
    {
        "cat":     "🎮 Gaming",
        "produit": "Console retro portable (10 000 jeux)",
        "cout_1688":        15.00,
        "frais_port":       3.50,
        "lbc_min": 18, "lbc_med": 52,  "lbc_max": 110, "lbc_nb": 65,
        "vt_min":  15,  "vt_med": 40,  "vt_max":  80,
        "an_min":  28,  "an_med": 65,  "an_max":  130,
        "frais_lbc": 0, "frais_vt": 5, "frais_an": 0,
        "rot_sem": 6,
        "strat": "Pic Noël, fêtes, anniversaires. Citer les jeux connus (Mario, Pac-Man). Anibis = très bon marché.",
    },
    {
        "cat":     "🧴 Beauté",
        "produit": "Épilateur lumière pulsée IPL",
        "cout_1688":        18.00,
        "frais_port":       4.00,
        "lbc_min": 30, "lbc_med": 65,  "lbc_max": 140, "lbc_nb": 45,
        "vt_min":  25,  "vt_med": 55,  "vt_max":  110,
        "an_min":  40,  "an_med": 78,  "an_max":  150,
        "frais_lbc": 0, "frais_vt": 5, "frais_an": 0,
        "rot_sem": 5,
        "strat": "Forte marge. Cible femmes 25-45 ans. Axer résultats (nombre de séances). Vinted = meilleur canal.",
    },
    {
        "cat":     "🏋️ Sport",
        "produit": "Corde à sauter intelligente (compteur)",
        "cout_1688":        8.00,
        "frais_port":       2.50,
        "lbc_min": 8,  "lbc_med": 28,  "lbc_max": 65,  "lbc_nb": 30,
        "vt_min":  5,   "vt_med": 22,  "vt_max":  50,
        "an_min":  12,  "an_med": 35,  "an_max":  75,
        "frais_lbc": 0, "frais_vt": 5, "frais_an": 0,
        "rot_sem": 6,
        "strat": "Saisonnier janv + été. Léger = frais port minimal. Insister sur compteur calories/sauts.",
    },
    {
        "cat":     "🏠 Électroménager",
        "produit": "Robot aspirateur mini (silencieux)",
        "cout_1688":        32.00,
        "frais_port":       6.00,
        "lbc_min": 40, "lbc_med": 90,  "lbc_max": 200, "lbc_nb": 85,
        "vt_min":  30,  "vt_med": 70,  "vt_max":  150,
        "an_min":  55,  "an_med": 115, "an_max":  250,
        "frais_lbc": 0, "frais_vt": 5, "frais_an": 0,
        "rot_sem": 4,
        "strat": "Encombrant → préférer remise en main propre ou colissimo épais. Anibis = prix élevés Suisse.",
    },
    {
        "cat":     "📷 Photo",
        "produit": "Mini caméra sport type action cam",
        "cout_1688":        18.00,
        "frais_port":       4.00,
        "lbc_min": 20, "lbc_med": 55,  "lbc_max": 130, "lbc_nb": 40,
        "vt_min":  15,  "vt_med": 42,  "vt_max":  90,
        "an_min":  30,  "an_med": 68,  "an_max":  150,
        "frais_lbc": 0, "frais_vt": 5, "frais_an": 0,
        "rot_sem": 4,
        "strat": "Ne jamais comparer à GoPro. Axer sur la résolution (4K) et les accessoires inclus.",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
def compute(d):
    cout = d["cout_1688"] + d["frais_port"]
    r = dict(d)
    r["cout_total"] = cout

    for plat, med_key, frais_key, fx in [
        ("lbc",    "lbc_med", "frais_lbc", 1.0),
        ("vinted", "vt_med",  "frais_vt",  1.0),
        ("anibis", "an_med",  "frais_an",  1/1.08),   # CHF → EUR approx
    ]:
        prix_med = d[med_key] * fx
        prix_cible = round(prix_med * 0.91, 2)       # -9% vs médiane = vendre vite
        frais_v = prix_cible * d[frais_key] / 100
        marge_eu = prix_cible - frais_v - cout
        marge_pct = marge_eu / prix_cible * 100 if prix_cible else 0
        roi = marge_eu / cout * 100 if cout else 0
        r[f"cible_{plat}"]    = prix_cible
        r[f"marge_eu_{plat}"] = marge_eu
        r[f"marge_pct_{plat}"]= marge_pct
        r[f"roi_{plat}"]      = roi
    return r

DATA = [compute(d) for d in MARKET_DATA]

# ══════════════════════════════════════════════════════════════════════════════
# FEUILLE 1 — TABLEAU DE BORD OPPORTUNITÉS
# ══════════════════════════════════════════════════════════════════════════════
def make_opps(wb):
    ws = wb.create_sheet("📊 OPPORTUNITÉS")
    ws.sheet_view.showGridLines = False

    MH(ws, 1, 1, 15,
       f"📊  ANALYSE CONCURRENTIELLE — PRIX MARCHÉ vs FOURNISSEUR 1688  |  Juin 2026",
       sz=13, h=30)

    headers = [
        ("A",  "Catégorie",           18, "left"),
        ("B",  "Produit",             32, "left"),
        ("C",  "Coût\ntotal unitaire",13, "center"),
        ("D",  "Prix médian\nLBC (€)", 13, "center"),
        ("E",  "Cible LBC\n(-9%)",    12, "center"),
        ("F",  "Marge €\nLBC",        11, "center"),
        ("G",  "Marge %\nLBC",        10, "center"),
        ("H",  "Prix médian\nVinted",  13, "center"),
        ("I",  "Cible Vinted",        12, "center"),
        ("J",  "Marge %\nVinted",     10, "center"),
        ("K",  "Prix médian\nAnibis",  14, "center"),
        ("L",  "Cible Anibis",        13, "center"),
        ("M",  "Marge %\nAnibis",     10, "center"),
        ("N",  "Meilleure\nplateforme",14, "center"),
        ("O",  "Rot.\n/sem",           9, "center"),
    ]
    for cl, label, w, al in headers:
        col = ord(cl) - ord("A") + 1
        H(ws, 2, col, label)
        ws.column_dimensions[cl].width = w
    ws.row_dimensions[2].height = 30

    for r_off, d in enumerate(sorted(DATA, key=lambda x: x["marge_pct_lbc"], reverse=True)):
        r = r_off + 3
        alt = C_ALT if r_off % 2 == 0 else C_WHT

        # Meilleure plateforme
        margins = {
            "LBC":    d["marge_pct_lbc"],
            "Vinted": d["marge_pct_vinted"],
            "Anibis": d["marge_pct_anibis"],
        }
        best_plat = max(margins, key=margins.get)
        best_m = margins[best_plat]

        bg_l, fg_l = marge_style(d["marge_pct_lbc"])
        bg_v, fg_v = marge_style(d["marge_pct_vinted"])
        bg_a, fg_a = marge_style(d["marge_pct_anibis"])
        bg_b = C_GBG if best_m >= 55 else C_YBG

        C(ws, r, 1,  d["cat"],       bg=alt, sz=9)
        C(ws, r, 2,  d["produit"],   bg=alt, bold=True, sz=9)
        C(ws, r, 3,  d["cout_total"],fmt=EUR, al="center", bg=alt, bold=True)

        C(ws, r, 4,  d["lbc_med"],    fmt=EUR, al="center", bg=alt)
        C(ws, r, 5,  d["cible_lbc"],  fmt=EUR, al="center", bg=C_YBG, bold=True)
        C(ws, r, 6,  d["marge_eu_lbc"],  fmt=EUR, al="center", bg=bg_l, bold=True, fg=fg_l)
        C(ws, r, 7,  d["marge_pct_lbc"], fmt=PCT, al="center", bg=bg_l, bold=True, fg=fg_l)

        C(ws, r, 8,  d["vt_med"],     fmt=EUR, al="center", bg=alt)
        C(ws, r, 9,  d["cible_vinted"], fmt=EUR, al="center", bg=C_YBG, bold=True)
        C(ws, r, 10, d["marge_pct_vinted"], fmt=PCT, al="center", bg=bg_v, bold=True, fg=fg_v)

        C(ws, r, 11, d["an_med"],     fmt='#,##0.00 " CHF"', al="center", bg=alt)
        C(ws, r, 12, d["cible_anibis"] * 1.08, fmt='#,##0" CHF"', al="center", bg=C_YBG, bold=True)
        C(ws, r, 13, d["marge_pct_anibis"], fmt=PCT, al="center", bg=bg_a, bold=True, fg=fg_a)

        C(ws, r, 14, f"{'✅' if best_m>=55 else '✔️'} {best_plat} ({best_m:.0f}%)",
          al="center", bg=bg_b, bold=True)
        C(ws, r, 15, d["rot_sem"], fmt=NB, al="center", bg=alt)

        ws.row_dimensions[r].height = 16

    ws.freeze_panes = "A3"
    ws.auto_filter.ref = f"A2:O{len(DATA)+2}"

    # Légende
    r_l = len(DATA) + 4
    MH(ws, r_l, 1, 15,
       "Prix cible = médiane concurrents × 91% pour vendre en priorité  |  "
       "Marge calculée après frais plateforme  |  Anibis converti CHF→EUR (×0.93)  |  "
       "Coût = prix 1688 + transport estimé par unité",
       bg=C_GRY, fg="555555", sz=9, h=22)


# ══════════════════════════════════════════════════════════════════════════════
# FEUILLE 2 — PRIX PAR PLATEFORME DÉTAILLÉ
# ══════════════════════════════════════════════════════════════════════════════
def make_prix_detail(wb):
    ws = wb.create_sheet("💰 PRIX DÉTAILLÉS")
    ws.sheet_view.showGridLines = False

    MH(ws, 1, 1, 13, "💰  FOURCHETTES DE PRIX PAR PLATEFORME — SOURCE MARCHÉ RÉEL", sz=12, h=28)

    headers = [
        ("A",  "Produit",       28, "left"),
        ("B",  "Coût total",    12, "center"),
        # LBC
        ("C",  "LBC Min",       10, "center"),
        ("D",  "LBC Médiane",   12, "center"),
        ("E",  "LBC Max",       10, "center"),
        ("F",  "LBC Nb ann.",    9, "center"),
        # Vinted
        ("G",  "Vinted Min",    10, "center"),
        ("H",  "Vinted Méd.",   12, "center"),
        ("I",  "Vinted Max",    10, "center"),
        # Anibis
        ("J",  "Anibis Min\n(CHF)", 12, "center"),
        ("K",  "Anibis Méd.\n(CHF)", 13, "center"),
        ("L",  "Anibis Max\n(CHF)", 12, "center"),
        # Écart
        ("M",  "Surplus\nAnibis vs LBC", 14, "center"),
    ]
    for cl, label, w, al in headers:
        col = ord(cl) - ord("A") + 1
        H(ws, 2, col, label, bg=C_TEAL)
        ws.column_dimensions[cl].width = w
    ws.row_dimensions[2].height = 30
    # Sous-en-têtes couleurs
    for col in range(3, 7):   ws.cell(row=2, column=col).fill = PatternFill("solid", fgColor=C_DARK)
    for col in range(7, 10):  ws.cell(row=2, column=col).fill = PatternFill("solid", fgColor="7030A0")
    for col in range(10, 13): ws.cell(row=2, column=col).fill = PatternFill("solid", fgColor=C_CHF)

    for r_off, d in enumerate(DATA):
        r = r_off + 3
        alt = C_ALT if r_off % 2 == 0 else C_WHT
        ecart = ((d["an_med"] / 1.08) - d["lbc_med"]) / d["lbc_med"] * 100 if d["lbc_med"] else 0

        C(ws, r, 1,  d["produit"],   bold=True, bg=alt, sz=9)
        C(ws, r, 2,  d["cout_total"], fmt=EUR, al="center", bg=alt, bold=True)
        C(ws, r, 3,  d["lbc_min"],   fmt=EUR, al="center", bg=alt)
        C(ws, r, 4,  d["lbc_med"],   fmt=EUR, al="center", bg=alt, bold=True)
        C(ws, r, 5,  d["lbc_max"],   fmt=EUR, al="center", bg=alt)
        C(ws, r, 6,  d["lbc_nb"],    fmt=NB,  al="center", bg=alt, sz=9)
        C(ws, r, 7,  d["vt_min"],    fmt=EUR, al="center", bg=alt)
        C(ws, r, 8,  d["vt_med"],    fmt=EUR, al="center", bg=alt, bold=True)
        C(ws, r, 9,  d["vt_max"],    fmt=EUR, al="center", bg=alt)
        C(ws, r, 10, d["an_min"],    fmt='#,##0 " CHF"', al="center", bg=alt)
        C(ws, r, 11, d["an_med"],    fmt='#,##0 " CHF"', al="center", bg=alt, bold=True)
        C(ws, r, 12, d["an_max"],    fmt='#,##0 " CHF"', al="center", bg=alt)
        ecart_bg = C_GBG if ecart >= 20 else (C_YBG if ecart >= 10 else C_OBG)
        C(ws, r, 13, ecart, fmt='0.0"%"', al="center", bg=ecart_bg, bold=True,
          fg=C_GREEN if ecart >= 20 else (C_YEL if ecart >= 10 else C_ORG))
        ws.row_dimensions[r].height = 16

    ws.freeze_panes = "A3"
    # Note Anibis
    r_n = len(DATA) + 4
    MH(ws, r_n, 1, 13,
       "🇨🇭 Anibis (Suisse) : les prix en CHF sont 20-40% plus élevés qu'en France pour les mêmes produits → "
       "Si vous pouvez livrer en Suisse, c'est la plateforme la plus rentable. "
       "1 CHF ≈ 0.93 € (juin 2026).",
       bg=C_YBG, fg=C_YEL, sz=10, h=28)


# ══════════════════════════════════════════════════════════════════════════════
# FEUILLE 3 — STRATÉGIE PAR PRODUIT
# ══════════════════════════════════════════════════════════════════════════════
def make_strategy(wb):
    ws = wb.create_sheet("🎯 STRATÉGIE")
    ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 3
    ws.column_dimensions["B"].width = 28
    ws.column_dimensions["C"].width = 14
    ws.column_dimensions["D"].width = 14
    ws.column_dimensions["E"].width = 14
    ws.column_dimensions["F"].width = 45

    MH(ws, 1, 1, 6, "🎯  STRATÉGIE PRODUIT PAR PRODUIT — COMMENT BATTRE LES CONCURRENTS", sz=13, h=28)

    for c_off, (label, bg) in enumerate([
        ("Produit",           C_DARK),
        ("Cible LBC (€)",     C_DARK),
        ("Cible Vinted (€)",  C_DARK),
        ("Cible Anibis (CHF)",C_DARK),
        ("Conseil stratégique", C_DARK),
    ], 2):
        H(ws, 2, c_off, label, bg=bg)
    ws.row_dimensions[2].height = 22

    top_data = sorted(DATA, key=lambda x: x["marge_pct_lbc"], reverse=True)

    for r_off, d in enumerate(top_data):
        r = r_off + 3
        alt = C_ALT if r_off % 2 == 0 else C_WHT
        best_m = max(d["marge_pct_lbc"], d["marge_pct_vinted"], d["marge_pct_anibis"])
        bg_row = C_GBG if best_m >= 55 else (C_YBG if best_m >= 35 else C_OBG)

        C(ws, r, 1, "●", al="center", bg=bg_row,
          fg=C_GREEN if best_m >= 55 else (C_YEL if best_m >= 35 else C_ORG), bold=True)
        C(ws, r, 2, d["produit"], bold=True, bg=alt, sz=9)
        C(ws, r, 3, d["cible_lbc"],    fmt=EUR, al="center", bg=C_YBG, bold=True)
        C(ws, r, 4, d["cible_vinted"], fmt=EUR, al="center", bg=C_YBG, bold=True)
        C(ws, r, 5, d["cible_anibis"] * 1.08, fmt='#,##0" CHF"', al="center", bg=C_YBG, bold=True)
        C(ws, r, 6, d["strat"], bg=alt, sz=9, wrap=True)
        ws.row_dimensions[r].height = 28


# ══════════════════════════════════════════════════════════════════════════════
# FEUILLE 4 — CALCUL MARGE PERSONNALISABLE
# ══════════════════════════════════════════════════════════════════════════════
def make_custom_calc(wb):
    ws = wb.create_sheet("🧮 CALCUL MARGE")
    ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 3
    ws.column_dimensions["B"].width = 34
    ws.column_dimensions["C"].width = 18
    ws.column_dimensions["D"].width = 34

    MH(ws, 1, 1, 4, "🧮  CALCULATEUR DE MARGE PERSONNALISÉ — MODIFIEZ LES VALEURS EN ORANGE", sz=12, h=28)

    def inp(r, label, val, fmt, hint=""):
        lc = ws.cell(row=r, column=2, value=label)
        lc.font = Font(name="Calibri", size=10); lc.border = brd()
        lc.fill = PatternFill("solid", fgColor=C_GRY)
        lc.alignment = Alignment(vertical="center")

        vc = ws.cell(row=r, column=3, value=val)
        vc.number_format = fmt
        vc.font = Font(name="Calibri", bold=True, color=C_DARK, size=12)
        vc.fill = PatternFill("solid", fgColor=C_YBG)
        vc.border = brd(C_ORG)
        vc.alignment = Alignment(horizontal="center", vertical="center")

        hc = ws.cell(row=r, column=4, value=hint)
        hc.font = Font(name="Calibri", italic=True, color="888888", size=9)
        hc.fill = PatternFill("solid", fgColor=C_GRY); hc.border = brd()
        hc.alignment = Alignment(vertical="center")
        ws.row_dimensions[r].height = 20

    def sec(r, label, bg=C_BLUE):
        ws.merge_cells(f"B{r}:D{r}")
        c = ws.cell(row=r, column=2, value=label)
        c.font = Font(name="Calibri", bold=True, color=C_WHT, size=11)
        c.fill = PatternFill("solid", fgColor=bg)
        c.border = brd(); c.alignment = Alignment(vertical="center", indent=1)
        ws.row_dimensions[r].height = 22

    def res(r, label, formula, fmt, highlight=False):
        lc = ws.cell(row=r, column=2, value=label)
        lc.font = Font(name="Calibri", bold=highlight, size=10)
        lc.fill = PatternFill("solid", fgColor=C_GBG if highlight else C_GRY)
        lc.border = brd(); lc.alignment = Alignment(vertical="center")

        vc = ws.cell(row=r, column=3, value=formula)
        vc.number_format = fmt
        vc.font = Font(name="Calibri", bold=True,
                       color=C_GREEN if highlight else C_DARK, size=13 if highlight else 11)
        vc.fill = PatternFill("solid", fgColor=C_GBG if highlight else C_WHT)
        vc.border = brd(); vc.alignment = Alignment(horizontal="center", vertical="center")
        ws.row_dimensions[r].height = 22 if highlight else 19

    sec(2,  "  📦  ACHAT 1688")
    inp(3,  "Prix achat unitaire 1688 (€)",    9.00,  EUR, "Converti depuis yuan")
    inp(4,  "Frais transport total lot (€)",   45.00, EUR, "Toute la commande")
    inp(5,  "Quantité dans le lot",            10,    NB,  "Nombre d'unités")
    inp(6,  "Droits de douane lot (€)",        0,     EUR, "0€ si lot <150€")

    sec(7,  "  🛒  VENTE")
    inp(8,  "Prix de vente (€)",              32.00, EUR, "Votre prix annonce")
    inp(9,  "Frais plateforme (%)",            5,    '0"%"', "Vinted=5%, LBC=0%, Anibis=0%")
    inp(10, "Frais livraison à votre charge",  6.00, EUR,  "0 si acheteur paie port")
    inp(11, "Unités vendues par semaine",      8,    NB,   "Estimation")

    sec(12, "  📊  RÉSULTATS", bg=C_GREEN)
    res(13, "Coût unitaire total",    "=(C3*C5+C4+C6)/C5", EUR)
    res(14, "Frais plateforme /unit", "=C8*C9/100",         EUR)
    res(15, "Prix net reçu",          "=C8-C14-C10",        EUR)
    res(16, "MARGE NETTE / UNITÉ",    "=C15-C13",           EUR, highlight=True)
    res(17, "MARGE NETTE %",          "=IF(C8=0,0,C16/C8*100)", PCT, highlight=True)
    res(18, "ROI %",                  "=IF(C13=0,0,C16/C13*100)", PCT)
    res(19, "CA HEBDO estimé (€)",    "=C8*C11",            EUR, highlight=True)
    res(20, "MARGE HEBDO estimée (€)","=C16*C11",           EUR, highlight=True)
    res(21, "MARGE MENSUELLE (€)",    "=C20*4",             EUR, highlight=True)
    res(22, "Seuil rentabilité (unités)", "=CEILING((C4+C6)/(C8-C3-C14-C10),1)", NB)

    # Produits pré-remplis en lecture rapide
    r_table = 25
    MH(ws, r_table, 1, 4, "📋  RÉFÉRENCES RAPIDES — COÛTS 1688 (mis à jour juin 2026)",
       bg=C_TEAL, sz=11, h=24)
    H(ws, r_table+1, 2, "Produit", bg=C_TEAL)
    H(ws, r_table+1, 3, "Coût total unitaire (1688 + port)", bg=C_TEAL)
    H(ws, r_table+1, 4, "Quantité min. conseillée", bg=C_TEAL)
    ws.row_dimensions[r_table+1].height = 22

    quick_ref = [
        ("Écouteurs TWS",           7.00,  "20 unités → 140€ total"),
        ("Haut-parleur Bluetooth", 12.50,  "10 unités → 125€ total"),
        ("Air Fryer 4L",           33.00,  "5 unités → 165€ total"),
        ("Montre connectée",       11.00,  "15 unités → 165€ total"),
        ("Batterie externe 20k",    9.00,  "15 unités → 135€ total"),
        ("Câbles USB-C lot ×3",     3.30,  "30 lots → 99€ total"),
        ("Lampe LED bureau",       10.00,  "10 unités → 100€ total"),
        ("Guirlandes LED",          3.50,  "20 unités → 70€ total"),
        ("Console retro portable", 18.50,  "8 unités → 148€ total"),
        ("Épilateur IPL",          22.00,  "5 unités → 110€ total"),
    ]
    for i, (nom, cout, hint) in enumerate(quick_ref):
        r = r_table + 2 + i
        alt = C_ALT if i % 2 == 0 else C_WHT
        C(ws, r, 2, nom,  bold=True, bg=alt, sz=9)
        C(ws, r, 3, cout, fmt=EUR, al="center", bg=C_GBG, bold=True, fg=C_GREEN)
        C(ws, r, 4, hint, bg=alt, sz=9)
        ws.row_dimensions[r].height = 16


# ══════════════════════════════════════════════════════════════════════════════
# FEUILLE 5 — LIENS FOURNISSEURS
# ══════════════════════════════════════════════════════════════════════════════
def make_suppliers(wb):
    ws = wb.create_sheet("🏭 FOURNISSEURS")
    ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 3
    ws.column_dimensions["B"].width = 30
    ws.column_dimensions["C"].width = 20
    ws.column_dimensions["D"].width = 14
    ws.column_dimensions["E"].width = 14
    ws.column_dimensions["F"].width = 14
    ws.column_dimensions["G"].width = 40

    MH(ws, 1, 1, 7, "🏭  FOURNISSEURS RECOMMANDÉS — COMMENT TROUVER SUR 1688 ET ALIBABA", sz=12, h=28)

    # Méthode de recherche
    tip = [
        ("🔎 Comment chercher sur 1688.com (en chinois) :",
         "Utilisez Google Translate dans Chrome → allez sur 1688.com → tapez le produit en pinyin ou utilisez la photo."),
        ("🌐 Alternative plus simple : Alibaba.com :",
         "Alibaba est en anglais. Cherchez 'TWS earphone', 'smartwatch', 'air fryer', 'power bank'. Prix ~20% plus chers qu'1688 mais plus simple."),
        ("📦 Minimum de commande :",
         "1688 : souvent 1 unité possible. Alibaba : MOQ (min order qty) affiché. Négociez pour démarrer avec 5-10 unités."),
        ("🚚 Transport recommandé :",
         "Budget Parcel / Superbuy / CSSBuy (agents 1688 vers France) : 3-6€/kg. Comptez 15-25 jours ouvrés."),
        ("💰 Paiement :",
         "Alibaba : carte visa, PayPal, Trade Assurance (sécurisé). 1688 : via agent sourcing (ils ont compte Alipay)."),
        ("📋 Conseils de négociation :",
         "Demandez toujours un échantillon avant grosse commande. Mentionnez que vous êtes revendeur régulier = prix meilleur."),
    ]

    r = 2
    for label, desc in tip:
        ws.merge_cells(f"B{r}:G{r}")
        c = ws.cell(row=r, column=2, value=label)
        c.font = Font(name="Calibri", bold=True, color=C_WHT, size=10)
        c.fill = PatternFill("solid", fgColor=C_BLUE)
        c.border = brd(); c.alignment = Alignment(vertical="center", indent=1)
        ws.row_dimensions[r].height = 20
        r += 1

        ws.merge_cells(f"B{r}:G{r}")
        c2 = ws.cell(row=r, column=2, value=desc)
        c2.font = Font(name="Calibri", size=10)
        c2.fill = PatternFill("solid", fgColor=C_ALT); c2.border = brd()
        c2.alignment = Alignment(vertical="center", wrap_text=True)
        ws.row_dimensions[r].height = 26
        r += 1

    r += 1

    # Table fournisseurs par produit
    MH(ws, r, 1, 7, "📋  MOTS-CLÉS DE RECHERCHE PAR PRODUIT (Alibaba anglais / 1688 chinois)",
       bg=C_TEAL, sz=11, h=24)
    r += 1

    for cl, label, bg in [
        (2, "Produit", C_TEAL), (3, "Mot-clé Alibaba (EN)", C_TEAL),
        (4, "Fourchette prix (€)", C_TEAL), (5, "MOQ conseillé", C_TEAL),
        (6, "Note qualité", C_TEAL), (7, "Délai livraison", C_TEAL),
    ]:
        H(ws, r, cl, label, bg=bg)
    ws.row_dimensions[r].height = 22
    r += 1

    suppliers = [
        ("Écouteurs TWS",         "TWS earphones bluetooth 5.3",    "3-8€",  "20+",  "⭐⭐⭐⭐", "18-25j"),
        ("Haut-parleur Bluetooth","portable bluetooth speaker IPX5", "8-15€", "10+",  "⭐⭐⭐⭐", "18-25j"),
        ("Air Fryer 4L",          "air fryer oven 4L 1500W",        "25-35€", "5+",  "⭐⭐⭐",  "20-30j"),
        ("Montre connectée",      "smartwatch fitness tracker AMOLED","8-15€","20+", "⭐⭐⭐⭐", "18-25j"),
        ("Bracelet fitness",      "fitness tracker band heart rate", "4-8€",  "20+",  "⭐⭐⭐⭐", "18-22j"),
        ("Batterie externe 20k",  "power bank 20000mAh 65W fast charge","6-12€","15+","⭐⭐⭐⭐","18-25j"),
        ("Câbles USB-C lot",      "USB-C cable fast charging 3 pack","1-3€", "50+",  "⭐⭐⭐",  "15-22j"),
        ("Lampe LED bureau",      "LED desk lamp touch dimmer 3 mode","6-12€","10+","⭐⭐⭐⭐", "18-25j"),
        ("Guirlandes LED",        "fairy lights USB string 5m",      "1.5-3€","50+","⭐⭐⭐",  "15-20j"),
        ("Console retro portable","retro game console handheld 10000","12-20€","8+","⭐⭐⭐⭐", "20-28j"),
        ("Épilateur IPL",         "IPL hair removal device 500000",  "15-25€","5+", "⭐⭐⭐",  "18-28j"),
        ("Robot aspirateur",      "robot vacuum cleaner 2000Pa quiet","30-50€","3+","⭐⭐⭐",  "25-35j"),
        ("Caméra action sport",   "action camera 4K waterproof sport","15-25€","5+","⭐⭐⭐",  "20-28j"),
        ("Corde à sauter smart",  "smart jump rope calorie counter",  "6-12€", "10+","⭐⭐⭐⭐","18-25j"),
    ]

    for i, row in enumerate(suppliers):
        rr = r + i
        alt = C_ALT if i % 2 == 0 else C_WHT
        for col, val in enumerate(row, 2):
            C(ws, rr, col, val, bg=alt, sz=9, al="center" if col > 2 else "left",
              bold=(col == 2))
        ws.row_dimensions[rr].height = 16


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════
def main():
    wb = openpyxl.Workbook()
    wb.remove(wb.active)

    make_opps(wb)
    make_prix_detail(wb)
    make_strategy(wb)
    make_custom_calc(wb)
    make_suppliers(wb)

    wb.active = wb["📊 OPPORTUNITÉS"]

    out = "/home/user/Rapport_Marche_Concurrents_2026.xlsx"
    wb.save(out)
    print(f"✅  Rapport créé : {out}")

if __name__ == "__main__":
    main()
