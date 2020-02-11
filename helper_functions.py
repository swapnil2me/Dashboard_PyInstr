import os
import re
import pandas as pd
import numpy as np
from sqlalchemy import create_engine


def createExperimentDbTable(data_directory,experiment_name):
    engine = create_engine('sqlite:///'+os.path.join(data_directory, 'experiments.db'), echo=False)
    r = re.compile("([\d\.\d]+)([a-zA-Z]+)")
    fileList = os.listdir(data_directory)
    for file in fileList:
        if file.endswith(".csv"):
            tableDict = {}
            strings = file.split('_')
            try:
                data = pd.read_csv(os.path.join(data_directory,file))
            except:
                continue
            keys = [string for string in strings if not r.match(string)][::-1]
            values = [r.match(string).groups() for string in strings if r.match(string)][::-1]
            while len(keys)>1:
                key = keys.pop()
                val = values.pop()
                tableDict[key] = val
                data[str(key)+'_'+str(val[1])] = [float(val[0])]*len(data)

            tableDict[keys[-1]] = values
            data.to_sql(experiment_name, con=engine, if_exists='append')


def getLatestFile(data_directory, past_stamp):
    fileList = os.listdir(data_directory)
    for file in fileList:
        #print(file)
        if file.endswith(".csv"):
            filename = os.path.join(data_directory,file)
            stamp = os.stat(filename).st_mtime
            if stamp > past_stamp:
                return file, stamp
    return 'empty',past_stamp


def updateCurrentRun(data_directory,experiment_name, past_stamp):
    r = re.compile("([\d\.\d]+)([a-zA-Z]+)")
    engine = create_engine('sqlite:///'+os.path.join(data_directory, 'experiments.db'), echo=False)
    file, stamp = getLatestFile(data_directory, past_stamp)
    if file != 'empty':
        tableDict = {}
        strings = file.split('_')
        try:
            data = pd.read_csv(os.path.join(data_directory,file))
        except:
            return past_stamp
        keys = [string for string in strings if not r.match(string)][::-1]
        values = [r.match(string).groups() for string in strings if r.match(string)][::-1]
        while len(keys)>1:
            key = keys.pop()
            val = values.pop()
            tableDict[key] = val
            data[str(key)+'_'+str(val[1])] = [float(val[0])]*len(data)

        tableDict[keys[-1]] = values
        data.to_sql(experiment_name, con=engine, if_exists='append')
    return stamp
