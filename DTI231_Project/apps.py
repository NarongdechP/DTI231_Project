from flask import Flask, render_template,request
from flask_wtf import FlaskForm
from wtforms import TextField,SubmitField
app = Flask(__name__)

@app.route('/')
def all_file():
    return render_template("All file.html")

@app.route('/home')
def home():
    return render_template("Home.html")

@app.route('/profile')
def profile():
    user = {"Username":"dada","Email":"jiraporn.boonsob@gmail.com"}
    return render_template("Profile.html",username= user)

@app.route('/sign_in')
def sign_in():
    return render_template("Sign in.html")

@app.route('/sign_up')
def sign_up():
    return render_template("Sign up.html")


if __name__ == '__main__':
    app.run(debug=True)


