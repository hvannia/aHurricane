import os, sys
import json

import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, desc

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask import Response

app = Flask(__name__)

#----------------------------------------------
# Return the homepage.


#Connect and Load data from csv into db:
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
engine = create_engine('sqlite:///db/Hurricane.sqlite', echo=False)
con = engine.connect()
con.execute('''CREATE TABLE IF NOT EXISTS Hurricanes(
                ID integer not null primary key, 
                Name Varchar (100),
                Time integer not null,
                Event Varchar (100),
                Status Varchar (100),
                Latitude integer not null,
                Longitude integer not null,
                Wind integer not null,
                Pressure integer not null,
                ISODate Varchar (100),
                Location Varchar (100)
                )''')

print("Creating database from csv file.")
csv_df = pd.read_csv('db/hurdat.csv', index_col=0)
csv_df.to_sql('Hurricanes', engine, if_exists='replace', index=True, index_label="id")

#landing page
@app.route("/")
def land():
    return render_template("timeline.html")


# timeline.html related
from getFromDb import getEvents, makeGeo, getEventHeader

@app.route("/b_events")  #background process - get all events
def back_events():
    allEvents = getEvents(engine)
    #print(allEvents[0])
    return jsonify(list(allEvents)) 

@app.route("/b_events/<id_x>")  #background process - get info for single event
def eventX(id_x):
    this_event_geo = makeGeo(engine,id_x)
    #print(this_event_geo)
    return jsonify(this_event_geo)

@app.route("/b_eventHeader/<id_x>")  #background process - get header for single event
def eventXHeader(id_x):
    this_event_header = getEventHeader(engine,id_x)
   # print(this_event_header)
    return this_event_header.to_json()

@app.route("/timeline")
def events():
    #try:
    return render_template("timeline.html")
    #except Exception, e:
     #   return (str(e))



if __name__ == "__main__":
    app.run(debug=True)


