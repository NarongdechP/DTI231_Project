from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# ตั้งค่าแอปพลิเคชันและฐานข้อมูล
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # ใช้ SQLite สำหรับการทดสอบ
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your-secret-key'

# ตั้งค่า Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'sign_in' 

# สร้างฐานข้อมูล
db = SQLAlchemy(app)

# โมเดล User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

# โหลดข้อมูลผู้ใช้จากฐานข้อมูล
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# หน้า Home
@app.route('/')
def home():
    return render_template('home.html')

# หน้า Sign In
@app.route('/sign-in', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # ค้นหาผู้ใช้จากฐานข้อมูล
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):  # ตรวจสอบรหัสผ่าน
            login_user(user)
            return redirect(url_for('profile'))  # เปลี่ยนเส้นทางไปหน้า Profile
        else:
            flash('Invalid username or password', 'danger')  # แจ้งเตือนหากข้อมูลไม่ถูกต้อง
    
    return render_template('sign_in.html')

# หน้า Sign Up
@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # ตรวจสอบว่าผู้ใช้นี้มีอยู่ในฐานข้อมูลหรือไม่
        user_exists = User.query.filter_by(username=username).first()
        if user_exists:
            flash('Username already exists', 'danger')
            return redirect(url_for('sign_up'))

        # สร้างผู้ใช้ใหม่
        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully. You can now sign in.', 'success')
        return redirect(url_for('sign_in'))
    
    return render_template('sign_up.html')

# หน้า Profile
@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', username=current_user.username, email=current_user.email)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
