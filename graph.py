from flask import Flask
from flask import send_file
from flask import request
from flask import render_template
app = Flask(__name__)

import io
import quadrants
from fractions import Fraction


@app.route("/", methods=["GET"])
def hello():
    try:
        m = float(Fraction(request.args.get("m", default=1)))
    except(ValueError):
        m = 1.0
    try:
        b = float(Fraction(request.args.get("b", default=0)))
    except(ValueError):
        b = 0.0

    paths = list()
    paths.append({"path": "api/v1/linear/graph/{}/{}".format(m, b), "m": "{:.2}".format(m), "b": b})
    paths.append({"path": "api/v1/linear/graph/{}/{}".format(-m, b), "m": "{:.2}".format(-m), "b": b})
    paths.append({"path": "api/v1/linear/graph/{}/{}".format(1/m, b), "m": "{:.2}".format(1/m), "b": b})
    paths.append({"path": "api/v1/linear/graph/{}/{}".format(-1/m, b), "m": "{:.2}".format(-1/m), "b": b})

    return render_template("index.html", paths=paths)

@app.route('/api/v1/linear/graph/<m>/<b>')
def get_image(m, b):
    try:
        m = float(m)
    except(ValueError):
        m = 1
    try:
        b = float(b)
    except(ValueError):
        b = 0.0
    f = io.BytesIO()
    quadrants.make_quandrants(m, b, f)
    f.seek(0)
    return send_file(f, mimetype='image/png')
