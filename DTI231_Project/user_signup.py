from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'


users = {}
files = {}

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('profile'))
    return render_template('Sign up.html')

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    
    # เก็บข้อมูลผู้ใช้ใน Dict
    if username not in users:
        users[username] = {'email': email, 'password': password}
        return redirect(url_for('login'))
    return 'Username already exists!'

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    if username in users and users[username]['password'] == password:
        session['username'] = username
        return redirect(url_for('profile'))
    return 'Invalid credentials, please try again.'

@app.route('/profile')
def profile():
    if 'username' not in session:
        return redirect(url_for('home'))
    
    username = session['username']
    user_info = users[username]
    return render_template('Profile.html', username=username, email=user_info['email'])

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/files')
def files_page():
    if 'username' not in session:
        return redirect(url_for('home'))
    
    return render_template('All files.html', files=files)

@app.route('/add_file', methods=['POST'])
def add_file():
    if 'username' not in session:
        return redirect(url_for('home'))
    
    file_name = request.form['file_name']
    modified_by = request.form['modified_by']
    file_size = request.form['file_size']
    
    # เก็บข้อมูลไฟล์ใน Dictionary
    files[file_name] = {'modified_by': modified_by, 'file_size': file_size, 'modified': 'Just now'}
    
    return redirect(url_for('files_page'))

if __name__ == '__main__':
    app.run(debug=True)