import re
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
    mobile = db.Column("Mobile", db.Integer,nullable = False)
    email = db.Column("Email", db.String(30), nullable = False)
    password = db.Column("password", db.String(20), nullable  =False)
    def __init__(self, name, mobile, email, password):
        self.name = name
        self.email = email
        self.mobile = mobile
        self.password = password

    def __repr__(self):
        return f'{self.name},{self.email}'




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

@app.route('/sign_up')
def sign_up():
    return render_template('/register.html')


@app.route('/', methods = ['GET','POST'])
def helloworld():
    if request.method == 'POST':
        one = request.form['one']
        two = request.form['two']
        three = request.form['three']
        four = request.form['four'] 

    return render_template('questions.html') 

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user_name = request.form['username']
        user_pass = request.form['password']
        names = Registrationform.query.with_entities(Registrationform.name)
        upass = Registrationform.query.with_entities(Registrationform.password)
        usr_name = []
        usr_pass = []

        for name in names:
            usr_name.append(name)
            print(name)
        for pass1 in upass:
            usr_pass.append(pass1)
            print(pass1)
        for u, p in zip(usr_name, usr_pass):
            if u == user_name and p == user_pass:
                error = 'Invalid Credentials. Please try again.'
            else:
               return redirect(url_for('home'))
    return render_template('login.html', error=error)

@app.route('/register', methods = ['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        mob = request.form['mob']
        email = request.form['email']
        password = request.form['user_password1']
        new_user = Registrationform(name = name, mobile=mob ,email = email, password = password)
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect('login')
        except:
            return "there is some problem to add new user"
    else:
        return render_template("register.html")


    
    return render_template('register.html', title = 'registration', form = form)

@app.route('/response')
def response():
    return render_template('response.html')

@app.route('/new')
def new():
    return render_template('new.html')



if __name__ == '__main__':
    app.run(debug=True, port=8000)