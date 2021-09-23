from flask import Flask, request
from flask.templating import render_template

app = Flask(__name__)

@app.route("/")
def index():
    # if request.method == "POST":
    #     return render_template("image.html")
    return render_template("index.html")

@app.route("/image", methods=["GET", "POST"])
def image():
    return render_template("image.html")

@app.route("/advanced", methods=["GET", "POST"])
def advanced():
    return render_template("advanced.html")