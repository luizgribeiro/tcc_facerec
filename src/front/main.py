from imutils.video import VideoStream
from flask import Response
from flask import Flask
from flask import render_template


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("./index.htm")

@app.route("/cadastro.htm")
def cadastro():
    return render_template("./cadastro.htm")


app.run(host='0.0.0.0', port=8080)