import os
import re
import pandas as pd
import numpy as np

data_directory = "E:\\Swapnil\\temp"
fileList = os.listdir(data_directory)

r = re.compile("([\d\.\d]+)([a-zA-Z]+)")
for file in fileList:
    if file.endswith(".csv"):
        tableDict = {}
        strings = file.split('_')
        #print(strings)
        keys = [string for string in strings if not r.match(string)][::-1]
        values = [r.match(string).groups() for string in strings if r.match(string)][::-1]
        while len(keys)>1:
            tableDict[keys.pop()] = values.pop()
        tableDict[keys[-1]] = values
        print(tableDict)

#engine = create_engine('sqlite:///'+os.path.join(os.getcwd(), 'experiments.db'), echo=False)
#df.to_sql('users', con=engine)
class Monkey(object):
    def __init__(self):
        self._cached_stamp = 0
        self.filename = '/path/to/file'

    def ook(self):
        stamp = os.stat(self.filename).st_mtime
        if stamp != self._cached_stamp:
            self._cached_stamp = stamp
            # File has changed, so do something...
