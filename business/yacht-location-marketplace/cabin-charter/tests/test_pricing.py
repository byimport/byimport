import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from pricing import price_berths


class TestPriceBerths(unittest.TestCase):
    def test_exemple_nominal(self):
        # Net 850 €, 8 couchettes, défauts (marge 25 %, uplift 1.30)
        p = price_berths(850, 8)
        self.assertEqual(p.prix_bateau_entier_eur, 1060)   # 850 × 1.25 = 1062.5 → 1060
        self.assertEqual(p.prix_couchette_eur, 175)        # 1060/8 × 1.3 = 172.25 → 175
        self.assertEqual(p.ca_plein_eur, 1400)
        self.assertGreater(p.uplift_vs_bateau_entier, 0.25)  # complet ≫ location entière
        self.assertEqual(p.couchettes_seuil_rentabilite, 5)  # 850/175 = 4.86 → 5
        self.assertEqual(p.couchettes_min_depart, 5)         # max(5, 8×0.5=4)

    def test_ca_plein_depasse_toujours_le_bateau_entier(self):
        for net, couch in [(650, 6), (800, 8), (1400, 10), (1600, 12)]:
            p = price_berths(net, couch)
            self.assertGreater(p.ca_plein_eur, p.prix_bateau_entier_eur, (net, couch))

    def test_seuils_bornes_par_la_capacite(self):
        p = price_berths(1000, 2, marge=0.0, uplift_couchette=1.0)
        self.assertLessEqual(p.couchettes_seuil_rentabilite, p.couchettes)
        self.assertLessEqual(p.couchettes_min_depart, p.couchettes)

    def test_remplissage_min_pousse_le_seuil_de_depart(self):
        p = price_berths(850, 8, remplissage_min=0.9)
        self.assertEqual(p.couchettes_min_depart, 8)  # ceil(8×0.9)=8 > rentabilité

    def test_entrees_invalides(self):
        for kwargs in (
            dict(tarif_net_jour_eur=0, couchettes=8),
            dict(tarif_net_jour_eur=800, couchettes=0),
            dict(tarif_net_jour_eur=800, couchettes=8, marge=-0.1),
            dict(tarif_net_jour_eur=800, couchettes=8, uplift_couchette=0.9),
            dict(tarif_net_jour_eur=800, couchettes=8, remplissage_min=0),
        ):
            with self.assertRaises(ValueError, msg=kwargs):
                price_berths(**kwargs)


if __name__ == "__main__":
    unittest.main()
