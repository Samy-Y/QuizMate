from flask import Flask,render_template

app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route("/")
def index():
    return render_template("index.html",css="static/styles.css")

@app.route("/signup")
def sign_up():
    return render_template("signup.html",css="static/styles.css")

app.run(debug=True)

# reload : aa