#################################################
# Import libraries
#################################################

import numpy as np

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
        f"<td style='padding: 10px'>/api/v1.0/<start>[/<end>]</td><td style='padding: 10px'>Returns minimum, average and maximum temperatures for the date range (yyyy-mm-dd)</td>"
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




if __name__ == "__main__":
    app.run(debug=True)
