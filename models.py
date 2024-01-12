from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4

db = SQLAlchemy()

def get_uuid():
    return uuid4().hex

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)

class Configuration(db.Model):
    __tablename__ = "configuration"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    location = db.Column(db.String(255), nullable=False, default='Location')
    company_name = db.Column(db.String(255), nullable=False, default='vinayan pvt ltd')
    duplicate_time_span = db.Column(db.String(200), nullable=False, default='1 millisecond')
    device_unique_id = db.Column(db.String(50), nullable=False, default='vinayan pvt ltd')
    main_url = db.Column(db.String(255), nullable=False, default='rtsp://admin:intozi@123@192.168.1.63/live')
    substream_url = db.Column(db.String(255), nullable=False, default='rtsp://admin:intozi@123@192.168.1.63:554/cam/realmonitor?channel=1subtype=0')
    image_resolution = db.Column(db.String(20), nullable=False, default='1920x1080')
    
class Network(db.Model):
   
    __tablename__ = "network"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ethernet_ip = db.Column(db.String(25), nullable=False, default='192.168.1.119')
    router_ip = db.Column(db.String(25), nullable=False, default='192.168.1.1')
    domain_address = db.Column(db.String(25), nullable=False, default='192.168.1.1')
    
class CapturedVehicle(db.Model):
    __tablename__ = "captured_vehicle"
    id = db.Column(db.Integer, primary_key=True)
    image_path = db.Column(db.TEXT)
    vehicle_image = db.Column(db.TEXT)
    number_plate_image = db.Column(db.TEXT)
    created_datetime = db.Column(db.TEXT)
    modified_datetime = db.Column(db.TEXT)
    
class Video(db.Model):   
    __tablename__ = "video"  
    id = db.Column(db.Integer, primary_key=True)
    folder_path = db.Column(db.String)
    file = db.Column(db.String)
    DateTime = db.Column(db.String)
    created_date_time = db.Column(db.DateTime)
class Settings(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    frame_rate = db.Column(db.Integer, default=3)
    water_mark = db.Column(db.String(255), default='None')
    color_mode = db.Column(db.String(255), default='RGB')
    resolution = db.Column(db.String(255), default='1920x1080')