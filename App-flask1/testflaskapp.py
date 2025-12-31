import random
from datetime import timedelta

from flask import Flask, render_template, request, flash, session, redirect, url_for
from flask_login import LoginManager, login_user,logout_user,current_user,login_required
from werkzeug.security import generate_password_hash, check_password_hash


from forms import RegisterForm, LoginForm, QuoteForm, AccountDeleteForm, ProfileForm
from models import db, User, Quotes

from flask_migrate import Migrate

app = Flask(__name__)
app.secret_key = "BunnyMe9WebAccess"                  #for session key
app.config['SECRET_KEY'] = 'BunnyMe9DBAccesskey'      #for database key
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///quotes.db'
app.permanent_session_lifetime = timedelta(days=1)

db.init_app(app)      # db = SQLAlchemy() it is declared in models.py
migrate =Migrate(app,db)

login_manager = LoginManager()
login_manager.login_view= 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

quotes = [
    "The best way to get started is to quit talking and begin doing.",
    "Success is not in what you have, but who you are.",
    "Do not wait for opportunity. Create it.",
    "Dream big and dare to fail.",
    "Action is the foundational key to all success."]

# @app.route("/login" , methods=["POST","GET"])
# def login():
#     if request.method == "POST":
#         session.permanent=True
#         user_mail = request.form.get("mail")
#         session["user_mail"] = user_mail
#         return redirect(url_for("user"))
#     else:
#         if "user_mail" in session:
#             flash("you are logged in")
#             return redirect(url_for("home"))
#         return render_template("login.html")


#This is just used for temporarily rendering database can be changed to quote feed
@app.route("/view")
def view():
    values = User.query.all()
    return render_template("view.html", values=values)


@app.route("/testdelete", methods=['POST','GET'])
#Account deletion page rendering route
def testdelete():
    form = AccountDeleteForm()
    return render_template("test_delete.html", form=form)

# @app.route("/editprofile", methods=['POST','GET'])
# #to render preferences.html
# def editprofile():
#     form = ProfileForm()
#     return render_template("preferences.html", form=form)

@app.route("/", methods = ["POST","GET"])
def home():
    quote = random.choice(quotes)

    if request.method == "POST":
        user_name = request.form.get("name")
        session["user_name"] = user_name
    return render_template("home.html", quote=quote, name="name")

# @app.route("/user")
# def user():
#     if "user_mail" in session:
#         user_mail = session["user_mail"]
#         flash("logged in")
#         return render_template("user.html", user_mail=user_mail)
#     else:
#         flash("Please Login")
#         return redirect(url_for("login"))


@app.route("/register", methods=["POST", "GET"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(user=form.username.data).first()
        if existing_user:
            flash("Username already taken. Please choose another one.", "danger")
            return redirect(url_for("register"))

        #create new user
        user = User(user=form.username.data, email=form.email.data, password=generate_password_hash(form.password.data, method='pbkdf2:sha256'))
        db.session.add(user)
        db.session.commit()
        flash("Account created", "success")
        return redirect(url_for("dashboard"))
    return render_template("register.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            return redirect(url_for('changes'))
        flash('Invalid credentials', 'danger')
    return render_template('login.html', form=form)

@app.route("/delete_account", methods=['POST','GET'])
@login_required
def delete_account():
    user = current_user
    #password conformation
    form = AccountDeleteForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            # check password hash
            if check_password_hash(current_user.password, form.password.data):
                #deleting Quotes
                Quotes.query.filter_by(user_id=user.id).delete()
                #now delete user
                db.session.delete(user)
                db.session.commit()
                logout_user()
                flash("account deleted permanently")
                return redirect(url_for("register"))
            else:
                flash("Invalid Password")
    return render_template("test_delete.html", form=form)

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    #Quote form handling
    form = QuoteForm()

    if form.validate_on_submit():
        note = Quotes(content=form.content.data, author=current_user)
        db.session.add(note)
        db.session.commit()
        flash('Note added!', 'success')
        return redirect(url_for('dashboard'))
    notes = Quotes.query.filter_by(user_id=current_user.id).all()
    return render_template('changes.html', form=form, notes=notes)

#backup route for dashboard
# @app.route('/changes', methods=['GET' , 'POST'])
# @login_required
# def changes():
#     form = QuoteForm()
#     if form.validate_on_submit():
#         note = Quotes(content=form.content.data, author=current_user)  #used variable name 'note' for quote
#         db.session.add(note)
#         db.session.commit()
#     notes = Quotes.query.filter_by(user_id=current_user.id).all()
#     return render_template('changes.html', form=form, notes=notes)


#this is used for saving profile updates such as user bio
@app.route("/editprofile", methods=["GET", "POST"])
@login_required
def editprofile():
    form = ProfileForm()

    # pre-fill form with existing bio
    if request.method == "GET":
        form.bio.data = current_user.bio   #helps to show bio if exists

    if form.validate_on_submit():
        current_user.bio = form.bio.data
        db.session.commit()
        flash("Profile updated successfully!", "success")
        return redirect(url_for("dashboard"))

    return render_template("preferences.html", form=form)


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_note(id):
    note = Quotes.query.get_or_404(id)
    form = QuoteForm(obj=note)
    if form.validate_on_submit():
        note.content = form.content.data
        db.session.commit()
        flash('Note updated!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('edit_note.html', form=form)

@app.route('/delete/<int:id>')
@login_required
def delete_note(id):
    note = Quotes.query.get_or_404(id)
    db.session.delete(note)
    db.session.commit()
    flash('Note deleted!', 'info')
    return redirect(url_for('dashboard'))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("you are logged out")
    return redirect(url_for("login"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

print("project by sanheeth")
