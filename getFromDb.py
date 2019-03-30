import pandas as pd
import numpy as np
import flask
import json as js
#import pyproj as pp

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base


from geojson import LineString, Feature, Point, GeometryCollection, FeatureCollection

def makeGeo(engine,id):
    edf=  pd.read_sql('Select * from Hurricanes where id="'+id+'" Order by Date,Time',engine)
    ls=LineString(edf[['Longitude','Latitude']].values.tolist())
    dates=edf['ISODate'].values.tolist()
    winds=edf['Wind'].values.tolist()
    name= edf['Name'].unique()[0].strip() 
    f=Feature(geometry=ls,properties={"id":id, "name":name , "dates":dates, "winds":winds})
    fc=FeatureCollection([f])
    return fc

def getEventHeader(engine,id):
    evdf= pd.read_sql('SELECT id, name, min(Date) AS sdate, max(Date) AS edate, min(time) AS stime, max(Time) AS etime,  max(Wind) AS ws FROM Hurricanes WHERE id="'+id+'"',engine)
  
    return evdf


def getStyle(windsp):
    if windsp > 156 : return "cat5"
    elif windsp > 129 : return "cat4"
    elif windsp > 110 : return "cat3"
    elif windsp > 95 : return "cat2"
    elif windsp > 73 : return "cat1"
    elif windsp > 38 : return "tstorm"
    else: return "storm"

def getEvents(engine):
    evdf= pd.read_sql('SELECT id, name, min(Date) AS sdate, max(Date) AS edate, max(Wind) AS ws FROM Hurricanes GROUP BY id',engine)
    hurrs=[]
    for index, row in evdf.iterrows():
        st=getStyle(row['ws'])
        sdstr=str(row['sdate'])
        sdate=sdstr[0:4]+"-"+sdstr[4:6]+"-"+sdstr[6:8]
        edstr=str(row['edate'])
        edate=edstr[0:4]+"-"+edstr[4:6]+"-"+edstr[6:8]
        thisevent={ "id": row['id'], "start":sdate, "end":edate, "content":row['Name'].strip(), 'className':st }
        hurrs.append(thisevent)
    return hurrs






