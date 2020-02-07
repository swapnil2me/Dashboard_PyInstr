import os
import re
import pandas as pd
import numpy as np
from sqlalchemy import Column, Integer, String, Float, create_engine


data_directory = "E:/Swapnil/temp"
experiment_name = 'Dispersion_2020_02_07'


def createExperimentDbTable(data_directory,experiment_name):
    engine = create_engine('sqlite:///'+os.path.join(data_directory, 'experiments.db'), echo=False)
    r = re.compile("([\d\.\d]+)([a-zA-Z]+)")
    fileList = os.listdir(data_directory)
    for file in fileList:
        if file.endswith(".csv"):
            tableDict = {}
            strings = file.split('_')
            data = pd.read_csv(os.path.join(data_directory,file))
            keys = [string for string in strings if not r.match(string)][::-1]
            values = [r.match(string).groups() for string in strings if r.match(string)][::-1]
            while len(keys)>1:
                key = keys.pop()
                val = values.pop()
                tableDict[key] = val
                data[str(key)+'_'+str(val[1])] = [val[0]]*len(data)

            tableDict[keys[-1]] = values
            data.to_sql(experiment_name, con=engine, if_exists='append')


createExperimentDbTable(data_directory,experiment_name)

#engine.execute("SELECT * FROM integers").fetchall()
class Monkey(object):
    def __init__(self):
        self._cached_stamp = 0
        self.filename = '/path/to/file'

    def ook(self):
        stamp = os.stat(self.filename).st_mtime
        if stamp != self._cached_stamp:
            self._cached_stamp = stamp
            # File has changed, so do something...
