from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, Length, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required

# ตั้งค่าแอปพลิเคชันและฐานข้อมูล
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # ใช้ SQLite สำหรับการทดสอบ
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your-secret-key'

# ตั้งค่า Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

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

# ฟอร์มลงทะเบียนผู้ใช้
class UserRegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=100)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(f"The email {email.data} is already taken.")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(f"The username {username.data} is already taken.")

# หน้า Sign Up
@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    form = UserRegistrationForm()

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = generate_password_hash(form.password.data, method='sha256')

        # สร้างผู้ใช้ใหม่
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully. You can now sign in.', 'success')
        return redirect(url_for('sign_in'))

    return render_template('sign_up.html', form=form)

# หน้า Sign In (จำลองไว้สำหรับทดสอบ)
@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        # รหัสผ่านและชื่อผู้ใช้จะถูกตรวจสอบที่นี่
        pass
    return render_template('sign_in.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # สร้างฐานข้อมูลหากยังไม่มี
    app.run(debug=True)