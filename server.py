from flask import Flask, render_template, session, flash,redirect,request,url_for,jsonify
from flask_wtf import FlaskForm
import requests
from user import User
from flask_mail import Mail, Message
import pyrebase
import time
from wtforms import (
    EmailField,
    PasswordField,
    SubmitField,
    StringField,
    RadioField,

)
from wtforms.validators import (
    InputRequired,
    Length,
    ValidationError,
    DataRequired,
    Email,
)
from firebase_admin import credentials, auth, firestore, initialize_app


config = {
  "apiKey": "",
  "authDomain": "",
  "projectId": "",
  "storageBucket": "",
  "messagingSenderId": "",
  "appId": "",
  "measurementId": "",
  "databaseURL": ""
}

api_key = ''

firebase = pyrebase.initialize_app(config)
firebaseAuth = firebase.auth()

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key_here"
cred = credentials.Certificate(
    "key/"
)

app.config['MAIL_SERVER'] = ''
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = ''  # Use your actual Gmail address
app.config['MAIL_PASSWORD'] = ''     # Use your generated App Password
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)

initialize_app(cred)
user = None
db = firestore.client()
            

class RegistrationForm(FlaskForm):
    email = StringField(
        "Email Address",
        validators=[InputRequired(), Email(), Length(min=4, max=50)],
    )
    password = PasswordField(
        "New Password",
        [DataRequired(), Length(min=6, max=15)],
    )
    role = RadioField(choices=[('user', 'User'), ('admin', 'Admin'),('librarian','Librarian')],default='user',validators=[DataRequired()],render_kw={"class":"radio"})
    submit = SubmitField("Register",render_kw={"class":"auth-button"})

    def validate_email(self, field):
        try:
            user = auth.get_user_by_email(field.data)
        except ValueError:
            raise ValidationError("Email is inappropriate")
        except auth.UserNotFoundError:
            user = None
        if user:
            raise ValidationError("Email already in use")


class LoginForm(FlaskForm):
    email = EmailField(
        " Email",
        validators=[InputRequired(), Length(min=4, max=50),Email()],
    )
    password = PasswordField(
        "password",
        validators=[InputRequired(), Length(min=6, max=80)],
    )
    role = RadioField(choices=[('user', 'User'), ('admin', 'Admin'),('librarian','Librarian')],default='user',validators=[DataRequired()],render_kw={"class":"radio"})
    submit = SubmitField("Login",render_kw={"class":"auth-button"})

@app.route("/")
def index():
    return redirect(url_for("landing"))
    # return redirect(url_for("register"))

@app.route("/landing",methods=["GET","POST"])
def landing():
    if 'user_id' in session:
        if session['role'] == 'user':
            return redirect(url_for("dashboard"))    
        return redirect(url_for("librarian"))
    return render_template("landing.html",books=[],query_title="")
    


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if request.method == "POST" and form.validate_on_submit():
        try:
            user = auth.get_user_by_email(form.email.data)
            role = form.role.data
            user = db.collection(f"{role}s").document(user.uid).get().to_dict()
            print(user)
            if user:
                userLogin = firebaseAuth.sign_in_with_email_and_password(form.email.data, form.password.data)
                if userLogin:
                    session['user_id'] = user['id']
                    session['role'] = role
                    if role == 'user':
                        return redirect(url_for("dashboard"))
                    elif role == 'admin':
                        pass
                    elif role == 'librarian':
                        return redirect(url_for("librarian"))

        except:
            flash("Invalid email or password or role")
            return render_template("authentication/login.html", form=form)
    return render_template("authentication/login.html", form=form)

    


@app.route("/signout",methods=["GET","POST"])
def logout():
    session.pop('user_id', None) 
    session.pop('role', None)
    return redirect(url_for("index"))


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()

    try:
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            role = form.role.data
            user = auth.create_user(email=email, password=password)
            db.collection(f"{role}s").document(user.uid).set(
                {"email": email, "id": user.uid}
            )
            db.collection("userData").document(user.uid).set(
                {"email": email, "id": user.uid,"role":role,"name":"","age":"","gender":"","genre":[],"address":""}
            )
            return redirect(url_for("login"))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"Error in {field}: {error}")
                    flash(f"Error in {field}: {error}")
    except:
        flash("Email already in use")

    return render_template("authentication/register.html", form=form)
    
    


@app.route("/dashboard",methods=["GET","POST"])
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for("login"))

    user_info = db.collection("userData").document(session['user_id']).get().to_dict()
    print(user_info)
    return render_template("home/main.html",user=user_info,books=[])

@app.route("/librarian",methods=["GET","POST"])
def librarian():
    if 'user_id' not in session:
        return redirect(url_for("login"))
    return render_template("librarian/librarian.html",books=[],query_title="")

@app.route("/search",methods=["GET","POST"])
def search_books():
    if 'user_id' not in session:
        return redirect(url_for("login"))
    query = request.args.get('query')
    books = booksAPI(query)
    return render_template("home/main.html",books=books,user=user)


@app.route("/searchD",methods=["GET","POST"])
def search_books_default():
    if 'user_id' not in session:
        return redirect(url_for("login"))
    query = request.args.get('query')
    books = booksAPI(query)
    return render_template("landing.html",books=books,query_title=query)


@app.route("/searchL",methods=["GET","POST"])
def search_books_Library():
    query = request.args.get('query')
    books = booksAPI(query)
    return render_template("librarian/librarian.html",books=books,query_title=query)


def booksAPI(query):
    url = f'https://www.googleapis.com/books/v1/volumes?q={query}&key={api_key}'
    response = requests.get(url)
    data = response.json()
    books = data.get('items', [])  # Get the first 12 books
    return books

def send_email(email):
    msg = Message(
        subject='Hello from the other side!', 
        sender='sukarvumare@gmail.com',  # Ensure this matches MAIL_USERNAME
        recipients=[email]  # Replace with actual recipient's email
    )
    msg.body = "Hey, sending you this email from my Flask app, let me know if it works."
    mail.send(msg)
    return "Message sent!"



# Route to handle adding book to the database
@app.route('/add_book', methods=['POST'])
def add_book():
    data = request.json
    isbn = data.get('isbn')
    db.collection('library').document(isbn).set({
        'isbn': isbn,
        'quantity': 1
    })
    flash('Book added successfully!')


    # Simulating a response
    return jsonify({'message': 'Book added successfully'})

@app.route('/delete_book', methods=['POST'])
def deleteBook():
    data = request.json
    isbn = data.get('isbn')
    db.collection('library').document(isbn).delete()
    flash('Book Deleted successfully!')
    return jsonify({'message': 'Book Deleted successfully'})


@app.route('/issue_book', methods=['POST'])
def issueBook():
    data = request.json
    isbn = data.get('isbn')
    db.collection('userBooks').document(session['user_id']).collection('books').document(isbn).set({
        'isbn': isbn,
        'currentDate':time.time(),
        'dueDate': time.time() + 604800,
        'isRetured': False
    })
    flash('Book Issued successfully!')
    send_email(user['email'])
    return jsonify({'message': 'Book Issued successfully'})

@app.route('/return_book', methods=['POST'])
def returnBook():
    data = request.json
    isbn = data.get('isbn')
    db.collection('userBooks').document(session['user_id']).collection('books').document(isbn).update({
        'isRetured': True
    })
    flash('Book Returned successfully!')
    return jsonify({'message': 'Book Returned successfully'})



if __name__ == "__main__":
    app.run(debug=True)
