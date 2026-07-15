import io
import json
import sys
import unittest
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE))
sys.path.insert(0, str(BASE / "leads"))

from collect_partners import parse_elements, write_csv  # noqa: E402
from pricing import price_extra  # noqa: E402
from propose import compose  # noqa: E402

FIXTURE = json.loads((BASE / "tests" / "fixtures" / "overpass_nice.json").read_text(encoding="utf-8"))
NICE = (43.6952, 7.2857)


class TestCollectPartners(unittest.TestCase):
    def test_parse_filtre_et_trie(self):
        leads = parse_elements(FIXTURE, *NICE)
        # 4 exploitables : le hotel sans nom et le restaurant (hors catégories) sont exclus
        self.assertEqual(len(leads), 4)
        self.assertEqual(leads[0]["nom"], "Port Lympia")  # le plus proche d'abord
        self.assertEqual(
            {l["categorie"] for l in leads},
            {"hôtel", "maison d'hôtes", "agence de voyage", "marina"},
        )
        hotel = next(l for l in leads if l["categorie"] == "hôtel")
        self.assertEqual(hotel["site_web"], "https://hotel-du-port.example")
        self.assertEqual(hotel["adresse"], "2 Quai Lunel Nice")
        self.assertLess(hotel["distance_m"], 200)
        self.assertIn("OpenStreetMap", hotel["source"])  # attribution ODbL

    def test_csv(self):
        buf = io.StringIO()
        write_csv(parse_elements(FIXTURE, *NICE), buf)
        lignes = buf.getvalue().strip().splitlines()
        self.assertEqual(len(lignes), 1 + 4)
        self.assertTrue(lignes[0].startswith("nom,categorie,site_web"))


class TestPriceExtra(unittest.TestCase):
    def test_marge_et_arrondi(self):
        self.assertEqual(price_extra(380, marge=0.5), 570)
        self.assertEqual(price_extra(300, marge=0.6), 480)
        self.assertEqual(price_extra(97), 150)  # 97×1.5=145.5 → arrondi 5 sup
        with self.assertRaises(ValueError):
            price_extra(0)


class TestCompose(unittest.TestCase):
    def test_proposition_complete(self):
        md = compose("nice", 4, 1, ["chef", "aperitif"], client="Famille Martin")
        self.assertIn("Famille Martin", md)
        # Oceanis 46.1 (8 couchettes, net 850) choisi : plus petit suffisant
        self.assertIn("Cap Ferrat", md)
        self.assertIn("175 € / personne / jour × 4 pers. × 1 j = **700 €**", md)
        self.assertIn("1060 € / jour × 1 j = **1060 €**", md)
        # Extras : chef 570 (380×1.5, jour×1) + apéritif 290 (180×1.6→arrondi 5, sortie×1)
        self.assertIn("**Total options : 860 €**", md)
        self.assertIn("Option couchettes + options : **1560 €**", md)
        self.assertIn("facture PayPal", md)

    def test_unite_jour_multipliee(self):
        md = compose("nice", 2, 3, ["chef"])
        self.assertIn("570 € / jour × 3", md)

    def test_demande_insatisfiable(self):
        with self.assertRaises(SystemExit):
            compose("nice", 20, 1, [])  # aucun bateau de 20 couchettes
        with self.assertRaises(SystemExit):
            compose("port-inexistant", 2, 1, [])
        with self.assertRaises(SystemExit):
            compose("nice", 2, 1, ["jacuzzi"])  # extra inconnu


if __name__ == "__main__":
    unittest.main()
