"""
Scraper de prix concurrents — LeBonCoin + Anibis + Vinted
+ Recherche fournisseurs Alibaba/1688
Génère un rapport Excel avec opportunités de marge.
"""

import re
import json
import time
import random
import statistics
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# ── Configuration ─────────────────────────────────────────────────────────────

PRODUCTS_TO_SEARCH = [
    {"query": "air fryer",          "cat_lbc": "electromenager", "supplier_price": 33.00, "min_price": 30, "max_price": 200},
    {"query": "ecouteurs bluetooth","cat_lbc": "telephone",       "supplier_price":  7.00, "min_price":  5, "max_price":  80},
    {"query": "montre connectee",   "cat_lbc": "telephone",       "supplier_price": 11.00, "min_price": 10, "max_price": 120},
    {"query": "batterie externe",   "cat_lbc": "telephone",       "supplier_price":  9.00, "min_price":  5, "max_price":  60},
    {"query": "haut parleur bluetooth", "cat_lbc": "multimedia",  "supplier_price": 12.00, "min_price":  8, "max_price":  90},
    {"query": "aspirateur robot",   "cat_lbc": "electromenager",  "supplier_price": 38.00, "min_price": 25, "max_price": 250},
]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "fr-FR,fr;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

RESULTS = {}   # {query: {"lbc": [...], "anibis": [...], "vinted": [...]}}

# ── Helpers ────────────────────────────────────────────────────────────────────

def clean_price(txt):
    """Extrait un float depuis une string de prix."""
    if not txt:
        return None
    txt = txt.replace(" ", "").replace("\xa0", "").replace(" ", "")
    txt = re.sub(r"[^\d,\.]", "", txt).replace(",", ".")
    try:
        v = float(txt)
        return v if v > 0 else None
    except Exception:
        return None

def sleep():
    time.sleep(random.uniform(1.2, 2.5))

# ══════════════════════════════════════════════════════════════════════════════
# SCRAPER LE BON COIN (API interne JSON)
# ══════════════════════════════════════════════════════════════════════════════
LBC_API = "https://api.leboncoin.fr/api/adfinder/v1/search"

LBC_CAT_IDS = {
    "electromenager": "17",
    "telephone": "15",
    "multimedia": "16",
    "informatique": "15",
}

def scrape_lbc(query: str, cat: str, min_p: int, max_p: int) -> list[dict]:
    cat_id = LBC_CAT_IDS.get(cat, "0")
    payload = {
        "filters": {
            "category": {"id": cat_id},
            "keywords": {"text": query, "type": "all"},
            "location": {},
            "ranges": {
                "price": {"min": min_p, "max": max_p}
            }
        },
        "limit": 35,
        "offset": 0,
        "sort_by": "time",
        "sort_order": "desc",
    }
    headers = {**HEADERS,
               "Content-Type": "application/json",
               "Origin": "https://www.leboncoin.fr",
               "Referer": "https://www.leboncoin.fr/"}
    try:
        r = requests.post(LBC_API, json=payload, headers=headers, timeout=12)
        r.raise_for_status()
        data = r.json()
        ads = data.get("ads", [])
        results = []
        for ad in ads:
            price = None
            for attr in ad.get("attributes", []):
                if attr.get("key") == "price":
                    price = clean_price(str(attr.get("value_label", "")))
            if price is None:
                price_raw = ad.get("price", [])
                if price_raw:
                    price = float(price_raw[0]) if price_raw else None
            if price:
                results.append({
                    "titre":    ad.get("subject", "")[:60],
                    "prix":     price,
                    "url":      f"https://www.leboncoin.fr/ad/{ad.get('list_id','')}",
                    "date":     ad.get("first_publication_date", "")[:10],
                    "source":   "LeBonCoin",
                })
        return results
    except Exception as e:
        print(f"  [LBC] Erreur sur '{query}': {e}")
        return []

# ══════════════════════════════════════════════════════════════════════════════
# SCRAPER ANIBIS (HTML)
# ══════════════════════════════════════════════════════════════════════════════
def scrape_anibis(query: str, min_p: int, max_p: int) -> list[dict]:
    url = (f"https://www.anibis.ch/fr/q/{requests.utils.quote(query)}"
           f"?priceFrom={min_p}&priceTo={max_p}")
    try:
        r = requests.get(url, headers=HEADERS, timeout=12)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "lxml")
        results = []

        # Anibis renvoie un JSON embedded dans une balise <script id="__NEXT_DATA__">
        script = soup.find("script", {"id": "__NEXT_DATA__"})
        if script and script.string:
            data = json.loads(script.string)
            # Naviguer dans la structure
            try:
                listings = (data["props"]["pageProps"]["initialState"]
                               ["listing"]["listing"]["Listings"])
                for item in listings[:30]:
                    price = item.get("Price")
                    title = item.get("Title", "")
                    item_id = item.get("Id", "")
                    if price:
                        results.append({
                            "titre":  title[:60],
                            "prix":   float(price),
                            "url":    f"https://www.anibis.ch/fr/d/{item_id}",
                            "date":   item.get("PublishedDate", "")[:10],
                            "source": "Anibis",
                        })
            except (KeyError, TypeError):
                # Fallback: scraping HTML classique
                for card in soup.select("[class*='listing'], [class*='card'], article")[:20]:
                    price_el = card.select_one("[class*='price'], [class*='Price']")
                    title_el = card.select_one("h2, h3, [class*='title']")
                    link_el  = card.select_one("a[href]")
                    if price_el and title_el:
                        price = clean_price(price_el.get_text())
                        if price:
                            results.append({
                                "titre":  title_el.get_text(strip=True)[:60],
                                "prix":   price,
                                "url":    "https://www.anibis.ch" + (link_el["href"] if link_el else ""),
                                "date":   "",
                                "source": "Anibis",
                            })
        return results
    except Exception as e:
        print(f"  [Anibis] Erreur sur '{query}': {e}")
        return []

# ══════════════════════════════════════════════════════════════════════════════
# SCRAPER VINTED (HTML + JSON embarqué)
# ══════════════════════════════════════════════════════════════════════════════
def scrape_vinted(query: str, min_p: int, max_p: int) -> list[dict]:
    url = (f"https://www.vinted.fr/catalog?"
           f"search_text={requests.utils.quote(query)}"
           f"&price_from={min_p}&price_to={max_p}&order=newest_first")
    try:
        r = requests.get(url, headers=HEADERS, timeout=12,
                         cookies={"v_sid": "noop"})
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "lxml")
        results = []

        # Vinted stocke les données dans window.__REDUX_INITIAL_STATE__
        for script in soup.find_all("script"):
            txt = script.string or ""
            if "catalog_items" in txt or "items" in txt:
                match = re.search(r'window\.__INITIAL_STATE__\s*=\s*(\{.*?\});', txt, re.DOTALL)
                if not match:
                    match = re.search(r'window\.__REDUX_INITIAL_STATE__\s*=\s*(\{.*?\});', txt, re.DOTALL)
                if match:
                    try:
                        state = json.loads(match.group(1))
                        items = (state.get("catalog", {}).get("items") or
                                 state.get("items", {}).get("catalogItems", {}).get("byId", {}).values())
                        for item in list(items)[:30]:
                            if isinstance(item, dict):
                                price = item.get("price") or item.get("priceNumeric")
                                title = item.get("title", "")
                                item_id = item.get("id", "")
                                if price:
                                    results.append({
                                        "titre":  str(title)[:60],
                                        "prix":   float(str(price).replace(",", ".")),
                                        "url":    f"https://www.vinted.fr/items/{item_id}",
                                        "date":   "",
                                        "source": "Vinted",
                                    })
                    except Exception:
                        pass

        # Fallback HTML
        if not results:
            for card in soup.select("[data-testid='regular-item-box'], [class*='item-box']")[:20]:
                price_el = card.select_one("[class*='price'], [data-testid*='price']")
                title_el = card.select_one("[class*='title'], [data-testid*='title'], img")
                link_el  = card.select_one("a[href]")
                if price_el:
                    price = clean_price(price_el.get_text())
                    title = title_el.get("alt", title_el.get_text(strip=True)) if title_el else query
                    if price:
                        results.append({
                            "titre":  str(title)[:60],
                            "prix":   price,
                            "url":    "https://www.vinted.fr" + (link_el["href"] if link_el and link_el.get("href","").startswith("/") else ""),
                            "date":   "",
                            "source": "Vinted",
                        })
        return results
    except Exception as e:
        print(f"  [Vinted] Erreur sur '{query}': {e}")
        return []

# ══════════════════════════════════════════════════════════════════════════════
# ANALYSE STATISTIQUE
# ══════════════════════════════════════════════════════════════════════════════
def analyse(listings: list[dict], supplier_cost: float, frais_pct: float = 0.0) -> dict:
    prices = [x["prix"] for x in listings if x["prix"] > 0]
    if not prices:
        return {}
    prices_sorted = sorted(prices)
    median  = statistics.median(prices)
    moyenne = statistics.mean(prices)
    p25     = prices_sorted[len(prices_sorted) // 4]
    p75     = prices_sorted[3 * len(prices_sorted) // 4]
    minimum = min(prices)
    maximum = max(prices)

    # Prix de vente recommandé = légèrement sous la médiane pour vendre vite
    prix_cible = round(median * 0.92, 2)
    frais_vente = prix_cible * frais_pct / 100
    marge_eu = prix_cible - frais_vente - supplier_cost
    marge_pct = marge_eu / prix_cible * 100 if prix_cible else 0

    # Combien de concurrents à battre ?
    concurrents_moins_cher = sum(1 for p in prices if p < prix_cible)

    return {
        "nb_annonces":  len(prices),
        "prix_min":     minimum,
        "prix_max":     maximum,
        "prix_median":  median,
        "prix_moyen":   moyenne,
        "p25":          p25,
        "p75":          p75,
        "prix_cible":   prix_cible,
        "marge_eu":     marge_eu,
        "marge_pct":    marge_pct,
        "cout_total":   supplier_cost,
        "concurrents_sous_cible": concurrents_moins_cher,
        "top3_moins_chers": sorted(listings, key=lambda x: x["prix"])[:3],
        "top3_plus_chers":  sorted(listings, key=lambda x: x["prix"], reverse=True)[:3],
    }

# ══════════════════════════════════════════════════════════════════════════════
# GÉNÉRATION EXCEL
# ══════════════════════════════════════════════════════════════════════════════
C_DARK   = "1F3864"; C_BLUE = "2E75B6"; C_GREEN = "375623"
C_GBG    = "E2EFDA"; C_GHL  = "70AD47"; C_RED   = "C00000"
C_REBG   = "FFE0E0"; C_ORG  = "ED7D31"; C_OBG   = "FCE4D6"
C_YBG    = "FFF2CC"; C_ALT  = "DCE6F1"; C_WHT   = "FFFFFF"
C_GRY    = "F2F2F2"; C_BDR  = "B8CCE4"
EUR = '#,##0.00 "€"'; PCT = '0.0"%"'; NB = '#,##0'

def _brd(c=C_BDR):
    s = Side(style="thin", color=c)
    return Border(left=s, right=s, top=s, bottom=s)

def _c(ws, r, col, v=None, fmt=None, bold=False, bg=None, fg="000000",
       al="left", wrap=False, sz=10):
    cl = ws.cell(row=r, column=col, value=v)
    cl.font = Font(name="Calibri", bold=bold, color=fg, size=sz)
    cl.alignment = Alignment(horizontal=al, vertical="center", wrap_text=wrap)
    cl.border = _brd()
    if fmt: cl.number_format = fmt
    if bg:  cl.fill = PatternFill("solid", fgColor=bg)
    return cl

def _h(ws, r, col, v, bg=C_DARK, fg=C_WHT, sz=10):
    return _c(ws, r, col, v, bold=True, bg=bg, fg=fg, al="center", sz=sz, wrap=True)

def _mhdr(ws, r, c1, c2, v, bg=C_DARK, fg=C_WHT, sz=12, h=26):
    cl = ws.cell(row=r, column=c1, value=v)
    cl.font = Font(name="Calibri", bold=True, color=fg, size=sz)
    cl.fill = PatternFill("solid", fgColor=bg)
    cl.alignment = Alignment(horizontal="center", vertical="center")
    cl.border = _brd()
    ws.merge_cells(start_row=r, start_column=c1, end_row=r, end_column=c2)
    ws.row_dimensions[r].height = h


def make_dashboard_sheet(wb, all_data: dict):
    ws = wb.create_sheet("📊 OPPORTUNITÉS")
    ws.sheet_view.showGridLines = False

    _mhdr(ws, 1, 1, 12,
          f"📊  ANALYSE CONCURRENTIELLE — PRIX MARCHÉ VS FOURNISSEUR  |  {datetime.now().strftime('%d/%m/%Y %H:%M')}",
          sz=13, h=32)

    cols = [
        ("A",  "Produit",                  28, "left"),
        ("B",  "Plateforme",               12, "center"),
        ("C",  "Annonces\ntrouvées",        10, "center"),
        ("D",  "Prix min\nconcurrents",     13, "center"),
        ("E",  "Prix médian\nconcurrents",  14, "center"),
        ("F",  "Prix max\nconcurrents",     13, "center"),
        ("G",  "Coût\nfournisseur",         14, "center"),
        ("H",  "Prix\ncible vente",         13, "center"),
        ("I",  "Marge\nnette (€)",          13, "center"),
        ("J",  "Marge\nnette (%)",          12, "center"),
        ("K",  "Concurrents\nmoins chers",  14, "center"),
        ("L",  "Statut",                    14, "center"),
    ]
    for col_letter, label, w, al in cols:
        col = ord(col_letter) - ord("A") + 1
        _h(ws, 2, col, label)
        ws.column_dimensions[col_letter].width = w
    ws.row_dimensions[2].height = 28

    r = 3
    for prod_query, platforms in all_data.items():
        for platform, stats in platforms.items():
            if not stats:
                continue
            alt = C_ALT if r % 2 == 0 else C_WHT
            marge = stats.get("marge_pct", 0)
            m_bg = C_GBG if marge >= 50 else (C_YBG if marge >= 30 else C_OBG)
            m_fg = C_GREEN if marge >= 50 else (C_ORG if marge >= 30 else C_RED)

            if marge >= 50:   statut, s_bg, s_fg = "✅ Excellent",   C_GBG,  C_GREEN
            elif marge >= 35: statut, s_bg, s_fg = "✔️ Bon",          C_YBG,  "7F6000"
            elif marge >= 20: statut, s_bg, s_fg = "⚠️ Correct",     C_OBG,  C_ORG
            else:             statut, s_bg, s_fg = "❌ Faible",       C_REBG, C_RED

            _c(ws, r, 1,  prod_query.title(), bold=True, bg=alt)
            _c(ws, r, 2,  platform, al="center", bg=alt)
            _c(ws, r, 3,  stats["nb_annonces"], fmt=NB, al="center", bg=alt)
            _c(ws, r, 4,  stats["prix_min"],    fmt=EUR, al="center", bg=alt)
            _c(ws, r, 5,  stats["prix_median"], fmt=EUR, al="center", bg=alt, bold=True)
            _c(ws, r, 6,  stats["prix_max"],    fmt=EUR, al="center", bg=alt)
            _c(ws, r, 7,  stats["cout_total"],  fmt=EUR, al="center", bg=alt)
            _c(ws, r, 8,  stats["prix_cible"],  fmt=EUR, al="center", bg=C_YBG, bold=True)
            _c(ws, r, 9,  stats["marge_eu"],    fmt=EUR, al="center", bg=m_bg, bold=True, fg=m_fg)
            _c(ws, r, 10, stats["marge_pct"],   fmt=PCT, al="center", bg=m_bg, bold=True, fg=m_fg)
            _c(ws, r, 11, stats["concurrents_sous_cible"], fmt=NB, al="center", bg=alt)
            _c(ws, r, 12, statut, al="center", bg=s_bg, bold=True, fg=s_fg)
            r += 1

    ws.freeze_panes = "A3"
    ws.auto_filter.ref = f"A2:L{r}"

    # Légende
    r += 2
    _mhdr(ws, r, 1, 12,
          "💡  Prix cible = médian concurrents × 92%  |  Marge calculée après frais plateforme  |  Coût = achat 1688 + transport estimé",
          bg=C_GRY, fg="555555", sz=9, h=20)
    ws.cell(row=r, column=1).font = Font(name="Calibri", italic=True, color="555555", size=9)


def make_detail_sheet(wb, prod_query: str, platform: str, listings: list[dict], stats: dict):
    safe_name = f"{prod_query[:12].strip()} {platform[:6]}"
    ws = wb.create_sheet(safe_name)
    ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 60
    ws.column_dimensions["B"].width = 14
    ws.column_dimensions["C"].width = 14
    ws.column_dimensions["D"].width = 14

    marge = stats.get("marge_pct", 0)
    color = C_GHL if marge >= 50 else (C_ORG if marge >= 30 else C_RED)

    _mhdr(ws, 1, 1, 4,
          f"🔍  {prod_query.upper()}  —  {platform.upper()}  |  {len(listings)} annonces analysées",
          bg=color, sz=12, h=28)

    # Stats résumé
    kpis = [
        ("Prix minimum concurrents",  stats.get("prix_min"), EUR),
        ("Prix médian concurrents",   stats.get("prix_median"), EUR),
        ("Prix moyen concurrents",    stats.get("prix_moyen"), EUR),
        ("Prix maximum concurrents",  stats.get("prix_max"), EUR),
        ("→ VOTRE PRIX CIBLE",        stats.get("prix_cible"), EUR),
        ("Coût fournisseur total",    stats.get("cout_total"), EUR),
        ("Marge nette par unité",     stats.get("marge_eu"), EUR),
        ("Marge nette %",             stats.get("marge_pct"), PCT),
    ]

    for i, (label, val, fmt) in enumerate(kpis):
        r = i + 2
        is_key = "CIBLE" in label or "Marge" in label
        bg = C_YBG if "CIBLE" in label else (C_GBG if "Marge" in label else C_GRY)
        _c(ws, r, 1, label, bold=is_key, bg=bg)
        _c(ws, r, 2, val, fmt=fmt, al="center", bold=is_key, bg=bg,
           fg=C_GREEN if "Marge" in label else "000000")
        ws.merge_cells(f"C{r}:D{r}")
        ws.row_dimensions[r].height = 18

    # Liste des annonces
    r_hdr = len(kpis) + 3
    _h(ws, r_hdr, 1, "Titre annonce", bg=C_BLUE)
    _h(ws, r_hdr, 2, "Prix (€)", bg=C_BLUE)
    _h(ws, r_hdr, 3, "Votre marge\nsi à ce prix", bg=C_BLUE)
    _h(ws, r_hdr, 4, "Date", bg=C_BLUE)
    ws.row_dimensions[r_hdr].height = 28

    for i, listing in enumerate(sorted(listings, key=lambda x: x["prix"])):
        r = r_hdr + 1 + i
        alt = C_ALT if i % 2 == 0 else C_WHT
        prix = listing["prix"]
        marge_item = ((prix * 0.95) - stats["cout_total"]) / prix * 100 if prix else 0
        m_bg = C_GBG if marge_item >= 50 else (C_YBG if marge_item >= 30 else C_OBG)

        cl = _c(ws, r, 1, listing["titre"], bg=alt, sz=9)
        cl.hyperlink = listing["url"]
        cl.font = Font(name="Calibri", color=C_BLUE, size=9, underline="single")

        _c(ws, r, 2, prix, fmt=EUR, al="center", bg=alt, bold=True)
        _c(ws, r, 3, marge_item, fmt=PCT, al="center", bg=m_bg, bold=True,
           fg=C_GREEN if marge_item >= 50 else (C_ORG if marge_item >= 30 else C_RED))
        _c(ws, r, 4, listing.get("date", ""), al="center", bg=alt, sz=9)
        ws.row_dimensions[r].height = 16

    # Top 3 moins chers = concurrents directs
    r_top = r_hdr + len(listings) + 2
    _mhdr(ws, r_top, 1, 4, "🏁  TOP 3 MOINS CHERS (vos vrais concurrents)", bg=C_DARK, h=22)
    for i, c_item in enumerate(stats.get("top3_moins_chers", [])):
        r = r_top + 1 + i
        prix = c_item["prix"]
        votre_marge = stats["prix_cible"] - stats["cout_total"]
        leur_marge  = prix - stats["cout_total"]
        _c(ws, r, 1, c_item["titre"], bg=C_REBG, sz=9)
        _c(ws, r, 2, prix, fmt=EUR, al="center", bg=C_REBG, bold=True, fg=C_RED)
        _c(ws, r, 3, f"Si vous vendez à {stats['prix_cible']:.0f}€, vous avez +{votre_marge-leur_marge:.0f}€ de marge vs eux", bg=C_REBG, sz=9)
        ws.row_dimensions[r].height = 16


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════
def main():
    print("=" * 60)
    print("  SCRAPER PRIX CONCURRENTS — LBC / ANIBIS / VINTED")
    print("=" * 60)

    all_data   = {}   # {query: {platform: stats}}
    all_listings = {} # {query: {platform: [raw listings]}}

    for prod in PRODUCTS_TO_SEARCH:
        query   = prod["query"]
        cat     = prod["cat_lbc"]
        cost    = prod["supplier_price"]
        min_p   = prod["min_price"]
        max_p   = prod["max_price"]

        print(f"\n📦  '{query}'")
        all_data[query]     = {}
        all_listings[query] = {}

        # — LBC
        print(f"  → LeBonCoin...")
        lbc = scrape_lbc(query, cat, min_p, max_p)
        print(f"     {len(lbc)} annonces")
        all_listings[query]["LeBonCoin"] = lbc
        if lbc:
            all_data[query]["LeBonCoin"] = analyse(lbc, cost)
        sleep()

        # — Anibis
        print(f"  → Anibis...")
        anibis = scrape_anibis(query, min_p, max_p)
        print(f"     {len(anibis)} annonces")
        all_listings[query]["Anibis"] = anibis
        if anibis:
            all_data[query]["Anibis"] = analyse(anibis, cost)
        sleep()

        # — Vinted
        print(f"  → Vinted...")
        vinted = scrape_vinted(query, min_p, max_p)
        print(f"     {len(vinted)} annonces")
        all_listings[query]["Vinted"] = vinted
        if vinted:
            frais = 5.0  # Vinted prend ~5%
            all_data[query]["Vinted"] = analyse(vinted, cost, frais_pct=frais)
        sleep()

    # ── Génération Excel
    print("\n📊  Génération du rapport Excel...")
    wb = openpyxl.Workbook()
    wb.remove(wb.active)

    make_dashboard_sheet(wb, all_data)

    for query, platforms in all_listings.items():
        for platform, listings in platforms.items():
            if listings and query in all_data and platform in all_data[query]:
                make_detail_sheet(
                    wb, query, platform,
                    listings, all_data[query][platform]
                )

    out = "/home/user/Analyse_Concurrents_Marges.xlsx"
    wb.save(out)
    print(f"\n✅  Rapport créé : {out}")

    # ── Résumé console
    print("\n" + "=" * 60)
    print("  RÉSUMÉ — TOP OPPORTUNITÉS PAR MARGE")
    print("=" * 60)
    opps = []
    for query, platforms in all_data.items():
        for plat, stats in platforms.items():
            if stats:
                opps.append((query, plat, stats.get("marge_pct", 0),
                             stats.get("marge_eu", 0), stats.get("prix_cible", 0),
                             stats.get("nb_annonces", 0)))
    for q, p, mp, me, pc, nb in sorted(opps, key=lambda x: x[2], reverse=True)[:10]:
        print(f"  {mp:5.1f}%  {me:+6.2f}€/unit  [{p:12s}]  {q} → cible {pc:.0f}€  ({nb} ann.)")

    return out


if __name__ == "__main__":
    main()
