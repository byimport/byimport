import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from generate import build

HERE = Path(__file__).resolve().parents[1]


def _load():
    ports = json.loads((HERE / "data" / "ports_europe.json").read_text(encoding="utf-8"))["ports"]
    boats = json.loads((HERE / "data" / "flotte_fixture.json").read_text(encoding="utf-8"))["bateaux"]
    return ports, boats


def _extras():
    return json.loads((HERE / "data" / "extras.json").read_text(encoding="utf-8"))["extras"]


class TestGenerate(unittest.TestCase):
    def test_build_complet(self):
        ports, boats = _load()
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            report = build(out, ports, boats, marge=0.25, uplift=1.30, base_url="https://example.com")

            ports_avec_bateaux = {b["port_id"] for b in boats}
            # Anti-doorway : une page par port AVEC bateau, aucune pour les autres
            self.assertEqual(sorted(report["generated"]), sorted(ports_avec_bateaux))
            self.assertEqual(
                len(report["skipped"]), len(ports) - len(ports_avec_bateaux)
            )
            self.assertEqual(
                {p.stem for p in (out / "port").glob("*.html")}, ports_avec_bateaux
            )

            # L'index référence tous les ports (avec page ou « ouverture prochaine »)
            index = (out / "index.html").read_text(encoding="utf-8")
            for port in ports:
                self.assertIn(port["nom"].split(" — ")[0], index)

            # Une page port contient localisation + les deux prix
            nice = (out / "port" / "nice.html").read_text(encoding="utf-8")
            self.assertIn("google.com/maps?q=43.6952,7.2857", nice)
            self.assertIn("/ couchette", nice)
            self.assertIn("/ bateau", nice)

            # Le sitemap ne liste que les pages réellement générées
            sitemap = (out / "sitemap.xml").read_text(encoding="utf-8")
            self.assertEqual(sitemap.count("<loc>"), 1 + len(report["generated"]))
            for pid in report["skipped"]:
                self.assertNotIn(f"/port/{pid}.html", sitemap)

    def test_extras_et_photos(self):
        ports, boats = _load()
        boats = [dict(b) for b in boats]
        # Un bateau avec photos, les autres sans → galerie vs « photos à venir »
        boats[0]["photos"] = [{"src": "photos/cap-ferrat-1.jpg", "alt": "Cap Ferrat au mouillage"}]
        port_du_bateau = boats[0]["port_id"]
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            build(out, ports, boats, marge=0.25, uplift=1.30,
                  base_url="https://example.com", extras=_extras())
            page = (out / "port" / f"{port_du_bateau}.html").read_text(encoding="utf-8")
            self.assertIn("photos/cap-ferrat-1.jpg", page)          # galerie réelle
            self.assertIn("en cours de shooting", page)             # placeholder honnête
            self.assertIn("Chef cuisinier à bord", page)            # upsell extras
            self.assertIn("570 €", page)                            # 380 × 1.5 arrondi 5

    def test_flotte_incoherente_rejetee(self):
        ports, boats = _load()
        boats = boats + [dict(boats[0], id="x", port_id="port-inexistant")]
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(SystemExit):
                build(Path(tmp), ports, boats, marge=0.25, uplift=1.30, base_url="https://example.com")


if __name__ == "__main__":
    unittest.main()
