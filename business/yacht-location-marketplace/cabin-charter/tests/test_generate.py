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

    def test_flotte_incoherente_rejetee(self):
        ports, boats = _load()
        boats = boats + [dict(boats[0], id="x", port_id="port-inexistant")]
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(SystemExit):
                build(Path(tmp), ports, boats, marge=0.25, uplift=1.30, base_url="https://example.com")


if __name__ == "__main__":
    unittest.main()
