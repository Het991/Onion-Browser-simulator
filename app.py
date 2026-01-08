from flask import Flask, jsonify, render_template_string
from faker import Faker
import random
import sqlite3
from datetime import datetime

app = Flask(__name__)
fake = Faker()

# Init DB
def init_db():
    conn = sqlite3.connect('darkweb.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS leaks (id INTEGER PRIMARY KEY, title TEXT, data TEXT, price REAL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS wallet (balance REAL)''')
    c.execute("INSERT OR IGNORE INTO wallet (balance) VALUES (1000.0)")  # Fake crypto
    conn.commit()
    conn.close()

init_db()

# Simulated leak data
def generate_leak():
    titles = ["Fresh CC Dumps 2026", "Gov Employee PWs", "Crypto Keys MegaLeak"]
    return {
        'title': random.choice(titles),
        'data': fake.paragraph(),
        'price': round(random.uniform(50, 500), 2),
        'seller': fake.name() + " (ParanoidHaxxor)"
    }
@app.route('/')
def index():
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <title>🧅 OnionBrowser v3.2.1 - Simulated</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            background: radial-gradient(circle at 20% 80%, #1a1a2e 0%, #16213e 50%, #0f0f23 100%);
            color: #00ff41; 
            font-family: 'Courier New', monospace; 
            height: 100vh; 
            overflow: hidden;
        }
        .tor-header {
            background: linear-gradient(90deg, #000, #001100, #000);
            padding: 10px 20px;
            border-bottom: 2px solid #00ff41;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .onion-bar {
            background: #111;
            border: 1px solid #333;
            border-radius: 5px;
            padding: 8px;
            flex: 1;
            margin: 0 20px;
            font-size: 14px;
        }
        .onion-bar input { 
            background: transparent; 
            border: none; 
            color: #00ff41; 
            width: 100%; 
            outline: none;
            font-family: inherit;
        }
        .status { font-size: 12px; }
        .status.connecting::after { content: " 🔄 Connecting..."; animation: blink 1s infinite; }
        @keyframes blink { 50% { opacity: 0; } }
        .site-frame {
            height: calc(100vh - 120px);
            width: 100%;
            border: none;
            background: #000;
        }
        .onion-nav {
            background: #111;
            padding: 10px;
            border-bottom: 1px solid #333;
            white-space: nowrap;
            overflow-x: auto;
        }
        .onion-link {
            color: #00ff41;
            text-decoration: none;
            margin-right: 20px;
            padding: 5px 10px;
            border: 1px solid transparent;
            border-radius: 3px;
            transition: all 0.3s;
        }
        .onion-link:hover {
            background: #00ff41;
            color: #000;
            border-color: #00ff41;
        }
        .warning {
            position: absolute;
            top: 20px;
            right: 20px;
            background: #ff0040;
            color: white;
            padding: 10px;
            border-radius: 5px;
            font-size: 12px;
            animation: glitch 2s infinite;
        }
        @keyframes glitch {
            0%, 100% { transform: translate(0); }
            20% { transform: translate(-2px, 2px); }
            40% { transform: translate(2px, -2px); }
        }
    </style>
</head>
<body>
    <div class="warning">⚠️ SIMULATION ONLY - Educational Purpose</div>
    
    <div class="tor-header">
        <div>🧅 <strong>OnionBrowser v3.2.1</strong> <span class="status connecting"></span></div>
        <div class="onion-bar">
            <input type="text" id="urlbar" placeholder="Enter .onion address..." value="localhost:5000/">
        </div>
        <div>● Circuit: 3 hops | 🔒 Secure</div>
    </div>
    
    <div class="onion-nav" id="nav">
        <!-- Links load here -->
    </div>
    
    <iframe class="site-frame" id="siteframe" src="/"></iframe>

    <script>
        const sites = {
            'scamshop.onion': '/scamshop',
            'leaks.onion': '/leaks', 
            'malware.onion': '/malware',
            'npc.onion': '/npc/chat/buy',
            'missions.onion': '/missions'
        };

        // Load nav links
        const nav = document.getElementById('nav');
        Object.keys(sites).forEach(site => {
            const a = document.createElement('a');
            a.href = '#';
            a.className = 'onion-link';
            a.textContent = site;
            a.onclick = () => loadSite(sites[site], site);
            nav.appendChild(a);
        });

        function loadSite(url, title) {
            document.getElementById('siteframe').src = url;
            document.getElementById('urlbar').value = title;
        }

        // URL bar enter
        document.getElementById('urlbar').addEventListener('keypress', e => {
            if (e.key === 'Enter') {
                const url = e.target.value;
                if (sites[url]) loadSite(sites[url], url);
                else alert('❌ Site not found - Tor connection failed');
            }
        });

        // Auto-connect effect
        setTimeout(() => {
            document.querySelector('.status').textContent = '● Connected';
            loadSite('/leaks', 'leaks.onion');
        }, 2000);
    </script>
</body>
</html>
    ''')

@app.route('/leaks')
def leaks():
    conn = sqlite3.connect('darkweb.db')
    c = conn.cursor()
    c.execute("INSERT INTO leaks (title, data, price) VALUES (?, ?, ?)", 
              (generate_leak()['title'], generate_leak()['data'], generate_leak()['price']))
    c.execute("SELECT * FROM leaks ORDER BY id DESC LIMIT 10")
    leaks = [{'id': row[0], 'title': row[1], 'data': row[2], 'price': row[3]} for row in c.fetchall()]
    conn.close()
    return jsonify({'sites': leaks, 'warning': '🚨 Real leaks could dox you!'})

@app.route('/scamshop')
def scamshop():
    products = [
        {'name': 'Magic Hacking Tool', 'price': 999, 'desc': 'Guaranteed root any box! (Spoiler: Malware)', 'scam_level': 'HIGH'},
        {'name': 'Fullz Pack', 'price': 50, 'desc': 'CC + SSN (fake data only here)'}
    ]
    return jsonify({'shop': products, 'npc_msg': 'Hey buyer, pay XMR now or GTFO! 💀'})

# Wallet sim (fake crypto buy)
@app.route('/wallet/buy/<float:amount>')
def buy(amount):
    conn = sqlite3.connect('darkweb.db')
    c = conn.cursor()
    c.execute("SELECT balance FROM wallet")
    bal = c.fetchone()[0]
    if bal >= amount:
        c.execute("UPDATE wallet SET balance = balance - ?", (amount,))
        conn.commit()
        conn.close()
        return jsonify({'tx': f'TXN: {random.randint(1000,9999)}-{datetime.now().isoformat()}', 'balance': bal - amount})
    conn.close()
    return jsonify({'error': 'Insufficient funds, noob'}), 400

# NPC Chat (simple stateful)
npcs = {'dealer': {'state': 'greeting', 'personality': 'shady', 'msgs': []}}

@app.route('/npc/chat/<action>')
def npc_chat(action):
    npc = npcs['dealer']
    if npc['state'] == 'greeting':
        resp = "Yo, want premium zero-days? 0.5 XMR."
        npc['state'] = 'offered'
    elif action == 'buy' and npc['state'] == 'offered':
        resp = "Funds received! Check your malware... wait, FBI? RUN!"
        npc['state'] = 'busted'
    else:
        resp = "You\'re being watched. Log off."
    npc['msgs'].append(resp)
    return jsonify({'reply': resp, 'personality': npc['personality']})

@app.route('/missions')
def missions():
    missions = [
        {'id': 1, 'name': 'Track the Leaker', 'desc': 'Analyze forum post for clues (check headers)', 'hint': 'Look for IP in fake logs'},
        {'id': 2, 'name': 'Bust Scam Shop', 'desc': 'Buy fake tool, reverse it to find "backdoor" flag'}
    ]
    return jsonify(missions)

if __name__ == '__main__':
    app.run(debug=True)
