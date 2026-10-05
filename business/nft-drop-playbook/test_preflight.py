"""Tests for preflight.run_checks -- proves the checks pass on a sound config
and fail on each specific mistake, without needing a live contract.

    python3 -m pytest test_preflight.py -q
"""

import datetime as dt

from preflight import NATIVE, ZERO32, run_checks

NOW = int(dt.datetime(2026, 10, 5, 12, 0, tzinfo=dt.timezone.utc).timestamp())

GOOD_CFG = {
    "total_supply_planned": 10000,
    "copy_claims": {"entry_price_eth": 0.005, "has_allowlist": False},
    "ladder": [
        {"units": 8697}, {"units": 700}, {"units": 300}, {"units": 250},
        {"units": 45}, {"units": 5}, {"units": 1},
    ],
}


def condition(**over):
    base = {
        "start": 0, "max_supply": 8697, "claimed": 0, "per_wallet": 5,
        "merkle_root": ZERO32, "price_wei": 5 * 10 ** 15,
        "currency": NATIVE, "metadata": "ipfs://x/0",
    }
    base.update(over)
    return base


def failures(conds, active_id, cfg=None, minted=2, lazy=10000):
    r = run_checks(conds, active_id, minted, lazy, cfg or GOOD_CFG, NOW)
    return {name for ok, name, _, _ in r.rows if not ok}


def test_sound_config_passes_everything():
    assert failures({8: condition()}, 8) == set()


def test_multiple_dated_phases_is_caught():
    # The exact shape that stranded 9,998 tokens on the audited drop.
    conds = {
        0: condition(start=NOW - 86400 * 30, max_supply=1000, price_wei=0),
        1: condition(start=NOW - 86400 * 20, max_supply=7699),
        2: condition(start=NOW + 86400, max_supply=700, price_wei=5 * 10 ** 16),
    }
    bad = failures(conds, 1)
    assert "single active condition" in bad
    assert "no future-dated phase" in bad


def test_price_divergence_from_copy_is_caught():
    bad = failures({8: condition(price_wei=5 * 10 ** 17)}, 8)   # charges 0.5, copy says 0.005
    assert "price matches the copy" in bad


def test_promised_allowlist_without_merkle_root_is_caught():
    cfg = dict(GOOD_CFG, copy_claims={"entry_price_eth": 0.005, "has_allowlist": True})
    assert "allowlist is real" in failures({8: condition()}, 8, cfg)
    # ...and a real root satisfies it
    assert failures({8: condition(merkle_root=b"\x11" * 32)}, 8, cfg) == set()


def test_stray_merkle_root_on_an_open_mint_is_caught():
    # The inverse mistake: copy promises open minting, contract gates it.
    assert "no stray allowlist" in failures({8: condition(merkle_root=b"\x11" * 32)}, 8)


def test_phase_not_yet_open_is_caught():
    bad = failures({8: condition(start=NOW + 3600)}, 8)
    assert "active phase is open" in bad
    assert "no future-dated phase" in bad


def test_ladder_that_does_not_sum_to_the_collection_is_caught():
    cfg = dict(GOOD_CFG, ladder=[{"units": 5000}])
    assert "ladder covers the supply" in failures({8: condition()}, 8, cfg)


def test_missing_lazy_minted_metadata_is_caught():
    assert "metadata lazy-minted" in failures({8: condition()}, 8, lazy=500)


def test_unexpected_currency_is_caught():
    usdc = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"
    assert "currency recognised" in failures({8: condition(currency=usdc)}, 8)
    # ...unless the config declares it
    cfg = dict(GOOD_CFG, currency=usdc)
    assert failures({8: condition(currency=usdc)}, 8, cfg) == set()


def test_active_supply_cannot_exceed_planned_collection():
    assert "active supply fits" in failures({8: condition(max_supply=9999)}, 8)
