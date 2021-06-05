from flask import Flask, render_template, redirect, url_for, request
from werkzeug.utils import invalidate_cached_property
from forms import RegistrationForm,LoginForm
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config['SECRET_KEY'] = '7dfd7bb73c0d762cf441c995a320f23e'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///form.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Form(db.Model):
    id = db.Column("ID",db.Integer, primary_key = True)
    title = db.Column("Title",db.String(100), nullable = False)
    ques = db.Column("Ques",db.String(200))
 
    def __init__(self,title, ques):
        self.title = title
        self.ques = ques

    def __repr__(self):
        return f'{self.title},{self.ques}'


class Registrationform(db.Model):
    id = db.Column("ID",db.Integer, primary_key = True)
    name = db.Column("Name", db.String(20),nullable = False)
    email = db.Column("Email", db.String(30), nullable = False)
    password = db.Column("password", db.String(20), nullable  =False)
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

posts =[
    {
        'author' : 'jane',
        'title':'first_post',
        'ques' : 'what is the web',
        'date_posted' : '3 june'
    },
    {
        'author' : 'rane',
        'title':'second_post',
        'ques' : 'what is the web_page',
        'date_posted' : '4june' 
    }
]


@app.route('/home')
def home():
    return render_template('home.html',title = 'home' ,posts = posts)


@app.route('/')
def helloworld():
    return render_template('questions.html') 

@app.route('/log', methods=['GET', 'POST'])
def log():
    error = None
    if request.method == 'POST':
        user_name = request.form.get('user_email')
        user_pass = request.form.get('user_password1')
        if user_name != 'admin@gmail.com' or user_pass != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('home'))
    return render_template('log.html', error=error)

@app.route('/register')
def register():
    form = RegistrationForm()
    return render_template('register.html', title = 'registration', form = form)

@app.route('/response')
def response():
    return render_template('response.html')



if __name__ == '__main__':
    app.run(debug=True, port=8000)