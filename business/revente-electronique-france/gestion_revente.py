"""
Générateur du fichier Excel de gestion de revente d'air fryers.
"""
import openpyxl
from openpyxl.styles import (
    Font, PatternFill, Alignment, Border, Side, numbers
)
from openpyxl.styles.numbers import FORMAT_NUMBER_COMMA_SEPARATED1
from openpyxl.utils import get_column_letter
from openpyxl.formatting.rule import ColorScaleRule, DataBarRule
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.chart import BarChart, Reference
from openpyxl.chart.series import SeriesLabel

# ── Palette ───────────────────────────────────────────────────────────────────
C_HEADER_BG   = "1F3864"   # bleu foncé
C_HEADER_FG   = "FFFFFF"
C_SUB_BG      = "2E75B6"   # bleu moyen
C_ALT_ROW     = "DCE6F1"   # bleu très clair
C_GREEN       = "70AD47"
C_RED         = "FF0000"
C_ORANGE      = "ED7D31"
C_YELLOW_BG   = "FFF2CC"
C_LIGHT_GREEN = "E2EFDA"
C_BORDER      = "B8CCE4"

EUR = '#,##0.00 "€"'
PCT = '0.00"%"'

def border(color=C_BORDER):
    s = Side(style="thin", color=color)
    return Border(left=s, right=s, top=s, bottom=s)

def hdr(ws, row, col, text, bg=C_HEADER_BG, fg=C_HEADER_FG, bold=True, size=11):
    c = ws.cell(row=row, column=col, value=text)
    c.font = Font(name="Calibri", bold=bold, color=fg, size=size)
    c.fill = PatternFill("solid", fgColor=bg)
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    c.border = border()
    return c

def data_cell(ws, row, col, value=None, fmt=None, bold=False, bg=None, align="left"):
    c = ws.cell(row=row, column=col, value=value)
    c.font = Font(name="Calibri", bold=bold, size=10)
    c.alignment = Alignment(horizontal=align, vertical="center")
    c.border = border()
    if fmt:
        c.number_format = fmt
    if bg:
        c.fill = PatternFill("solid", fgColor=bg)
    return c

def set_col_width(ws, widths: dict):
    for col_letter, w in widths.items():
        ws.column_dimensions[col_letter].width = w

def freeze(ws, cell="A2"):
    ws.freeze_panes = cell

# ══════════════════════════════════════════════════════════════════════════════
# FEUILLE 1 — STOCK
# ══════════════════════════════════════════════════════════════════════════════
def make_stock(wb):
    ws = wb.create_sheet("📦 STOCK")
    ws.sheet_view.showGridLines = False
    ws.row_dimensions[1].height = 30

    headers = [
        ("A", "ID",             10),
        ("B", "Produit",        28),
        ("C", "Date achat",     14),
        ("D", "Fournisseur",    18),
        ("E", "Prix achat (€)", 16),
        ("F", "Frais transport\n(€ total)", 18),
        ("G", "Qté achetée",   13),
        ("H", "Coût unitaire\ntotal (€)", 18),
        ("I", "Qté vendue",    13),
        ("J", "Stock dispo",   13),
        ("K", "Valeur stock\n(€)", 16),
        ("L", "Notes",         30),
    ]
    for col_letter, label, width in headers:
        col = ord(col_letter) - ord("A") + 1
        hdr(ws, 1, col, label)
        ws.column_dimensions[col_letter].width = width

    # 10 lignes d'exemple (air fryer Ninja)
    example = [
        (1, "Ninja AF100EU Air Fryer 4L",  "2026-06-20", "1688.com", 28.50, 45.00, 10),
    ]
    for r_offset, row in enumerate(example):
        r = r_offset + 2
        alt = C_ALT_ROW if r_offset % 2 == 0 else None
        aid, produit, date_achat, fourn, prix_achat, frais_total, qty_achetee = row
        data_cell(ws, r, 1, aid, align="center", bg=alt)
        data_cell(ws, r, 2, produit, bg=alt)
        data_cell(ws, r, 3, date_achat, bg=alt)
        data_cell(ws, r, 4, fourn, bg=alt)
        data_cell(ws, r, 5, prix_achat, fmt=EUR, bg=alt)
        data_cell(ws, r, 6, frais_total, fmt=EUR, bg=alt)
        data_cell(ws, r, 7, qty_achetee, align="center", bg=alt)
        # H = coût unitaire total = (prix_achat * qté + frais) / qté
        c = data_cell(ws, r, 8, None, fmt=EUR, bold=True, bg=alt)
        c.value = f"=(E{r}*G{r}+F{r})/G{r}"
        # I = qté vendue (saisie manuelle) — préremplie à 0
        data_cell(ws, r, 9, 0, align="center", bg=alt)
        # J = stock dispo
        c = data_cell(ws, r, 10, None, align="center", bg=alt, bold=True)
        c.value = f"=G{r}-I{r}"
        c.font = Font(name="Calibri", bold=True, color=C_HEADER_BG, size=10)
        # K = valeur stock
        c = data_cell(ws, r, 11, None, fmt=EUR, bg=alt)
        c.value = f"=J{r}*H{r}"
        data_cell(ws, r, 12, "", bg=alt)

    # Laisser 19 lignes vides prêtes
    for r in range(len(example) + 2, len(example) + 22):
        r_offset = r - 2
        alt = C_ALT_ROW if r_offset % 2 == 0 else None
        next_id = r - 1
        data_cell(ws, r, 1, next_id, align="center", bg=alt)
        for col in range(2, 13):
            data_cell(ws, r, col, None, bg=alt)
        # formules dans les colonnes calculées
        data_cell(ws, r, 8, None, fmt=EUR, bg=alt).value = f"=IF(G{r}=0,0,(E{r}*G{r}+F{r})/G{r})"
        data_cell(ws, r, 9, 0, align="center", bg=alt)
        c = data_cell(ws, r, 10, None, align="center", bold=True, bg=alt)
        c.value = f"=G{r}-I{r}"
        c.font = Font(name="Calibri", bold=True, color=C_HEADER_BG, size=10)
        c = data_cell(ws, r, 11, None, fmt=EUR, bg=alt)
        c.value = f"=J{r}*H{r}"

    freeze(ws, "A2")
    ws.auto_filter.ref = f"A1:L{len(example)+21}"

# ══════════════════════════════════════════════════════════════════════════════
# FEUILLE 2 — CLIENTS
# ══════════════════════════════════════════════════════════════════════════════
def make_clients(wb):
    ws = wb.create_sheet("👥 CLIENTS")
    ws.sheet_view.showGridLines = False
    ws.row_dimensions[1].height = 30

    headers = [
        ("A", "ID Client",    12),
        ("B", "Nom",          18),
        ("C", "Prénom",       18),
        ("D", "Téléphone",    16),
        ("E", "Email",        28),
        ("F", "Adresse",      35),
        ("G", "Code postal",  14),
        ("H", "Ville",        20),
        ("I", "Pays",         14),
        ("J", "Plateforme\ncontact", 16),
        ("K", "Nb commandes", 14),
        ("L", "Total dépensé\n(€)", 16),
        ("M", "Notes",        30),
    ]
    for col_letter, label, width in headers:
        col = ord(col_letter) - ord("A") + 1
        hdr(ws, 1, col, label)
        ws.column_dimensions[col_letter].width = width

    # Validation plateforme
    dv = DataValidation(
        type="list",
        formula1='"Vinted,Le Bon Coin,Anibis,Direct,Autre"',
        allow_blank=True
    )
    ws.add_data_validation(dv)
    dv.sqref = "J2:J200"

    # Un client exemple
    example = [
        (1, "Dupont", "Marie", "+33 6 12 34 56 78", "marie.dupont@email.fr",
         "12 rue des Lilas", "74000", "Annecy", "France", "Vinted"),
    ]
    for r_offset, row in enumerate(example):
        r = r_offset + 2
        alt = C_ALT_ROW if r_offset % 2 == 0 else None
        for col, val in enumerate(row, 1):
            data_cell(ws, r, col, val, bg=alt)
        # K = nb commandes (formule COUNTIF sur COMMANDES)
        c = data_cell(ws, r, 11, None, align="center", bold=True, bg=alt)
        c.value = f"=COUNTIF('📋 COMMANDES'!B:B,A{r})"
        # L = total dépensé
        c = data_cell(ws, r, 12, None, fmt=EUR, bold=True, bg=alt)
        c.value = f"=SUMIF('📋 COMMANDES'!B:B,A{r},'📋 COMMANDES'!G:G)"
        data_cell(ws, r, 13, "", bg=alt)

    for r in range(len(example) + 2, len(example) + 52):
        r_offset = r - 2
        alt = C_ALT_ROW if r_offset % 2 == 0 else None
        next_id = r - 1
        data_cell(ws, r, 1, next_id, align="center", bg=alt)
        for col in range(2, 14):
            data_cell(ws, r, col, None, bg=alt)
        c = data_cell(ws, r, 11, None, align="center", bold=True, bg=alt)
        c.value = f"=COUNTIF('📋 COMMANDES'!B:B,A{r})"
        c = data_cell(ws, r, 12, None, fmt=EUR, bold=True, bg=alt)
        c.value = f"=SUMIF('📋 COMMANDES'!B:B,A{r},'📋 COMMANDES'!G:G)"

    freeze(ws, "A2")
    ws.auto_filter.ref = f"A1:M{len(example)+51}"

# ══════════════════════════════════════════════════════════════════════════════
# FEUILLE 3 — COMMANDES
# ══════════════════════════════════════════════════════════════════════════════
def make_commandes(wb):
    ws = wb.create_sheet("📋 COMMANDES")
    ws.sheet_view.showGridLines = False
    ws.row_dimensions[1].height = 30

    headers = [
        ("A", "ID Cmd",        9),
        ("B", "ID Client",    10),
        ("C", "Nom client",   20),
        ("D", "Date vente",   13),
        ("E", "Produit",      28),
        ("F", "Plateforme",   14),
        ("G", "Prix vente\n(€)", 14),
        ("H", "Frais\nplateforme (€)", 16),
        ("I", "Prix net\nreçu (€)", 14),
        ("J", "Coût achat\nunitaire (€)", 16),
        ("K", "Marge\n(€)", 12),
        ("L", "Marge\n(%)", 12),
        ("M", "Statut\npaiement", 14),
        ("N", "Statut\nlivraison", 14),
        ("O", "Adresse livraison", 35),
        ("P", "N° suivi", 20),
        ("Q", "Notes", 25),
    ]
    for col_letter, label, width in headers:
        col = ord(col_letter) - ord("A") + 1
        hdr(ws, 1, col, label)
        ws.column_dimensions[col_letter].width = width

    # Validations
    dv_plat = DataValidation(type="list",
        formula1='"Vinted,Le Bon Coin,Anibis,Direct,Autre"', allow_blank=True)
    dv_pay = DataValidation(type="list",
        formula1='"Payé,En attente,Remboursé"', allow_blank=True)
    dv_liv = DataValidation(type="list",
        formula1='"Livré,En cours,Expédié,Annulé"', allow_blank=True)
    ws.add_data_validation(dv_plat)
    ws.add_data_validation(dv_pay)
    ws.add_data_validation(dv_liv)
    dv_plat.sqref = "F2:F500"
    dv_pay.sqref  = "M2:M500"
    dv_liv.sqref  = "N2:N500"

    # Frais plateforme par défaut: Vinted=5%, LBC=0%, Anibis=0%
    # On laisse la saisie manuelle mais on prépare la formule
    example = [
        (1, 1, "Dupont Marie", "2026-06-25", "Ninja AF100EU Air Fryer 4L",
         "Vinted", 89.00, 4.45, None, None, None, None,
         "Payé", "Livré",
         "12 rue des Lilas, 74000 Annecy", "1Z999AA10123456784", ""),
    ]
    for r_offset, row in enumerate(example):
        r = r_offset + 2
        alt = C_ALT_ROW if r_offset % 2 == 0 else None
        (cmd_id, cli_id, cli_nom, date_v, produit, plat,
         prix_vente, frais_plat, _, _, _, _,
         stat_pay, stat_liv, adresse, suivi, notes) = row

        data_cell(ws, r, 1, cmd_id, align="center", bg=alt)
        data_cell(ws, r, 2, cli_id, align="center", bg=alt)
        data_cell(ws, r, 3, cli_nom, bg=alt)
        data_cell(ws, r, 4, date_v, bg=alt)
        data_cell(ws, r, 5, produit, bg=alt)
        data_cell(ws, r, 6, plat, align="center", bg=alt)
        data_cell(ws, r, 7, prix_vente, fmt=EUR, bg=alt)
        data_cell(ws, r, 8, frais_plat, fmt=EUR, bg=alt)
        # I = prix net
        c = data_cell(ws, r, 9, None, fmt=EUR, bg=alt)
        c.value = f"=G{r}-H{r}"
        # J = coût achat (lookup dans STOCK, simplifié: saisie manuelle)
        data_cell(ws, r, 10, 33.00, fmt=EUR, bg=alt)
        # K = marge €
        c = data_cell(ws, r, 11, None, fmt=EUR, bold=True, bg=alt)
        c.value = f"=I{r}-J{r}"
        c.font = Font(name="Calibri", bold=True, size=10)
        # L = marge %
        c = data_cell(ws, r, 12, None, fmt=PCT, bold=True, bg=alt)
        c.value = f"=IF(G{r}=0,0,K{r}/G{r}*100)"
        c.font = Font(name="Calibri", bold=True, size=10)

        data_cell(ws, r, 13, stat_pay, align="center", bg=alt)
        data_cell(ws, r, 14, stat_liv, align="center", bg=alt)
        data_cell(ws, r, 15, adresse, bg=alt)
        data_cell(ws, r, 16, suivi, bg=alt)
        data_cell(ws, r, 17, notes, bg=alt)

    for r in range(len(example) + 2, len(example) + 202):
        r_offset = r - 2
        alt = C_ALT_ROW if r_offset % 2 == 0 else None
        data_cell(ws, r, 1, r - 1, align="center", bg=alt)
        for col in [2, 3, 4, 5, 6, 7, 8, 10, 13, 14, 15, 16, 17]:
            data_cell(ws, r, col, None, bg=alt)
        c = data_cell(ws, r, 9, None, fmt=EUR, bg=alt)
        c.value = f"=IF(G{r}=0,\"\",G{r}-H{r})"
        c = data_cell(ws, r, 11, None, fmt=EUR, bold=True, bg=alt)
        c.value = f"=IF(G{r}=0,\"\",I{r}-J{r})"
        c.font = Font(name="Calibri", bold=True, size=10)
        c = data_cell(ws, r, 12, None, fmt=PCT, bold=True, bg=alt)
        c.value = f"=IF(G{r}=0,\"\",K{r}/G{r}*100)"
        c.font = Font(name="Calibri", bold=True, size=10)

    # Mise en forme conditionnelle couleur sur marge %
    from openpyxl.formatting.rule import ColorScaleRule
    color_rule = ColorScaleRule(
        start_type="num", start_value=0,  start_color="FF0000",
        mid_type="num",   mid_value=20,   mid_color="FFFF00",
        end_type="num",   end_value=50,   end_color="70AD47",
    )
    ws.conditional_formatting.add(f"L2:L{len(example)+201}", color_rule)

    freeze(ws, "A2")
    ws.auto_filter.ref = f"A1:Q{len(example)+201}"

# ══════════════════════════════════════════════════════════════════════════════
# FEUILLE 4 — TABLEAU DE BORD
# ══════════════════════════════════════════════════════════════════════════════
def make_dashboard(wb):
    ws = wb.create_sheet("📊 TABLEAU DE BORD")
    ws.sheet_view.showGridLines = False

    def title(r, c, text, span=4, bg=C_HEADER_BG):
        cell = ws.cell(row=r, column=c, value=text)
        cell.font = Font(name="Calibri", bold=True, color="FFFFFF", size=14)
        cell.fill = PatternFill("solid", fgColor=bg)
        cell.alignment = Alignment(horizontal="center", vertical="center")
        ws.merge_cells(start_row=r, start_column=c, end_row=r, end_column=c + span - 1)
        ws.row_dimensions[r].height = 32

    def kpi(ws, row, col, label, formula, fmt=EUR, color=C_HEADER_BG):
        lc = ws.cell(row=row, column=col, value=label)
        lc.font = Font(name="Calibri", bold=True, color="666666", size=9)
        lc.alignment = Alignment(horizontal="center")
        lc.fill = PatternFill("solid", fgColor="F2F2F2")
        lc.border = border()

        vc = ws.cell(row=row + 1, column=col, value=formula)
        vc.font = Font(name="Calibri", bold=True, color=color, size=20)
        vc.alignment = Alignment(horizontal="center", vertical="center")
        vc.fill = PatternFill("solid", fgColor="FFFFFF")
        vc.border = border()
        vc.number_format = fmt
        ws.row_dimensions[row + 1].height = 40

    # ── Titre principal
    ws.merge_cells("A1:H1")
    t = ws["A1"]
    t.value = "🛒  GESTION REVENTE — AIR FRYER NINJA"
    t.font = Font(name="Calibri", bold=True, color="FFFFFF", size=18)
    t.fill = PatternFill("solid", fgColor=C_HEADER_BG)
    t.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 40

    # ── KPI ligne 3-4
    title(3, 1, "PERFORMANCES GLOBALES", span=8)

    kpi(ws, 4, 1, "VENTES TOTALES",
        "=COUNTA('📋 COMMANDES'!A2:A500)-COUNTBLANK('📋 COMMANDES'!A2:A500)",
        fmt="0", color=C_SUB_BG)
    kpi(ws, 4, 2, "CHIFFRE D'AFFAIRES",
        "=SUMIF('📋 COMMANDES'!M2:M500,\"Payé\",'📋 COMMANDES'!G2:G500)",
        color=C_GREEN)
    kpi(ws, 4, 3, "MARGE TOTALE",
        "=SUMIF('📋 COMMANDES'!M2:M500,\"Payé\",'📋 COMMANDES'!K2:K500)",
        color=C_GREEN)
    kpi(ws, 4, 4, "MARGE MOYENNE PAR VENTE",
        "=IFERROR(AVERAGEIF('📋 COMMANDES'!M2:M500,\"Payé\",'📋 COMMANDES'!K2:K500),0)",
        color=C_ORANGE)
    kpi(ws, 4, 5, "MARGE MOYENNE %",
        "=IFERROR(AVERAGEIF('📋 COMMANDES'!M2:M500,\"Payé\",'📋 COMMANDES'!L2:L500),0)",
        fmt=PCT, color=C_ORANGE)
    kpi(ws, 4, 6, "STOCK RESTANT",
        "=SUMIF('📦 STOCK'!B2:B50,\"Ninja AF100EU Air Fryer 4L\",'📦 STOCK'!J2:J50)",
        fmt="0 unités", color=C_RED)
    kpi(ws, 4, 7, "EN ATTENTE LIVRAISON",
        "=COUNTIF('📋 COMMANDES'!N2:N500,\"En cours\")+COUNTIF('📋 COMMANDES'!N2:N500,\"Expédié\")",
        fmt="0", color=C_ORANGE)
    kpi(ws, 4, 8, "VALEUR STOCK",
        "=SUM('📦 STOCK'!K2:K50)",
        color=C_SUB_BG)

    # ── Séparateur
    for c in range(1, 9):
        ws.row_dimensions[6].height = 10
        ws.cell(row=6, column=c).fill = PatternFill("solid", fgColor="FFFFFF")

    # ── Stats par plateforme
    title(7, 1, "PAR PLATEFORME", span=4, bg=C_SUB_BG)
    title(7, 5, "ESTIMATION HEBDOMADAIRE", span=4, bg=C_SUB_BG)

    plat_headers = ["Plateforme", "Nb ventes", "CA (€)", "Marge (€)"]
    for i, h in enumerate(plat_headers):
        hdr(ws, 8, i + 1, h, bg=C_SUB_BG)
    plateformes = ["Vinted", "Le Bon Coin", "Anibis", "Direct"]
    for r_offset, plat in enumerate(plateformes):
        r = 9 + r_offset
        alt = C_ALT_ROW if r_offset % 2 == 0 else None
        data_cell(ws, r, 1, plat, bold=True, bg=alt)
        c = data_cell(ws, r, 2, None, align="center", bg=alt)
        c.value = f'=COUNTIF(\'📋 COMMANDES\'!F2:F500,"{plat}")'
        c = data_cell(ws, r, 3, None, fmt=EUR, bg=alt)
        c.value = (f'=SUMPRODUCT((\'📋 COMMANDES\'!F2:F500="{plat}")*'
                   f'(\'📋 COMMANDES\'!M2:M500="Payé")*\'📋 COMMANDES\'!G2:G500)')
        c = data_cell(ws, r, 4, None, fmt=EUR, bold=True, bg=alt)
        c.value = (f'=SUMPRODUCT((\'📋 COMMANDES\'!F2:F500="{plat}")*'
                   f'(\'📋 COMMANDES\'!M2:M500="Payé")*\'📋 COMMANDES\'!K2:K500)')

    # ── Estimation hebdomadaire (colonne 5-8)
    hdr_hebdo = ["Indicateur", "Cette semaine", "Moy. / semaine", "Objectif"]
    for i, h in enumerate(hdr_hebdo):
        hdr(ws, 8, i + 5, h, bg=C_SUB_BG)

    hebdo_rows = [
        ("Ventes",    '=COUNTIFS(\'📋 COMMANDES\'!D2:D500,">="&(TODAY()-WEEKDAY(TODAY(),2)+1),\'📋 COMMANDES\'!D2:D500,"<="&(TODAY()-WEEKDAY(TODAY(),2)+7))', "0",    5,  "0"),
        ("CA (€)",    '=SUMPRODUCT((\'📋 COMMANDES\'!D2:D500>=(TODAY()-WEEKDAY(TODAY(),2)+1))*(\'📋 COMMANDES\'!D2:D500<=(TODAY()-WEEKDAY(TODAY(),2)+7))*(\'📋 COMMANDES\'!M2:M500="Payé")*\'📋 COMMANDES\'!G2:G500)', EUR, 400, EUR),
        ("Marge (€)", '=SUMPRODUCT((\'📋 COMMANDES\'!D2:D500>=(TODAY()-WEEKDAY(TODAY(),2)+1))*(\'📋 COMMANDES\'!D2:D500<=(TODAY()-WEEKDAY(TODAY(),2)+7))*(\'📋 COMMANDES\'!M2:M500="Payé")*\'📋 COMMANDES\'!K2:K500)', EUR, 200, EUR),
    ]
    for r_offset, (label, formula, fmt, objectif, obj_fmt) in enumerate(hebdo_rows):
        r = 9 + r_offset
        alt = C_ALT_ROW if r_offset % 2 == 0 else None
        data_cell(ws, r, 5, label, bold=True, bg=alt)
        c = data_cell(ws, r, 6, None, fmt=fmt, bold=True, bg=alt)
        c.value = formula
        # Moy semaine = total / nb semaines depuis début
        c = data_cell(ws, r, 7, None, fmt=fmt, bg=alt)
        c.value = "—"
        c = data_cell(ws, r, 8, objectif, fmt=obj_fmt, bold=True,
                      bg=C_LIGHT_GREEN if r_offset % 2 == 0 else C_YELLOW_BG)

    # ── Largeurs colonnes
    for col_letter, w in [
        ("A", 22), ("B", 14), ("C", 16), ("D", 16),
        ("E", 22), ("F", 18), ("G", 18), ("H", 14),
    ]:
        ws.column_dimensions[col_letter].width = w

    # ── Note bas de page
    r_note = 15
    ws.row_dimensions[r_note].height = 20
    note = ws.cell(row=r_note, column=1,
                   value="ℹ️  Saisissez vos commandes dans '📋 COMMANDES' et votre stock dans '📦 STOCK' — ce tableau se met à jour automatiquement.")
    note.font = Font(name="Calibri", italic=True, color="666666", size=9)
    ws.merge_cells(f"A{r_note}:H{r_note}")

# ══════════════════════════════════════════════════════════════════════════════
# FEUILLE 5 — GUIDE D'UTILISATION
# ══════════════════════════════════════════════════════════════════════════════
def make_guide(wb):
    ws = wb.create_sheet("📖 GUIDE")
    ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 5
    ws.column_dimensions["B"].width = 30
    ws.column_dimensions["C"].width = 60

    ws.merge_cells("A1:C1")
    t = ws["A1"]
    t.value = "📖  GUIDE D'UTILISATION — GESTION REVENTE AIR FRYER NINJA"
    t.font = Font(name="Calibri", bold=True, color="FFFFFF", size=16)
    t.fill = PatternFill("solid", fgColor=C_HEADER_BG)
    t.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 36

    steps = [
        ("", "", ""),
        ("1️⃣", "STOCK — Premier achat",
         "Allez dans '📦 STOCK'. Remplissez : Produit, Date achat, Fournisseur (1688.com), Prix achat unitaire en €, Frais de transport total, Quantité achetée. Le coût unitaire total se calcule automatiquement."),
        ("", "", ""),
        ("2️⃣", "CLIENTS — Enregistrer un acheteur",
         "Allez dans '👥 CLIENTS'. Remplissez : Nom, Prénom, Téléphone, Email, Adresse complète, Code postal, Ville, Pays, et la plateforme où vous avez vendu (Vinted / Le Bon Coin / Anibis). Le nombre de commandes et total dépensé se calculent automatiquement."),
        ("", "", ""),
        ("3️⃣", "COMMANDES — Saisir une vente",
         "Allez dans '📋 COMMANDES'. Remplissez : ID Client (doit correspondre à un ID dans CLIENTS), Nom client, Date de vente, Produit vendu, Plateforme, Prix de vente, Frais plateforme (ex: 5% sur Vinted = prix × 0.05), Coût achat unitaire (colonne J — trouvez-le dans STOCK colonne H), Adresse de livraison, N° de suivi. La marge se calcule automatiquement."),
        ("", "", ""),
        ("4️⃣", "TABLEAU DE BORD — Suivi automatique",
         "Le tableau de bord '📊 TABLEAU DE BORD' se met à jour seul. Vous y voyez : CA total, marge totale, marge par plateforme, stock restant, commandes en cours de livraison, et les ventes de la semaine en cours."),
        ("", "", ""),
        ("💡", "FRAIS DE PLATEFORME",
         "Vinted : ~5% du prix de vente (ex: 89€ × 5% = 4.45€)\nLe Bon Coin : gratuit pour particuliers\nAnibis : gratuit jusqu'à 5 annonces/mois"),
        ("", "", ""),
        ("💡", "FRAIS DE DOUANE",
         "Import depuis la Chine (1688.com) : TVA 20% + droits de douane ~3.7% sur électroménager. Un transitaire (ex: Superbuy) gère ça pour vous."),
        ("", "", ""),
        ("⚠️", "EXEMPLE DE CALCUL",
         "Air fryer à 28.50€ sur 1688 + 4.50€ frais transport = 33€ coût unitaire\nVendu 89€ sur Vinted - 4.45€ frais = 84.55€ net\nMarge = 84.55 - 33 = 51.55€ soit 57.9% de marge"),
    ]

    for r_offset, (num, label, desc) in enumerate(steps):
        r = r_offset + 2
        ws.row_dimensions[r].height = 18 if desc else 8

        c1 = ws.cell(row=r, column=1, value=num)
        c1.font = Font(name="Calibri", bold=True, size=12)
        c1.alignment = Alignment(horizontal="center", vertical="center")

        c2 = ws.cell(row=r, column=2, value=label)
        c2.font = Font(name="Calibri", bold=True, color=C_HEADER_BG, size=11)
        c2.alignment = Alignment(vertical="center")

        c3 = ws.cell(row=r, column=3, value=desc)
        c3.font = Font(name="Calibri", size=10)
        c3.alignment = Alignment(vertical="center", wrap_text=True)

        if label:
            ws.row_dimensions[r].height = max(18, len(desc) // 3)
            bg = C_ALT_ROW if r_offset % 4 in (0, 1) else None
            for c in [c1, c2, c3]:
                if bg:
                    c.fill = PatternFill("solid", fgColor=bg)

# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════
def main():
    wb = openpyxl.Workbook()
    # Supprimer la feuille par défaut
    wb.remove(wb.active)

    make_dashboard(wb)
    make_stock(wb)
    make_clients(wb)
    make_commandes(wb)
    make_guide(wb)

    # Mettre le tableau de bord en premier
    wb.active = wb["📊 TABLEAU DE BORD"]

    out = "/home/user/Gestion_Revente_AirFryer.xlsx"
    wb.save(out)
    print(f"✅ Fichier créé : {out}")

if __name__ == "__main__":
    main()
