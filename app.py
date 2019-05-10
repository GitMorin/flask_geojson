# Main app imports
from flask import Flask, request, jsonify

# To Create tables and db connection
from flask_sqlalchemy import SQLAlchemy
from geoalchemy2 import functions
from geoalchemy2.shape import to_shape
from geoalchemy2 import Geometry
from shapely import geometry
import geoalchemy2, shapely
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database, drop_database
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import load_only
import json
from geojson import Point, MultiLineString

# Init app
app = Flask(__name__)

# Database
conn_string = 'postgresql://postgres:postgres@localhost:5432/test'
app.config['SQLALCHEMY_DATABASE_URI'] = conn_string

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "SECRET_KEY"
app.config['DEBUG'] = True

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=True)
Session = sessionmaker(bind=engine)
session = Session() # Create a session - So we can add/remove/make changes to those objects before we commit them

# Define the model base
Base = declarative_base()

# Init SQLAlchemy
#db = SQLAlchemy(app)

# Product Class/Model
class Points(Base):
    __tablename__ = "points"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    description = Column(String(200))
    geom = Column(Geometry(geometry_type="POINT", srid=4326))

""" def __init__(self, name, description,):
    self.name = name
    self.description = description
    self.geom = geom """

#Base.metadata.create_all(bind=engine) # Can also be called from python itself after importing Base and engine

#point = Point()

""" point1 = Point()
point1.name = "Awesome place2"
point1.description = "Above could be said about this point"
point1.geom = 'SRID=4326;POINT({} {})'.format(11, 55)

point2 = Point()
point2.name = "Second point"
point2.description = "Nice place"
point2.geom = 'SRID=4326;POINT({} {})'.format(12, 56)

point3 = Point()
point3.name = "Point nr 3!"
point3.description = "Not so nice"
point3.geom = 'SRID=4326;POINT({} {})'.format(10, 52)

session.add(point1)
session.add(point2)
session.add(point3)
session.commit() """

# points = session.query(Point).all()

""" for point in points:
    print(point.name, point.geom, point.description) """

# session.close()

def kristians_amazing_jsonify(what_shit_you_want_me_to_jsonify):
    print(vars(what_shit_you_want_me_to_jsonify[0]))
    return {'ds':{p:v for p, v in vars(o).items() if p not in ('_sa_instance_state', 'geom')} for o in what_shit_you_want_me_to_jsonify }

@app.route('/', methods=['GET'])
def get_home():
    return jsonify({'msg': 'Hello World'})

@app.route('/points', methods=['GET'])
def get_points():
    smapping = shapely.geometry.geo.mapping
    
    #first_point = session.query(Points).first()

    all_points = session.query(Points).all()

    #all_points = session.query(functions.ST_AsGeoJSON(Points.geom)).all() #Does not work

    print(type(all_points[0]), all_points)

    for item in all_points:
        print(item, type(item))

    data = [
        {
            "type": "Feature", 
            "properties":{"description":point.description},
            "geometry":{"type":"Point",
            "coordinates":smapping(to_shape(point.geom))["coordinates"]},
        } for point in all_points]

    return jsonify({"type": "FeatureCollection", "features":data})


    #return jsonify({kristians_amazing_jsonify(all_points)})

    # return {'items':[item.json() for item in all_points]}


# Run Server
if __name__ == '__main__':
    app.run()