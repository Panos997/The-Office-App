import os
import sqlite3
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Δημιουργία/Σύνδεση στη βάση δεδομένων
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save_user', methods=['POST'])
def save_user():
    data = request.json
    name = data.get('name')
    if name:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (name) VALUES (?)", (name,))
        conn.commit()
        conn.close()
        return jsonify({"status": "success", "message": f"Γεια σου {name}!"})
    return jsonify({"status": "error"}), 400

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
