from flask import Flask, render_template , request, session, redirect, url_for
from models import UserHandler, UserTiffin, UserAddress
from forms import SignupForm, LoginForm, NewTiffinForm

app = Flask(__name__)

userHandler = UserHandler()

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
            userHandler.insert_user(form.first_name.data, form.last_name.data, form.email.data.lower(), form.password.data)
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
            user = userHandler.get_user(email)
            if user is not None and userHandler.check_password(password, user[2]):
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
    user = userHandler.get_user(session['email'])
    usertiffins = UserTiffin(session['email'])
    cols = ['Timing', 'Type', 'Size','Delivery Address', 'Delivery Status' ]
    return render_template("home.html", username = user[0], tiffins = usertiffins.get_active_tiffins(), cols = cols)

@app.route("/orderNewTiffin", methods = ['GET', 'POST'])
def order_new_tiffin():
    if 'email' not in session:
        return redirect(url_for('login.html'))
    userAdd = UserAddress(session['email'])
    form = NewTiffinForm()
    form.existingAddress.choices = userAdd.get_existing_addresses_for_user()
    if request.method == 'POST':
        if form.validate() == False:
            return render_template("newTiffin.html", form = form)
        else:
            userTiffin = UserTiffin(session['email'])
            activeTiffinPresent = userTiffin.check_active_tiffin(form.timing.data)
            if activeTiffinPresent:
                #To Do : Display a message that an active Tiffin is already present for this timing and clear form data.
                print('Active tiffin already present for this timing')
                return render_template("newTiffin.html", form = form)
            if len(form.newAddressName.data) > 0:
                # userAddress = UserAddress(session['email'])
                userAdd.add_new_delivery_address(form.newAddressName.data, form.addressLine1.data, form.addressLine2.data, form.city.data, form.pincode.data)
                userTiffin.add_new_tiffin(form.timing.data, form.tiffinType.data, form.size.data, form.newAddressName.data)
                return redirect(url_for('submit_tiffin'))
            userTiffin.add_new_tiffin(form.timing.data, form.tiffinType.data, form.size.data, form.existingAddress.data)
            return redirect(url_for('submit_tiffin'))

    elif request.method == 'GET':
        return render_template("newTiffin.html", form=form)



@app.route("/cancelTiffin")
def cancel_tiffin():
    return render_template("cancelTiffin.html")

@app.route("/reviewTiffin")
def review_tiffin():
    return render_template("reviewTiffin.html")

@app.route("/submitTiffin")
def submit_tiffin():
    return render_template("submitTiffin.html")

	
if __name__ == "__main__":
    app.run(debug=True)
