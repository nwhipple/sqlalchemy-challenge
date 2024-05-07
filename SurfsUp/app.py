# Import the dependencies.
import numpy as np
import datetime as dt
import numpy as np
import pandas as pd
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
Base.prepare(autoload_with=engine)

# Save references to each table
Precipitation = Base.classes.measurement
Stations = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
session = Session(engine)
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
    )


@app.route("/api/v1.0/precipitation")
def passengers():
    # Create our session (link) from Python to the DB

    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all passengers
    results = session.query(Precipitation.date, Precipitation.prcp).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_prcp = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)


@app.route("/api/v1.0/stations")
def names():
    # Create our session (link) from Python to the DB

    """Return a list of all stations"""
    # Query all passengers
    results = session.query(Stations.name).all()

    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)

# Part 4: /api/v1.0/tobs
# Query the dates and temperature observations of the most-active station for the previous year of data.
#The TA walked me through all of the text below
@app.route("/api/v1.0/tobs")
def tobs():
    most_active_station = "USC00519281"
    query_date = dt.date(2017,8,23) - dt.timedelta(days=365)
    results = session.query(Precipitation.date, Precipitation.tobs).filter(Precipitation.station==most_active_station).filter(Precipitation.date>=query_date).all()
    df = results.DataFrame(results).to_dict("records")

# Return a JSON list of temperature observations for the previous year.
    session.close()
    return jsonify(df)
# Part 5: /api/v1.0/<start> and /api/v1.0/<start>/<end>
@app.route("/api/v1.0/<start>")
def userentry(start):
    results = session.query(func.min(Precipitation.tobs), func.avg(Precipitation.tobs), func.max(Precipitation.tobs)).filter(Precipitation.date>=start).first()
    session.close()
    return jsonify(list(results))

# Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.
@app.route("/api/v1.0/<start>/<end>")
def startend(start,end):
    results = session.query(func.min(Precipitation.tobs), func.avg(Precipitation.tobs), func.max(Precipitation.tobs)).filter(Precipitation.date>=start).filter(Precipitation.date<=end).first()
    session.close()
    return jsonify(list(results))
# For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.

# For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.


if __name__ == '__main__':
    app.run(debug=True)