from flask import Flask
from flask import send_file
from flask import request
from flask import render_template
app = Flask(__name__)

import io
import quadrants
from fractions import Fraction


@app.route("/", methods=["GET", "POST"])
def hello():
    m = request.args.get("m", default=1)
    b = request.args.get("b", default=0)
    path = "api/v1/linear/graph/{}/{}".format(m, b)
    return render_template("index.html", image=path)

@app.route('/api/v1/linear/graph/<m>/<b>')
def get_image(m, b):
    try:
        m = float(Fraction(m))
    except(ValueError):
        m = 1
    try:
        b = float(Fraction(b))
    except(ValueError):
        b = 0.0
    f = io.BytesIO()
    quadrants.make_quandrants(m, b, f)
    f.seek(0)
    return send_file(f, mimetype='image/png')
