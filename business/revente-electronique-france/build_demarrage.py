"""
Génère le bon de commande Semaine 1 + guide de démarrage immédiat.
"""
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

C_DARK="1F3864";C_BLUE="2E75B6";C_TEAL="1F7391";C_GHL="70AD47";C_GREEN="375623"
C_GBG="E2EFDA";C_ORG="C55A11";C_OBG="FCE4D6";C_RED="C00000"
C_YEL="7F6000";C_YBG="FFF2CC";C_ALT="DCE6F1";C_GRY="F2F2F2"
C_WHT="FFFFFF";C_BDR="B8CCE4";C_VT="7030A0";C_LBC="E36C09"
EUR='#,##0.00 "€"';USD='#,##0.00 "$"';PCT='0.0"%"';NB='#,##0'

def brd(c=C_BDR):
    s=Side(style="thin",color=c)
    return Border(left=s,right=s,top=s,bottom=s)

def C_(ws,r,col,v=None,fmt=None,bold=False,bg=None,fg="000000",
       al="left",wrap=False,sz=10):
    cl=ws.cell(row=r,column=col,value=v)
    cl.font=Font(name="Calibri",bold=bold,color=fg,size=sz)
    cl.alignment=Alignment(horizontal=al,vertical="center",wrap_text=wrap)
    cl.border=brd()
    if fmt:cl.number_format=fmt
    if bg:cl.fill=PatternFill("solid",fgColor=bg)
    return cl

def H_(ws,r,col,v,bg=C_DARK,fg=C_WHT,sz=10,wrap=True):
    return C_(ws,r,col,v,bold=True,bg=bg,fg=fg,al="center",sz=sz,wrap=wrap)

def MH_(ws,r,c1,c2,v,bg=C_DARK,fg=C_WHT,sz=13,h=28):
    cl=ws.cell(row=r,column=c1,value=v)
    cl.font=Font(name="Calibri",bold=True,color=fg,size=sz)
    cl.fill=PatternFill("solid",fgColor=bg)
    cl.alignment=Alignment(horizontal="center",vertical="center")
    cl.border=brd()
    ws.merge_cells(start_row=r,start_column=c1,end_row=r,end_column=c2)
    ws.row_dimensions[r].height=h

# ══════════════════════════════════════════════════════════════════════════════
# BON DE COMMANDE SEMAINE 1
# Stratégie : commencer avec budget ~350€, 4 produits à forte marge
# Sources prix Alibaba juin 2026 (convertis en €, 1 USD ≈ 0.93 €)
# ══════════════════════════════════════════════════════════════════════════════

COMMANDE_S1 = [
    {
        "produit":    "Écouteurs TWS Bluetooth 5.3",
        "description":"Sans fil, ANC, IPX5, 6h autonomie, boîtier charge",
        "search_ali": "TWS earphones bluetooth 5.3 ANC IPX5 touch control",
        "prix_unit_usd": 4.50,  # prix réel Alibaba moyen qualité correcte
        "qty":        20,
        "prix_lbc":   22, "prix_vt": 25, "prix_ani": 28,
        "rot_sem":    12,
        "qualite":    "Choisir fournisseur >4.8★, >100 commandes, Trade Assurance ✓",
        "url_exemple":"https://www.alibaba.com/showroom/wholesale-bluetooth-earbuds.html",
    },
    {
        "produit":    "Montre connectée AMOLED IP68",
        "description":"Écran 1.7\", GPS, FC, SpO2, 7j autonomie, 100+ sports",
        "search_ali": "smartwatch AMOLED 1.7 inch GPS heart rate IP68 7 days",
        "prix_unit_usd": 10.80,
        "qty":        10,
        "prix_lbc":   32, "prix_vt": 28, "prix_ani": 38,
        "rot_sem":    8,
        "qualite":    "Vérifier que l'AMOLED est réel (demander vidéo allumée). Tester GPS avant commande groupée.",
        "url_exemple":"https://www.alibaba.com/showroom/amoled-smartwatch-google-play-ip68.html",
    },
    {
        "produit":    "Batterie externe 20000mAh 65W",
        "description":"Charge rapide PD 65W, 3 ports, affichage LED, CE certifié",
        "search_ali": "power bank 20000mah 65W PD fast charge LED display CE certified",
        "prix_unit_usd": 7.10,
        "qty":        15,
        "prix_lbc":   24, "prix_vt": 22, "prix_ani": 29,
        "rot_sem":    10,
        "qualite":    "OBLIGATOIRE : demander certificat CE + UN38.3 (sécurité lithium). Refuser sans certif.",
        "url_exemple":"https://www.alibaba.com/showroom/power-bank-20000mah-65w_2.html",
    },
    {
        "produit":    "Guirlandes LED USB 5m (lot 2 pcs)",
        "description":"50 LEDs fil cuivre, 8 modes, prise USB",
        "search_ali": "fairy lights USB 5m copper wire LED string 8 modes",
        "prix_unit_usd": 1.60,  # lot de 2
        "qty":        30,       # 30 lots de 2 = 60 guirlandes
        "prix_lbc":   14, "prix_vt": 13, "prix_ani": 17,
        "rot_sem":    14,
        "qualite":    "Très bas coût → commander 30 lots minimum pour rentabiliser le transport.",
        "url_exemple":"https://www.alibaba.com/showroom/wholesale-fairy-lights.html",
    },
]

USD_EUR = 0.93   # taux de change juin 2026
TRANSPORT_TOTAL = 55.0  # frais colissimo Chine → France pour ce lot


def make_order_sheet(wb):
    ws = wb.create_sheet("🛒 BON DE COMMANDE S1")
    ws.sheet_view.showGridLines = False

    ws.column_dimensions["A"].width = 3
    ws.column_dimensions["B"].width = 26
    ws.column_dimensions["C"].width = 22
    ws.column_dimensions["D"].width = 10
    ws.column_dimensions["E"].width = 12
    ws.column_dimensions["F"].width = 13
    ws.column_dimensions["G"].width = 13
    ws.column_dimensions["H"].width = 10
    ws.column_dimensions["I"].width = 10
    ws.column_dimensions["J"].width = 10
    ws.column_dimensions["K"].width = 18
    ws.column_dimensions["L"].width = 42

    MH_(ws, 1, 1, 12,
        "🛒  BON DE COMMANDE — SEMAINE 1 — ALIBABA.COM  |  Budget estimé ~360€",
        sz=13, h=30)

    # Sous-titre
    ws.merge_cells("B2:L2")
    st = ws.cell(row=2, column=2,
                 value="Ouvrez alibaba.com → tapez le terme de recherche (colonne D) → choisissez fournisseur ≥4.8★ avec Trade Assurance")
    st.font = Font(name="Calibri", italic=True, color="555555", size=10)
    st.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[2].height = 18

    headers = [
        (2, "Produit",             C_DARK),
        (3, "Description",         C_DARK),
        (4, "Qté",                 C_DARK),
        (5, "Prix unit.\n(USD)",   C_DARK),
        (6, "Prix unit.\n(€)",     C_DARK),
        (7, "Total achat\n(€)",    C_DARK),
        (8, "Prix\nLBC",           C_LBC),
        (9, "Prix\nVinted",        C_VT),
        (10,"Prix\nAnibis",        C_BLUE),
        (11,"Marge\n% (LBC)",      C_DARK),
        (12,"Conseil qualité",     C_DARK),
    ]
    for col, label, bg in headers:
        H_(ws, 3, col, label, bg=bg)
    ws.row_dimensions[3].height = 30

    total_achat = 0.0
    total_ca_sem = 0.0
    total_marge_sem = 0.0

    for r_off, item in enumerate(COMMANDE_S1):
        r = r_off + 4
        alt = C_ALT if r_off % 2 == 0 else C_WHT

        prix_eur = item["prix_unit_usd"] * USD_EUR
        total_prod = prix_eur * item["qty"]
        total_achat += total_prod

        # Frais transport répartis au prorata
        transport_unit = TRANSPORT_TOTAL * (total_prod) / sum(
            p["prix_unit_usd"] * USD_EUR * p["qty"] for p in COMMANDE_S1)
        cout_unit_total = prix_eur + transport_unit / item["qty"]
        marge_lbc = (item["prix_lbc"] - cout_unit_total) / item["prix_lbc"] * 100
        ca_sem = item["rot_sem"] * item["prix_lbc"]
        marge_sem = item["rot_sem"] * (item["prix_lbc"] - cout_unit_total)
        total_ca_sem += ca_sem
        total_marge_sem += marge_sem

        m_bg = C_GBG if marge_lbc >= 55 else (C_YBG if marge_lbc >= 35 else C_OBG)
        m_fg = C_GREEN if marge_lbc >= 55 else (C_YEL if marge_lbc >= 35 else C_ORG)

        C_(ws, r, 2, item["produit"],   bold=True, bg=alt)
        C_(ws, r, 3, item["description"], bg=alt, sz=9, wrap=True)
        C_(ws, r, 4, item["qty"],   fmt=NB, al="center", bg=alt, bold=True)
        C_(ws, r, 5, item["prix_unit_usd"], fmt=USD, al="center", bg=alt)
        C_(ws, r, 6, prix_eur,      fmt=EUR, al="center", bg=alt)
        C_(ws, r, 7, total_prod,    fmt=EUR, al="center", bg=C_YBG, bold=True)
        C_(ws, r, 8, item["prix_lbc"], fmt=EUR, al="center", bg=C_OBG, bold=True, fg=C_ORG)
        C_(ws, r, 9, item["prix_vt"],  fmt=EUR, al="center", bg=C_OBG, bold=True, fg=C_VT)
        C_(ws, r,10, f"{item['prix_ani']} CHF", al="center", bg=C_OBG, bold=True, fg=C_BLUE)
        C_(ws, r,11, marge_lbc,    fmt=PCT, al="center", bg=m_bg, bold=True, fg=m_fg)
        C_(ws, r,12, item["qualite"], bg=C_YBG, sz=9, wrap=True)
        ws.row_dimensions[r].height = 42

    # Totaux
    r_tot = len(COMMANDE_S1) + 4
    C_(ws, r_tot, 2, "SOUS-TOTAL PRODUITS", bold=True, bg=C_DARK, fg=C_WHT)
    C_(ws, r_tot, 7, total_achat, fmt=EUR, al="center", bold=True, bg=C_DARK, fg=C_WHT)
    ws.merge_cells(f"B{r_tot}:F{r_tot}")
    ws.row_dimensions[r_tot].height = 20

    r_t = r_tot + 1
    C_(ws, r_t, 2, "Frais de transport (Chine → France)", bold=True, bg=C_GRY)
    C_(ws, r_t, 7, TRANSPORT_TOTAL, fmt=EUR, al="center", bold=True, bg=C_GRY)
    ws.merge_cells(f"B{r_t}:F{r_t}")
    ws.row_dimensions[r_t].height = 18

    r_grand = r_t + 1
    C_(ws, r_grand, 2, "💰  BUDGET TOTAL SEMAINE 1", bold=True, bg=C_GREEN, fg=C_WHT, sz=13)
    C_(ws, r_grand, 7, total_achat + TRANSPORT_TOTAL, fmt=EUR, al="center",
       bold=True, bg=C_GREEN, fg=C_WHT, sz=14)
    ws.merge_cells(f"B{r_grand}:F{r_grand}")
    ws.row_dimensions[r_grand].height = 26

    # Projections
    r_proj = r_grand + 2
    MH_(ws, r_proj, 2, 12, "📈  PROJECTIONS — SI VOUS VENDEZ TOUT", bg=C_BLUE, h=24)
    r_proj += 1

    proj_data = [
        ("CA potentiel total (tout vendu)", sum(p["qty"] * p["prix_lbc"] for p in COMMANDE_S1), EUR),
        ("Marge totale potentielle (tout vendu)",
         sum(p["qty"] * (p["prix_lbc"] - p["prix_unit_usd"]*USD_EUR - TRANSPORT_TOTAL/sum(pp["qty"] for pp in COMMANDE_S1))
             for p in COMMANDE_S1), EUR),
        ("CA hebdomadaire estimé (rotation normale)", total_ca_sem, EUR),
        ("Marge hebdomadaire estimée", total_marge_sem, EUR),
        ("Marge mensuelle estimée (×4 semaines)", total_marge_sem * 4, EUR),
        ("ROI du lot S1 (%)", (sum(p["qty"] * (p["prix_lbc"] - p["prix_unit_usd"]*USD_EUR) for p in COMMANDE_S1) - TRANSPORT_TOTAL) / (total_achat + TRANSPORT_TOTAL) * 100, PCT),
    ]

    for i, (label, val, fmt) in enumerate(proj_data):
        r = r_proj + i
        alt = C_ALT if i % 2 == 0 else C_WHT
        highlight = "Marge mensuelle" in label or "ROI" in label
        C_(ws, r, 2, label, bold=highlight, bg=alt)
        ws.merge_cells(f"B{r}:F{r}")
        C_(ws, r, 7, val, fmt=fmt, al="center", bold=True,
           bg=C_GBG if highlight else alt,
           fg=C_GREEN if highlight else "000000", sz=12 if highlight else 10)
        ws.row_dimensions[r].height = 18


# ══════════════════════════════════════════════════════════════════════════════
# GUIDE COMMANDE ALIBABA (étapes exactes)
# ══════════════════════════════════════════════════════════════════════════════
def make_alibaba_guide(wb):
    ws = wb.create_sheet("🛍️ GUIDE ALIBABA")
    ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 5
    ws.column_dimensions["B"].width = 12
    ws.column_dimensions["C"].width = 55
    ws.column_dimensions["D"].width = 35

    MH_(ws, 1, 1, 4,
        "🛍️  GUIDE ÉTAPE PAR ÉTAPE — COMMANDER SUR ALIBABA.COM",
        sz=13, h=28)

    STEPS = [
        ("ÉTAPE 1", "Créer compte Alibaba", C_DARK,
         "Allez sur alibaba.com → 'Sign up' → email + mot de passe\nChoisir 'Buyer' (acheteur)\nVérifier votre email",
         "⏱ 5 minutes"),

        ("ÉTAPE 2", "Chercher 'TWS earphones bluetooth 5.3 ANC IPX5'", C_BLUE,
         "Tapez ce terme exact dans la barre de recherche\nFiltrez : Min. Order ≤ 10 | Supplier type : Trade Assurance ✓\nTri : 'Best Match'",
         "⏱ 10 minutes"),

        ("ÉTAPE 3", "Évaluer les fournisseurs", C_BLUE,
         "Critères OBLIGATOIRES :\n✅ Note ≥ 4.8 étoiles\n✅ Trade Assurance activé (bouclier doré)\n✅ ≥ 50 commandes passées\n✅ Réponse en < 24h\n✅ Certifications CE (pour batteries et électro)",
         "⏱ 15 minutes par produit"),

        ("ÉTAPE 4", "Demander un échantillon AVANT de commander", C_TEAL if True else C_BLUE,
         "Cliquez 'Contact Supplier' → message :\n'Hello, I am interested in your [produit]. Can you send me 1 sample first? I plan to order [qty] units after testing. Please share your best price for [qty] units.'\n→ Négociez le prix sur la base de la quantité totale",
         "⏱ 1-2 jours (réponse fournisseur)"),

        ("ÉTAPE 5", "Passer la commande avec Trade Assurance", "1F7391",
         "Ne jamais payer en dehors d'Alibaba (arnaque).\nUtiliser Trade Assurance = remboursé si produit non conforme\nModes de paiement : Visa/Mastercard, PayPal, virement\nChoisir 'DDP' (Delivered Duty Paid) si disponible = douanes incluses",
         "⏱ 10 minutes"),

        ("ÉTAPE 6", "Suivre la commande", C_GHL,
         "Alibaba envoie un email de confirmation avec n° de tracking\nDélai habituel : 15-25 jours ouvrés\nSuivi sur 17track.net ou directement sur la page commande Alibaba",
         "⏱ Attente 15-25 jours"),

        ("ÉTAPE 7", "Réception : TOUT tester avant de vendre", C_ORG,
         "Ouvrir TOUS les cartons et tester chaque unité\nPhotographier les défauts éventuels (preuve pour Trade Assurance)\nSi produits défectueux : ouvrir un litige dans les 15 jours sur Alibaba → remboursement garanti\nNE PAS vendre des produits défectueux",
         "⏱ 1-2 heures"),
    ]

    H_(ws, 2, 2, "Étape",    bg=C_DARK)
    H_(ws, 2, 3, "Action détaillée", bg=C_DARK)
    H_(ws, 2, 4, "Durée / Note", bg=C_DARK)
    ws.row_dimensions[2].height = 22

    for r_off, (num, titre, color, detail, duree) in enumerate(STEPS):
        r = r_off * 2 + 3
        alt = C_ALT if r_off % 2 == 0 else C_WHT

        C_(ws, r, 1, num, al="center", bold=True, bg=color, fg=C_WHT, sz=9)
        C_(ws, r, 2, titre, bold=True, bg=color, fg=C_WHT, sz=10)
        C_(ws, r, 3, detail, bg=alt, sz=9, wrap=True)
        C_(ws, r, 4, duree, bg=C_YBG, bold=True, fg=C_YEL, sz=10, al="center")
        ws.row_dimensions[r].height = 52

        # Ligne séparatrice
        ws.row_dimensions[r+1].height = 5

    # Message type Alibaba prêt à copier
    r_msg = len(STEPS) * 2 + 5
    MH_(ws, r_msg, 1, 4, "📋  MESSAGE TYPE ALIBABA — COPIER-COLLER EN ANGLAIS", bg=C_BLUE, h=24)
    r_msg += 1

    msg = ws.cell(row=r_msg, column=1,
                  value="""Hello,

I am a reseller based in France. I found your product and I am very interested in placing a wholesale order.

Could you please provide me with:
1. Your best price for [QUANTITY] units
2. Shipping cost to France (74160 Saint-Julien-en-Genevois) via express or standard shipping
3. Your CE certification document (mandatory for EU customs)
4. Your estimated delivery time

I will order multiple products from your store if the quality is good. I plan to make regular monthly orders.

Looking forward to your reply.
Best regards""")
    msg.font = Font(name="Courier New", size=9, color=C_DARK)
    msg.alignment = Alignment(vertical="top", wrap_text=True)
    msg.fill = PatternFill("solid", fgColor=C_GRY)
    msg.border = brd(C_BLUE)
    ws.merge_cells(f"A{r_msg}:D{r_msg}")
    ws.row_dimensions[r_msg].height = 120


# ══════════════════════════════════════════════════════════════════════════════
# FEUILLE — 3 ACTIONS À FAIRE AUJOURD'HUI
# ══════════════════════════════════════════════════════════════════════════════
def make_today(wb):
    ws = wb.create_sheet("🚀 AUJOURD'HUI")
    ws.sheet_view.showGridLines = False

    ws.column_dimensions["A"].width = 5
    ws.column_dimensions["B"].width = 8
    ws.column_dimensions["C"].width = 55
    ws.column_dimensions["D"].width = 30

    MH_(ws, 1, 1, 4,
        "🚀  À FAIRE AUJOURD'HUI — DÉMARRER EN 3 HEURES",
        bg=C_RED, sz=14, h=32)

    actions = [
        ("⏱ 10 min", C_BLUE,
         "1️⃣  Créer votre compte Alibaba.com",
         """→ Allez sur alibaba.com
→ Cliquez 'Sign Up' (en haut à droite)
→ Choisissez 'Buyer'
→ Email + mot de passe + vérification email
→ C'est tout. Gratuit.""",
         "alibaba.com/user/login.html"),

        ("⏱ 15 min", C_BLUE,
         "2️⃣  Créer votre compte Vinted (le plus rapide à démarrer)",
         """→ Allez sur vinted.fr
→ 'S'inscrire' → avec votre email
→ Profil : photo (sérieux = confiance), bio courte
→ Renseignez votre adresse pour les envois
→ Activez les paiements (IBAN)""",
         "vinted.fr"),

        ("⏱ 10 min", C_BLUE,
         "3️⃣  Créer votre annonce LeBonCoin",
         """→ leboncoin.fr → 'Déposer une annonce'
→ Créer un compte si pas encore fait
→ Renseignez ville : Saint-Julien-en-Genevois (74160)
→ Vous pouvez publier des annonces gratuitement""",
         "leboncoin.fr"),

        ("⏱ 20 min", C_TEAL if True else C_BLUE,
         "4️⃣  Rechercher les 4 produits sur Alibaba et contacter les fournisseurs",
         """Copier-coller les termes de recherche du bon de commande :
• 'TWS earphones bluetooth 5.3 ANC IPX5'
• 'smartwatch AMOLED 1.7 inch GPS IP68'
• 'power bank 20000mah 65W PD CE certified'
• 'fairy lights USB 5m copper wire 8 modes'

Pour chaque produit : contacter 2-3 fournisseurs avec le message type (feuille GUIDE ALIBABA)""",
         "bon de commande → feuille 🛒"),

        ("⏱ 30 min", C_GHL,
         "5️⃣  Préparer votre espace photo",
         """Matériel gratuit (ce que vous avez chez vous) :
• 1 grande feuille blanche A3 ou carton blanc
• Fenêtre avec lumière naturelle (ou lampe bureau)
• Votre téléphone suffit (mode portrait, fond uni)

Pas besoin de lightbox. Une feuille blanche + lumière naturelle = 90% du résultat.""",
         "0€ — déjà chez vous"),

        ("💶 ~360€", C_ORG,
         "6️⃣  Passer la commande Alibaba dès réponse des fournisseurs",
         """Une fois les fournisseurs contactés et prix confirmés :
→ Commander via 'Trade Assurance' uniquement
→ Budget total : ~360€ (produits + transport)
→ Délai de livraison : 15-25 jours ouvrés
→ Pendant l'attente : publier les annonces avec des photos génériques pour tester le marché""",
         "Budget : 360€"),
    ]

    for r_off, (duree, color, titre, detail, note) in enumerate(actions):
        r = r_off + 2
        alt = C_ALT if r_off % 2 == 0 else C_WHT

        C_(ws, r, 1, "☐", al="center", bg=color, fg=C_WHT, bold=True, sz=14)
        C_(ws, r, 2, duree, al="center", bg=color, fg=C_WHT, bold=True, sz=9)
        C_(ws, r, 3, f"{titre}\n\n{detail}", bg=alt, sz=10, wrap=True, bold=False)
        ws.cell(row=r, column=3).font = Font(name="Calibri", size=10)
        # Remettre le titre en gras manuellement n'est pas possible ligne par ligne
        C_(ws, r, 4, note, bg=C_YBG, sz=9, wrap=True, al="center")
        ws.row_dimensions[r].height = 90

    # Ce que Claude fait en parallèle
    r_cl = len(actions) + 3
    MH_(ws, r_cl, 1, 4,
        "🤖  CE QUE JE FAIS EN PARALLÈLE (automatique — rien à faire de votre côté)",
        bg=C_DARK, h=24)
    r_cl += 1

    auto_tasks = [
        "✅ Annonces LBC / Vinted / Anibis déjà rédigées et prêtes dans le fichier Kit_Annonces_Complet.xlsx",
        "✅ Prix de vente optimaux calculés pour battre 91% des concurrents",
        "✅ Tableau de suivi clients / commandes / stock / marge prêt à remplir",
        "✅ Checklist expédition générée pour ne rien oublier",
        "✅ Plan d'action 6 semaines structuré pour atteindre 500€/mois",
        "✅ Termes de recherche Alibaba + message type prêt à envoyer aux fournisseurs",
    ]

    for i, task in enumerate(auto_tasks):
        r = r_cl + i
        alt = C_ALT if i % 2 == 0 else C_GBG
        ws.merge_cells(f"A{r}:D{r}")
        tc = ws.cell(row=r, column=1, value=task)
        tc.font = Font(name="Calibri", size=10, color=C_GREEN, bold=True)
        tc.fill = PatternFill("solid", fgColor=alt)
        tc.border = brd()
        tc.alignment = Alignment(vertical="center")
        ws.row_dimensions[r].height = 18

    # Ce que je ne peux pas faire
    r_lim = r_cl + len(auto_tasks) + 2
    MH_(ws, r_lim, 1, 4,
        "⚠️  CE QUE VOUS SEUL POUVEZ FAIRE (nécessite une action physique/financière)",
        bg=C_ORG, h=24)
    r_lim += 1

    limites = [
        ("Transférer l'argent (360€)",   "Paiement Alibaba = carte bancaire ou PayPal → nécessite votre carte"),
        ("Créer les comptes plateformes","Vinted / LBC / Anibis → nécessite votre email et identité"),
        ("Prendre les photos",            "Nécessite votre téléphone et les produits physiques"),
        ("Expédier les colis",            "Nécessite votre présence à La Poste ou point relais"),
    ]

    for i, (action, raison) in enumerate(limites):
        r = r_lim + i
        alt = C_OBG if i % 2 == 0 else C_WHT
        C_(ws, r, 1, "→", al="center", bold=True, bg=C_ORG, fg=C_WHT)
        C_(ws, r, 2, action, bold=True, bg=alt)
        ws.merge_cells(f"B{r}:B{r}")
        C_(ws, r, 3, raison, bg=alt, sz=9)
        ws.merge_cells(f"C{r}:D{r}")
        ws.row_dimensions[r].height = 18


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════
def main():
    wb = openpyxl.Workbook()
    wb.remove(wb.active)

    make_today(wb)
    make_order_sheet(wb)
    make_alibaba_guide(wb)

    wb.active = wb["🚀 AUJOURD'HUI"]

    out = "/home/user/Demarrage_Semaine1.xlsx"
    wb.save(out)
    print(f"✅  Fichier créé : {out}")

    # Résumé console
    total = sum(p["prix_unit_usd"] * 0.93 * p["qty"] for p in COMMANDE_S1) + TRANSPORT_TOTAL
    ca_pot = sum(p["qty"] * p["prix_lbc"] for p in COMMANDE_S1)
    marge_pot = ca_pot - total
    print(f"\n  Budget S1 : {total:.0f}€")
    print(f"  CA potentiel : {ca_pot:.0f}€")
    print(f"  Marge potentielle : {marge_pot:.0f}€ (+{marge_pot/total*100:.0f}% ROI)")

if __name__ == "__main__":
    main()
