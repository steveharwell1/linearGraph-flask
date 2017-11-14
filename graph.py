from flask import Flask
from flask import send_file
from flask import request
from flask import render_template
app = Flask(__name__)

import numpy as np
import matplotlib.pyplot as plt
from fractions import Fraction


@app.route("/")
def hello():
    m = float(Fraction(request.args.get("m", default=1)))
    b = float(Fraction(request.args.get("b", default=0)))
    path = graph(m, b)
    return render_template("index.html", image=path)

@app.route('/get_image')
def get_image():
    filename = request.args.get('image')
    return send_file(filename, mimetype='image/png')


def graph(m, b):
    plt.clf()
    x = np.linspace(-10, 10, num=500)
    plt.plot(x, m*x + b)
    plt.ylabel("{}x+{}".format(m, b))
    st = "img/{}{}.png".format(m, b)
    plt.savefig(st)
    return st
