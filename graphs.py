import os
import sqlite3
import requests
from flask import Flask, request, redirect, url_for, render_template, send_file
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
import quadrants
from fractions import Fraction
import qrcode


def connect_db():
    """Connects to the specific database"""
    rv = sqlit3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


@app.route("/", methods=["GET"])
def index():
    try:
        m = Fraction(request.args.get("m", default=1))
    except(ValueError):
        m = 1.0
    try:
        b = Fraction(request.args.get("b", default=0))
    except(ValueError):
        b = 0.0

    paths = [
       {"path":url_for("get_image", m=esc(m), b=b), "m":m, "b":b},
       {"path":url_for("get_image", m=esc(-m), b=b), "m":-m, "b":b},
       {"path":url_for("get_image", m=esc(1/m), b=b), "m":1/m, "b":b},
       {"path":url_for("get_image", m=esc(-1/m), b=b), "m":-1/m, "b":b},
    ]

    qrcodes = [
        url_for("get_qrcode", m=esc(m), b=b),
        url_for("get_qrcode", m=esc(-m), b=b),
        url_for("get_qrcode", m=esc(1/m), b=b),
        url_for("get_qrcode", m=esc(-1/m), b=b),
    ]

    return render_template("index.html", paths=paths, qrcodes=qrcodes)


@app.route('/api/v1/linear/graph/<m>/<b>')
def get_image(m, b):
    try:
        m = float(Fraction(unescape(m)))
    except(ValueError):
        m = 1
    try:
        b = float(Fraction(unescape(b)))
    except(ValueError):
        b = 0.0
    f = io.BytesIO()
    quadrants.make_quandrants(m, b, f)
    f.seek(0)
    return send_file(f, mimetype='image/png')


@app.route('/api/v1/linear/qrcode/<m>/<b>')
def get_qrcode(m, b):
    f = io.BytesIO()
    sitename = "http://192.168.0.13:5000"
    path = url_for("get_image", m=m, b=b)
    make_qrcode(path, f)
    f.seek(0)
    return send_file(f, mimetype='image/png')


def make_qrcode(path, fp):
    path = make_tinyurl(path)
    img = qrcode.make(path)
    img.save(fp)

def make_tinyurl(path):
    response = requests.get("http://www.tinyurl.com/api-create.php", params={"url": path})
    return response.content

def esc(exp):
    return str(exp).replace("/", "%2F")

def unescape(exp):
    return str(exp).replace("%2F" ,"/")
