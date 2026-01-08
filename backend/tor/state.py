import random
import string
from datetime import datetime

TOR_STATE = {
    "connected": False,
    "identity": None,
    "last_rotated": None
}

def generate_identity():
    return "anon-" + "".join(random.choices(string.digits, k=4))

def connect_tor():
    TOR_STATE["connected"] = True
    TOR_STATE["identity"] = generate_identity()
    TOR_STATE["last_rotated"] = datetime.now()
    return TOR_STATE

def disconnect_tor():
    TOR_STATE["connected"] = False
    TOR_STATE["identity"] = None
    return TOR_STATE

def rotate_tor():
    if TOR_STATE["connected"]:
        TOR_STATE["identity"] = generate_identity()
        TOR_STATE["last_rotated"] = datetime.now()
    return TOR_STATE
