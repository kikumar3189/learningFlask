from flask import Flask, render_template , request, session, redirect, url_for
from models import DatabaseHandler
from forms import SignupForm, LoginForm

app = Flask(__name__)

db = DatabaseHandler('.//static//Data//Database.db')

@app.route("/")
def index():
    return render_template("index.html")

app.secret_key = "development-key"


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/signup", methods = ['GET','POST'])
def signup():
    if 'email' in session:
        return redirect(url_for('home'))
    form = SignupForm()
    if request.method == 'POST':
        if form.validate() == False:
            return render_template("signup.html",form = form)
        else:
            db.insert_user(form.first_name.data, form.last_name.data, form.email.data.lower(), form.password.data)
            # newUser = User(form.first_name.data,form.last_name.data,form.email.data,form.password.data)
            # db.session.add(newUser)
            # db.session.commit()
            session['email'] = form.email.data.lower()
            return redirect(url_for('home'))
    elif request.method == 'GET':
        return render_template("signup.html",form = form)

@app.route("/login", methods = ['GET', 'POST'])
def login():

    if 'email' in session:
        return redirect(url_for('home'))
    form = LoginForm()
    if request.method == 'POST':
        if form.validate() == False:
            return render_template("login.html", form = form)
        else:
            email = form.email.data.lower()
            password = form.password.data

            user = db.get_user(email)
            if user is not None and db.check_password(password, user[0][2]):
                session['email'] = form.email.data.lower()
                return redirect(url_for('home'))
            else:
                return redirect(url_for('login'))
    elif request.method == 'GET':
        return render_template("login.html",form = form)


@app.route("/logout")
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))

@app.route("/home")
def home():
    if 'email' not in session:
        return redirect(url_for('login'))
    return render_template("home.html")

	
if __name__ == "__main__":
    app.run(debug=True)
