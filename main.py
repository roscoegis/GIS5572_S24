import os
import sqlalchemy
import numpy
from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Yep!"


@app.route("/hello")
def hello():
    return "hello"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
