import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
render_template, flash, send_file
app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'graph.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))

app.config.from_envvar('GRAPH_SETTINGS', silent=True)

import io
import graphs.quadrants as quadrants
from fractions import Fraction


def connect_db():
    """Connects to the specific database"""
    rv = sqlit3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

@app.route("/", methods=["GET"])
def index():
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
