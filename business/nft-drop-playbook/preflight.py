#!/usr/bin/env python3
"""Pre-launch invariant check for a thirdweb DropERC721 mint.

Reads the drop's live claim conditions and asserts them against what your
website actually promises. Built after auditing a real drop that sold 2 of
10,000 because its price ladder advanced by calendar date instead of by units
sold -- see ../monkeyspunk/AUDIT.md.

Every check here exists because that drop failed it. Run it before launch,
and again after any claim-condition change.

    python3 preflight.py --expect my-drop.json

Exit code 0 = all checks pass, 1 = at least one FAIL. Stdlib only, read-only,
no private key. Needs `curl` or direct HTTPS.
"""

import argparse
import datetime as dt
import json
import shutil
import subprocess
import sys
import urllib.request

NATIVE = "0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"
ZERO32 = bytes(32)
UINT256_MAX = (1 << 256) - 1
UNLIMITED = UINT256_MAX // 2

SEL = {
    "totalSupply":               "0x18160ddd",
    "nextTokenIdToMint":         "0x3b1475a7",
    "getActiveClaimConditionId": "0xc68907de",
    "claimCondition":            "0xd637ed59",
    "getClaimConditionById":     "0x6f8934f4",
}


class Chain:
    def __init__(self, rpcs, address):
        self.rpcs, self.address = rpcs, address

    def _post(self, url, payload):
        try:
            req = urllib.request.Request(
                url, data=payload.encode(), headers={"content-type": "application/json"})
            with urllib.request.urlopen(req, timeout=25) as r:
                return json.load(r)
        except Exception:
            if not shutil.which("curl"):
                raise
            out = subprocess.run(
                ["curl", "-sS", "-m", "25", "-X", "POST", url,
                 "-H", "content-type: application/json", "-d", payload],
                capture_output=True, text=True)
            if out.returncode != 0 or not out.stdout.strip():
                raise RuntimeError(out.stderr.strip() or "no output from curl")
            return json.loads(out.stdout)

    def call(self, data):
        payload = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "eth_call",
                              "params": [{"to": self.address, "data": data}, "latest"]})
        last = None
        for url in self.rpcs:
            try:
                res = self._post(url, payload)
            except Exception as exc:
                last = exc
                continue
            if "error" in res:
                last = RuntimeError(res["error"].get("message", "rpc error"))
                continue
            if res.get("result") not in (None, "0x"):
                return res["result"]
            last = RuntimeError("empty result (reverted?)")
        raise RuntimeError(f"all RPCs failed: {last}")


def word(raw, i):
    return int.from_bytes(raw[i * 32:(i + 1) * 32], "big")


def decode_condition(hexstr):
    raw = bytes.fromhex(hexstr[2:])
    base = word(raw, 0) // 32
    meta_at = word(raw, base + 7) // 32 + base
    mlen = word(raw, meta_at)
    return {
        "start": word(raw, base + 0),
        "max_supply": word(raw, base + 1),
        "claimed": word(raw, base + 2),
        "per_wallet": word(raw, base + 3),
        "merkle_root": raw[(base + 4) * 32:(base + 5) * 32],
        "price_wei": word(raw, base + 5),
        "currency": "0x" + raw[(base + 6) * 32 + 12:(base + 7) * 32].hex(),
        "metadata": raw[(meta_at + 1) * 32:(meta_at + 1) * 32 + mlen].decode("utf-8", "replace"),
    }


class Report:
    def __init__(self):
        self.rows = []

    def add(self, ok, name, detail, why=""):
        self.rows.append((ok, name, detail, why))

    def render(self):
        width = max(len(n) for _, n, _, _ in self.rows)
        failed = 0
        for ok, name, detail, why in self.rows:
            mark = "PASS" if ok else "FAIL"
            print(f"  [{mark}] {name.ljust(width)}  {detail}")
            if not ok:
                failed += 1
                if why:
                    print(f"         {'':{width}}  -> {why}")
        print()
        if failed:
            print(f"{failed} of {len(self.rows)} checks FAILED - do not launch in this state.")
        else:
            print(f"All {len(self.rows)} checks passed.")
        return failed


def run_checks(conds, active_id, minted, lazy, cfg, now):
    """Pure: given decoded chain state + intent, return the Report. Unit-testable."""
    copy = cfg.get("copy_claims", {})
    act = conds[active_id]
    count = len(conds)
    r = Report()

    # 1. The failure that killed the audited drop: several dated phases.
    r.add(count == 1, "single active condition", f"count = {count}",
          "Several conditions means thirdweb advances to whichever one's start date has "
          "passed, regardless of sales. Keep ONE condition and replace it on sell-out.")

    # 2. Any future-dated condition is a landmine that re-prices the mint on a clock.
    future = sorted(cid for cid, c in conds.items() if c["start"] > now)
    r.add(not future, "no future-dated phase",
          "none" if not future else f"ids {future} activate later",
          "A future start date will take over automatically and change the price even if "
          "nothing has sold. Price steps belong to units sold, not to the calendar.")

    # 3. The active phase must actually be open.
    r.add(act["start"] <= now, "active phase is open",
          dt.datetime.fromtimestamp(act["start"], dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
          "The active condition starts in the future, so nobody can mint right now.")

    # 4. Contract price must equal what the page advertises.
    price_eth = act["price_wei"] / 10 ** 18
    want = copy.get("entry_price_eth")
    r.add(want is None or abs(price_eth - want) < 1e-12, "price matches the copy",
          f"chain {price_eth:g} ETH vs copy {want} ETH",
          "Your page advertises one price and the contract charges another. With paid "
          "traffic this is an advertising-accuracy problem, not just lost conversions.")

    # 5/6. 'Allowlist' is a merkle root, not a word on a page -- and a stray root locks everyone out.
    has_root = act["merkle_root"] != ZERO32
    if copy.get("has_allowlist"):
        r.add(has_root, "allowlist is real", "merkleRoot set" if has_root else "merkleRoot is ZERO",
              "The copy promises an allowlist but the phase has no merkle root: it is an "
              "open mint that bots will drain, 1 per wallet.")
    else:
        r.add(not has_root, "no stray allowlist",
              "merkleRoot zero" if not has_root else "merkleRoot SET unexpectedly",
              "A merkle root is set while the copy promises an open mint - only listed "
              "wallets can claim, so the public mint will appear broken.")

    # 7. Supply must be reachable, not stranded.
    planned = cfg.get("total_supply_planned")
    reachable = act["max_supply"] if act["max_supply"] <= UNLIMITED else lazy - minted
    ladder = sum(s["units"] for s in cfg.get("ladder", []))
    if ladder:
        r.add(ladder + minted == planned, "ladder covers the supply",
              f"{ladder} + {minted} minted = {ladder + minted} vs planned {planned}",
              "Your planned steps do not add up to the collection size: some tokens are "
              "unreachable or double-counted.")
    r.add(reachable + minted <= (planned or lazy), "active supply fits",
          f"{reachable} claimable + {minted} minted <= {planned or lazy}",
          "The active condition can mint past the planned collection size.")

    # 8. Metadata must be uploaded, or claims revert.
    r.add(lazy >= (planned or 0), "metadata lazy-minted",
          f"nextTokenIdToMint = {lazy}",
          "Fewer tokens are lazy-minted than planned; claims past that point revert.")

    # 9. Currency sanity.
    known = act["currency"] == NATIVE or act["currency"] == (cfg.get("currency") or "").lower()
    r.add(known, "currency recognised", act["currency"],
          "Unexpected payment currency - buyers would need that exact ERC-20.")

    return r


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--expect", required=True, help="JSON file describing the intended drop")
    args = ap.parse_args()
    cfg = json.load(open(args.expect))

    chain = Chain(cfg.get("rpcs") or ["https://ethereum-rpc.publicnode.com",
                                      "https://eth.drpc.org"], cfg["contract"])
    now = int(dt.datetime.now(dt.timezone.utc).timestamp())
    copy = cfg.get("copy_claims", {})

    minted = int(chain.call(SEL["totalSupply"]), 16)
    lazy = int(chain.call(SEL["nextTokenIdToMint"]), 16)
    active_id = int(chain.call(SEL["getActiveClaimConditionId"]), 16)
    cc = bytes.fromhex(chain.call(SEL["claimCondition"])[2:])
    start_id, count = word(cc, 0), word(cc, 1)

    conds = {}
    for cid in range(start_id, start_id + count):
        conds[cid] = decode_condition(
            chain.call(SEL["getClaimConditionById"] + format(cid, "064x")))
    act = conds[active_id]

    act = conds[active_id]
    print(f"\ncontract {cfg['contract']}")
    print(f"minted {minted} / lazy-minted {lazy} | {count} condition(s), active id {active_id}\n")

    r = run_checks(conds, active_id, minted, lazy, cfg, now)
    failed = r.render()

    cap = act["max_supply"] if act["max_supply"] <= UNLIMITED else None
    pct = (act["claimed"] / cap * 100) if cap else 0.0
    print(f"\nprogress on the active phase: {act['claimed']}/{cap if cap else 'unlimited'}"
          + (f" ({pct:.2f}%)" if cap else ""))

    return 1 if failed else 0



if __name__ == "__main__":
    sys.exit(main())
