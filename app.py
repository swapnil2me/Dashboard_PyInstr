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
startTime = dt.now()
app = Flask(__name__)
#app.debug = True
basedir = os.path.abspath(os.path.dirname(__file__))

engine = create_engine('sqlite:///'+os.path.join(data_directory, 'experiments.db'), echo=False)

@app.route("/")
def index():
    experiments = engine.table_names()
    return render_template("index.html", experiments = experiments, directory = data_directory)


@app.route("/freqSweepLive-<experiment>")
def freqSweepLive(experiment):
    return render_template("freqResponse.html",experiment = experiment)


@app.route("/postSweepData-<experiment_name>")
def postSweepData(experiment_name):
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
    dataDict = {'fwd':{col: list(df_fwd.tail(plotLenFwd)[col]) for col in ['f','A','P']},
                'bkw':{col: list(df_bkw.tail(plotLenBkw)[col]) for col in ['f','A','P']}}
    response = jsonify(dataDict)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route("/fig")
def plot_svg():
    df = pd.read_sql_table("Dispersion",str(engine.url))
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

    dfIMG = df_fwd[['VgDC(V)','f','A']]

    imgdata = dfIMG.pivot(index='f',columns='VgDC(V)',values='A')
    #fig, ax = plt.subplots(figsize=(6,6))
    #ax.imshow(imgdata, cmap=plt.cm.Reds, interpolation='none', extent=[0,2,50,52])
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.imshow(imgdata, cmap=plt.cm.Reds, interpolation='none', extent=[0,2,50,52])
    output = io.BytesIO()
    FigureCanvasSVG(fig).print_svg(output)
    return Response(output.getvalue(), mimetype="image/svg+xml")


if __name__ == '__main__':

    import webbrowser
    webbrowser.open("http://127.0.0.1:8001/")
    app.run(port=8001)
