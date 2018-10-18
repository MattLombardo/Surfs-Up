import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite", 
    connect_args={'check_same_thread': False})
Base = automap_base()
Base.prepare(engine, reflect=True)
Station = Base.classes.station
Measurement = Base.classes.measurement
session = Session(engine)

app = Flask(__name__)

@app.route("/")
def home():
    return (
        f"= Available Routes = <br/>"
        f"<br/>"
        f"<br/>"
        f"Precipitation over last 12 months: <br/> /api/v1.0/precipitation <br/>"
        f"<br/>"
        f"List of stations: <br/> /api/v1.0/stations <br/>"
        f"<br/>"
        f"List of temperature observations over the past year: <br/> /api/v1.0/tobs <br/>"
        f"<br/>"
        f"List of temperature min, avg, max starting on the start date (year-month-day): <br/> /api/v1.0/start <br/>"
        f"<br/>"
        f"List of temperature min, avg, max for date range (year-month-day): <br/> /api/v1.0/start/end <br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation_def():

    prcp_12_months = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= "2016-08-23").\
    order_by(Measurement.date).all()

    prcp_obs = []
    for i in range(0,len(prcp_12_months)):
        if prcp_12_months[i][1] == None:
            continue
        else:
            prcp_dict = {}
            prcp_dict["date"] = prcp_12_months[i][0]
            prcp_dict["prcp"] = prcp_12_months[i][1]
            prcp_obs.append(prcp_dict)
    
    return jsonify(prcp_obs)
    
@app.route("/api/v1.0/stations")
def stations_def():

    stations = session.query(Station.station).all()
    station_list = list(np.ravel(stations))

    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs_def():
    
    tobs_1_year = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= "2016-08-23").\
    order_by(Measurement.date).all()

    tobs_obs = []
    for i in range(0,len(tobs_1_year)):
        tobs_obs.append(tobs_1_year[i][1])
    
    tobs_list = list(np.ravel(tobs_obs))

    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def tobs_start_def(start):

    tobs_start = session.query(func.min(Measurement.tobs),
        func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).\
    group_by(Measurement.date).all()

    tobs_start_list = list(np.ravel(tobs_start))

    return jsonify(tobs_start_list)

@app.route("/api/v1.0/<start>/<end>")
def tobs_start_end_def(start,end):

    tobs_start_end = session.query(func.min(Measurement.tobs),
        func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).\
    filter(Measurement.date <= end).\
    group_by(Measurement.date).all()

    tobs_start_end_list = list(np.ravel(tobs_start_end))

    return jsonify(tobs_start_end_list)

if __name__ == '__main__':
    app.run(debug=True)
