from flask import Flask, render_template, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

app = Flask(__name__)

# Setup the SQLAlchemy database URI correctly
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Optional, to avoid a warning
app.config['SECRET_KEY'] = '1234567'

db = SQLAlchemy(app)

# User model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    
    # Constructor for creating a user with hashed password
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password  # Hash the password here
        
    # Function to check password
    def check_password(self, password):
        return check_password_hash(self.password, password)

# Create the database tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    print(f"Login Attempt: {username}, {password}")


    # Check if the username exists
    user = User.query.filter_by(username=username).first()

    if user:
        if user.check_password(password):
            # Set session for logged-in user
            session['username'] = user.username
            print(f"Session set for {username}")  # Debug: Check if session is being set
            return redirect('/dashboard')  # Redirect to dashboard
        else:
            # If password is incorrect, show the error on the login page
            error = 'Invalid password. Please try again.'
            return render_template('index.html', error=error)
    else:
        # If username does not exist, show the error on the login page
        error = 'Username not found. Please sign up first.'
        return render_template('index.html', error=error)


# Sign Up Route
@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    
    # For existing user by email
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        error = "Email is already registered! Please use a different one."
        return render_template('index.html', error=error)
    
    # For existing user by username
    existing_user_by_username = User.query.filter_by(username=username).first()
    if existing_user_by_username:
        error = "Username is already taken! Please choose a different one."
        return render_template('index.html', error=error)
    
    # Hash the password and create a new user
    hashed_password = generate_password_hash(password)
    new_user = User(username=username, email=email, password=hashed_password)
    
    db.session.add(new_user)
    db.session.commit()
    
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    # Use session.get() to avoid KeyError
    username = session.get('username')
    if username:
        user = User.query.filter_by(username=username).first()
        return render_template('dashboard.html', user=user)
    else:
        return redirect('/login')

@app.route('/user_profile')
def profile():
    if 'username' in session:
        user = User.query.filter_by(username=session['username']).first()
        return render_template('profile.html', username=user.username, email=user.email)
    return redirect('/')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

@app.route('/ecg')
def ecg():
    if "username" in session:
        return render_template('ecg.html')
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
