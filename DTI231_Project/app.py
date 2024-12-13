from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import hashlib

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # สำหรับ session และ flash messages

# ฟังก์ชั่นเชื่อมต่อกับฐานข้อมูล SQLite
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# ฟังก์ชั่นสำหรับการสมัครสมาชิก
def create_user(username, password):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    try:
        c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
        conn.commit()
    except sqlite3.IntegrityError:
        flash("Username already exists!")
    finally:
        conn.close()

# ฟังก์ชั่นสำหรับการล็อกอิน
def check_user(username, password):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT password FROM users WHERE username = ?', (username,))
    result = c.fetchone()
    conn.close()
    
    if result:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        if hashed_password == result[0]:
            return True
    return False

# หน้าแรกที่ใช้ในการล็อกอิน
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if check_user(username, password):
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid username or password")
    return render_template('login.html')

# หน้า Dashboard หลังจากล็อกอิน
@app.route('/dashboard')
def dashboard():
    return "Welcome to your dashboard!"

# หน้า Signup สำหรับสร้างบัญชีผู้ใช้ใหม่
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        create_user(username, password)
        return redirect(url_for('login'))
    return render_template('signup.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
