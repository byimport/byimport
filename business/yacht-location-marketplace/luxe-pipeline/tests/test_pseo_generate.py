#!/usr/bin/env python3
"""Hermetic tests for the pSEO generator and its anti-doorway guard."""
from __future__ import annotations

import os
import re
import sys
import tempfile
import unittest

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from connectors.avinode import fetch_from_fixture  # noqa: E402
from pseo import generate as G  # noqa: E402
from store import json_store  # noqa: E402

FIXTURE = os.path.join(_ROOT, "tests", "fixtures", "avinode_trip_search.json")


class TestPseo(unittest.TestCase):
    def setUp(self) -> None:
        self.out = tempfile.mkdtemp(prefix="pseo-test-")
        legs_path = os.path.join(self.out, "legs.json")
        json_store.save(fetch_from_fixture(FIXTURE), legs_path)
        self.report = G.generate(self.out, empty_legs_path=legs_path, thin_policy="skip")

    def test_pages_generated(self) -> None:
        self.assertGreater(len(self.report.generated), 10)

    def test_anti_doorway_skips_thin_pages(self) -> None:
        reasons = {pid: reason for pid, reason in self.report.skipped}
        # route with no price and aircraft with no hourly rate must be skipped
        self.assertIn("route:LCY-IBZ", reasons)
        self.assertIn("aircraft:legacy-600", reasons)
        # the skipped page files must NOT exist
        self.assertFalse(os.path.exists(
            os.path.join(self.out, "private-jet-charter/routes/london-to-ibiza/index.html")))

    def test_pillars_exist(self) -> None:
        self.assertTrue(os.path.exists(
            os.path.join(self.out, "private-jet-charter/index.html")))
        self.assertTrue(os.path.exists(
            os.path.join(self.out, "yacht-charter/index.html")))

    def test_empty_legs_injected_into_matching_route(self) -> None:
        page = os.path.join(self.out,
                            "private-jet-charter/routes/paris-to-nice/index.html")
        with open(page, encoding="utf-8") as fh:
            html = fh.read()
        self.assertIn("Live empty legs", html)
        self.assertIn("8900", html)  # the LBG->NCE leg price

    def test_route_has_required_seo_and_cro_elements(self) -> None:
        page = os.path.join(self.out,
                            "private-jet-charter/routes/geneva-to-nice/index.html")
        with open(page, encoding="utf-8") as fh:
            html = fh.read()
        self.assertIn('"@type": "Service"', html)
        self.assertIn('"@type": "FAQPage"', html)
        self.assertIn('class="quote"', html)         # quote form
        self.assertIn("sticky-cta", html)            # mobile sticky CTA
        self.assertIn("wa.me", html)                 # WhatsApp CTA
        self.assertIn("<link rel=\"canonical\"", html)

    def test_per_person_pricing_and_card_payment(self) -> None:
        page = os.path.join(self.out,
                            "private-jet-charter/routes/geneva-to-nice/index.html")
        with open(page, encoding="utf-8") as fh:
            html = fh.read()
        self.assertIn("/ person", html)              # per-person headline (÷ group)
        self.assertIn("total", html)                 # total shown (compliance)
        self.assertIn("guests", html)                # group basis shown
        self.assertIn("Book &amp; pay by card", html)  # card payment CTA

    def test_assets_copied_and_linked(self) -> None:
        css = os.path.join(self.out, "assets", "styles.css")
        self.assertTrue(os.path.isfile(css))
        self.assertGreater(os.path.getsize(css), 500)
        page = os.path.join(self.out, "index.html")
        with open(page, encoding="utf-8") as fh:
            html = fh.read()
        self.assertIn('/assets/styles.css', html)

    def test_margin_split_math(self) -> None:
        from pseo import pricing
        total = 8200
        self.assertEqual(pricing.per_person(total, 10), 820)
        self.assertAlmostEqual(
            pricing.owner_payout(total) + pricing.platform_margin(total), total, places=2)
        # platform keeps the configured margin share
        self.assertAlmostEqual(
            pricing.platform_margin(total), total * pricing.MARGIN_PCT, places=2)

    def test_sitemap_lists_all_generated(self) -> None:
        with open(os.path.join(self.out, "sitemap.xml"), encoding="utf-8") as fh:
            sitemap = fh.read()
        locs = re.findall(r"<loc>", sitemap)
        self.assertEqual(len(locs), len(self.report.generated))

    def test_noindex_policy_emits_stubs(self) -> None:
        out2 = tempfile.mkdtemp(prefix="pseo-test2-")
        rep = G.generate(out2, empty_legs_path=None, thin_policy="noindex")
        thin_dir = os.path.join(out2, "_thin")
        self.assertTrue(os.path.isdir(thin_dir))
        self.assertGreaterEqual(len(os.listdir(thin_dir)), 1)
        self.assertTrue(rep.skipped)


if __name__ == "__main__":
    unittest.main()
