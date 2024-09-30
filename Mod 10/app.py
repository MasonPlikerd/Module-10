from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
import pandas as pd
from datetime import datetime, timedelta

# Database Setup
engine = create_engine('sqlite:///path_to_your_database.db')  # Replace with your database path
Base = automap_base()
Base.prepare(autoload_with=engine)

Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(bind=engine)

# Flask Setup
app = Flask(__name__)

# Flask Routes
@app.route('/api/v1.0/precipitation')
def precipitation():
    results = session.query(Measurement.date, Measurement.prcp).all()
    precipitation_data = {date: prcp for date, prcp in results}
    return jsonify(precipitation_data)

@app.route('/api/v1.0/stations')
def stations():
    results = session.query(Station.station).all()
    stations_list = [station[0] for station in results]
    return jsonify(stations_list)

@app.route('/api/v1.0/tobs/<station_id>')
def tobs(station_id):
    most_recent_date = session.query(func.max(Measurement.date)).scalar()
    one_year_ago = datetime.strptime(most_recent_date, '%Y-%m-%d') - timedelta(days=365)
    
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == station_id).\
        filter(Measurement.date >= one_year_ago).\
        all()
    
    tobs_data = [temp[0] for temp in results]
    return jsonify(tobs_data)

if __name__ == '__main__':
    app.run(debug=True)