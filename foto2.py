from flask import Flask, render_template
from removeBackground import removeBackground

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("removebg.html")


@app.route("/removebg", methods=["POST"])
def upload():
    return removeBackground()


if __name__ == "__main__":
    app.run(debug=True)
