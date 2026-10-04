#!/usr/bin/env python3
"""Decode the thirdweb DropERC721 claim conditions of a Monkeys Punk style drop.

Reproduces the phase table in ../AUDIT.md straight from Ethereum mainnet, so the
audit can be re-verified at any time without trusting this repository.

Usage:
    python3 read-claim-conditions.py
    python3 read-claim-conditions.py --address 0xABC... --eth-usd 2702.32

Stdlib only. Needs outbound HTTPS; falls back to `curl` when urllib is blocked
by a proxy. Read-only: it never sends a transaction and needs no private key.
"""

import argparse
import datetime as dt
import json
import shutil
import subprocess
import sys
import urllib.request

DEFAULT_ADDRESS = "0xA2571Bf11a38dAB2a9829d0232eb83170E1bDD84"
RPCS = (
    "https://ethereum-rpc.publicnode.com",
    "https://eth.drpc.org",
    "https://cloudflare-eth.com",
)

# Function selectors (keccak256 of the signature, first 4 bytes).
SEL_TOTAL_SUPPLY = "0x18160ddd"  # totalSupply()
SEL_NEXT_ID = "0x3b1475a7"  # nextTokenIdToMint()
SEL_ACTIVE_ID = "0xc68907de"  # getActiveClaimConditionId()
SEL_CONDITION = "0xd637ed59"  # claimCondition() -> (currentStartId, count)
SEL_BY_ID = "0x6f8934f4"  # getClaimConditionById(uint256)

UINT256_MAX = (1 << 256) - 1
UNLIMITED = UINT256_MAX // 2
ZERO32 = bytes(32)


class RpcError(RuntimeError):
    pass


def _post(url: str, payload: str) -> dict:
    try:
        req = urllib.request.Request(
            url, data=payload.encode(), headers={"content-type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=25) as resp:
            return json.load(resp)
    except Exception:
        if not shutil.which("curl"):
            raise
        out = subprocess.run(
            ["curl", "-sS", "-m", "25", "-X", "POST", url,
             "-H", "content-type: application/json", "-d", payload],
            capture_output=True, text=True,
        )
        if out.returncode != 0 or not out.stdout.strip():
            raise RpcError(out.stderr.strip() or "curl produced no output")
        return json.loads(out.stdout)


def eth_call(address: str, data: str) -> str:
    payload = json.dumps({
        "jsonrpc": "2.0", "id": 1, "method": "eth_call",
        "params": [{"to": address, "data": data}, "latest"],
    })
    last = None
    for url in RPCS:
        try:
            res = _post(url, payload)
        except Exception as exc:  # try the next endpoint
            last = exc
            continue
        if "error" in res:
            last = RpcError(res["error"].get("message", "rpc error"))
            continue
        result = res.get("result")
        if result and result != "0x":
            return result
        last = RpcError("empty result (call reverted?)")
    raise RpcError(f"all RPC endpoints failed: {last}")


def word(raw: bytes, index: int) -> int:
    return int.from_bytes(raw[index * 32:(index + 1) * 32], "big")


def decode_condition(hexstr: str) -> dict:
    """Decode one ClaimCondition struct.

    struct ClaimCondition {
        uint256 startTimestamp; uint256 maxClaimableSupply; uint256 supplyClaimed;
        uint256 quantityLimitPerWallet; bytes32 merkleRoot; uint256 pricePerToken;
        address currency; string metadata;
    }

    The struct holds a dynamic member (metadata), so the return data opens with
    an offset to the tuple rather than the tuple itself.
    """
    raw = bytes.fromhex(hexstr[2:])
    base = word(raw, 0) // 32
    meta_at = word(raw, base + 7) // 32 + base
    meta_len = word(raw, meta_at)
    metadata = raw[(meta_at + 1) * 32:(meta_at + 1) * 32 + meta_len]
    return {
        "start": word(raw, base + 0),
        "max_supply": word(raw, base + 1),
        "claimed": word(raw, base + 2),
        "per_wallet": word(raw, base + 3),
        "merkle_root": raw[(base + 4) * 32:(base + 5) * 32],
        "price_wei": word(raw, base + 5),
        "currency": "0x" + raw[(base + 6) * 32 + 12:(base + 7) * 32].hex(),
        "metadata": metadata.decode("utf-8", "replace"),
    }


def quantity(value: int) -> str:
    return "unlim" if value > UNLIMITED else str(value)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--address", default=DEFAULT_ADDRESS, help="drop contract address")
    ap.add_argument("--eth-usd", type=float, default=None,
                    help="ETH/USD rate used to annotate prices (optional)")
    args = ap.parse_args()

    try:
        minted = int(eth_call(args.address, SEL_TOTAL_SUPPLY), 16)
        lazy = int(eth_call(args.address, SEL_NEXT_ID), 16)
        active = int(eth_call(args.address, SEL_ACTIVE_ID), 16)
        raw_cond = bytes.fromhex(eth_call(args.address, SEL_CONDITION)[2:])
    except RpcError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    start_id, count = word(raw_cond, 0), word(raw_cond, 1)
    now = dt.datetime.now(dt.timezone.utc)

    print(f"contract        {args.address}")
    print(f"lazy-minted     {lazy}")
    print(f"minted so far   {minted}")
    print(f"phases          {count} (ids {start_id}..{start_id + count - 1}), active = {active}")
    print(f"now (UTC)       {now:%Y-%m-%d %H:%M}\n")

    head = f"{'id':>2} {'opens (UTC)':<17} {'state':>7} {'supply':>7} {'claimed':>7} " \
           f"{'/wallet':>8} {'price ETH':>12} {'allowlist':>9}"
    if args.eth_usd:
        head += f" {'approx USD':>12}"
    print(head)
    print("-" * len(head))

    total_supply = total_claimed = 0
    for cid in range(start_id, start_id + count):
        try:
            cond = decode_condition(eth_call(args.address, SEL_BY_ID + format(cid, "064x")))
        except RpcError as exc:
            print(f"{cid:>2} <unreadable: {exc}>")
            continue
        opens = dt.datetime.fromtimestamp(cond["start"], dt.timezone.utc)
        eth = cond["price_wei"] / 10 ** 18
        total_supply += cond["max_supply"]
        total_claimed += cond["claimed"]
        row = (f"{cid:>2} {opens:%Y-%m-%d %H:%M} {'PAST' if opens <= now else 'future':>7} "
               f"{quantity(cond['max_supply']):>7} {cond['claimed']:>7} "
               f"{quantity(cond['per_wallet']):>8} {eth:>12.4f} "
               f"{('YES' if cond['merkle_root'] != ZERO32 else 'no'):>9}")
        if args.eth_usd:
            row += "         free" if eth == 0 else f" {eth * args.eth_usd:>12,.0f}"
        print(row)

    print("-" * len(head))
    print(f"sum of phase supplies: {total_supply} | total claimed across phases: {total_claimed}")

    print("\nReading: thirdweb activates the LAST phase whose start timestamp has passed.")
    print("Cheap phases marked PAST with claimed=0 are unreachable until the owner")
    print("replays setClaimConditions(). See ../AUDIT.md section 3.1.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
