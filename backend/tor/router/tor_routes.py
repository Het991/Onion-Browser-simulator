from fastapi import APIRouter
from tor.state import connect_tor, disconnect_tor, rotate_tor, TOR_STATE

router = APIRouter()

@router.post("/tor/connect")
def tor_connect():
    return {
        "status": "connected",
        "state": connect_tor()
    }

@router.post("/tor/disconnect")
def tor_disconnect():
    return {
        "status": "disconnected",
        "state": disconnect_tor()
    }

@router.post("/tor/rotate")
def tor_rotate():
    return {
        "status": "rotated",
        "state": rotate_tor()
    }

@router.get("/tor/status")
def tor_status():
    return TOR_STATE
