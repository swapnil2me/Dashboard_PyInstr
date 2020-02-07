import io
import random
from flask import Flask, jsonify, request, Response, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, create_engine
from flask_marshmallow import Marshmallow
import os
import helper_functions as hf
import pandas as pd
import numpy as np
import time

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.backends.backend_svg import FigureCanvasSVG

data_directory = "E:/Swapnil/temp"
experiment_name = 'Dispersion_2020_02_07'
startTime = time.time()
app = Flask(__name__)
app.debug = True
basedir = os.path.abspath(os.path.dirname(__file__))


engine = create_engine('sqlite:///'+os.path.join(data_directory, 'experiments.db'), echo=False)


@app.route("/")
def index():
    """ Returns html with the img tag for your plot.
    """
    num_x_points = int(request.args.get("num_x_points", 50))
    # in a real app you probably want to use a flask template.
    return render_template("index.html", num_x_points=num_x_points)
    # from flask import render_template
    # return render_template("yourtemplate.html", num_x_points=num_x_points)


@app.route("/matplot-as-image-<int:num_x_points>.png")
def plot_png(num_x_points=50):
    """ renders the plot on the fly.
    """
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    df = getCurrentDF()[['f','A','P']]
    x_points = df['f']
    axis.plot(x_points, df['A'])

    output = io.BytesIO()
    FigureCanvasAgg(fig).print_png(output)
    return Response(output.getvalue(), mimetype="image/png")


@app.route("/matplot-as-image-<int:num_x_points>.svg")
def plot_svg(num_x_points=50):
    """ renders the plot on the fly.
    """
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    df = getCurrentDF()[['f','A','P']]
    x_points = df['f']
    axis.plot(x_points, df['P'])

    output = io.BytesIO()
    FigureCanvasSVG(fig).print_svg(output)
    return Response(output.getvalue(), mimetype="image/svg+xml")


@app.route("/matplot-as-disp-<int:num_x_points>.svg")
def plot_disp_svg(num_x_points=50):
    """ renders the plot on the fly.
    """
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


@app.cli.command('db_create')
def db_create():
    hf.createExperimentDbTable(data_directory,experiment_name)
    print('Database Created !')


def list_tables():
    return engine.table_names()


def getCurrentDF():
    #print('--')
    #print((mylist))
    global startTime
    print('Looking for changes')
    startTime = hf.updateCurrentRun(data_directory,experiment_name, startTime)
    print('Updated DF on {}'.format(startTime))
    table = 'Dispersion_2020_02_07'
    df = pd.read_sql_table(table,'sqlite:///' + os.path.join(data_directory, 'experiments.db'))
    sweepSpace = {column : list(df[column].unique()) for column in df.columns if column not in ['f','A','P','index'] and len(df[column].unique()) > 1}
    currentSweep = {}
    for key, val in sweepSpace.items():
        currentSweep[key] = val[-1]
    return pd.merge(pd.DataFrame(currentSweep, index =[0]), df)

def getExperimentDF():
    #tables = list_tables()
    table = 'Dispersion_2020_02_07'
    tableDict = {}
    df = pd.read_sql_table(table,'sqlite:///' + os.path.join(data_directory, 'experiments.db'))
    sweepSpace = {column : list(df[column].unique()) for column in df.columns if column not in ['f','A','P','index'] and len(df[column].unique()) > 1}
    tableDict[table] = {'df':df,
                        'sweepSpace':sweepSpace}
    return tableDict


if __name__ == '__main__':

    import webbrowser

    #print(getCurrentDF()[['f','A','P']])
    #webbrowser.open("http://127.0.0.1:5000/")
    app.run()
