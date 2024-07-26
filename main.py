from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import sqlite3

app = Flask(__name__)
app.secret_key = 'SomethingUniqueAndSecret'

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, id, username, email, password):
        self.id = id
        self.username = username
        self.email = email
        self.password = password

@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    if user:
        return User(user[0], user[1], user[2], user[3])
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        try:
            c.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', (username, email, password))
            conn.commit()
            flash('Account created successfully!', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username or email already exists', 'danger')
        finally:
            conn.close()
    return render_template('signup.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username,password))
        user = cursor.fetchone()
        conn.close()
        if user:
            print('success')

            user_obj = User(id=user[0],
                            username=user[1],
                            email=user[2],
                            password=user[3])
            login_user(user_obj)
            session['user_id'] = user[0]
            session['username'] = username
            session['email'] = user[2]
            session['password'] = user[3]
            return redirect(url_for("panel"))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template("login.html")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/panel')
@login_required
def panel():
    return render_template("panel.html",css="styles.css",username=session.get('username'))

@app.route("/account",methods=["GET","POST"])
@login_required
def account():
    if request.method == "GET":
        return render_template("account.html",css="styles.css",
                               username=session.get('username'),
                               email=session.get('email'),
                               password=session.get('password'))
    else:
        new_username = request.form.get('username')
        new_email = request.form.get('email')
        new_password = request.form.get('password')
        user_id = session.get('user_id')

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE username = ?, email = ?, password = ? WHERE id = ?;",(new_username,new_email,new_password))

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)
