"""
Génère un kit complet pour démarrer la revente :
1. Annonces prêtes à copier-coller (LBC / Vinted / Anibis)
2. Plan d'action semaine par semaine
3. Tableau de bord opérationnel
"""
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

C_DARK="1F3864";C_BLUE="2E75B6";C_TEAL="1F7391";C_GHL="70AD47"
C_GREEN="375623";C_GBG="E2EFDA";C_ORG="C55A11";C_OBG="FCE4D6"
C_RED="C00000";C_RBG="FFE0E0";C_YEL="7F6000";C_YBG="FFF2CC"
C_ALT="DCE6F1";C_GRY="F2F2F2";C_WHT="FFFFFF";C_BDR="B8CCE4"
C_VT="7030A0";C_LBC="E36C09";C_ANI="2D6A9F"
EUR='#,##0.00 "€"';PCT='0.0"%"';NB='#,##0'

def brd(c=C_BDR):
    s=Side(style="thin",color=c)
    return Border(left=s,right=s,top=s,bottom=s)

def C(ws,r,col,v=None,fmt=None,bold=False,bg=None,fg="000000",
      al="left",wrap=False,sz=10):
    cl=ws.cell(row=r,column=col,value=v)
    cl.font=Font(name="Calibri",bold=bold,color=fg,size=sz)
    cl.alignment=Alignment(horizontal=al,vertical="center",wrap_text=wrap)
    cl.border=brd()
    if fmt:cl.number_format=fmt
    if bg:cl.fill=PatternFill("solid",fgColor=bg)
    return cl

def H(ws,r,col,v,bg=C_DARK,fg=C_WHT,sz=10,wrap=True):
    return C(ws,r,col,v,bold=True,bg=bg,fg=fg,al="center",sz=sz,wrap=wrap)

def MH(ws,r,c1,c2,v,bg=C_DARK,fg=C_WHT,sz=13,h=28):
    cl=ws.cell(row=r,column=c1,value=v)
    cl.font=Font(name="Calibri",bold=True,color=fg,size=sz)
    cl.fill=PatternFill("solid",fgColor=bg)
    cl.alignment=Alignment(horizontal="center",vertical="center")
    cl.border=brd()
    ws.merge_cells(start_row=r,start_column=c1,end_row=r,end_column=c2)
    ws.row_dimensions[r].height=h

# ══════════════════════════════════════════════════════════════════════════════
# ANNONCES PRÊTES À PUBLIER
# ══════════════════════════════════════════════════════════════════════════════
LISTINGS = [
  {
    "produit": "Air Fryer 4-5L",
    "cout": 33.0,
    "prix_lbc": 55, "prix_vt": 49, "prix_ani": 65,
    "lbc_titre": "Friteuse sans huile Air Fryer 4L — Neuf jamais utilisé",
    "lbc_desc": """Friteuse à air chaud 4 litres, 1500W, idéale pour 2-4 personnes.
✅ Cuisine jusqu'à 60% moins grasse qu'une friture classique
✅ Cuisson rapide en 10-20 minutes
✅ Température réglable 80°C à 200°C — minuterie intégrée
✅ Panier antiadhésif lavable au lave-vaisselle
✅ Livré avec livre de recettes

Parfait pour frites, poulet, légumes, pizza, desserts.
Produit neuf, jamais déballé. Envoi soigné en colissimo suivi.

Prix ferme : 55€ — envoi possible ou remise main propre 74160 St-Julien-en-Genevois.""",

    "vt_titre": "Air fryer friteuse sans huile 4L neuf ✨",
    "vt_desc": """Friteuse sans huile 4L neuve, jamais utilisée 🍟
1500W | Temp. 80-200°C | Minuterie | Panier antiadhésif
Cuisine saine : -60% de matières grasses vs friture classique
Idéal frites, poulet, légumes, gâteaux 🥗

Envoi rapide colissimo suivi 📦
N'hésitez pas à me faire une offre !""",

    "ani_titre": "Friteuse air fryer 4L — NEUF — livraison Suisse",
    "ani_desc": """Friteuse à air chaud 4L, 1500W — état neuf, jamais utilisée.
✔ 80°C à 200°C — minuterie intégrée
✔ Panier antiadhésif, lavable lave-vaisselle
✔ Cuisine saine sans huile
✔ Livre de recettes inclus

Envoi La Poste CH ou remise en main propre région Genève/St-Julien.
Prix : 65 CHF ferme.""",

    "photo_tips": "Fond blanc ou bois. Panier ouvert visible. Photo face + vue de côté + panier seul. Ajoutez un aliment (frites) pour visualiser la taille.",
    "cat_lbc": "Electroménager",
    "cat_vt": "Electroménager",
    "cat_ani": "Electroménager / Petit électro",
  },
  {
    "produit": "Écouteurs TWS sans fil",
    "cout": 7.0,
    "prix_lbc": 22, "prix_vt": 25, "prix_ani": 28,
    "lbc_titre": "Écouteurs sans fil Bluetooth 5.3 — Neuf — Son HiFi",
    "lbc_desc": """Écouteurs intra-auriculaires sans fil Bluetooth 5.3
✅ Son HiFi stéréo avec basses prononcées
✅ Réduction du bruit (ANC passive) pour vos appels
✅ 6h d'autonomie + 24h avec boîtier de charge
✅ Commandes tactiles sur chaque écouteur
✅ Compatible iOS et Android
✅ Résistants à la transpiration IPX5

Dans leur boîte d'origine. Idéal sport, transports, télétravail.
Envoi colissimo suivi ou remise en main propre 74160.
Prix : 22€""",

    "vt_titre": "Écouteurs Bluetooth sans fil — neufs 🎧 son HiFi",
    "vt_desc": """Écouteurs TWS bluetooth 5.3 tout neufs 🎵
Son HiFi | 6h autonomie + boîtier 24h | Tactile | IPX5
Compatible iPhone & Android 📱
Idéal sport, vélo, transports, gaming 🎮

Envoi soigné sous 24h 📦 — Prix négociable pour lot""",

    "ani_titre": "Écouteurs Bluetooth TWS sans fil — neufs — livraison Suisse",
    "ani_desc": """Écouteurs intra-auriculaires sans fil Bluetooth 5.3 — état neuf.
✔ Son HiFi stéréo, basses profondes
✔ 6h autonomie + boîtier de recharge (24h total)
✔ Commandes tactiles, micro intégré
✔ IPX5 résistant à la transpiration
✔ Compatible iOS / Android

Envoi en Suisse ou remise Genève/St-Julien.
28 CHF""",

    "photo_tips": "Écouteurs sortis du boîtier, posés sur fond noir ou blanc. Photo boîtier ouvert + fermé. Gros plan sur les écouteurs. Photo de quelqu'un les portant.",
    "cat_lbc": "Audio & Hi-Fi",
    "cat_vt": "Électronique",
    "cat_ani": "Téléphonie / Audio",
  },
  {
    "produit": "Montre connectée smartwatch",
    "cout": 11.0,
    "prix_lbc": 32, "prix_vt": 28, "prix_ani": 38,
    "lbc_titre": "Montre connectée sport — Écran AMOLED — Neuf boîte",
    "lbc_desc": """Montre connectée intelligente — Écran AMOLED 1.7 pouces HD
✅ Suivi santé : fréquence cardiaque, SpO2, sommeil, stress
✅ GPS intégré pour vos activités sport (course, vélo, natation)
✅ Notifications : appels, SMS, WhatsApp, emails sur le poignet
✅ Étanche IP68 — utilisable piscine et douche
✅ Autonomie 7 jours — Compatible iOS & Android
✅ Plus de 100 modes sport

Neuve, non déballée, boîte d'origine.
Envoi colissimo suivi ou remise main propre 74160 St-Julien.
Prix : 32€""",

    "vt_titre": "Montre connectée neuve ⌚ AMOLED GPS sport santé",
    "vt_desc": """Montre connectée neuve dans sa boîte 📦
Écran AMOLED 1.7" | GPS | FC + SpO2 | IP68 🏊
100+ modes sport | 7 jours autonomie
Notifications WhatsApp, appels, SMS ⌚

Compatible iPhone & Android 📱
Envoi rapide colissimo suivi — n'hésitez pas pour offre !""",

    "ani_titre": "Montre connectée GPS sport AMOLED — neuve — Suisse",
    "ani_desc": """Montre connectée intelligente — neuve dans sa boîte.
✔ Écran AMOLED HD 1.7 pouces
✔ GPS, fréquence cardiaque, SpO2, sommeil
✔ 100+ modes sport, étanche IP68
✔ Autonomie 7 jours
✔ Compatible iOS et Android

38 CHF — livraison Suisse ou remise Genève.""",

    "photo_tips": "Montre sur fond blanc ou poignet. Photo face, profil, et écran allumé (mode sport ou cadran principal). Bracelet visible. Boîte à côté.",
    "cat_lbc": "Montres & Bijoux",
    "cat_vt": "Montres",
    "cat_ani": "Bijouterie / Montres",
  },
  {
    "produit": "Batterie externe 20 000 mAh",
    "cout": 9.0,
    "prix_lbc": 24, "prix_vt": 22, "prix_ani": 29,
    "lbc_titre": "Batterie externe 20000mAh Charge Rapide 65W — Neuf",
    "lbc_desc": """Batterie externe ultra-capacité 20 000 mAh — Charge rapide 65W
✅ Charge 3 appareils simultanément (2× USB-A + 1× USB-C)
✅ 65W Power Delivery : charge un laptop en ~1h30
✅ Recharge votre téléphone 4 à 5 fois complètes
✅ Affichage LED pourcentage de charge restant
✅ Compact et léger : tient dans une poche de veste
✅ Certifié CE — Sécurité anti-surcharge

Neuve, dans sa boîte d'origine.
Envoi colissimo suivi ou remise main propre 74160.
Prix : 24€""",

    "vt_titre": "Batterie externe 20000mAh 65W neuve ⚡ charge rapide",
    "vt_desc": """Batterie externe 20 000 mAh neuve 🔋
65W charge rapide | 3 ports USB | Laptop compatible 💻
Recharge téléphone 4-5× | Affichage LED
Compact, certifié CE ✅

Envoi soigné sous 24h 📦""",

    "ani_titre": "Batterie externe 20000mAh 65W — neuve — Suisse",
    "ani_desc": """Batterie externe 20 000 mAh charge rapide 65W — neuve.
✔ 3 ports (2× USB-A + 1× USB-C PD)
✔ Charge laptop + téléphone + tablette
✔ Affichage LED autonomie
✔ 4-5 recharges smartphone

29 CHF — envoi La Poste CH ou remise Genève.""",

    "photo_tips": "Fond blanc. Photo face + côté (pour voir les ports). Photo à côté d'un iPhone pour l'échelle. Photo branchée avec un câble visible.",
    "cat_lbc": "Téléphones & Objets connectés",
    "cat_vt": "Électronique",
    "cat_ani": "Téléphonie / Accessoires",
  },
  {
    "produit": "Haut-parleur Bluetooth compact",
    "cout": 12.5,
    "prix_lbc": 35, "prix_vt": 32, "prix_ani": 42,
    "lbc_titre": "Enceinte Bluetooth portable 360° — Neuf — IPX7 étanche",
    "lbc_desc": """Enceinte Bluetooth portable — Son 360° puissant
✅ Bluetooth 5.0 — connexion jusqu'à 10m
✅ Étanche IPX7 : plage, piscine, douche
✅ Autonomie 12 heures de lecture continue
✅ Son stéréo 360° avec basses profondes
✅ Micro intégré pour appels mains-libres
✅ Compatible iOS, Android, PC

Neuve, jamais ouverte, boîte scellée.
Idéal plein air, terrasse, randonnée.
Envoi colissimo suivi ou remise 74160.
Prix : 35€""",

    "vt_titre": "Enceinte Bluetooth portable neuve 🔊 IPX7 étanche 12h",
    "vt_desc": """Enceinte Bluetooth 360° neuve dans sa boîte 🎵
Bluetooth 5.0 | IPX7 étanche | 12h autonomie
Son puissant 360° + basses | Micro mains-libres 📞
Idéal plage, terrasse, sport 🏖️

Envoi rapide — offre bienvenue 📦""",

    "ani_titre": "Enceinte Bluetooth portable IPX7 — neuve — Suisse",
    "ani_desc": """Enceinte Bluetooth portable 360° — neuve dans sa boîte.
✔ Bluetooth 5.0, portée 10m
✔ IPX7 étanche (plage, piscine, douche)
✔ 12h d'autonomie
✔ Son stéréo 360° + micro intégré

42 CHF — livraison Suisse ou remise Genève/St-Julien.""",

    "photo_tips": "Photo en extérieur (terrasse, bord de piscine) pour illustrer l'usage. Photo face + dessus + dessous (pour montrer ports). Fond neutre.",
    "cat_lbc": "Audio & Hi-Fi",
    "cat_vt": "Électronique",
    "cat_ani": "Audio Hi-Fi",
  },
  {
    "produit": "Guirlandes LED USB 5m",
    "cout": 3.5,
    "prix_lbc": 14, "prix_vt": 13, "prix_ani": 17,
    "lbc_titre": "Guirlande LED 5m USB — Neuf — Lumières féeriques",
    "lbc_desc": """Guirlande lumineuse LED 5 mètres — Alimentation USB
✅ 50 micro-LEDs chaudes, blanches ou multicolores
✅ 8 modes d'éclairage (fixe, clignotant, fondu, vagues)
✅ Fonctionne sur USB (chargeur, PC, batterie externe)
✅ Fil de cuivre flexible et indétectable
✅ Parfait chambre, salon, terrasse, jardin, événements

Neuve dans son emballage.
Prix : 14€ — lot de 2 disponible : 24€""",

    "vt_titre": "Guirlande LED 5m USB neuve ✨ chambre déco lumineuse",
    "vt_desc": """Guirlande LED 5m USB neuve 🌟
50 LEDs | 8 modes | Fil cuivre flexible
Chambre, salon, terrasse, événement 🎉
Disponible en lot 2 pièces 🎁

Envoi sous 24h 📦""",

    "ani_titre": "Guirlande LED 5m USB — neuve — lumières féeriques",
    "ani_desc": """Guirlande lumineuse LED 5m alimentation USB — neuve.
✔ 50 LEDs | 8 modes d'éclairage
✔ Fil cuivre souple et fin
✔ Chambre, salon, terrasse, jardin

17 CHF (lot de 2 disponible : 28 CHF)
Livraison Suisse ou remise Genève.""",

    "photo_tips": "Photo dans une chambre avec lumières tamisées — c'est LA photo qui vend. Guirlande enroulée autour d'un miroir ou d'une tête de lit. Photo emballage aussi.",
    "cat_lbc": "Maison & Décoration",
    "cat_vt": "Maison",
    "cat_ani": "Maison / Décoration",
  },
  {
    "produit": "Console retro portable 10 000 jeux",
    "cout": 18.5,
    "prix_lbc": 52, "prix_vt": 45, "prix_ani": 65,
    "lbc_titre": "Console rétro portable 10 000 jeux — Mario, Sonic, GBA — Neuf",
    "lbc_desc": """Console de jeux portable rétro — 10 000 jeux pré-installés
✅ Écran LCD 3.5 pouces couleur
✅ Jeux classiques : Mario, Sonic, Pac-Man, Street Fighter, Contra...
✅ Compatible NES, SNES, GBA, GBC, Sega Genesis
✅ Autonomie 4-6 heures — charge USB-C
✅ 2 manettes incluses pour jouer à 2
✅ Sortie HDMI pour jouer sur TV

Neuve, jamais ouverte.
Idéal cadeau anniversaire, Noël, pour les enfants et nostalgiques.
Envoi colissimo ou remise 74160.
Prix : 52€""",

    "vt_titre": "Console retro portable 10000 jeux 🎮 Mario Sonic GBA neuve",
    "vt_desc": """Console retro 10 000 jeux — neuve dans sa boîte 🕹️
Mario, Sonic, GBA, SNES, Sega 🎮
Écran 3.5" | 2 manettes incluses | HDMI TV
USB-C | 4-6h autonomie

Cadeau parfait ! Envoi soigné 📦""",

    "ani_titre": "Console rétro portable 10000 jeux — Mario, Sega, GBA — neuve",
    "ani_desc": """Console portable rétro 10 000 jeux pré-installés — neuve.
✔ Écran LCD 3.5 pouces
✔ Mario, Sonic, Pac-Man, GBA, SNES, Sega...
✔ 2 manettes | Sortie HDMI TV
✔ Charge USB-C | 4-6h autonomie

65 CHF — cadeau parfait ! Livraison Suisse ou remise Genève.""",

    "photo_tips": "Photo console allumée avec un jeu Mario visible. Photo 2 manettes dépliées. Photo boîte. Photo sur une table de salon avec TV. Nostalgie = vend bien.",
    "cat_lbc": "Jeux vidéo",
    "cat_vt": "Jeux vidéo",
    "cat_ani": "Jeux vidéo / Console",
  },
  {
    "produit": "Épilateur lumière pulsée IPL",
    "cout": 22.0,
    "prix_lbc": 65, "prix_vt": 60, "prix_ani": 78,
    "lbc_titre": "Épilateur lumière pulsée IPL — 500 000 flashs — Neuf",
    "lbc_desc": """Épilateur à lumière pulsée IPL professionnel maison
✅ 500 000 flashs — durée de vie 10+ ans d'utilisation
✅ 5 niveaux d'intensité pour tous types de peau
✅ Zones : jambes, aisselles, bikini, visage, bras
✅ Résultats visibles dès la 3e séance (8 semaines)
✅ Tête de rasage incluse pour une peau lisse immédiate
✅ Sécurité UV intégrée — homologué CE

Neuf, dans sa boîte. Évitez les salons coûteux (150-300€ par séance).
Envoi colissimo ou remise 74160.
Prix : 65€""",

    "vt_titre": "Épilateur IPL lumière pulsée 500k flashs NEUF 🌸",
    "vt_desc": """Épilateur IPL neuf dans sa boîte ✨
500 000 flashs | 5 intensités | Toutes zones 🦵
Résultats dès la 3e séance | Certifié CE
Tête rasage incluse | Sécurité UV

Économisez 1000€+ vs instituts 💰
Envoi soigné 48h 📦""",

    "ani_titre": "Épilateur IPL lumière pulsée 500 000 flashs — neuf — Suisse",
    "ani_desc": """Épilateur à lumière pulsée IPL professionnel — neuf.
✔ 500 000 flashs (usage illimité)
✔ 5 niveaux d'intensité
✔ Jambes, aisselles, bikini, visage
✔ Résultats visibles en 8 semaines
✔ Certifié CE, sécurité UV

78 CHF — livraison Suisse ou remise Genève.""",

    "photo_tips": "Photo produit sur fond blanc + fond rose/lavande pour audience féminine. Photo sur une peau (bras) pour montrer l'application. Photo boîte ouverte.",
    "cat_lbc": "Beauté & Santé",
    "cat_vt": "Beauté / Soins",
    "cat_ani": "Beauté / Santé",
  },
]

# ══════════════════════════════════════════════════════════════════════════════
# FEUILLE 1 — ANNONCES LBC
# ══════════════════════════════════════════════════════════════════════════════
def make_listings_sheet(wb, platform, title_key, desc_key, price_key, color, plat_label):
    ws = wb.create_sheet(f"📝 {plat_label}")
    ws.sheet_view.showGridLines = False

    ws.column_dimensions["A"].width = 3
    ws.column_dimensions["B"].width = 30
    ws.column_dimensions["C"].width = 18
    ws.column_dimensions["D"].width = 65
    ws.column_dimensions["E"].width = 28

    MH(ws, 1, 1, 5,
       f"📝  ANNONCES PRÊTES À COPIER — {plat_label.upper()}  |  Copier-coller directement",
       bg=color, sz=13, h=28)

    H(ws, 2, 2, "Produit",              bg=color)
    H(ws, 2, 3, f"Prix conseillé",      bg=color)
    H(ws, 2, 4, "Titre + Description",  bg=color)
    H(ws, 2, 5, "Conseils photos",      bg=color)
    ws.row_dimensions[2].height = 22

    for r_off, item in enumerate(LISTINGS):
        r = r_off * 2 + 3
        marge = (item[price_key] - item["cout"]) / item[price_key] * 100
        m_bg = "E2EFDA" if marge >= 55 else ("FFF2CC" if marge >= 35 else "FCE4D6")

        C(ws, r, 2, item["produit"], bold=True, bg=m_bg, sz=11)
        C(ws, r, 3, item[price_key], fmt=EUR, al="center", bold=True, bg=m_bg, sz=14,
          fg="375623" if marge >= 55 else ("7F6000" if marge >= 35 else "C55A11"))

        # Titre en gras + description
        full_text = f"TITRE : {item[title_key]}\n\n{item[desc_key]}"
        tc = ws.cell(row=r, column=4, value=full_text)
        tc.font = Font(name="Calibri", size=9)
        tc.alignment = Alignment(vertical="top", wrap_text=True)
        tc.border = brd(); tc.fill = PatternFill("solid", fgColor=C_GRY)

        C(ws, r, 5, item["photo_tips"], bg=C_YBG, sz=9, wrap=True)

        ws.row_dimensions[r].height = max(120, len(item[desc_key]) // 3)

        # Marge info
        r2 = r + 1
        marge_txt = (f"Coût : {item['cout']:.0f}€ | Prix : {item[price_key]}€ | "
                     f"Marge : {item[price_key]-item['cout']:.0f}€ ({marge:.0f}%)")
        ws.merge_cells(f"B{r2}:E{r2}")
        mc = ws.cell(row=r2, column=2, value=marge_txt)
        mc.font = Font(name="Calibri", italic=True, size=9,
                       color=C_GREEN if marge >= 55 else C_ORG)
        mc.fill = PatternFill("solid", fgColor=m_bg)
        mc.alignment = Alignment(vertical="center"); mc.border = brd()
        ws.row_dimensions[r2].height = 14


# ══════════════════════════════════════════════════════════════════════════════
# FEUILLE — PLAN D'ACTION SEMAINE PAR SEMAINE
# ══════════════════════════════════════════════════════════════════════════════
def make_action_plan(wb):
    ws = wb.create_sheet("📅 PLAN D'ACTION")
    ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 5
    ws.column_dimensions["B"].width = 18
    ws.column_dimensions["C"].width = 50
    ws.column_dimensions["D"].width = 22
    ws.column_dimensions["E"].width = 20

    MH(ws, 1, 1, 5, "📅  PLAN D'ACTION — DE ZÉRO À 500€/MOIS EN 6 SEMAINES", sz=13, h=28)

    PLAN = [
        # sem, qui, quoi, comment, budget
        ("SEMAINE 1", "Vous", "Commander premier lot test sur Alibaba",
         "Écouteurs TWS ×20 (~9€/unit = 180€ total)\nMontre connectée ×10 (~12€/unit = 120€ total)\n→ Budget total : ~300€",
         "~300€"),

        ("SEMAINE 1", "Vous", "Créer comptes sur les 3 plateformes",
         "- Vinted.fr : compte vendeur (gratuit)\n- Leboncoin.fr : profil vendeur particulier (gratuit)\n- Anibis.ch : compte gratuit",
         "Gratuit"),

        ("SEMAINE 1", "Vous", "Préparer votre espace photos",
         "Fond blanc (feuille A3 ou carton), lampe LED de bureau.\nTotal : 0€ si vous improvisez, ou 15€ pour une lightbox Amazon.",
         "0-15€"),

        ("SEMAINE 2-3", "Vous", "Réception et vérification des produits",
         "Tester chaque unité à réception.\nCompter et vérifier vs commande.\nPhotographier tout sur fond blanc.",
         "0€"),

        ("SEMAINE 2-3", "Claude\n(moi)", "Annonces prêtes dans ce fichier",
         "Copier-coller les titres et descriptions des feuilles 📝 LBC / Vinted / Anibis.\nAdaptez seulement : ville, n° de téléphone, disponibilité.",
         "0€"),

        ("SEMAINE 3", "Vous", "Publier les premières annonces",
         "Commencez par LBC (plus de trafic) + Vinted pour les écouteurs et montres.\nPublier d'abord 3-4 annonces, pas tout en même temps.",
         "0€"),

        ("SEMAINE 3-4", "Vous", "Gérer les premières ventes",
         "Répondre dans l'heure (algorithme favorise les vendeurs réactifs).\nEnvoi colissimo sous 48h.\nSaisir chaque vente dans le fichier '📦 GESTION'.",
         "~8€/envoi"),

        ("SEMAINE 4", "Vous", "Ajuster les prix selon les retours",
         "Si 0 vue après 5 jours : baisser de 5-10%.\nSi beaucoup de vues mais pas d'achat : améliorer les photos.\nSi vendu en 1 jour : remonter le prix de 5€.",
         "0€"),

        ("SEMAINE 4", "Vous", "Commander le 2e lot (produits validés)",
         "Commander ×2 de ce qui a le mieux vendu.\nAjouter 1 nouveau produit test (air fryer ou console retro).",
         "~300-500€"),

        ("SEMAINE 5", "Vous", "Ouvrir sur Anibis (Suisse)",
         "Adapter les prix en CHF (×1.08 × 1.1 = +20% vs France).\nLa région 74 (Haute-Savoie) est idéale : frontaliers achètent des 2 côtés.",
         "0€"),

        ("SEMAINE 6", "Vous", "Analyser et pivoter",
         "Quels produits = meilleure marge ?\nQuelles plateformes convertissent le mieux ?\nRéévaluer le stock mort (baisser prix ou bundle).",
         "0€"),

        ("MOIS 2+", "Vous", "Scaler vers 500-1000€/mois",
         "Commandes régulières : 1 commande 1688 toutes les 3 semaines.\nVisez 8-12 ventes/semaine sur 2-3 produits phares.\nDéclarer les revenus si >3000€/an ou >20 transactions.",
         "~500€/mois"),
    ]

    H(ws, 2, 2, "Semaine",    bg=C_DARK)
    H(ws, 2, 3, "Action à faire", bg=C_DARK)
    H(ws, 2, 4, "Comment faire",  bg=C_DARK)
    H(ws, 2, 5, "Budget estimé",  bg=C_DARK)
    ws.row_dimensions[2].height = 22

    sem_colors = {
        "SEMAINE 1": C_BLUE, "SEMAINE 2-3": C_TEAL,
        "SEMAINE 3": "1F7391", "SEMAINE 3-4": "2E7F5F",
        "SEMAINE 4": C_GHL, "SEMAINE 5": C_ORG, "SEMAINE 6": "7030A0",
        "MOIS 2+": C_RED,
    }

    for r_off, (sem, who, quoi, comment, budget) in enumerate(PLAN):
        r = r_off + 3
        alt = C_ALT if r_off % 2 == 0 else C_WHT
        sc = sem_colors.get(sem, C_DARK)

        C(ws, r, 1, "●", al="center", bold=True, bg=alt, fg=sc)
        C(ws, r, 2, f"{sem}\n({who})", bold=True, bg=alt, fg=sc, sz=9, wrap=True)
        C(ws, r, 3, quoi, bold=True, bg=alt, sz=10)
        C(ws, r, 4, comment, bg=C_GRY, sz=9, wrap=True)
        bg_b = C_GBG if budget == "Gratuit" or budget == "0€" else C_YBG
        C(ws, r, 5, budget, al="center", bold=True, bg=bg_b, sz=10,
          fg=C_GREEN if "Gratuit" in budget or budget == "0€" else C_YEL)
        ws.row_dimensions[r].height = 42


# ══════════════════════════════════════════════════════════════════════════════
# FEUILLE — CHECKLIST PAR VENTE
# ══════════════════════════════════════════════════════════════════════════════
def make_checklist(wb):
    ws = wb.create_sheet("✅ CHECKLIST VENTE")
    ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 5
    ws.column_dimensions["B"].width = 8
    ws.column_dimensions["C"].width = 55
    ws.column_dimensions["D"].width = 35

    MH(ws, 1, 1, 4, "✅  CHECKLIST — À FAIRE POUR CHAQUE VENTE", sz=13, h=28)

    sections = [
        ("📸 AVANT DE PUBLIER", C_BLUE, [
            ("Prendre 4-5 photos (fond blanc + usage + boîte)", "Fond A3, lumière fenêtre ou lampe"),
            ("Tester le produit (marche-t-il ?)", "Ne jamais vendre un produit non testé"),
            ("Copier le titre depuis ce fichier (feuilles LBC/Vinted/Anibis)", "Adapter ville et disponibilité"),
            ("Fixer le prix selon les feuilles de prix", "Jamais en dessous du coût total"),
            ("Choisir la bonne catégorie sur la plateforme", "Voir colonne 'Catégorie' dans les feuilles annonces"),
        ]),
        ("💬 QUAND UN ACHETEUR CONTACTE", C_TEAL, [
            ("Répondre dans l'heure (max 2h)", "Les acheteurs passent vite à la concurrence"),
            ("Vérifier l'adresse de livraison complète (rue, CP, ville, pays)", "Demander par message ou via la plateforme"),
            ("Confirmer le mode de paiement", "Vinted : paiement intégré. LBC : Paylib/virement/liquide. Anibis : Twint/virement"),
            ("NE PAS communiquer en dehors de la plateforme", "Risque d'arnaque si on quitte la messagerie"),
        ]),
        ("📦 EXPÉDITION", C_GHL, [
            ("Emballer soigneusement : bulle + carton rigide", "Un produit cassé = remboursement obligatoire"),
            ("Imprimer l'étiquette colissimo (laposte.fr ou pré-affranchir)", "Colissimo suivi : ~6-8€ selon poids"),
            ("Coller l'étiquette lisiblement sur le carton", ""),
            ("Déposer le colis dans les 48h ouvrées", "Objectif : 24h pour bonne note vendeur"),
            ("Envoyer le numéro de suivi à l'acheteur", "Message sur la plateforme avec le numéro de tracking"),
        ]),
        ("📋 APRÈS LA VENTE", C_ORG, [
            ("Marquer 'Vendu' ou 'Livré' sur la plateforme", "Libère le stock visible"),
            ("Saisir dans le fichier '📦 GESTION' : client, prix, plateforme, date", "Pour suivre les marges et payer les impôts"),
            ("Demander un avis au client (message de suivi)", "Les avis = crédibilité = ventes suivantes"),
            ("Mettre à jour le stock dans l'onglet STOCK", ""),
            ("Déclarer si >3 000€/an ou >20 transactions", "Les plateformes transmettent au fisc automatiquement"),
        ]),
    ]

    r = 2
    for section_name, color, items in sections:
        ws.merge_cells(f"B{r}:D{r}")
        sc = ws.cell(row=r, column=2, value=section_name)
        sc.font = Font(name="Calibri", bold=True, color=C_WHT, size=11)
        sc.fill = PatternFill("solid", fgColor=color)
        sc.border = brd(); sc.alignment = Alignment(vertical="center", indent=1)
        ws.row_dimensions[r].height = 22
        r += 1

        for i, (task, hint) in enumerate(items):
            alt = C_ALT if i % 2 == 0 else C_WHT
            C(ws, r, 2, "☐", al="center", bg=alt, sz=14, bold=True)
            C(ws, r, 3, task, bg=alt, sz=10)
            C(ws, r, 4, hint, bg=C_GRY, sz=9, wrap=True)
            ws.row_dimensions[r].height = 18
            r += 1
        r += 1

    # Note déclaration fiscale
    ws.merge_cells(f"A{r}:D{r}")
    n = ws.cell(row=r, column=1,
                value="⚠️  FISCAL : Vinted, LBC et Anibis transmettent automatiquement vos revenus au fisc si >3 000€/an ou >20 transactions. "
                      "Au-delà, déclarez en revenus BIC (micro-entrepreneur ou déclaration 2042). "
                      "Conservez toutes vos factures 1688/Alibaba comme justificatifs de coûts.")
    n.font = Font(name="Calibri", italic=True, color=C_RED, size=9, bold=True)
    n.alignment = Alignment(wrap_text=True, vertical="center")
    n.fill = PatternFill("solid", fgColor=C_RBG); n.border = brd(C_RED)
    ws.row_dimensions[r].height = 40


# ══════════════════════════════════════════════════════════════════════════════
# FEUILLE — SUIVI STOCK + VENTES (opérationnel)
# ══════════════════════════════════════════════════════════════════════════════
def make_ops_tracker(wb):
    ws = wb.create_sheet("📦 GESTION")
    ws.sheet_view.showGridLines = False

    MH(ws, 1, 1, 12, "📦  SUIVI STOCK & VENTES — À REMPLIR AU FUR ET À MESURE", sz=12, h=26)

    # Stock
    H(ws, 2, 1,  "Produit",         bg=C_DARK)
    H(ws, 2, 2,  "Coût unitaire",   bg=C_DARK)
    H(ws, 2, 3,  "Qté achetée",     bg=C_DARK)
    H(ws, 2, 4,  "Qté vendue",      bg=C_DARK)
    H(ws, 2, 5,  "Stock dispo",     bg=C_DARK)
    H(ws, 2, 6,  "CA généré",       bg=C_DARK)
    H(ws, 2, 7,  "Marge totale",    bg=C_DARK)
    H(ws, 2, 8,  "Nb ventes",       bg=C_DARK)
    ws.row_dimensions[2].height = 26

    widths = [30, 14, 12, 12, 12, 14, 14, 10]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w

    stock_data = [
        ("Écouteurs TWS sans fil",              7.0,  20, 0),
        ("Montre connectée smartwatch",         11.0, 10, 0),
        ("Air Fryer 4-5L",                      33.0,  5, 0),
        ("Batterie externe 20000mAh",            9.0, 15, 0),
        ("Haut-parleur Bluetooth compact",      12.5, 10, 0),
        ("Guirlandes LED USB 5m",                3.5, 20, 0),
        ("Console retro portable",              18.5,  8, 0),
        ("Épilateur IPL",                       22.0,  5, 0),
    ]

    for i, (prod, cout, qty_a, qty_v) in enumerate(stock_data):
        r = i + 3
        alt = C_ALT if i % 2 == 0 else C_WHT
        C(ws, r, 1, prod,   bold=True, bg=alt)
        C(ws, r, 2, cout,   fmt=EUR, al="center", bg=alt)
        C(ws, r, 3, qty_a,  fmt=NB,  al="center", bg=alt)
        C(ws, r, 4, qty_v,  fmt=NB,  al="center", bg=C_YBG)  # saisie manuelle
        # Stock dispo = qté achetée - vendue
        cl = C(ws, r, 5, None, fmt=NB, al="center", bold=True, bg=C_GBG)
        cl.value = f"=C{r}-D{r}"
        # CA et marge viennent du tableau commandes (SUMIF)
        cl2 = C(ws, r, 6, None, fmt=EUR, al="center", bg=alt)
        cl2.value = f"=SUMIF('📋 COMMANDES'!E:E,A{r},'📋 COMMANDES'!G:G)"
        cl3 = C(ws, r, 7, None, fmt=EUR, al="center", bg=C_GBG, bold=True)
        cl3.value = f"=SUMIF('📋 COMMANDES'!E:E,A{r},'📋 COMMANDES'!K:K)"
        cl4 = C(ws, r, 8, None, fmt=NB, al="center", bg=alt)
        cl4.value = f"=COUNTIF('📋 COMMANDES'!E:E,A{r})"
        ws.row_dimensions[r].height = 18

    # Totaux
    r_tot = len(stock_data) + 3
    C(ws, r_tot, 1, "TOTAL", bold=True, bg=C_DARK, fg=C_WHT)
    for col in range(2, 9):
        cl = C(ws, r_tot, col, None, fmt=EUR if col in (2, 6, 7) else NB,
               al="center", bold=True, bg=C_DARK, fg=C_WHT)
        col_l = get_column_letter(col)
        cl.value = f"=SUM({col_l}3:{col_l}{r_tot-1})"
    ws.row_dimensions[r_tot].height = 20

    # Tableau ventes
    r_cmd = r_tot + 3
    MH(ws, r_cmd, 1, 12, "📋  HISTORIQUE DES VENTES", bg=C_BLUE, sz=11, h=24)
    r_cmd += 1

    cmd_headers = [
        "Date", "Produit", "Plateforme", "Prix vente",
        "Frais plat.", "Prix net", "Coût achat", "Marge €", "Marge %",
        "Acheteur", "Adresse livraison", "Statut"
    ]
    for i, h in enumerate(cmd_headers, 1):
        H(ws, r_cmd, i, h, bg=C_BLUE, sz=9)
    ws.row_dimensions[r_cmd].height = 22
    r_cmd += 1

    # 50 lignes vides
    for i in range(50):
        r = r_cmd + i
        alt = C_ALT if i % 2 == 0 else C_WHT
        for col in [1, 2, 3, 4, 5, 7, 10, 11, 12]:
            C(ws, r, col, None, bg=alt)
        # Prix net
        cl = C(ws, r, 6, None, fmt=EUR, al="center", bg=alt)
        cl.value = f"=IF(D{r}=0,\"\",D{r}-E{r})"
        # Marge €
        cl = C(ws, r, 8, None, fmt=EUR, al="center", bg=C_GBG, bold=True)
        cl.value = f"=IF(D{r}=0,\"\",F{r}-G{r})"
        # Marge %
        cl = C(ws, r, 9, None, fmt=PCT, al="center", bg=C_GBG, bold=True)
        cl.value = f"=IF(D{r}=0,\"\",H{r}/D{r}*100)"
        ws.row_dimensions[r].height = 16

    ws.freeze_panes = "A3"

    # Validation plateforme
    from openpyxl.worksheet.datavalidation import DataValidation
    dv = DataValidation(type="list",
        formula1='"Vinted,Le Bon Coin,Anibis,Direct"', allow_blank=True)
    ws.add_data_validation(dv)
    dv.sqref = f"C{r_cmd}:C{r_cmd+49}"

    dv2 = DataValidation(type="list",
        formula1='"Livré,Expédié,En cours,Annulé"', allow_blank=True)
    ws.add_data_validation(dv2)
    dv2.sqref = f"L{r_cmd}:L{r_cmd+49}"


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════
def main():
    wb = openpyxl.Workbook()
    wb.remove(wb.active)

    # Annonces par plateforme
    make_listings_sheet(wb, "lbc",    "lbc_titre", "lbc_desc", "prix_lbc", C_LBC, "LBC")
    make_listings_sheet(wb, "vinted", "vt_titre",  "vt_desc",  "prix_vt",  C_VT,  "Vinted")
    make_listings_sheet(wb, "anibis", "ani_titre", "ani_desc", "prix_ani", C_ANI, "Anibis")

    # Outils opérationnels
    make_action_plan(wb)
    make_checklist(wb)
    make_ops_tracker(wb)

    wb.active = wb["📝 LBC"]

    out = "/home/user/Kit_Annonces_Complet.xlsx"
    wb.save(out)
    print(f"✅  Kit créé : {out}")

if __name__ == "__main__":
    main()
