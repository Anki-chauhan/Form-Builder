from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config['SECRET_KEY'] = '7dfd7bb73c0d762cf441c995a320f23e'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Qform(db.Model):
    id = db.Column("ID",db.Integer, primary_key = True)
    question = db.Column("Question",db.String(500), nullable = False)
    op1 = db.Column("Option1",db.String(30),nullable =False)
    op2 = db.Column("Option2",db.String(30),nullable =False)
    op3 = db.Column("Option3",db.String(30),nullable =False)
    op4 = db.Column("Option4",db.String(30),nullable =False)
 
    def __init__(self,question,op1,op2,op3,op4):
        self.question = question
        self.op1 = op1
        self.op2 = op2
        self.op3 = op3
        self.op4 = op4

    def __repr__(self):
        return f'{self.question}'


class Registrationform(db.Model):
    id = db.Column("ID",db.Integer, primary_key = True)
    name = db.Column("Name", db.String(20),nullable = False)
    mobile = db.Column("Mobile", db.Integer,nullable = False)
    email = db.Column("Email", db.String(30), nullable = False)
    password = db.Column("Password", db.String(20), nullable  =False)
    subject = db.Column("Subject", db.String(20), nullable = False )
    gender = db.Column("Gender", db.String(10), nullable = False)
    def __init__(self, name, mobile, email, password, subject, gender):
        self.name = name 
        self.email = email
        self.mobile = mobile
        self.password = password
        self.subject = subject
        self.gender = gender
    def __repr__(self):
        return f'{self.name},{self.email}'



@app.route('/') 
def home():
    return render_template('home.html')

@app.route('/sign_up')
def sign_up():
    return render_template('/register.html')


@app.route('/start')
def start():
    return render_template('questions.html') 

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user_email = request.form['email']
        user_pass = request.form['password']
        uemail = Registrationform.query.with_entities(Registrationform.email)
        upass = Registrationform.query.with_entities(Registrationform.password)
        usr_email = []
        usr_pass = []

        for email in uemail:
            usr_email.append(list(email))
        for pass1 in upass:
            usr_pass.append(list(pass1))
    
        if user_email not in usr_email and user_pass not in usr_pass:
            error = 'Invalid Credentials. Please try again.'
        else:
            return render_template('home.html')
    return render_template('login.html', error=error)

@app.route('/register', methods = ['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        mob = request.form['mob']
        email = request.form['email']
        password = request.form['user_password1']
        subject = request.form['select']
        gender = request.form['gender']
        new_user = Registrationform(name = name, mobile=mob ,email = email, password = password, subject = subject, gender = gender)
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect('questions')
        except:
            return "there is some problem to add new user"
    else:
        return render_template("register.html")


@app.route('/response')
def response():
    return render_template('response.html')


@app.route('/submit', methods= ['GET','POST'])
def submit():
    if request.method == "POST":
        untitle = request.form['untitle']
        question = request.form['question']
        option = request.form['option']
        ques = Qform(question=question, option = option)
        try:
            db.session.add(ques)
            db.session.commit()
        except:
            return 'unable to add question in database'

@app.route('/questions')
def questions():
    return render_template("questions.html")


if __name__ == '__main__':
    app.run(debug=True, port=8000)