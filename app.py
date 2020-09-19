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
station = Base.classes.station
measurement = Base.classes.measurement

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """Available api routes:"""
    return (
        f"Welcome to my sqlalchemy-challenge api!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start/<start><br/>"
        f"/api/v1.0/start/end/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Daily Precipitation Amounts"""
    # Query all passengers
    result = session.query(measurement.date, measurement.prcp).filter(measurement.date > '2016-08-23')
    
    session.close()

    # Convert results to dict and jsonify
    daily_prcp = []
    for date, prcp in result:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["prcp"] = prcp
        daily_prcp.append(precip_dict)


    return jsonify(daily_prcp)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Unique Station List"""
    # Query all passengers
    result = session.query(measurement.station).distinct().all()

    session.close()

    return jsonify(result)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Daily Temps at Most Active Station - USC00519281"""
    # Query all passengers
    result = session.query(measurement.date, measurement.tobs).filter(measurement.date > '2016-08-23').filter(measurement.station == 'USC00519281').all()

    session.close()

    return jsonify(result)

@app.route("/api/v1.0/start/<start>")
def temp_stats_start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Returns a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range."""
    
    result = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs) ).\
        filter(measurement.date == start).all()

    session.close()

    return jsonify(result)

@app.route("/api/v1.0/start/end/<start>/<end>")
def temp_stats_start_end(start, end):

    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Returns a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range."""
    
    result = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start).filter(measurement.date <= end).all()

    session.close()

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)