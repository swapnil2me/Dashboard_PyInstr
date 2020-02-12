"""https://gist.github.com/tebeka/5426211
"""
import io
import os
import random

from datetime import datetime as dt

from flask import Flask, jsonify, request, Response, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, create_engine
from flask_marshmallow import Marshmallow

import pandas as pd
import numpy as np
import time
import base64


import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.backends.backend_svg import FigureCanvasSVG


data_directory = "C:/Users/nemslab4/Documents/"
experiment_name = 'Dispersion'
startTime = dt.now()
app = Flask(__name__)
app.debug = True
basedir = os.path.abspath(os.path.dirname(__file__))


engine = create_engine('sqlite:///'+os.path.join(data_directory, 'experiments.db'), echo=False)


@app.route("/")
def index():

    #x = int(request.args.get("x", 50))
    return render_template("index.html")


@app.route("/fig")
def plot_svg():

    df = pd.read_sql_table(experiment_name,str(engine.url))
    sweepSpace = {column : list(df[column].unique()) for column in df.columns if column not in ['f','A','P','index','timeStamp']}
    df_fwd = df.loc[df['direction']==1]
    df_bkw = df.loc[df['direction']==-1]
    dfLen = len(df)
    freqLen = len(df['f'].unique())
    if dfLen%(freqLen*2) == 0:
        plotLenFwd = freqLen
        plotLenBkw = freqLen
    else:
        plotLen = dfLen%(freqLen*2)
        if plotLen > freqLen:
            plotLenFwd = freqLen
            plotLenBkw = plotLen - freqLen
        else:
            plotLenFwd = plotLen
            plotLenBkw = 0
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    df_fwd.tail(plotLenFwd).plot(ax=ax,x='f',y='P',style='r-')
    df_bkw.tail(plotLenBkw).plot(ax=ax,x='f',y='P',style='b-')

    ioFig = io.BytesIO()
    fig.savefig(ioFig, format='png')
    data = base64.encodestring(ioFig.getvalue()).decode('utf-8')
    html = '''
            <html>
                <body>
                    <img src="data:image/png;base64,{}" />
                </body>
            </html>
            '''
    return html.format(data)



@app.route("/matplot-as-disp.svg")
def plot_disp_svg():
    tableDict = getExperimentDF()
    for key, val in tableDict.items():
        print(key)
        df = val['df']
        sweepSpace = val['sweepSpace']
        for sweep, volt in sweepSpace.items():
            y = df[df[sweep]==volt[0]]['f']
            x = volt
            X,Y = np.meshgrid(x,y)
            ZA = np.array(df['A'])
            ZA = ZA.reshape(X.T.shape).T
            ZP = np.array(df['P'])
            ZP = ZP.reshape(X.T.shape).T
            fig, (ax0, ax1) = plt.subplots(2, 1)
            c = ax0.pcolor(X, Y, ZA, cmap='RdBu')
            fig.colorbar(c, ax=ax0)
            c = ax1.pcolor(X, Y, ZP, cmap='RdBu')
            fig.colorbar(c, ax=ax1)

    output = io.BytesIO()
    FigureCanvasSVG(fig).print_svg(output)
    return Response(output.getvalue(), mimetype="image/svg+xml")


if __name__ == '__main__':

    #import webbrowser
    #webbrowser.open("http://127.0.0.1:5000/")
    app.run(port=8001)
