from fastapi import APIRouter, HTTPException
from tor.state import TOR_STATE
import json
from pathlib import Path

router = APIRouter()
DATA = Path(__file__).parent.parent / "data" / "marketplace.json"

@router.get("/api/marketplace")
def marketplace():
    if not TOR_STATE["connected"]:
        raise HTTPException(
            status_code=403,
            detail="Tor is not connected"
        )

    with open(DATA) as f:
        data = json.load(f)

    return {
        "identity": TOR_STATE["identity"],
        "items": data["items"],
        "vendors": data["vendors"]
    }
