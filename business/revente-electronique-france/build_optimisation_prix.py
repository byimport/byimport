#!/usr/bin/env python3
"""
Rapport d'optimisation des prix — meilleurs vendeurs scrappés
Produits Semaine 1 : TWS, Smartwatch, Power Bank, Guirlandes LED
"""
from openpyxl import Workbook
from openpyxl.styles import (
    Font, PatternFill, Alignment, Border, Side, numbers
)
from openpyxl.utils import get_column_letter
from openpyxl.chart import BarChart, Reference
from openpyxl.formatting.rule import ColorScaleRule, DataBarRule
from openpyxl.worksheet.datavalidation import DataValidation
import datetime

# ── Palette ─────────────────────────────────────────────────────────────────
C_DARK   = "1A1A2E"   # fond titres
C_BLUE   = "16213E"
C_TEAL   = "0F3460"
C_ACC    = "E94560"   # accent rouge-rose
C_GREEN  = "27AE60"
C_GOLD   = "F39C12"
C_ORANGE = "E67E22"
C_LGRAY  = "F5F5F5"
C_WHITE  = "FFFFFF"
C_YELLOW = "FFF176"
C_LIME   = "DCEDC8"

def hd(ws, row, col, txt, bg=C_DARK, fg=C_WHITE, bold=True, size=12, wrap=False, align="center"):
    c = ws.cell(row=row, column=col, value=txt)
    c.font = Font(bold=bold, color=fg, size=size, name="Calibri")
    c.fill = PatternFill("solid", fgColor=bg)
    c.alignment = Alignment(horizontal=align, vertical="center", wrap_text=wrap)
    return c

def bd(ws, row, col, txt, bg=C_WHITE, fg="000000", bold=False, size=10, align="left", wrap=False, fmt=None):
    c = ws.cell(row=row, column=col, value=txt)
    c.font = Font(bold=bold, color=fg, size=size, name="Calibri")
    c.fill = PatternFill("solid", fgColor=bg)
    c.alignment = Alignment(horizontal=align, vertical="center", wrap_text=wrap)
    if fmt:
        c.number_format = fmt
    return c

def thin_border():
    s = Side(border_style="thin", color="CCCCCC")
    return Border(left=s, right=s, top=s, bottom=s)

def apply_borders(ws, min_row, max_row, min_col, max_col):
    for r in range(min_row, max_row+1):
        for c in range(min_col, max_col+1):
            ws.cell(row=r, column=c).border = thin_border()

# ── Données marché (collectées par WebSearch juin 2026) ────────────────────
# Structure : produit, achat_1688, fret_unit, douane_unit,
#             lbc_min, lbc_med, lbc_max, vt_min, vt_med, vt_max,
#             ani_min_chf, ani_med_chf, ani_max_chf

MARKET = [
    {
        "id": "TWS",
        "nom": "Écouteurs TWS Bluetooth 5.3",
        "cat_lbc": "Accessoires téléphone",
        "cat_vt":  "Montres / Bracelets",
        "cat_ani": "Audio & Hi-Fi",
        "achat":   2.80,   # € — prix 1688 par unité (lot 20)
        "fret":    0.55,
        "douane":  0.10,
        "lbc_min": 7.90,  "lbc_med": 18.0,  "lbc_max": 35.0,
        "vt_min":  8.0,   "vt_med":  16.0,  "vt_max":  30.0,
        "ani_min": 10.0,  "ani_med": 20.0,  "ani_max": 40.0,
        # Titres gagnants observés chez les meilleurs vendeurs
        "top_titres_lbc": [
            "Écouteurs Bluetooth 5.3 TWS – Son HiFi – Neuf sous blister",
            "Écouteurs sans fil TWS Q11 – Basses puissantes – Boîtier charge inclus",
        ],
        "top_titres_vt": [
            "Écouteurs TWS Bluetooth neuf – livraison rapide",
            "Airbuds sans fil Bluetooth 5.3 – neuf jamais servi",
        ],
        "top_titres_ani": [
            "Écouteurs Bluetooth TWS 5.3 – neuf avec boîtier charge – 20 CHF",
            "True Wireless Earbuds HiFi – Livraison Suisse",
        ],
        "desc_fr": (
            "✅ NEUFS – jamais portés.\n"
            "Écouteurs sans fil Bluetooth 5.3 avec boîtier de charge compact.\n"
            "• Autonomie : ~4h écoute + 3 recharges via le boîtier\n"
            "• Son HiFi, basses profondes\n"
            "• Connexion automatique, compatible iOS & Android\n"
            "• Idéal sport, transport, télétravail\n"
            "Livraison Mondial Relay ou Colissimo. Paiement sécurisé."
        ),
        "tips": "Photo : boîtier ouvert, écouteurs dedans, fond blanc. Ajouter photo câble USB-C inclus.",
        "vitesse_vente": "Rapide (1–3 jours)",
    },
    {
        "id": "WATCH",
        "nom": "Smartwatch AMOLED 1.43\" Appels BT",
        "cat_lbc": "Montres & Bijoux",
        "cat_vt":  "Montres sport / bracelets connectés",
        "cat_ani": "Montres & Bijoux",
        "achat":  10.50,
        "fret":    1.20,
        "douane":  0.45,
        "lbc_min": 25.0,  "lbc_med": 38.0,  "lbc_max": 79.0,
        "vt_min":  20.0,  "vt_med":  32.0,  "vt_max":  65.0,
        "ani_min": 28.0,  "ani_med": 42.0,  "ani_max": 80.0,
        "top_titres_lbc": [
            "Montre connectée AMOLED 1.43\" – Appels Bluetooth – Neuve boîte",
            "Smartwatch AMOLED Homme/Femme – GPS sport – Neuve jamais utilisée",
        ],
        "top_titres_vt": [
            "Smartwatch AMOLED neuve – appels Bluetooth – écran 1.43\"",
            "Montre connectée sport AMOLED – neuf – boîte d'origine",
        ],
        "top_titres_ani": [
            "Smartwatch AMOLED 1.43\" – Appels BT – Neuve – 39 CHF",
            "Montre connectée AMOLED – sport & santé – Livraison Suisse",
        ],
        "desc_fr": (
            "✅ NEUVE – jamais portée, boîte d'origine.\n"
            "Smartwatch avec écran AMOLED 1.43\" ultra-lisible.\n"
            "• Appels Bluetooth directement depuis la montre\n"
            "• Fréquence cardiaque, SpO2, suivi sommeil\n"
            "• 100+ modes sport, GPS activité\n"
            "• Compatible iOS & Android\n"
            "• Autonomie ~7 jours\n"
            "Livraison Mondial Relay. Facture disponible sur demande."
        ),
        "tips": "Photo : montre allumée (écran AMOLED visible) + boîte. Fond neutre. Gros plan cadran.",
        "vitesse_vente": "Moyen (3–7 jours)",
    },
    {
        "id": "PB",
        "nom": "Batterie externe 20000mAh USB-C",
        "cat_lbc": "Accessoires téléphone",
        "cat_vt":  "Accessoires téléphone",
        "cat_ani": "Accessoires téléphone",
        "achat":   5.80,
        "fret":    1.10,
        "douane":  0.25,
        "lbc_min": 11.0,  "lbc_med": 17.0,  "lbc_max": 25.0,
        "vt_min":  10.0,  "vt_med":  15.0,  "vt_max":  22.0,
        "ani_min": 17.0,  "ani_med": 25.0,  "ani_max": 40.0,
        "top_titres_lbc": [
            "Batterie externe 20000mAh USB-C – Charge rapide – Neuve emballée",
            "Power Bank 20000mAh 2 ports USB – Neuf – compatible iPhone & Samsung",
        ],
        "top_titres_vt": [
            "Batterie externe 20000mAh neuve – charge rapide USB-C",
            "Power Bank 20000 mAh – neuf – iPhone Android Switch",
        ],
        "top_titres_ani": [
            "Batterie externe 20000mAh USB-C – Neuve – 22 CHF livraison Suisse",
            "Power Bank 20000mAh 2x USB + USB-C – Nouveau emballé",
        ],
        "desc_fr": (
            "✅ NEUVE – scellée, jamais ouverte.\n"
            "Batterie externe 20000mAh haute capacité.\n"
            "• 2× ports USB-A + 1× USB-C\n"
            "• Charge rapide 22,5W compatible iPhone, Samsung, Switch\n"
            "• Indicateur LED niveau batterie\n"
            "• Idéal voyage, festival, randonnée\n"
            "Envoi en recommandé. Satisfait ou remboursé 7 jours."
        ),
        "tips": "Photo : batterie avec câbles branchés + téléphone en charge. Montre l'utilisation concrète.",
        "vitesse_vente": "Rapide (1–4 jours)",
    },
    {
        "id": "LED",
        "nom": "Guirlande LED USB 10m 100 LEDs",
        "cat_lbc": "Décoration",
        "cat_vt":  "Décoration maison",
        "cat_ani": "Mobilier & Décoration",
        "achat":   1.50,
        "fret":    0.40,
        "douane":  0.05,
        "lbc_min":  9.99, "lbc_med": 13.0,  "lbc_max": 25.0,
        "vt_min":   8.0,  "vt_med":  12.0,  "vt_max":  20.0,
        "ani_min": 12.0,  "ani_med": 16.0,  "ani_max": 25.0,
        "top_titres_lbc": [
            "Guirlande LED 10m USB – 100 LED – Chambre / Salon – Neuve",
            "Guirlande lumineuse 100 LED USB – Télécommande – 8 modes – Neuve",
        ],
        "top_titres_vt": [
            "Guirlande LED chambre 10m USB – neuve – livraison rapide",
            "Décoration lumineuse LED 100 ampoules – neuve emballée",
        ],
        "top_titres_ani": [
            "Guirlande LED 10m USB 100 LED – Neuve – 14 CHF Suisse",
            "Décoration LED chambre bureau – 8 modes – Nouvelle emballée",
        ],
        "desc_fr": (
            "✅ NEUVE – emballage d'origine.\n"
            "Guirlande lumineuse LED 10m, 100 ampoules, alimentation USB.\n"
            "• 8 modes d'éclairage + minuterie\n"
            "• Télécommande incluse\n"
            "• Parfaite chambre, salon, bureau, terrasse\n"
            "• IP44 – peut s'utiliser en extérieur abrité\n"
            "Expédiée sous 24h. Envoi suivi inclus."
        ),
        "tips": "Photo : guirlande allumée dans une chambre sombre. Ambiance chaleureuse. Très impactant.",
        "vitesse_vente": "Très rapide (< 24h en été)",
    },
]

FX_CHF_EUR = 0.927   # 1 CHF = 0.927 €  (juin 2026)
FRAIS_VT   = 0.05    # Vinted : 5% frais vendeur
FRAIS_LBC  = 0.00    # LBC particulier : 0%
FRAIS_ANI  = 0.00    # Anibis : 0%

def cout_total(p):
    return round(p["achat"] + p["fret"] + p["douane"], 2)

def marge(prix_eur, cout, frais_pct):
    net = prix_eur * (1 - frais_pct)
    return round(net - cout, 2)

def marge_pct(prix_eur, cout, frais_pct):
    net = prix_eur * (1 - frais_pct)
    if net == 0:
        return 0
    return round((net - cout) / net * 100, 1)

def prix_cible(med, pct_discount=0.91):
    """Prix légèrement en dessous de la médiane pour vendre vite"""
    return round(med * pct_discount, 2)

# ── SHEET 1 : RÉSUMÉ EXÉCUTIF ─────────────────────────────────────────────
def make_resume(wb):
    ws = wb.create_sheet("RÉSUMÉ PRIX")
    ws.sheet_properties.tabColor = "E94560"
    ws.freeze_panes = "A4"

    ws.column_dimensions["A"].width = 28
    for col in "BCDEFGHIJ":
        ws.column_dimensions[col].width = 16
    ws.column_dimensions["K"].width = 40

    # Titre
    ws.merge_cells("A1:K1")
    hd(ws, 1, 1, "OPTIMISATION PRIX — MEILLEURS VENDEURS SCRAPPÉS | Juin 2026",
       C_ACC, C_WHITE, size=14)
    ws.row_dimensions[1].height = 32

    ws.merge_cells("A2:K2")
    hd(ws, 2, 1,
       f"Données collectées le {datetime.date.today().strftime('%d/%m/%Y')} — "
       "LeBonCoin · Vinted · Anibis.ch | FX: 1 CHF = {:.3f} €".format(FX_CHF_EUR),
       C_TEAL, C_WHITE, size=10)
    ws.row_dimensions[2].height = 20

    # En-têtes
    headers = [
        "Produit", "Coût total €", "LBC cible €", "Marge LBC %",
        "VT cible €", "Marge VT %", "ANI cible CHF", "Marge ANI %",
        "Vitesse vente", "ROI %", "Titre LBC recommandé"
    ]
    for ci, h in enumerate(headers, 1):
        hd(ws, 3, ci, h, C_DARK, C_WHITE, size=10)
    ws.row_dimensions[3].height = 24

    for ri, p in enumerate(MARKET, 4):
        ct = cout_total(p)
        lbc_c = prix_cible(p["lbc_med"])
        vt_c  = prix_cible(p["vt_med"])
        ani_c_chf = prix_cible(p["ani_med"])
        ani_c_eur = round(ani_c_chf * FX_CHF_EUR, 2)

        m_lbc = marge_pct(lbc_c, ct, FRAIS_LBC)
        m_vt  = marge_pct(vt_c,  ct, FRAIS_VT)
        m_ani = marge_pct(ani_c_eur, ct, FRAIS_ANI)
        roi   = round((lbc_c - ct) / ct * 100, 0) if ct > 0 else 0

        bg = C_LGRAY if ri % 2 == 0 else C_WHITE

        bd(ws, ri, 1, p["nom"],    bg=bg, bold=True, size=10, align="left")
        bd(ws, ri, 2, ct,          bg=bg, fmt="#,##0.00 €",  align="right")
        bd(ws, ri, 3, lbc_c,       bg=bg, fmt="#,##0.00 €",  align="right", bold=True)
        # Marge LBC avec couleur
        c_ml = ws.cell(row=ri, column=4, value=m_lbc/100)
        c_ml.number_format = "0%"
        c_ml.font = Font(bold=True, color=C_WHITE if m_lbc > 40 else "000000", size=10)
        c_ml.fill = PatternFill("solid", fgColor=C_GREEN if m_lbc > 40 else C_GOLD if m_lbc > 20 else C_ACC)
        c_ml.alignment = Alignment(horizontal="center", vertical="center")

        bd(ws, ri, 5, vt_c,        bg=bg, fmt="#,##0.00 €",  align="right")
        c_mv = ws.cell(row=ri, column=6, value=m_vt/100)
        c_mv.number_format = "0%"
        c_mv.font = Font(bold=True, color=C_WHITE if m_vt > 40 else "000000", size=10)
        c_mv.fill = PatternFill("solid", fgColor=C_GREEN if m_vt > 40 else C_GOLD if m_vt > 20 else C_ACC)
        c_mv.alignment = Alignment(horizontal="center", vertical="center")

        bd(ws, ri, 7, ani_c_chf,   bg=bg, fmt="#,##0.00 CHF", align="right")
        c_ma = ws.cell(row=ri, column=8, value=m_ani/100)
        c_ma.number_format = "0%"
        c_ma.font = Font(bold=True, color=C_WHITE if m_ani > 40 else "000000", size=10)
        c_ma.fill = PatternFill("solid", fgColor=C_GREEN if m_ani > 40 else C_GOLD if m_ani > 20 else C_ACC)
        c_ma.alignment = Alignment(horizontal="center", vertical="center")

        bd(ws, ri, 9,  p["vitesse_vente"], bg=bg, align="center")
        bd(ws, ri, 10, roi/100, bg=bg, fmt="0%", bold=True, align="center")
        bd(ws, ri, 11, p["top_titres_lbc"][0], bg=bg, wrap=True, size=9, align="left")
        ws.row_dimensions[ri].height = 36

    apply_borders(ws, 3, 3+len(MARKET), 1, 11)
    return ws

# ── SHEET 2 : DÉTAIL PAR PLATEFORME ──────────────────────────────────────
def make_detail(wb):
    ws = wb.create_sheet("PRIX PAR PLATEFORME")
    ws.sheet_properties.tabColor = "27AE60"
    ws.freeze_panes = "A4"

    col_w = [28, 12, 12, 12, 14, 14, 12, 12, 12, 14, 14, 12, 12, 12, 14, 14]
    for i, w in enumerate(col_w, 1):
        ws.column_dimensions[get_column_letter(i)].width = w

    ws.merge_cells("A1:P1")
    hd(ws, 1, 1, "ANALYSE CONCURRENTIELLE PAR PLATEFORME — DONNÉES RÉELLES MARCHÉ",
       C_TEAL, C_WHITE, size=13)
    ws.row_dimensions[1].height = 30

    # Sous-headers plateformes
    ws.merge_cells("B2:F2");  hd(ws, 2, 2, "🇫🇷 LeBonCoin", C_BLUE, C_WHITE, size=11)
    ws.merge_cells("G2:K2");  hd(ws, 2, 7, "👗 Vinted",    C_TEAL, C_WHITE, size=11)
    ws.merge_cells("L2:P2");  hd(ws, 2, 12, "🇨🇭 Anibis.ch", "17202A", C_WHITE, size=11)

    headers_sub = ["Min", "Médiane", "Max", "CIBLE VENTE", "Marge %"] * 3
    bd(ws, 3, 1, "Produit", bg=C_DARK, fg=C_WHITE, bold=True, align="center")
    for ci, h in enumerate(headers_sub, 2):
        ws.cell(row=3, column=ci, value=h)
        ws.cell(row=3, column=ci).font = Font(bold=True, size=9, color=C_WHITE)
        ws.cell(row=3, column=ci).fill = PatternFill("solid", fgColor=C_DARK)
        ws.cell(row=3, column=ci).alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[3].height = 22

    for ri, p in enumerate(MARKET, 4):
        ct = cout_total(p)
        lbc_c = prix_cible(p["lbc_med"])
        vt_c  = prix_cible(p["vt_med"])
        ani_c = prix_cible(p["ani_med"])
        ani_eur = round(ani_c * FX_CHF_EUR, 2)

        m_lbc = marge_pct(lbc_c, ct, FRAIS_LBC)
        m_vt  = marge_pct(vt_c,  ct, FRAIS_VT)
        m_ani = marge_pct(ani_eur, ct, FRAIS_ANI)

        bg = C_LGRAY if ri % 2 == 0 else C_WHITE

        bd(ws, ri, 1,  p["nom"],       bg=bg, bold=True, size=9)
        # LBC
        bd(ws, ri, 2,  p["lbc_min"],   bg=bg, fmt="#,##0.00 €", align="right", size=9)
        bd(ws, ri, 3,  p["lbc_med"],   bg=bg, fmt="#,##0.00 €", align="right", size=9)
        bd(ws, ri, 4,  p["lbc_max"],   bg=bg, fmt="#,##0.00 €", align="right", size=9)
        c = ws.cell(row=ri, column=5, value=lbc_c)
        c.number_format = "#,##0.00 €"; c.font = Font(bold=True, color=C_ACC, size=10)
        c.fill = PatternFill("solid", fgColor="FFF3F3")
        c.alignment = Alignment(horizontal="right", vertical="center")
        c_m = ws.cell(row=ri, column=6, value=m_lbc/100)
        c_m.number_format = "0%"
        c_m.font = Font(bold=True, color=C_WHITE, size=10)
        c_m.fill = PatternFill("solid", fgColor=C_GREEN if m_lbc > 40 else C_GOLD)
        c_m.alignment = Alignment(horizontal="center", vertical="center")
        # Vinted
        bd(ws, ri, 7,  p["vt_min"],    bg=bg, fmt="#,##0.00 €", align="right", size=9)
        bd(ws, ri, 8,  p["vt_med"],    bg=bg, fmt="#,##0.00 €", align="right", size=9)
        bd(ws, ri, 9,  p["vt_max"],    bg=bg, fmt="#,##0.00 €", align="right", size=9)
        c2 = ws.cell(row=ri, column=10, value=vt_c)
        c2.number_format = "#,##0.00 €"; c2.font = Font(bold=True, color=C_ACC, size=10)
        c2.fill = PatternFill("solid", fgColor="FFF3F3")
        c2.alignment = Alignment(horizontal="right", vertical="center")
        c_m2 = ws.cell(row=ri, column=11, value=m_vt/100)
        c_m2.number_format = "0%"
        c_m2.font = Font(bold=True, color=C_WHITE, size=10)
        c_m2.fill = PatternFill("solid", fgColor=C_GREEN if m_vt > 40 else C_GOLD)
        c_m2.alignment = Alignment(horizontal="center", vertical="center")
        # Anibis CHF
        bd(ws, ri, 12, p["ani_min"],   bg=bg, fmt="#,##0 CHF", align="right", size=9)
        bd(ws, ri, 13, p["ani_med"],   bg=bg, fmt="#,##0 CHF", align="right", size=9)
        bd(ws, ri, 14, p["ani_max"],   bg=bg, fmt="#,##0 CHF", align="right", size=9)
        c3 = ws.cell(row=ri, column=15, value=ani_c)
        c3.number_format = "#,##0.00 CHF"; c3.font = Font(bold=True, color=C_ACC, size=10)
        c3.fill = PatternFill("solid", fgColor="FFF3F3")
        c3.alignment = Alignment(horizontal="right", vertical="center")
        c_m3 = ws.cell(row=ri, column=16, value=m_ani/100)
        c_m3.number_format = "0%"
        c_m3.font = Font(bold=True, color=C_WHITE, size=10)
        c_m3.fill = PatternFill("solid", fgColor=C_GREEN if m_ani > 40 else C_GOLD)
        c_m3.alignment = Alignment(horizontal="center", vertical="center")

        ws.row_dimensions[ri].height = 26

    apply_borders(ws, 2, 3+len(MARKET), 1, 16)

    # Note de lecture
    nr = 4 + len(MARKET) + 1
    ws.merge_cells(f"A{nr}:P{nr}")
    hd(ws, nr, 1,
       "💡 Méthode : Prix cible = Médiane × 91% — Vous êtes 9% moins cher que la médiane ⟹ vous vendez en premier. "
       "Marge ANI calculée après conversion CHF→EUR (taux 0.927). Frais Vinted 5% déduits.",
       C_LGRAY, "444444", bold=False, size=9, align="left")

# ── SHEET 3 : TITRES & DESCRIPTIONS ───────────────────────────────────────
def make_annonces(wb):
    ws = wb.create_sheet("ANNONCES OPTIMISÉES")
    ws.sheet_properties.tabColor = "F39C12"
    ws.freeze_panes = "A3"

    ws.column_dimensions["A"].width = 22
    ws.column_dimensions["B"].width = 20
    ws.column_dimensions["C"].width = 52
    ws.column_dimensions["D"].width = 52
    ws.column_dimensions["E"].width = 45

    ws.merge_cells("A1:E1")
    hd(ws, 1, 1, "ANNONCES PRÊTES À COLLER — TITRES & DESCRIPTIONS OPTIMISÉS",
       C_GOLD, C_WHITE, size=13)
    ws.row_dimensions[1].height = 28

    for ci, h in enumerate(["Produit", "Plateforme", "Titre (copier-coller)", "Description (copier-coller)", "Tips photo"], 1):
        hd(ws, 2, ci, h, C_DARK, C_WHITE, size=10)
    ws.row_dimensions[2].height = 22

    row = 3
    for p in MARKET:
        platforms = [
            ("LeBonCoin",  p["top_titres_lbc"][0], p["top_titres_lbc"][1]),
            ("Vinted",     p["top_titres_vt"][0],  p["top_titres_vt"][1]),
            ("Anibis.ch",  p["top_titres_ani"][0], p["top_titres_ani"][1]),
        ]
        for pname, titre1, titre2 in platforms:
            bg_p = {"LeBonCoin": "E8F4FD", "Vinted": "E8F8F5", "Anibis.ch": "FEF9E7"}.get(pname, C_WHITE)
            bd(ws, row, 1, p["nom"],    bg=bg_p, bold=True, wrap=True, size=9)
            bd(ws, row, 2, pname,       bg=bg_p, bold=True, align="center", size=9)
            bd(ws, row, 3, titre1,      bg=bg_p, wrap=True, size=9)
            bd(ws, row, 4, p["desc_fr"],bg=bg_p, wrap=True, size=9)
            bd(ws, row, 5, p["tips"],   bg=bg_p, wrap=True, size=9)
            ws.row_dimensions[row].height = 80
            row += 1

        # Titre alternatif en gris clair
        bd(ws, row, 1, "",  bg="F9F9F9")
        bd(ws, row, 2, "Alt. 2", bg="F9F9F9", align="center", size=8, fg="888888")
        bd(ws, row, 3, platforms[0][2], bg="F9F9F9", wrap=True, size=8, fg="666666")
        bd(ws, row, 4, platforms[1][2], bg="F9F9F9", wrap=True, size=8, fg="666666")
        bd(ws, row, 5, platforms[2][2], bg="F9F9F9", wrap=True, size=8, fg="666666")
        ws.row_dimensions[row].height = 30
        row += 1

    apply_borders(ws, 2, row - 1, 1, 5)

# ── SHEET 4 : CALCUL MARGE DÉTAILLÉ ───────────────────────────────────────
def make_marge(wb):
    ws = wb.create_sheet("CALCUL MARGES")
    ws.sheet_properties.tabColor = "27AE60"
    ws.freeze_panes = "A4"

    ws.column_dimensions["A"].width = 28
    for col in "BCDEFGHIJKLM":
        ws.column_dimensions[col].width = 14

    ws.merge_cells("A1:M1")
    hd(ws, 1, 1, "CALCUL DE MARGES DÉTAILLÉ — 4 PRODUITS × 3 PLATEFORMES",
       C_GREEN, C_WHITE, size=13)
    ws.row_dimensions[1].height = 30

    ws.merge_cells("B2:E2");  hd(ws, 2, 2, "COÛTS", "2C3E50", C_WHITE)
    ws.merge_cells("F2:H2");  hd(ws, 2, 6, "LeBonCoin", C_BLUE, C_WHITE)
    ws.merge_cells("I2:J2");  hd(ws, 2, 9, "Vinted (-5%)", C_TEAL, C_WHITE)
    ws.merge_cells("K2:M2");  hd(ws, 2, 11, "Anibis.ch (CHF)", "2C3E50", C_WHITE)

    sub = ["Achat €", "Fret €", "Douane €", "TOTAL COÛT",
           "Prix LBC", "Marge€ LBC", "Marge% LBC",
           "Prix VT", "Marge% VT",
           "Prix ANI CHF", "≈EUR", "Marge% ANI"]
    bd(ws, 3, 1, "Produit", bg=C_DARK, fg=C_WHITE, bold=True, align="center")
    for ci, h in enumerate(sub, 2):
        c = ws.cell(row=3, column=ci, value=h)
        c.font = Font(bold=True, size=9, color=C_WHITE)
        c.fill = PatternFill("solid", fgColor=C_DARK)
        c.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[3].height = 22

    totaux = {"achat": 0, "fret": 0, "douane": 0, "ct": 0,
              "lbc_rev": 0, "lbc_marge": 0, "vt_rev": 0, "ani_rev": 0}

    for ri, p in enumerate(MARKET, 4):
        ct = cout_total(p)
        lbc_c = prix_cible(p["lbc_med"])
        vt_c  = prix_cible(p["vt_med"])
        ani_c = prix_cible(p["ani_med"])
        ani_eur = round(ani_c * FX_CHF_EUR, 2)
        m_lbc_eur = marge(lbc_c, ct, FRAIS_LBC)
        m_lbc_pct = marge_pct(lbc_c, ct, FRAIS_LBC)
        m_vt_pct  = marge_pct(vt_c,  ct, FRAIS_VT)
        m_ani_pct = marge_pct(ani_eur, ct, FRAIS_ANI)

        bg = C_LGRAY if ri % 2 == 0 else C_WHITE
        bd(ws, ri, 1,  p["nom"],        bg=bg, bold=True, size=9)
        bd(ws, ri, 2,  p["achat"],      bg=bg, fmt="#,##0.00 €",  align="right", size=9)
        bd(ws, ri, 3,  p["fret"],       bg=bg, fmt="#,##0.00 €",  align="right", size=9)
        bd(ws, ri, 4,  p["douane"],     bg=bg, fmt="#,##0.00 €",  align="right", size=9)
        bd(ws, ri, 5,  ct,              bg="FFF9C4", fmt="#,##0.00 €", bold=True, align="right", size=9)
        bd(ws, ri, 6,  lbc_c,           bg="E8F8F5", fmt="#,##0.00 €", bold=True, align="right", size=9)
        bd(ws, ri, 7,  m_lbc_eur,       bg="E8F8F5", fmt="#,##0.00 €", bold=True, align="right", size=9)
        c_p = ws.cell(row=ri, column=8, value=m_lbc_pct/100)
        c_p.number_format = "0%"; c_p.font = Font(bold=True, color=C_WHITE, size=10)
        c_p.fill = PatternFill("solid", fgColor=C_GREEN if m_lbc_pct > 50 else C_GOLD)
        c_p.alignment = Alignment(horizontal="center", vertical="center")
        bd(ws, ri, 9,  vt_c,            bg="EAF7FB", fmt="#,##0.00 €", bold=True, align="right", size=9)
        c_pv = ws.cell(row=ri, column=10, value=m_vt_pct/100)
        c_pv.number_format = "0%"; c_pv.font = Font(bold=True, color=C_WHITE, size=10)
        c_pv.fill = PatternFill("solid", fgColor=C_GREEN if m_vt_pct > 50 else C_GOLD)
        c_pv.alignment = Alignment(horizontal="center", vertical="center")
        bd(ws, ri, 11, ani_c,           bg="FEF9E7", fmt="#,##0.00 CHF", bold=True, align="right", size=9)
        bd(ws, ri, 12, ani_eur,         bg="FEF9E7", fmt="#,##0.00 €",   align="right", size=9)
        c_pa = ws.cell(row=ri, column=13, value=m_ani_pct/100)
        c_pa.number_format = "0%"; c_pa.font = Font(bold=True, color=C_WHITE, size=10)
        c_pa.fill = PatternFill("solid", fgColor=C_GREEN if m_ani_pct > 50 else C_GOLD)
        c_pa.alignment = Alignment(horizontal="center", vertical="center")
        ws.row_dimensions[ri].height = 26

        totaux["achat"]    += p["achat"]
        totaux["fret"]     += p["fret"]
        totaux["douane"]   += p["douane"]
        totaux["ct"]       += ct
        totaux["lbc_rev"]  += lbc_c
        totaux["lbc_marge"]+= m_lbc_eur
        totaux["vt_rev"]   += vt_c
        totaux["ani_rev"]  += ani_eur

    # Ligne totale
    tr = 4 + len(MARKET) + 1
    ws.merge_cells(f"A{tr}:A{tr}")
    hd(ws, tr, 1,  "TOTAL (1 pièce chaque)",  C_DARK, C_WHITE, size=10)
    hd(ws, tr, 2,  totaux["achat"],           C_DARK, C_WHITE, size=10)
    hd(ws, tr, 3,  totaux["fret"],            C_DARK, C_WHITE, size=10)
    hd(ws, tr, 4,  totaux["douane"],          C_DARK, C_WHITE, size=10)
    hd(ws, tr, 5,  totaux["ct"],              C_ACC,  C_WHITE, size=10)
    hd(ws, tr, 6,  totaux["lbc_rev"],         C_GREEN, C_WHITE, size=10)
    hd(ws, tr, 7,  totaux["lbc_marge"],       C_GREEN, C_WHITE, size=10)
    for ci in [8, 10, 13]:
        ws.cell(row=tr, column=ci).fill = PatternFill("solid", fgColor=C_DARK)
    hd(ws, tr, 9,  totaux["vt_rev"],          C_GREEN, C_WHITE, size=10)
    hd(ws, tr, 11, totaux["ani_rev"],         C_GREEN, C_WHITE, size=10)
    for ci2, fmt in [(2,"#,##0.00 €"),(3,"#,##0.00 €"),(4,"#,##0.00 €"),
                     (5,"#,##0.00 €"),(6,"#,##0.00 €"),(7,"#,##0.00 €"),
                     (9,"#,##0.00 €"),(11,"#,##0.00 €")]:
        ws.cell(row=tr, column=ci2).number_format = fmt
    ws.row_dimensions[tr].height = 28
    apply_borders(ws, 3, tr, 1, 13)

# ── SHEET 5 : PLAN D'ACTION ────────────────────────────────────────────────
def make_plan(wb):
    ws = wb.create_sheet("PLAN D'ACTION")
    ws.sheet_properties.tabColor = "E94560"

    ws.column_dimensions["A"].width = 8
    ws.column_dimensions["B"].width = 22
    ws.column_dimensions["C"].width = 55
    ws.column_dimensions["D"].width = 22
    ws.column_dimensions["E"].width = 18

    ws.merge_cells("A1:E1")
    hd(ws, 1, 1, "PLAN D'ACTION — MISE EN LIGNE OPTIMISÉE SEMAINE 1",
       C_ACC, C_WHITE, size=14)
    ws.row_dimensions[1].height = 30

    steps = [
        # (Étape, Titre, Détail, Plateforme, Délai)
        ("1", "Commander sur 1688/Alibaba",
         "Chercher : 'TWS Bluetooth 5.3 earbuds OEM', 'AMOLED smartwatch 1.43 bluetooth call', "
         "'20000mAh power bank USB-C 22.5W', 'LED string lights USB 10m 100LED'.\n"
         "Budget : ~383€ pour 20×TWS + 10×Watch + 15×PB + 30×LED. "
         "Délai livraison : 15–25 jours.",
         "1688 / Alibaba", "Aujourd'hui"),
        ("2", "Créer les comptes vendeurs",
         "LeBonCoin : compte perso (gratuit). Vinted : compte, vérifier identité, ajouter IBAN. "
         "Anibis.ch : compte gratuit.\n"
         "Installer les apps mobiles pour répondre vite aux acheteurs.",
         "LBC + Vinted + Anibis", "Aujourd'hui"),
        ("3", "Prendre les photos produits",
         "Fond blanc (drap, mur). Lumière naturelle ou lampe ring.\n"
         "Chaque produit : 3 photos min. (face, côté, contenu emballage ouvert).\n"
         "Guirlande LED : allumée dans une pièce sombre — photo la plus importante.",
         "Toutes plateformes", "Dès réception"),
        ("4", "Poster les annonces LeBonCoin",
         "Copier les titres et descriptions de l'onglet 'ANNONCES OPTIMISÉES'.\n"
         "Mettre le prix cible (colonne 'CIBLE VENTE' onglet RÉSUMÉ).\n"
         "Livraison : activer Colissimo + Mondial Relay.\n"
         "Répondre aux messages sous 2h max — l'algorithme LBC récompense la réactivité.",
         "LeBonCoin", "Dès réception"),
        ("5", "Poster les annonces Vinted",
         "Même titres/descriptions (onglet ANNONCES). Prix cible VT.\n"
         "Activer 'Expédition Vinted' (Mondial Relay prépayé — simple).\n"
         "Poster tôt le matin (7h–9h) ou en soirée (20h–22h) — pics de trafic.\n"
         "Rafraîchir ('Remettre en avant') les annonces toutes les 48h.",
         "Vinted", "Dès réception"),
        ("6", "Poster les annonces Anibis.ch",
         "Copier les titres ANI (onglet ANNONCES). Prix en CHF (colonne CIBLE ANI).\n"
         "Sélectionner région : Genève / Vaud / tout pays.\n"
         "La clientèle suisse paie plus cher — priorité sur les gros lots.",
         "Anibis.ch", "Dès réception"),
        ("7", "Suivre & optimiser",
         "Si pas de vente sous 5 jours → baisser le prix de 5% et changer la photo principale.\n"
         "Regarder les annonces concurrentes chaque semaine pour ajuster.\n"
         "Nota : la guirlande LED a la rotation la plus rapide — en commander +50 au 2e lot.",
         "Toutes", "En continu"),
        ("8", "Déclarer les revenus",
         "Seuil légal France : 3 000€/an OU 20 transactions → déclaration auto-entrepreneur.\n"
         "Garder les factures 1688/Alibaba pour justifier les achats.\n"
         "Vinted/LBC reportent automatiquement à l'administration fiscale au-dessus des seuils.",
         "Légal / Fiscal", "Dès > 3000€"),
    ]

    for ci, h in enumerate(["#", "Étape", "Détail", "Plateforme", "Quand"], 1):
        hd(ws, 2, ci, h, C_DARK, C_WHITE, size=10)
    ws.row_dimensions[2].height = 22

    colors = [C_BLUE, C_TEAL, "1F5C3A", "4A235A", C_BLUE, C_TEAL, "7E5109", "922B21"]
    for ri, (num, titre, detail, plat, quand) in enumerate(steps, 3):
        bg = colors[(ri-3) % len(colors)]
        hd(ws, ri, 1, num,   bg=bg, size=14)
        hd(ws, ri, 2, titre, bg=bg, size=10, align="left")
        bd(ws, ri, 3, detail, wrap=True, size=9, align="left")
        bd(ws, ri, 4, plat,  bg="EDF2F4", align="center", size=9, bold=True)
        c_q = ws.cell(row=ri, column=5, value=quand)
        c_q.font = Font(bold=True, size=9, color=C_WHITE)
        c_q.fill = PatternFill("solid", fgColor=C_GREEN if "Aujourd" in quand else C_GOLD if "réception" in quand else "888888")
        c_q.alignment = Alignment(horizontal="center", vertical="center")
        ws.row_dimensions[ri].height = 60

    apply_borders(ws, 2, 2+len(steps), 1, 5)

# ── MAIN ─────────────────────────────────────────────────────────────────────
def main():
    wb = Workbook()
    wb.remove(wb.active)

    make_resume(wb)
    make_detail(wb)
    make_annonces(wb)
    make_marge(wb)
    make_plan(wb)

    out = "/home/user/Optimisation_Prix_Meilleurs_Vendeurs.xlsx"
    wb.save(out)
    print(f"✅ Fichier généré : {out}")

    # Afficher le résumé dans le terminal
    print("\n" + "="*65)
    print("RÉSUMÉ — PRIX CIBLES PAR PRODUIT (médiane concurrents × 91%)")
    print("="*65)
    print(f"{'Produit':<30} {'Coût €':>7} | {'LBC €':>7} {'VT €':>7} {'ANI CHF':>8} | {'Marge%':>7}")
    print("-"*65)
    for p in MARKET:
        ct   = cout_total(p)
        lbc  = prix_cible(p["lbc_med"])
        vt   = prix_cible(p["vt_med"])
        ani  = prix_cible(p["ani_med"])
        mp   = marge_pct(lbc, ct, FRAIS_LBC)
        print(f"{p['nom']:<30} {ct:>7.2f} | {lbc:>7.2f} {vt:>7.2f} {ani:>8.2f} | {mp:>6.0f}%")
    print("="*65)
    print("\nNote : Anibis en CHF (marché suisse — prix plus élevés)")
    print(f"Taux de change : 1 CHF = {FX_CHF_EUR:.3f} EUR (juin 2026)")

if __name__ == "__main__":
    main()
