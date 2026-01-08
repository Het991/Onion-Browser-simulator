from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime

from services.marketplace_router import router as marketplace_router
from tor.router.tor_routes import router as tor_router
from services.marketplace import get_marketplace

import requests
from bs4 import BeautifulSoup

app = FastAPI()

# --- Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Routers ---
app.include_router(tor_router)
app.include_router(marketplace_router)
# --- Models ---
class TrafficEvent(BaseModel):
    type: str
    details: dict | None = None
    timestamp: int

# --- Utils ---
def log(msg: str):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

# --- Routes ---
@app.post("/traffic/event")
def traffic_event(event: TrafficEvent):
    log(f"Traffic event: {event.type} | {event.details}")
    return {"status": "ok"}

ALLOWED_SITES = {
    "example": "https://example.com",
    "httpbin": "https://httpbin.org/html",
    "wikipedia": "https://en.wikipedia.org/wiki/Tor_(network)"
}

@app.get("/fetch/{site_name}")
def fetch_site(site_name: str):
    if site_name not in ALLOWED_SITES:
        raise HTTPException(status_code=400, detail="Site not allowed")

    url = ALLOWED_SITES[site_name]
    log(f"Fetching external site: {url}")

    try:
        resp = requests.get(url, timeout=5)
    except Exception:
        raise HTTPException(status_code=502, detail="Fetch failed")

    soup = BeautifulSoup(resp.text, "html.parser")

    for tag in soup(["script", "style", "iframe"]):
        tag.decompose()

    text = soup.get_text(separator="\n")
    cleaned = "\n".join(
        line.strip() for line in text.splitlines() if line.strip()
    )[:5000]

    return {
        "site": site_name,
        "url": url,
        "status_code": resp.status_code,
        "headers": {
            "server": resp.headers.get("Server"),
            "content_type": resp.headers.get("Content-Type")
        },
        "content": cleaned
    }

@app.get("/api/onion/marketplace")
def marketplace_onion():
    return get_marketplace()
