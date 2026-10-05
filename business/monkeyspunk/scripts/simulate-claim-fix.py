import json,subprocess,sys
sys.path.insert(0,'.')
from keccak import sel

RPC="https://ethereum-rpc.publicnode.com"
NFT="0xA2571Bf11a38dAB2a9829d0232eb83170E1bDD84"
OWNER="0x0f4d3ea5525046254a2b58c23f694eb1c781536d"
NATIVE="0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"

def h(n): return format(n,'064x')
def addr(a): return h(int(a,16))

def encode_set_claim_conditions(conds, reset):
    """setClaimConditions(ClaimCondition[],bool) — ClaimCondition holds a dynamic
    string, so array elements are encoded by offset."""
    selector = sel("setClaimConditions((uint256,uint256,uint256,uint256,bytes32,uint256,address,string)[],bool)")
    head = h(0x40) + h(1 if reset else 0)          # array offset, bool
    # --- array section
    body = h(len(conds))
    elems, offs, cursor = [], [], 32*len(conds)    # offsets are relative to post-length
    for c in conds:
        meta = c["metadata"].encode()
        pad = (-len(meta)) % 32
        e = (h(c["startTimestamp"]) + h(c["maxClaimableSupply"]) + h(0)          # supplyClaimed ignored on input
             + h(c["quantityLimitPerWallet"]) + c["merkleRoot"][2:].rjust(64,'0')
             + h(c["pricePerToken"]) + addr(c["currency"])
             + h(0x100)                                                          # offset to string (8 words)
             + h(len(meta)) + meta.hex() + "00"*pad)
        offs.append(cursor); cursor += len(e)//2
        elems.append(e)
    body += "".join(h(o) for o in offs) + "".join(elems)
    return "0x" + selector[2:] + head + body

def rpc(method, params):
    p=json.dumps({"jsonrpc":"2.0","id":1,"method":method,"params":params})
    out=subprocess.run(["curl","-sS","-m","30","-X","POST",RPC,
        "-H","content-type: application/json","-d",p],capture_output=True,text=True).stdout
    return json.loads(out)

# ---- the proposed emergency condition: restore the advertised 0.005 ETH tier
cond = {
  "startTimestamp": 0,                     # active immediately, can never expire
  "maxClaimableSupply": 8697,              # Common+Uncommon band (8699) minus the 2 already minted
  "quantityLimitPerWallet": 5,
  "merkleRoot": "0x" + "00"*32,            # no allowlist
  "pricePerToken": 5 * 10**15,             # 0.005 ETH
  "currency": NATIVE,
  "metadata": "ipfs://QmVvUrbnwT1FMhkvFyvxwsTE5kFbLohsGEj7qK2YWHvzuq/0",
}
data = encode_set_claim_conditions([cond], True)
print("calldata bytes:", (len(data)-2)//2)

print("\n--- simulate AS OWNER (eth_call never writes) ---")
r = rpc("eth_call",[{"from":OWNER,"to":NFT,"data":data},"latest"])
if "error" in r:
    print("REVERT:", r["error"].get("message"))
else:
    print("SUCCESS - returns", repr(r["result"]), "=> owner can execute this call")

print("\n--- control: same call from a NON-owner must revert ---")
r2 = rpc("eth_call",[{"from":"0x000000000000000000000000000000000000dEaD","to":NFT,"data":data},"latest"])
print("non-owner:", r2.get("error",{}).get("message","NO REVERT (unexpected!)"))

print("\n--- gas estimate for the real transaction ---")
g = rpc("eth_estimateGas",[{"from":OWNER,"to":NFT,"data":data}])
print("gas:", int(g["result"],16) if "result" in g else g.get("error",{}).get("message"))

if "--out" in sys.argv:                      # only write when explicitly asked
    dest = sys.argv[sys.argv.index("--out")+1]
    open(dest,"w").write(data+"\n")
    print("\ncalldata written to", dest)
else:
    print("\ncalldata:", data)
