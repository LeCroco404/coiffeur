from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Initialisation de la base
def init_db():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS rdv (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT,
        heure TEXT
    )''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/prendre-rdv', methods=['POST'])
def prendre_rdv():
    nom = request.form['nom']
    heure = request.form['heure']
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("INSERT INTO rdv (nom, heure) VALUES (?, ?)", (nom, heure))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == '1234':
            session['admin'] = True
            return redirect(url_for('admin'))
    return render_template('login.html')

@app.route('/admin')
def admin():
    if not session.get('admin'):
        return redirect(url_for('login'))
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM rdv")
    rdvs = c.fetchall()
    conn.close()
    return render_template('admin.html', rdvs=rdvs)

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('index'))

app.run(host='0.0.0.0', port=8080)