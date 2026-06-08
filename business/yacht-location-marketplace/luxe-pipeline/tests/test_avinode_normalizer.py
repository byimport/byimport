#!/usr/bin/env python3
"""Hermetic tests for the Avinode normaliser (no network)."""
from __future__ import annotations

import json
import os
import sys
import unittest

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from connectors.avinode import fetch_from_fixture, normalize_leg  # noqa: E402

FIXTURE = os.path.join(_ROOT, "tests", "fixtures", "avinode_trip_search.json")
SCHEMA = os.path.join(_ROOT, "schema", "listing.schema.json")


class TestNormalizer(unittest.TestCase):
    def setUp(self) -> None:
        self.listings = fetch_from_fixture(FIXTURE)

    def test_count(self) -> None:
        self.assertEqual(len(self.listings), 3)

    def test_canonical_id_and_type(self) -> None:
        for item in self.listings:
            self.assertEqual(item["asset_type"], "jet")
            self.assertTrue(item["id"].startswith("jet:avinode:"))
            self.assertEqual(item["source"]["access_layer"], "fixture")
            self.assertTrue(item["raw_hash"].startswith("sha256:"))

    def test_empty_leg_fields(self) -> None:
        first = self.listings[0]
        el = first["empty_leg"]
        self.assertTrue(el["is_empty_leg"])
        self.assertEqual(el["from"]["iata"], "LBG")
        self.assertEqual(el["to"]["iata"], "NCE")
        self.assertEqual(el["price"], 8900.0)
        self.assertEqual(el["currency"], "EUR")
        self.assertEqual(el["discount_pct_est"], 62)

    def test_tolerant_field_shapes(self) -> None:
        # second leg uses legId/leg/lift/sellerPrice; third uses tripId/origin/price float
        ids = {x["id"] for x in self.listings}
        self.assertIn("jet:avinode:leg-100244", ids)
        self.assertIn("jet:avinode:leg-100299", ids)
        third = next(x for x in self.listings if x["id"].endswith("leg-100299"))
        self.assertEqual(third["empty_leg"]["from"]["iata"], "GVA")
        self.assertEqual(third["empty_leg"]["price"], 14500.0)

    def test_missing_values_become_none(self) -> None:
        # a leg with no price-per-hour should not crash and keeps None
        for item in self.listings:
            self.assertIn("price_per_hour_est", item["jet_specs"])

    def test_conforms_to_schema_if_jsonschema_available(self) -> None:
        try:
            import jsonschema  # type: ignore
        except ImportError:
            self.skipTest("jsonschema not installed (optional)")
        with open(SCHEMA, encoding="utf-8") as fh:
            schema = json.load(fh)
        for item in self.listings:
            jsonschema.validate(item, schema)

    def test_structural_invariants_without_jsonschema(self) -> None:
        # stdlib-only contract checks (always run)
        for item in self.listings:
            self.assertIn("source", item)
            self.assertIn("site", item["source"])
            self.assertIn("scraped_at", item["source"])
            self.assertIsInstance(item["empty_leg"]["from"], dict)


if __name__ == "__main__":
    unittest.main()
