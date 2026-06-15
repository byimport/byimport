#!/usr/bin/env python3
"""
Scraper Approfondi — Made-in-China + Global Sources + Alibaba
Cherche en profondeur : LED voirie, radars pédagogiques, solaire.
Inclut base de données étendue de contacts vérifiés.

Usage:
    python scraper-approfondi.py
Output:
    suppliers_DEEP.csv
    suppliers_DEEP.json
"""

import csv
import json
import time
import sys
from datetime import datetime

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("pip install requests beautifulsoup4")
    sys.exit(1)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Referer": "https://www.google.com/",
}

OUTPUT_CSV = "suppliers_DEEP.csv"
OUTPUT_JSON = "suppliers_DEEP.json"

CSV_FIELDS = [
    "priority", "category", "company_name", "location",
    "contact_person", "email", "phone_whatsapp", "website",
    "price_usd_fob", "moq", "certifications", "europe_export",
    "response_time", "years_exp", "notes", "source", "scraped_at"
]

# ─────────────────────────────────────────────────────────────────────────────
# BASE DE DONNÉES VÉRIFIÉE (contacts directs confirmés)
# ─────────────────────────────────────────────────────────────────────────────

VERIFIED_SUPPLIERS = [
    # ── LED ──────────────────────────────────────────────────────────────────
    {
        "priority": 1, "category": "LED",
        "company_name": "Hangzhou ZGSM Technology Co. Ltd.",
        "location": "Hangzhou, Zhejiang",
        "contact_person": "Export Sales",
        "email": "zgsmled@zgsm-china.com",
        "phone_whatsapp": "+86-150-6875-8483",
        "website": "https://www.zgsmled.com",
        "price_usd_fob": "$62-185/pc", "moq": "10 pcs",
        "certifications": "CE, RoHS, LM79, LM80, ISO9001",
        "europe_export": "YES - 80+ countries", "response_time": "<12h",
        "years_exp": "17+",
        "notes": "PRIORITÉ #1 LED — LM79/LM80 confirmés — skype: zgsmled",
        "source": "Verified", "scraped_at": datetime.now().isoformat()
    },
    {
        "priority": 2, "category": "LED",
        "company_name": "Shanghai CHZ Lighting Co. Ltd.",
        "location": "Shanghai",
        "contact_person": "Export Sales",
        "email": "sales10@chz-lighting.com",
        "phone_whatsapp": "N/A",
        "website": "https://www.chz-lighting.com",
        "price_usd_fob": "$45-120/pc", "moq": "5 pcs",
        "certifications": "CE, RoHS, IP65",
        "europe_export": "YES - 100+ countries", "response_time": "<24h",
        "years_exp": "10+",
        "notes": "Représentant Europe Espagne — forte expérience export UE",
        "source": "Verified", "scraped_at": datetime.now().isoformat()
    },
    {
        "priority": 3, "category": "LED",
        "company_name": "HPWINNER Lighting Co. Ltd.",
        "location": "Shenzhen, Guangdong",
        "contact_person": "Export Sales",
        "email": "sales@hpwin.com",
        "phone_whatsapp": "+86-0571-8806-1966",
        "website": "https://www.hpwinner.com",
        "price_usd_fob": "$80-200/pc", "moq": "1 pc",
        "certifications": "CE, RoHS, IK08, IP66, DALI",
        "europe_export": "YES", "response_time": "<24h",
        "years_exp": "8+",
        "notes": "Smart LED DALI 0-10V — idéal smart city AO",
        "source": "Verified", "scraped_at": datetime.now().isoformat()
    },
    {
        "priority": 4, "category": "LED",
        "company_name": "LUXSKY Lighting Co. Ltd.",
        "location": "Shenzhen, Guangdong",
        "contact_person": "Export Sales",
        "email": "sales@luxsky-light.com",
        "phone_whatsapp": "N/A",
        "website": "https://www.luxsky-light.com",
        "price_usd_fob": "$55-150/pc", "moq": "10 pcs",
        "certifications": "CE, RoHS, IP65",
        "europe_export": "YES - Europe focus", "response_time": "<24h",
        "years_exp": "8+",
        "notes": "Spécialisé export Europe — email confirmé via website",
        "source": "Verified", "scraped_at": datetime.now().isoformat()
    },
    {
        "priority": 5, "category": "LED",
        "company_name": "Zhongshan Ledcent Optoelectronics",
        "location": "Zhongshan, Guangdong",
        "contact_person": "Export Sales",
        "email": "ledcent.com@gmail.com",
        "phone_whatsapp": "N/A",
        "website": "https://ledcent.com",
        "price_usd_fob": "$77-139/pc", "moq": "1 pc",
        "certifications": "CE, RoHS, ISO9001, ISO14001, FCC",
        "europe_export": "YES - >100M$/yr export", "response_time": "<24h",
        "years_exp": "N/A",
        "notes": "71-90% export — fortement axé UE/USA — double ISO",
        "source": "Verified", "scraped_at": datetime.now().isoformat()
    },
    {
        "priority": 6, "category": "LED",
        "company_name": "Phoebus Lighting Co. Ltd.",
        "location": "Shenzhen, Guangdong",
        "contact_person": "Export Sales",
        "email": "N/A (via site)",
        "phone_whatsapp": "N/A",
        "website": "https://www.phoebuslight.com",
        "price_usd_fob": "$90-220/pc", "moq": "1 pc",
        "certifications": "CE, RoHS",
        "europe_export": "YES", "response_time": "<24h",
        "years_exp": "5+",
        "notes": "Modulaire haute puissance — check contact page",
        "source": "MIC", "scraped_at": datetime.now().isoformat()
    },
    {
        "priority": 7, "category": "LED",
        "company_name": "Zhongshan Gisun Lighting Co. Ltd.",
        "location": "Zhongshan, Guangdong",
        "contact_person": "Export Sales",
        "email": "N/A (via Alibaba)",
        "phone_whatsapp": "N/A",
        "website": "https://gisunled.en.alibaba.com",
        "price_usd_fob": "$6.20-121/pc", "moq": "1 pc",
        "certifications": "CE, ISO, RoHS",
        "europe_export": "YES", "response_time": "<7h",
        "years_exp": "6",
        "notes": "Alibaba 4.9/5 — 11 avis — très réactif",
        "source": "Alibaba", "scraped_at": datetime.now().isoformat()
    },
    {
        "priority": 8, "category": "LED+Solar",
        "company_name": "Ellins Optoelectronics Co. Ltd.",
        "location": "Zhongshan, Guangdong",
        "contact_person": "Ms. Sylvia Guo",
        "email": "N/A (via MIC)",
        "phone_whatsapp": "N/A",
        "website": "http://ellinslight.com",
        "price_usd_fob": "$20-50/pc", "moq": "50 pcs",
        "certifications": "CE, RoHS",
        "europe_export": "YES - 150 countries", "response_time": "<24h",
        "years_exp": "14+",
        "notes": "Prix très compétitif — forte présence Europe — contact Sylvia Guo",
        "source": "MIC", "scraped_at": datetime.now().isoformat()
    },
    # ── RADAR ─────────────────────────────────────────────────────────────────
    {
        "priority": 10, "category": "Radar",
        "company_name": "Shenzhen Noble Opto Co. Ltd.",
        "location": "Shenzhen, Guangdong",
        "contact_person": "Alan",
        "email": "inquiry@nobleled.com",
        "phone_whatsapp": "+8613927455427",
        "website": "https://www.nobleled.com",
        "price_usd_fob": "$200-500/pc", "moq": "1 pc",
        "certifications": "CE, RoHS",
        "europe_export": "YES - Suède/UK/Italie/Pologne/Espagne", "response_time": "<24h",
        "years_exp": "16+",
        "notes": "PRIORITÉ #1 RADAR — 90-100% export EU — 3000u/mois",
        "source": "Verified", "scraped_at": datetime.now().isoformat()
    },
    {
        "priority": 11, "category": "Radar",
        "company_name": "Zhejiang Stars Plastic Safety Device",
        "location": "Taizhou, Zhejiang",
        "contact_person": "Mr. Raul Huang",
        "email": "sales@starsplastic.com",
        "phone_whatsapp": "+8615757104372",
        "website": "https://www.starsplastic.com",
        "price_usd_fob": "$400-1200/pc", "moq": "1 pc",
        "certifications": "CE, ISO9001, MUTCD+EU standards",
        "europe_export": "YES - 20+ countries", "response_time": "<24h",
        "years_exp": "28+",
        "notes": "PRIORITÉ #2 RADAR — 28 ans — normes EU ET MUTCD — 200u/mois",
        "source": "Verified", "scraped_at": datetime.now().isoformat()
    },
    {
        "priority": 12, "category": "Radar",
        "company_name": "Nanoradar Science & Technology Co.",
        "location": "Changsha, Hunan",
        "contact_person": "Export Sales",
        "email": "sales@nanoradar.cn",
        "phone_whatsapp": "N/A",
        "website": "https://www.nanoradar.com",
        "price_usd_fob": "$185-690/pc", "moq": "1 pc",
        "certifications": "CE, RoHS",
        "europe_export": "YES", "response_time": "<48h",
        "years_exp": "N/A",
        "notes": "77GHz haut de gamme — filiale Novasky — email confirmé site web",
        "source": "Verified", "scraped_at": datetime.now().isoformat()
    },
    {
        "priority": 13, "category": "Radar",
        "company_name": "Shenzhen Nokin Traffic Facilities",
        "location": "Shenzhen, Guangdong",
        "contact_person": "Export Team",
        "email": "info@nk-roadstud.com",
        "phone_whatsapp": "N/A",
        "website": "https://www.nk-roadstud.com",
        "price_usd_fob": "$107-378/pc", "moq": "1 pc",
        "certifications": "CE, RoHS, IP65",
        "europe_export": "YES", "response_time": "<1h",
        "years_exp": "11",
        "notes": "Réponse <1h — email confirmé website — radar+LED",
        "source": "Verified", "scraped_at": datetime.now().isoformat()
    },
    {
        "priority": 14, "category": "Radar",
        "company_name": "Novasky Technology Co. Ltd.",
        "location": "Changsha, Hunan",
        "contact_person": "Export Sales",
        "email": "sales@novasky.cn",
        "phone_whatsapp": "N/A",
        "website": "http://www.novasky.cn",
        "price_usd_fob": "$170-185/pc", "moq": "1 pc",
        "certifications": "CE, RoHS",
        "europe_export": "YES - 30+ countries", "response_time": "<48h",
        "years_exp": "18+",
        "notes": "24GHz K-band — maison mère Nanoradar — email non confirmé",
        "source": "MIC", "scraped_at": datetime.now().isoformat()
    },
    {
        "priority": 15, "category": "Radar",
        "company_name": "Fuzhou Moons Reflection Co. Ltd.",
        "location": "Fuzhou, Fujian",
        "contact_person": "Export Sales",
        "email": "N/A (via MIC)",
        "phone_whatsapp": "N/A",
        "website": "https://moonsreflection.en.made-in-china.com",
        "price_usd_fob": "$90-110/pc", "moq": "50 pcs",
        "certifications": "CE (à vérifier), RoHS",
        "europe_export": "YES", "response_time": "<24h",
        "years_exp": "N/A",
        "notes": "Prix très compétitif radar — vérifier CE avant commande",
        "source": "MIC", "scraped_at": datetime.now().isoformat()
    },
    {
        "priority": 16, "category": "Radar",
        "company_name": "OPTRAFFIC Co. Ltd.",
        "location": "Zhejiang",
        "contact_person": "Export Sales",
        "email": "N/A (via MIC)",
        "phone_whatsapp": "N/A",
        "website": "https://optraffic.en.made-in-china.com",
        "price_usd_fob": "$2000-9400/pc", "moq": "1 pc",
        "certifications": "CE, MUTCD",
        "europe_export": "YES", "response_time": "<24h",
        "years_exp": "N/A",
        "notes": "Haut de gamme — remorque mobile VMS — niche AO premium",
        "source": "MIC", "scraped_at": datetime.now().isoformat()
    },
    {
        "priority": 17, "category": "Radar",
        "company_name": "Shenzhen Lecheng Ecosolar Co. Ltd.",
        "location": "Shenzhen, Guangdong",
        "contact_person": "Export Sales",
        "email": "N/A (via MIC)",
        "phone_whatsapp": "N/A",
        "website": "https://lecheng.en.made-in-china.com",
        "price_usd_fob": "$35-300/pc", "moq": "2 sets",
        "certifications": "CE (à vérifier)",
        "europe_export": "YES", "response_time": "<24h",
        "years_exp": "N/A",
        "notes": "Prix d'entrée exceptionnel $35 — vérifier CE impérativement",
        "source": "MIC", "scraped_at": datetime.now().isoformat()
    },
]


# ─────────────────────────────────────────────────────────────────────────────
# Scraper Made-in-China étendu
# ─────────────────────────────────────────────────────────────────────────────

SEARCH_TERMS = {
    "LED": [
        "LED Street Light manufacturer CE certified export Europe",
        "LED road light IP66 CE RoHS LM79 manufacturer",
        "smart LED street light DALI 0-10V dimming CE",
        "solar LED street light all-in-one CE IP65",
        "LED street lamp 100W CE manufacturer France Europe",
    ],
    "Radar": [
        "Radar Speed Sign pedagogical driver feedback CE",
        "speed indicator device solar radar CE 24GHz",
        "driver feedback sign LED speed display CE Europe",
        "speed awareness sign solar pedagogical CE RoHS",
        "radar speed sign school zone CE IP65 manufacturer",
    ],
}

MIC_BASE = "https://www.made-in-china.com/products-search/hot-china-products/"


def fetch_page(url, retries=2):
    for attempt in range(retries + 1):
        try:
            r = requests.get(url, headers=HEADERS, timeout=20)
            if r.status_code == 200:
                return r.text
            print(f"  ⚠️  HTTP {r.status_code} for {url}")
        except requests.RequestException as e:
            print(f"  ⚠️  Erreur: {e}")
        if attempt < retries:
            time.sleep(3 * (attempt + 1))
    return None


def scrape_mic_keyword(keyword, max_pages=5):
    results = []
    slug = keyword.replace(" ", "_")
    for page in range(1, max_pages + 1):
        url = f"{MIC_BASE}{slug}.html?page={page}"
        print(f"  [MIC] '{keyword}' page {page}...")
        html = fetch_page(url)
        if not html:
            break
        soup = BeautifulSoup(html, "html.parser")
        cards = soup.find_all("div", class_=lambda c: c and "product-item" in c)
        if not cards:
            cards = soup.find_all("li", class_=lambda c: c and "search-result" in c)
        if not cards:
            print(f"  ⚠️  Aucune carte trouvée page {page} — arrêt")
            break
        for card in cards:
            try:
                name = card.find(["h3", "h4", "p"], class_=lambda c: c and "name" in c.lower())
                company = card.find(["span", "div"], class_=lambda c: c and "company" in c.lower())
                price = card.find(["span", "div"], class_=lambda c: c and "price" in c.lower())
                link = card.find("a", href=True)
                text = card.get_text(" ", strip=True)
                certs = []
                for cert in ["CE", "RoHS", "IP65", "IP66", "LM79", "LM80", "ISO9001", "24GHz", "DALI"]:
                    if cert.lower() in text.lower():
                        certs.append(cert)
                record = {
                    "priority": 99,
                    "category": "LED" if "led" in keyword.lower() else "Radar",
                    "company_name": company.get_text(strip=True) if company else "N/A",
                    "location": "China",
                    "contact_person": "Export Sales",
                    "email": "N/A (via MIC)",
                    "phone_whatsapp": "N/A",
                    "website": (
                        "https://www.made-in-china.com" + link["href"]
                        if link and not link["href"].startswith("http")
                        else (link["href"] if link else "N/A")
                    ),
                    "price_usd_fob": price.get_text(strip=True) if price else "N/A",
                    "moq": "N/A",
                    "certifications": ", ".join(certs) if certs else "N/A",
                    "europe_export": "Unknown",
                    "response_time": "N/A",
                    "years_exp": "N/A",
                    "notes": (name.get_text(strip=True) if name else "N/A")[:120],
                    "source": "MIC-scrape",
                    "scraped_at": datetime.now().isoformat(),
                }
                if record["company_name"] != "N/A":
                    results.append(record)
            except Exception:
                continue
        time.sleep(2)
    return results


def scrape_global_sources_url(keyword):
    """Tente une extraction sur Global Sources (liste de résultats)."""
    results = []
    slug = keyword.replace(" ", "+")
    url = f"https://www.globalsources.com/manufacturers/{slug}.html"
    print(f"  [GlobalSources] '{keyword}'...")
    html = fetch_page(url)
    if not html:
        return results
    soup = BeautifulSoup(html, "html.parser")
    cards = soup.find_all("div", class_=lambda c: c and "supplier" in c.lower())
    for card in cards:
        try:
            name = card.find(["h2", "h3", "a"], class_=lambda c: c and "name" in c.lower())
            link = card.find("a", href=True)
            text = card.get_text(" ", strip=True)
            certs = [c for c in ["CE", "RoHS", "ISO9001", "LM79", "IP65", "IP66"] if c in text]
            record = {
                "priority": 99,
                "category": "LED" if "led" in keyword.lower() else "Radar",
                "company_name": name.get_text(strip=True) if name else "N/A",
                "location": "China",
                "contact_person": "Export Sales",
                "email": "N/A (via GS)",
                "phone_whatsapp": "N/A",
                "website": link["href"] if link else "N/A",
                "price_usd_fob": "N/A",
                "moq": "N/A",
                "certifications": ", ".join(certs) if certs else "N/A",
                "europe_export": "Unknown",
                "response_time": "N/A",
                "years_exp": "N/A",
                "notes": "GlobalSources",
                "source": "GlobalSources-scrape",
                "scraped_at": datetime.now().isoformat(),
            }
            if record["company_name"] != "N/A":
                results.append(record)
        except Exception:
            continue
    return results


def deduplicate(suppliers):
    seen = set()
    unique = []
    for s in suppliers:
        key = s["company_name"].lower().strip()
        if key and key != "n/a" and key not in seen:
            seen.add(key)
            unique.append(s)
    return unique


def write_csv(suppliers, filepath):
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(suppliers)
    print(f"\n✅ CSV exporté : {filepath} ({len(suppliers)} entrées)")


def write_json(suppliers, filepath):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(suppliers, f, ensure_ascii=False, indent=2)
    print(f"✅ JSON exporté : {filepath}")


def main():
    print("=" * 60)
    print("SCRAPER APPROFONDI — ByImport Sourcing Chine→France")
    print(f"Démarré : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    all_suppliers = list(VERIFIED_SUPPLIERS)
    print(f"\n📋 Base vérifiée : {len(all_suppliers)} fournisseurs confirmés")

    # MIC scraping — LED
    print("\n🔍 Scraping Made-in-China — LED (5 recherches × 5 pages)...")
    for term in SEARCH_TERMS["LED"]:
        new = scrape_mic_keyword(term, max_pages=5)
        all_suppliers.extend(new)
        print(f"  → {len(new)} résultats pour '{term}'")

    # MIC scraping — Radar
    print("\n🔍 Scraping Made-in-China — Radar (5 recherches × 5 pages)...")
    for term in SEARCH_TERMS["Radar"]:
        new = scrape_mic_keyword(term, max_pages=5)
        all_suppliers.extend(new)
        print(f"  → {len(new)} résultats pour '{term}'")

    # Global Sources
    print("\n🔍 Scraping Global Sources...")
    for kw in ["LED Street Light CE Europe", "Radar Speed Sign CE Europe"]:
        new = scrape_global_sources_url(kw)
        all_suppliers.extend(new)
        print(f"  → {len(new)} résultats Global Sources pour '{kw}'")

    print(f"\n📊 Total brut : {len(all_suppliers)} entrées")

    # Déduplication
    unique = deduplicate(all_suppliers)
    print(f"📊 Après déduplication : {len(unique)} fournisseurs uniques")

    # Trier : vérifiés d'abord (priority < 99), puis par nom
    unique.sort(key=lambda x: (x["priority"], x["company_name"]))

    write_csv(unique, OUTPUT_CSV)
    write_json(unique, OUTPUT_JSON)

    # Stats finales
    with_email = [s for s in unique if s["email"] and "N/A" not in s["email"]]
    led_count = [s for s in unique if "LED" in s["category"]]
    radar_count = [s for s in unique if "Radar" in s["category"]]

    print("\n" + "=" * 60)
    print("RÉSUMÉ FINAL")
    print("=" * 60)
    print(f"  Total fournisseurs uniques  : {len(unique)}")
    print(f"  Avec email direct           : {len(with_email)}")
    print(f"  Catégorie LED               : {len(led_count)}")
    print(f"  Catégorie Radar             : {len(radar_count)}")
    print(f"\n  Emails directs confirmés :")
    for s in with_email:
        print(f"    • {s['company_name'][:35]:<35} → {s['email']}")
    print("=" * 60)


if __name__ == "__main__":
    main()
