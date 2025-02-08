import requests
import sympy
import numpy as np
from fastecdsa.curve import secp256k1
from fastecdsa.point import Point

p = secp256k1.p
G = secp256k1.G

def fetch_public_key(address):
    try:
        url = f"https://blockchain.info/rawaddr/{address}"
        data = requests.get(url).json()
        tx = data["txs"][0]
        pubkey_hex = tx["inputs"][0]["script"][-66:]
        x, y = int(pubkey_hex[:64], 16), int(pubkey_hex[64:], 16)
        return Point(x, y, secp256k1)
    except:
        print("[-] Public Key Fetch Failed.")
        return None

def torsion_attack(public_key):
    for k in range(1, 1000000):
        weak_point = k * public_key
        if weak_point.x % 2 == 0 and weak_point.y % 2 == 0:
            priv_key = k % p
            with open("found.txt", "a") as f:
                f.write(f"Private Key Found: {hex(priv_key)}\n")
            print("[✔] Private Key Extracted:", hex(priv_key))
            return priv_key
    print("[-] No Weakness Found.")
    return None

btc_address = input("Enter Bitcoin Address: ")
pubkey = fetch_public_key(btc_address)
if pubkey:
    print("[✔] Public Key Found:", pubkey)
    torsion_attack(pubkey)
