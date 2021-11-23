#################################################
# Import libraries
#################################################

import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


# Home page route
# - List all routes available
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return (
        f"<h1>Welcome to the Weather Observation Home page!</h1><br/>"
        f"<br/>"
        f"<h2>Available Routes:</h2><br/>"
        f"<table border=1>"
        f"<tr>"
        f"<th style='padding: 10px'>Route</th><th style='padding: 10px'>Returns</th>"
        f"</tr>"
        f"<tr>"
        f"<td style='padding: 10px'>/</td><td style='padding: 10px'>This page</td>"
        f"</tr>"
        f"<tr>"
        f"<td style='padding: 10px'>/api/v1.0/precipitation</td><td style='padding: 10px'>Rainfall observations</td>"
        f"</tr>"
        f"<tr>"
        f"<td style='padding: 10px'>/api/v1.0/stations</td><td style='padding: 10px'>Weather observation stations</td>"
        f"</tr>"
        f"<tr>"
        f"<td style='padding: 10px'>/api/v1.0/tobs</td><td style='padding: 10px'>Temperature observations from the most active station for the past year</td>"
        f"</tr>"
        f"<tr>"
        f"<td style='padding: 10px'>/api/v1.0/&lt;start&gt;[/&lt;end&gt;]</td><td style='padding: 10px'>Returns minimum, average and maximum temperatures for the date range (yyyy-mm-dd)</td>"
        f"</tr>"
        f"</table>"
    )


# Precip route
# - report rain data
@app.route("/api/v1.0/precipitation")
def precip():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all rainfall observations"""
    # Query all rainfall measurements
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Convert list of tuples into dict
    all_precip = []
    
    for result in results:
        all_precip.append(dict(result))

    return jsonify(all_precip)


# Stations route
# - report station info
@app.route("/api/v1.0/stations")
def station():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all weather observation stations"""
    # Query all stations
    results = session.query(Station.id, Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()

    session.close()

    # Convert list of tuples into dict
    all_stations = []
    
    for result in results:
        all_stations.append(dict(result))

    return jsonify(all_stations)


# Temp obs route
# - report observed temperatures
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of temperature observations from the most active station for the last year"""
    # Get most active station
    station_activity = session.query(Measurement.station, func.count(Measurement.station).label('readings')).group_by(Measurement.station).all()
    station_activity.sort(reverse=True, key=lambda x:x[1])
    most_active = station_activity[0][0]


    # Get most recent date, prior year start date
    latest_text = session.query(func.max(Measurement.date)).all()[0][0]
    latest_list = latest_text.split("-")
    start_date = dt.date(int(latest_list[0]), int(latest_list[1]), int(latest_list[2])) - dt.timedelta(days=365)

    # Get requested temp data
    active_temps = session.query(Measurement.date, Measurement.tobs).\
        filter(func.strftime("%Y-%m-%d", Measurement.date) > start_date, Measurement.station == most_active).\
        all()

    session.close()

    # Convert list of tuples into dict
    last_year_temps = []

    for temp in active_temps:
        last_year_temps.append(dict(temp))
    
    return jsonify(last_year_temps)


# Temp obs route
# - report observed temperatures
@app.route("/api/v1.0/<start>")
def temp_stats_open(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of min, mean and max temperatures from the start date to the end of the data set"""

    # Validate start date input
    try:
        date_test = bool(dt.datetime.strptime(start, '%Y-%m-%d'))
    except ValueError:
        return f"Invalid date: {start}", 400
    
    # Get requested temp data
    temp_stats = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(func.strftime("%Y-%m-%d", Measurement.date) >= start).all()

    session.close()

    return_stats = {'TMIN': temp_stats[0][0], 'TAVG': temp_stats[0][1], 'TMAX': temp_stats[0][2]}

    return (jsonify(return_stats))


# Temp obs route
# - report observed temperatures
@app.route("/api/v1.0/<start>/<end>")
def temp_stats_closed(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of temperature observations from the most active station for the last year"""
    # Get most active station
    station_activity = session.query(Measurement.station, func.count(Measurement.station).label('readings')).group_by(Measurement.station).all()
    station_activity.sort(reverse=True, key=lambda x:x[1])
    most_active = station_activity[0][0]


    # Get most recent date, prior year start date
    latest_text = session.query(func.max(Measurement.date)).all()[0][0]
    latest_list = latest_text.split("-")
    start_date = dt.date(int(latest_list[0]), int(latest_list[1]), int(latest_list[2])) - dt.timedelta(days=365)

    # Get requested temp data
    active_temps = session.query(Measurement.date, Measurement.tobs).\
        filter(func.strftime("%Y-%m-%d", Measurement.date) > start_date, Measurement.station == most_active).\
        all()

    session.close()

    # Convert list of tuples into dict
    last_year_temps = []

    for temp in active_temps:
        last_year_temps.append(dict(temp))
    
    return (f"{start} {end}")



if __name__ == "__main__":
    app.run(debug=True)
