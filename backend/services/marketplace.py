import json
import time
import random
from pathlib import Path

DATA_PATH = Path(__file__).parent.parent / "data" / "marketplace.json"

def simulate_tor_latency():
    # Simulate 3-hop Tor circuit (ms)
    hops = random.randint(3, 4)
    latency = random.randint(300, 1200)
    time.sleep(latency / 1000)
    return {
        "hops": hops,
        "latency_ms": latency
    }

def load_marketplace():
    with open(DATA_PATH, "r") as f:
        return json.load(f)

def get_marketplace():
    circuit = simulate_tor_latency()
    data = load_marketplace()
    return {
        "circuit": circuit,
        "service": data
    }
