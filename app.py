from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'change_this_secret_key'  # 🔐 Change cette clé pour plus de sécurité

# Initialisation de la base de données
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS rdv (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            telephone TEXT NOT NULL,
            date TEXT NOT NULL,
            heure TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Page d'accueil
@app.route('/')
def index():
    return render_template('index.html')

# Prise de rendez-vous
@app.route('/rdv', methods=['GET', 'POST'])
def rdv():
    if request.method == 'POST':
        nom = request.form['nom']
        telephone = request.form['telephone']
        date = request.form['date']
        heure = request.form['heure']

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('INSERT INTO rdv (nom, telephone, date, heure) VALUES (?, ?, ?, ?)',
                  (nom, telephone, date, heure))
        conn.commit()
        conn.close()

        return redirect(url_for('confirmation'))

    return render_template('rdv.html')

# Confirmation
@app.route('/confirmation')
def confirmation():
    return "<h2>Merci ! Votre rendez-vous a été enregistré.</h2>"

# Connexion admin
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # ⚠️ À améliorer avec bcrypt plus tard
        if username == 'admin' and password == 'motdepasse':
            session['admin'] = True
            return redirect(url_for('admin'))
        else:
            return "<h3>Identifiants incorrects</h3>"

    return render_template('login.html')

# Tableau de bord admin
@app.route('/admin')
def admin():
    if not session.get('admin'):
        return redirect(url_for('login'))

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM rdv ORDER BY date, heure')
    rdvs = c.fetchall()
    conn.close()
    return render_template('admin.html', rdvs=rdvs)

# Déconnexion
@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)