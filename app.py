import os
import sqlite3
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# --- ΡΥΘΜΙΣΗ ΒΑΣΗΣ ΔΕΔΟΜΕΝΩΝ ---
def init_db():
    """Δημιουργεί τον πίνακα χρηστών αν δεν υπάρχει ήδη."""
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  name TEXT NOT NULL, 
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

# Αρχικοποίηση της βάσης κατά την εκκίνηση
init_db()

# --- ROUTES ---

@app.route('/')
def index():
    """Η αρχική σελίδα του App."""
    return render_template('index.html')

@app.route('/save_user', methods=['POST'])
def save_user():
    """Αποθηκεύει το όνομα του χρήστη στη SQLite."""
    data = request.json
    name = data.get('name')
    
    if not name:
        return jsonify({"status": "error", "message": "No name provided"}), 400
    
    try:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (name) VALUES (?)", (name,))
        conn.commit()
        conn.close()
        return jsonify({"status": "success", "message": f"Γεια σου {name}!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/admin_list')
def admin_list():
    """Σελίδα που δείχνει όλους τους χρήστες που γράφτηκαν."""
    try:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        # Παίρνουμε τα ονόματα με σειρά από το πιο πρόσφατο
        c.execute("SELECT name, timestamp FROM users ORDER BY id DESC")
        users = c.fetchall()
        conn.close()
        
        # Δημιουργία μιας απλής HTML λίστας
        if not users:
            return "<h1>Δεν υπάρχουν ακόμα εγγεγραμμένοι χρήστες.</h1><a href='/'>Πίσω</a>"
        
        user_rows = "".join([f"<li><strong>{u[0]}</strong> <small>({u[1]})</small></li>" for u in users])
        html_response = f"""
        <html>
            <head><title>Admin Panel</title></head>
            <body style="font-family:sans-serif; padding:20px; background:#f4f4f4;">
                <h2>Λίστα Χρηστών (Database)</h2>
                <ul>{user_rows}</ul>
                <br>
                <a href="/">Επιστροφή στην εφαρμογή</a>
            </body>
        </html>
        """
        return html_response
    except Exception as e:
        return f"Σφάλμα βάσης: {str(e)}"

# --- ΕΚΚΙΝΗΣΗ ---
if __name__ == '__main__':
    # Το Render ορίζει αυτόματα τη θύρα μέσω της μεταβλητής PORT
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
