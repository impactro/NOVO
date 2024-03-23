from flask import Flask, render_template
from card1 import card1Upload
from removeBackground import removeBackground


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/removebg")
def removebg():
    return render_template("removebg.html")


@app.route("/removebg", methods=["POST"])
def removebgResult():
    return removeBackground()


@app.route("/card1")
def card1():
    return render_template("aplicaFundo.html")


@app.route("/card1", methods=["POST"])
def card1Result():
    return card1Upload()


if __name__ == "__main__":
    app.run(debug=True)
