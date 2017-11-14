from flask import Flask
from flask import send_file
from flask import request
from flask import render_template
app = Flask(__name__)

import io
import numpy as np
import matplotlib.pyplot as plt
from fractions import Fraction


@app.route("/")
def hello():
    m = float(Fraction(request.args.get("m", default=1)))
    b = float(Fraction(request.args.get("b", default=0)))
    path = "api/v1/graph/{}/{}".format(m, b)
    return render_template("index.html", image=path)

@app.route('/api/v1/graph/<float:m>/<float:b>')
def get_image(m, b):
    f = io.BytesIO()
    graph(m, b, f)
    f.seek(0)
    return send_file(f, mimetype='image/png')

def graph(m, b, fp):
    plt.clf()
    x = np.linspace(-10, 10, num=500)
    plt.plot(x, m*x + b)
    plt.ylabel("{}x+{}".format(m, b))
    
    plt.savefig(fp)
    return fp
