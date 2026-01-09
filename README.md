# Onion Browser Simulator

An educational Tor Onion Browser Simulator built to demonstrate how Tor sessions,
identity rotation, OPSEC risks, and onion services work in a safe environment.

## Features
- Tor session simulation (connect, rotate identity, disconnect)
- Circuit visualization (entry, middle, exit nodes)
- OPSEC warnings based on user behavior
- Integrated onion services:
  - Marketplace (reputation, escrow, risk modeling)
  - Forum (anonymous discussions, timing correlation concepts)
  - Mail (identity-bound encrypted messaging simulation)
- Single Page Application (SPA) frontend

## Tech Stack
- FastAPI (Python)
- Vanilla JavaScript
- HTML / CSS

## Purpose
This project is for **educational and demonstration purposes only**.
No real Tor traffic or illegal activity is involved.

## How to Run

### Backend
```bash
cd backend
uvicorn main:app

## Screenshots

### Tor Connected Session
![Tor Connected]('Screenshot 2026-01-09 at 01-21-53 Onion Browser Simulator.png')

### Marketplace Onion Service
![Marketplace]('Screenshot 2026-01-09 at 01-22-10 Onion Browser Simulator.png')

### Forum Onion Service
![Forum](screenshots-forum.png)

