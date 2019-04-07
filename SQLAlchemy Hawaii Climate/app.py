import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Importing flask
from flask import Flask, jsonify


engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)


# Creating app an app
app = Flask(__name__)

@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    # List all routes that are available
    return (
        f"Welcome to Hawaii weather stations API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"-- Please enter dates as YYYY-MM-DD<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_date/end_date"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    print("Server received request for 'precipitation' page...")
    # Convert the query results to a Dictionary using date as the key and prcp as the value
    # Return the JSON representation of your dictionary
    results = session.query(Measurement.date, func.sum(Measurement.prcp).label("prcp")).\
            filter(Measurement.prcp != 'None').\
            group_by(Measurement.date).order_by(Measurement.date).all()
    all_precipitation = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        all_precipitation.append(precipitation_dict)
    return jsonify(all_precipitation)

@app.route("/api/v1.0/stations")
def stations():
    print("Server received request for 'stations' page...")
    # Return the JSON representation of your dictionary
    results = session.query(Station).all()
    all_stations = []
    for result in results:
        stations_dict = {}
        stations_dict["id"] = result.id
        stations_dict["station"] = result.station
        stations_dict["name"] = result.name
        stations_dict["latitude"] = result.latitude
        stations_dict["longitude"] = result.longitude
        stations_dict["elevation"] = result.elevation
        all_stations.append(stations_dict)
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    print("Server received request for 'tobs' page...")
    # query for the dates and temperature observations from a year from the last data point.
    # Return a JSON list of Temperature Observations (tobs) for the previous year
    results = session.query(Measurement.date, func.avg(Measurement.tobs).label("tobs")).\
            filter(Measurement.date >= '2016-08-23', Measurement.date <= '2017-08-23').\
            group_by(Measurement.date).order_by(Measurement.date).all()
    all_tobs = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        all_tobs.append(tobs_dict)
    return jsonify(all_tobs)

@app.route("/api/v1.0/<start_dt>")
def avg_min_max_start_dt(start_dt):
    print("Server received request for 'start' page...")
    # Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    # When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
    results = session.query(func.max(Measurement.date).label("ENDDT"), func.min(Measurement.tobs).label("TMIN"), func.avg(Measurement.tobs).label("TAVG"), func.max(Measurement.tobs).label("TMAX")).\
            filter(Measurement.date >= start_dt).all()
    all_tobs = []
    for result in results:
        tobs_dict = {}
        tobs_dict["STARTDT"] = start_dt
        tobs_dict["ENDDT"] = result.ENDDT
        tobs_dict["TMIN"] = result.TMIN
        tobs_dict["TAVG"] = result.TAVG
        tobs_dict["TMAX"] = result.TMAX
        all_tobs.append(tobs_dict)
    return jsonify(all_tobs)

@app.route("/api/v1.0/<start_dt>/<end_dt>")
def avg_min_max_start_end_dt(start_dt,end_dt):
    print("Server received request for 'start/end' page...")
    # Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    # When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
    results = session.query(func.min(Measurement.tobs).label("TMIN"), func.avg(Measurement.tobs).label("TAVG"), func.max(Measurement.tobs).label("TMAX")).\
            filter(Measurement.date >= start_dt, Measurement.date <= end_dt).all()
    all_tobs = []
    for result in results:
        tobs_dict = {}
        tobs_dict["STARTDT"] = start_dt
        tobs_dict["ENDDT"] = end_dt
        tobs_dict["TMIN"] = result.TMIN
        tobs_dict["TAVG"] = result.TAVG
        tobs_dict["TMAX"] = result.TMAX
        all_tobs.append(tobs_dict)
    return jsonify(all_tobs)

if __name__ == "__main__":
    app.run(debug=True)