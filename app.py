from flask import Flask, render_template, request, redirect, url_for, session, flash
import numpy as np
import joblib
import time
import mysql.connector

app = Flask(__name__)
app.secret_key = "dzaky7205" # Key rahasia untuk session

# --- KONFIGURASI DATABASE ---
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="db_valorant"
    )

# --- LOAD MODELS ---
try:
    knn = joblib.load("model/knn_model.pkl")
    rf_model = joblib.load("model/rf_model.pkl")
    scaler = joblib.load("model/scaler.pkl")
    le = joblib.load("model/label_encoder.pkl")
except Exception as e:
    print(f"Error loading models: {e}")

deskripsi_role = {
    "Duelist": "Sering mendapatkan First Blood dan Kill/Round tinggi — bermain agresif.",
    "Initiator": "Memiliki rata-rata Assist/Round tinggi — berperan aktif membantu tim.",
    "Controller": "KDA baik dan jarang mati — stabil dan menjaga konsistensi.",
    "Sentinel": "Bermain defensif dan cenderung aman — fokus menjaga area/site."
}

rekomendasi_agent = {
    "Duelist": "Jett, Reyna, Waylay, Raze",
    "Initiator": "Fade, Sova, Breach, Skye",
    "Controller": "Omen, Brimstone, Miks, Harbor",
    "Sentinel": "Vyse, Cypher, Killjoy, Veto"
}

def get_float(value):
    try:
        return float(value) if value != "" else 0.0
    except ValueError:
        return 0.0

# --- ROUTING AUTHENTICATION ---

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role = "user" 

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash("Username sudah digunakan, cari yang lain!", "danger")
            return redirect(url_for('register'))

        cursor.execute("INSERT INTO users (username, password, role, is_online) VALUES (%s, %s, %s, 0)", 
                       (username, password, role))
        conn.commit()
        cursor.close()
        conn.close()

        flash("Registrasi Berhasil! Silakan Login.", "success")
        return redirect(url_for('login'))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()

        if user:
            cursor.execute("UPDATE users SET is_online = 1 WHERE username = %s", (username,))
            conn.commit()
            
            session.clear() 
            session['logged_in'] = True
            session['username'] = user['username']
            session['role'] = user['role']
            
            cursor.close()
            conn.close()
            
            flash(f"Login Berhasil! Selamat Datang {user['username']}", "success")
            
            if user['role'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('home'))
        else:
            cursor.close()
            conn.close()
            flash("Username atau Password Salah!", "danger")
    
    return render_template("login.html")

@app.route("/logout")
def logout():
    if 'username' in session:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET is_online = 0 WHERE username = %s", (session['username'],))
        conn.commit()
        cursor.close()
        conn.close()

    session.clear()
    flash("Anda telah logout.", "info")
    return redirect(url_for('home'))

# --- ROUTING CORE ---

@app.route("/")
def home():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tournaments")
    tournaments = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("home.html", tournaments=tournaments)

@app.route("/predict_page")
def predict_page():
    if 'logged_in' not in session:
        flash("Silakan login terlebih dahulu.", "warning")
        return redirect(url_for('login'))
    return render_template("predict.html")

@app.route("/predict", methods=["POST"])
def predict():
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    try:
        time.sleep(2.0) 
        input_features = [
            get_float(request.form["kda"]),
            get_float(request.form["winrate"]),
            get_float(request.form["acs"]),
            get_float(request.form["kill_round"]),
            get_float(request.form["assist_round"]),
            get_float(request.form["death_round"]),
            get_float(request.form["first_blood"]),
            get_float(request.form["headshot"]),
            get_float(request.form["clutch"])
        ]

        data_array = np.array(input_features).reshape(1, -1)
        data_scaled = scaler.transform(data_array)

        # --- PREDIKSI KNN ---
        knn_res = knn.predict(data_scaled)
        knn_role = le.inverse_transform(knn_res)[0]
        knn_prob = np.max(knn.predict_proba(data_scaled)) * 100

        # --- PREDIKSI RANDOM FOREST ---
        rf_res = rf_model.predict(data_scaled)
        rf_role = le.inverse_transform(rf_res)[0]
        rf_prob = np.max(rf_model.predict_proba(data_scaled)) * 100

        # Kita gunakan hasil KNN sebagai tampilan utama karena akurasinya lebih tinggi (94%)
        # Namun tetap menampilkan hasil Random Forest sebagai perbandingan
        return render_template(
            "result.html",
            role=knn_role,
            rf_role=rf_role,
            desc=deskripsi_role.get(knn_role, ""),
            agents=rekomendasi_agent.get(knn_role, ""),
            knn_confidence=round(knn_prob, 2),
            rf_confidence=round(rf_prob, 2),
            reason=f"Sistem membandingkan dua algoritma: KNN memprediksi {knn_role} dan Random Forest memprediksi {rf_role}.",
            stats=input_features
        )
    except Exception as e:
        return f"Terjadi kesalahan: {str(e)}"


# --- ROUTING ADMIN ---

@app.route("/admin")
def admin_dashboard():
    if 'role' not in session or session['role'] != 'admin':
        flash("Akses Ditolak!", "danger")
        return redirect(url_for('home'))
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tournaments")
    tournaments = cursor.fetchall()
    cursor.execute("SELECT id, username, role, is_online FROM users")
    all_users = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template("admin.html", tournaments=tournaments, all_users=all_users)

@app.route("/tambah_tournament", methods=["POST"])
def tambah_tournament():
    if session.get('role') != 'admin':
        return redirect(url_for('home'))

    nama = request.form['nama_tournament']
    deskripsi = request.form['deskripsi']
    link = request.form['link_tournament'] 

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tournaments (nama_tournament, deskripsi, link_tournament) VALUES (%s, %s, %s)", 
                   (nama, deskripsi, link))
    conn.commit()
    cursor.close()
    conn.close()

    flash("Tournament Berhasil Ditambahkan!", "success")
    return redirect(url_for('admin_dashboard'))

@app.route("/hapus_tournament/<int:id>")
def hapus_tournament(id):
    if session.get('role') != 'admin':
        return redirect(url_for('home'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tournaments WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()

    flash("Data Tournament Berhasil Dihapus!", "warning")
    return redirect(url_for('admin_dashboard'))

if __name__ == "__main__":
    app.run(debug=True)