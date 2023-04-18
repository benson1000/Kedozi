from flask import Flask
from flask_bootstrap import Bootstrap
from os import path
from flask_login import LoginManager
import psycopg2
from . auth import *
from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from flask_login import login_required,logout_user, current_user,  login_user
import psycopg2 ##this is for connecting POSTGRES db with the python file.
from . forms import RegistrationForm, LoginForm
from flask_bcrypt import Bcrypt



def create_app():
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres@benso7130@kedozi"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
    app.config['SECRET_KEY'] = 'Thisisforkedozirealestatecompany'
    
    
auth = Blueprint("auth", __name__)
bcrypt = Bcrypt()

conn = psycopg2.connect(user = "postgres",password = "@benso7130",  host = "localhost",  database = "kedozi")
cursor = conn.cursor()

@auth.route('/register', methods=['GET','POST'], strict_slashes=False)
def register():
    if current_user.is_authenticated:
        return redirect(url_for("auth.dashboard"))
    form = RegistrationForm(request.form)
    
    # Get Form Values
    if request.method == 'POST' and form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        password = form.password.data
        
        hashed_password = bcrypt.generate_password_hash(password,10).decode('utf-8')
        
        #check if the user email exists
        #searching the user by email
        conn = psycopg2.connect(user = "postgres",password = "#",  host = "localhost",  database = "kedozi")
        cursor = conn.cursor()
        
        #user = cursor.execute("SELECT * FROM users WHERE email=%s", (form.email,)).fetchone()
            
        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user_exists = cursor.fetchone()
        if not user_exists:
            try:
                # Execute Query
                cursor.execute("""INSERT INTO users (first_name,last_name, email, password) 
                        VALUES(%s,%s, %s, %s)""", 
                        (first_name, last_name, email,  hashed_password))
                #commit to the users database
                conn.commit()
                conn.close()
            except:
                    flash("Something is wrong. Please try again later", 'danger')
                    return redirect(url_for('register'))
            else:
                #close the cursor
                cursor.close()
                flash("Successful Registration, Login", "success")
            return redirect(url_for('auth.login'))
        else:
            flash("Your email has already being registered. Please Login","danger")
            cursor.close()
        return redirect(url_for('auth.login'))
    
    # get the request
    return render_template('register.html', form=form, user=current_user)

@auth.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    if current_user.is_authenticated:
        return redirect(url_for("auth.dashboard"))
    form = LoginForm(request.form)
    
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password_candidate = form.password.data
        
        #search the user by email
        conn = psycopg2.connect(user = "postgres",password = "@benso7130",  host = "localhost",  database = "kedozi")
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE email=%s", (email, ))
        user = cursor.fetchone()
        #fname = results[1]
        #print(fname)
        
        #compare the passwords to check if they are similar
        if user:
            password = user[4]
            if bcrypt.check_password_hash(password, password_candidate):
                cursor.close()
                session['logged_in']= True
                session['email'] = email
                flash("Login successful","success")
                #login_user(user, remember=True)
                
                return redirect(url_for('auth.dashboard'))
                
            else:
                cursor.close()
                flash("INCORRECT password","danger")
                return render_template('login.html', form=form, title = 'login')
        else:
            # User email doesn't exist
            cursor.close()
            flash('EMAIL Does NOT exist, Please Register', 'danger')
        return redirect(url_for('auth.register'))
    #the login form
    return render_template('login.html', form=form, title='login', user=current_user)

@login_required
@auth.route('/dashboard', strict_slashes=False)
def dashboard():
    conn = psycopg2.connect(user = "postgres",password = "@benso7130",  host = "localhost",  database = "kedozi")
    cursor = conn.cursor()
    
    email = dict(session)['email']
    
    #cursor.execute("SELECT * FROM users WHERE email = %s",(email,))
    query1 = f"""SELECT first_name, last_name FROM users WHERE email='{email}'"""

    cursor.execute(query1)
    first_name = cursor.fetchone()

    cursor.close()
    #print(email)
    if first_name:
            return render_template('dashboard.html',
                                   first_name=first_name[0] + ' ' + first_name[1])
    else:
        print("Not available")
        
    return render_template('dashboard.html')


@auth.route('/more_information')
@login_required
def more_information():
    return "HELLO WORLD!!"

@login_required
@auth.route('/logout', strict_slashes=False)
#this functions logs out the user in session
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('views.home'))

def is_authenticated(self):
        return True 
    
    bootstrap = Bootstrap(app)
    
    from .views import views
    from .auth import auth
    
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    login_manager.login_message_category = "info"
    
    @login_manager.user_loader
    def load_user(email):
        
        #making the query into the database
        conn = psycopg2.connect(user = "postgres",password = "@benso7130",  host = "localhost",  database = "kedozi")
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()
        
        email = dict(session)['email']
        
        return user.email
    return app
