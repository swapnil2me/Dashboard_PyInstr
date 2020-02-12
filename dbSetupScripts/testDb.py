"""
scource: https://hackersandslackers.com/sqlalchemy-data-models/
"""

import os
import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Float, Boolean, PickleType
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
data_directory = "C:/Users/nemslab4/Documents/"
experiment_name = 'Dispersion_2020_02_07'
db_uri = 'sqlite:///' + os.path.join(data_directory, 'experiments.db')
engine = create_engine(db_uri, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

class DispersioModel(Base):
    __tablename__ = experiment_name

    id = Column(Integer,
                primary_key=True,
                nullable=False)
    name = Column(String(100),
                  nullable=False)
    description = Column(Text,
                         nullable=True)


    def __repr__(self):
        return '<Example model {}>'.format(self.id)

Base.metadata.create_all(engine)

#print(dir(engine))

newModel = ExampleModel(name='todd',
                        description='im testing this',
                        )

#result = engine.execute('INSERT INTO "example_table" (name, description, join_date, vip) VALUES ("s", "s", "s", "s")')

# create table
engine.execute('CREATE TABLE "EX1" ('
               'id INTEGER NOT NULL,'
               'name VARCHAR, '
               'PRIMARY KEY (id));')
# insert a raw
engine.execute('INSERT INTO "example_table" '
               '(name, description) '
               'VALUES ("1","raw1")')
#"""INSERT INTO example_table (name, description, join_date, vip) VALUES (?, ?, ?, ?)""""
session.add(newModel)
session.commit()
print(newModel)
#print(result)
