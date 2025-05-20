from flask import Flask, render_template
#from flask_login import LoginManager
#from config import Config

app = Flask(__name__)

@app.route("/")
def welcome():
    return render_template('welcome.html')

if __name__ == '__main__':
    app.run(debug=True)