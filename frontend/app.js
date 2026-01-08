/*************************************************
 * Onion Browser Simulator — FINAL SPA VERSION
 * Educational / Resume-Ready
 *************************************************/

console.log("Onion Browser Simulator app.js loaded");

// =====================
// GLOBAL STATE
// =====================
const BACKEND = "http://127.0.0.1:8000";

const appState = {
    tor: {
        status: "disconnected", // disconnected | connecting | connected
        sessionId: null
    },
    circuit: {
        entry: null,
        middle: null,
        exit: null
    },
    opsecWarnings: []
};

// =====================
// UTILITIES
// =====================
function randNode(prefix) {
    return `${prefix}-${Math.floor(Math.random() * 1000)}`;
}

function newSessionId() {
    return "anon-" + Math.floor(Math.random() * 1000000);
}

function buildCircuit() {
    appState.circuit.entry = randNode("entry");
    appState.circuit.middle = randNode("middle");
    appState.circuit.exit = randNode("exit");
}

function clearCircuit() {
    appState.circuit.entry = null;
    appState.circuit.middle = null;
    appState.circuit.exit = null;
}

// =====================
// TOR CONTROLS
// =====================
function startTor() {
    if (appState.tor.status !== "disconnected") return;

    appState.tor.status = "connecting";
    renderStatus();

    setTimeout(() => {
        appState.tor.status = "connected";
        appState.tor.sessionId = newSessionId();
        buildCircuit();

        fetch(`${BACKEND}/tor/connect`, { method: "POST" }).catch(() => {});
        renderStatus();
        renderWelcome();
    }, 1500);
}

function rotateTor() {
    if (appState.tor.status !== "connected") return;
    buildCircuit();
    fetch(`${BACKEND}/tor/rotate`, { method: "POST" }).catch(() => {});
    renderStatus();
}

function disconnectTor() {
    if (appState.tor.status !== "connected") return;
    appState.tor.status = "disconnected";
    appState.tor.sessionId = null;
    clearCircuit();
    fetch(`${BACKEND}/tor/disconnect`, { method: "POST" }).catch(() => {});
    renderStatus();
    renderWelcome();
}

// =====================
// RENDER: STATUS BAR
// =====================
function renderStatus() {
    const status = document.getElementById("status-indicator");
    if (appState.tor.status === "connected") {
        status.textContent = `Connected (${appState.tor.sessionId})`;
    } else if (appState.tor.status === "connecting") {
        status.textContent = "Connecting…";
    } else {
        status.textContent = "Disconnected";
    }
}

// =====================
// RENDER: WELCOME
// =====================
function renderWelcome() {
    document.getElementById("content-panel").innerHTML = `
        <h2>Welcome</h2>
        <p>This simulator demonstrates Tor routing, identity rotation,
        OPSEC risks, and onion services in a safe environment.</p>
    `;
}

// =====================
// MARKETPLACE
// =====================
async function loadMarketplace() {
    if (appState.tor.status !== "connected") return;

    const res = await fetch(`${BACKEND}/api/marketplace`);
    const data = await res.json();

    document.getElementById("content-panel").innerHTML = `
        <h2>🧅 market7xk2.onion</h2>
        <p><b>Tor Identity:</b> ${appState.tor.sessionId}</p>

        <div class="opsec">
            ⚠ OPSEC: Reputation ≠ Identity. Escrow reduces risk, not exposure.
        </div>

        <h3>Vendors</h3>
        ${data.vendors.map(v => `
            <div class="card">
                <b>${v.name}</b><br>
                Rating: ⭐ ${v.rating}<br>
                Status: ${v.trusted ? "✔ Trusted" : "⚠ Unverified"}
            </div>
        `).join("")}

        <h3>Listings</h3>
        ${data.items.map(i => `
            <div class="card">
                <b>${i.title}</b><br>
                Vendor: ${i.vendor}<br>
                Price: ${i.price_btc} BTC<br>
                Escrow: ${i.escrow ? "ON" : "OFF"}<br>
                Risk: ${i.escrow ? "LOW" : "HIGH"}<br>
                <button disabled>Buy (simulation)</button>
            </div>
        `).join("")}
    `;
}

// =====================
// FORUM
// =====================
function loadForum() {
    if (appState.tor.status !== "connected") return;

    document.getElementById("content-panel").innerHTML = `
        <h2>🧅 forum.onion</h2>
        <p><b>Posting as:</b> ${appState.tor.sessionId}</p>

        <div class="opsec">
            ⚠ OPSEC: Posting patterns can reveal identity through timing.
        </div>

        <div class="card">
            <b>[Thread]</b> Identity rotation — when is it harmful?<br>
            <small>Posted by anon-48291 · 3 minutes ago</small>
        </div>

        <div class="card">
            <b>[Thread]</b> Marketplace trust vs escrow<br>
            <small>Posted by anon-77412 · 9 minutes ago</small>
        </div>

        <p class="muted">Replies disabled (educational simulation)</p>
    `;
}

// =====================
// MAIL
// =====================
function loadMail() {
    if (appState.tor.status !== "connected") return;

    document.getElementById("content-panel").innerHTML = `
        <h2>🧅 mail.onion</h2>
        <p><b>Mailbox:</b> ${appState.tor.sessionId}@onion</p>

        <div class="opsec">
            ⚠ OPSEC: Mailbox identity should never be reused outside Tor.
        </div>

        <div class="card">
            📧 <b>Welcome</b><br>
            <small>Encrypted message (simulated)</small>
        </div>

        <div class="card">
            📧 <b>Vendor Reply</b><br>
            <small>PGP-secured message (simulated)</small>
        </div>
    `;
}

// =====================
// INIT
// =====================
document.addEventListener("DOMContentLoaded", () => {
    renderStatus();
    renderWelcome();

    document.getElementById("btn-start-session").onclick = startTor;
    document.getElementById("btn-rotate-identity").onclick = rotateTor;
    document.getElementById("btn-disconnect").onclick = disconnectTor;

    document.querySelectorAll(".onion-link").forEach(btn => {
        btn.onclick = () => {
            const site = btn.textContent.trim();
            if (site === "marketplace.onion") loadMarketplace();
            if (site === "forum.onion") loadForum();
            if (site === "mail.onion") loadMail();
        };
    });
});
