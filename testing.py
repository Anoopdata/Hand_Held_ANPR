# # Import necessary modules and classes


# from flask import Flask, Response, render_template, jsonify, request, session, send_file, abort,send_from_directory
# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime,date
# from flask import Flask, render_template, send_from_directory
# import os
# import glob
# from flask_cors import CORS
# from flask import send_file, url_for, jsonify
# from threading import Thread
# import numpy as np
# import cv2
# from models import db, User, Configuration, Network,CapturedVehicle,Settings,Video
# from detection_cls import Ppe_Detection_1
# from multiple_detection_copy import Ppe_Detection
# from flask import Flask, Response, render_template, jsonify,request,session,send_file,abort
# #C:\flask_dev\flaskreact\app.py
# from flask_bcrypt import Bcrypt #pip install Flask-Bcrypt = https://pypi.org/project/Flask-Bcrypt/
# from flask_cors import CORS, cross_origin #ModuleNotFoundError: No module named 'flask_cors' = pip install Flask-Cors
# from flask import Flask, render_template, send_from_directory, jsonify, send_file,request

# # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trilok.db'
# # Initialize the line parameters (y-coordinate where the line will be drawn)
# # You can adjust this value based on your setup
# margin = 20
# line_y = 150
# desired_frame_size = (800, 380)

# app = Flask(__name__)
# CORS(app, resources={r"/save-settings": {"origins": "http://localhost:3000"}})
# CORS(app, supports_credentials=True)
# app.config['IMAGE_FOLDER'] = os.path.abspath(r'C:\Users\anoop\Documents\sign\venv\flaskreact\24-11-2023')
# app.config['SECRET_KEY'] = 'cairocoders-ednalan'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fla.db'
# SQLALCHEMY_TRACK_MODIFICATIONS = False
# SQLALCHEMY_ECHO = True
# bcrypt = Bcrypt(app)
# CORS(app, supports_credentials=True)
# db.init_app(app)

# # db = SQLAlchemy(app)


# # db.create_all()
# # Provide the absolute path to the videos directory
# videos_directory = os.path.abspath(r"C:\Users\anoop\Documents\sign\venv\flaskreact\2023-12-04\10_Hour")
# app.static_folder = videos_directory

# with app.app_context():
#     existing_files = set((video.folder_path, video.file) for video in Video.query.all())
#     for root, dirs, files in os.walk(videos_directory):
#         for file in files:
#             if file.endswith(".mp4"):
#                 folder_path = root
#                 file_name_with_extension = os.path.basename(file)
#                 file_name, file_extension = os.path.splitext(file_name_with_extension)
#                 file = file_name + '.mp4'
#                 DateTime = datetime.now().strftime('%Y-%m-%d')
#                 created_date_time = date.today()  # Replace this with the actual creation date of the file

#                 if (folder_path, file) not in existing_files:
#                     video = Video(folder_path=folder_path, file=file, DateTime=DateTime, created_date_time=created_date_time)
#                     db.session.add(video)
#                     existing_files.add((folder_path, file))  # Add to the existing files set

#     db.session.commit()
# def get_video_list():
#     video_folder = os.path.join(app.static_folder)
#     videos = []
#     for root, dirs, files in os.walk(video_folder):
#         for file in files:
#             if file.endswith(".mp4"):
#                 video_path = os.path.join(root, file)
#                 videos.append(os.path.relpath(video_path, video_folder))

#     return videos
# def fetch_and_update_data(target_image_path):
#     with app.app_context():
#         entries = CapturedVehicle.query.filter(CapturedVehicle.image_path.like(f"%{target_image_path}%")).all()

#         for entry in entries:
#             if entry.vehicle_image and entry.vehicle_image.startswith("frame"):
#                 entry.vehicle_image = send_file(os.path.join(app.config['IMAGE_FOLDER'], entry.image_path, entry.vehicle_image), mimetype='image/jpeg')
#             elif entry.number_plate_image and entry.number_plate_image.startswith("plate"):
#                 entry.number_plate_image = send_file(os.path.join(app.config['IMAGE_FOLDER'], entry.image_path, entry.number_plate_image), mimetype='image/jpeg')
#             else:
#                 print(f"Ignoring entry with ID {entry.id}")
#             entry.modified_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         db.session.commit()


# def insert_image_data(image_name, path):
#     date_added = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     with app.app_context():
#         if image_name.startswith("frame"):
#             plate_image_name = image_name.replace("frame", "plate")
#             plate_image_path = os.path.join(os.path.dirname(path), plate_image_name)
#             if os.path.exists(plate_image_path):
#                 new_image = CapturedVehicle(
#                     vehicle_image=image_name,
#                     number_plate_image=plate_image_name,
#                     image_path=date_added,
#                     created_datetime=date_added,
#                     modified_datetime=date_added
#                 )
#                 db.session.add(new_image)
#             else:
#                 print(f"Ignoring entry with frame image '{image_name}' as corresponding plate image not found.")
#         elif image_name.startswith("plate"):
#             frame_image_name = image_name.replace("plate", "frame")
#             frame_image_path = os.path.join(os.path.dirname(path), frame_image_name)
#             if os.path.exists(frame_image_path):
#                 new_image = CapturedVehicle(
#                     vehicle_image=frame_image_name,
#                     number_plate_image=image_name,
#                     image_path=date_added,
#                     created_datetime=date_added,
#                     modified_datetime=date_added
#                 )
#                 db.session.add(new_image)
#             else:
#                 print(f"Ignoring entry with plate image '{image_name}' as corresponding frame image not found.")
#         db.session.commit()
# def draw_line(frame, line_y):
#      cv2.line(frame, (0, line_y), (frame.shape[1], line_y), (0, 255, 0), 2)
# def is_vehicle_in_roi(x, y, w, h):
#     # Check if the bottom of the bounding box is below the ROI line
#     return (y + h / 2) > line_y

# def save_frame_and_plate(frame, cropped_img, detected_number_plate):
#     # Save the frame and number plate image in a folder with the current date
#     folder_path = os.path.join(os.getcwd(), current_date)

#     if not os.path.exists(folder_path):
#         os.makedirs(folder_path)

#     timestamp = datetime.datetime.now().strftime("%H-%M-%S")
#     frame_filename = os.path.join(folder_path, f"frame_{timestamp}.jpeg")
#     plate_filename = os.path.join(folder_path, f"plate_{timestamp}.jpeg")

#     cv2.imwrite(frame_filename, frame)
#     cv2.imwrite(plate_filename, cropped_img)
    
# def final_inference(frame):
#     with app.app_context():
#         net = cv2.dnn.readNet('ocr-tiny-v3-PI-256_200000.weights', 'ocr-tiny-v3-PI-256.cfg')
#         classes = []
#         with open("ocr.names", "r") as f:
#             classes = [line.strip() for line in f]
#         cropped_img = None
#         run = Ppe_Detection().detection(frame)
#         print("run", run)

#         try:
#             x, y, w, h, cls, conf = run[0]

#             if cls and (y + h / 2) > line_y:
#                 print("Number Plate detected:", cls)
#                 cropped_img = frame[y - margin:y + h + margin, x - margin:x + w + margin]
#                 save_frame_and_plate(frame, cropped_img,cls)  # Save the frame and plate within the app context
#                 gray_frame = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)
#                 blob = cv2.dnn.blobFromImage(gray_frame, scalefactor=1/255.0, size=(416, 416), swapRB=True, crop=False)
#                 net.setInput(blob)
#                 outs = net.forward(net.getUnconnectedOutLayersNames())
#                 boxes = []
#                 confidences = []
#                 class_ids = []

#                 for out in outs:
#                     for detection in out:
#                         scores = detection[5:]
#                         class_id = np.argmax(scores)
#                         confidence = scores[class_id]

#                         if confidence > 0.5:
#                             center_x = int(detection[0] * frame.shape[1])
#                             center_y = int(detection[1] * frame.shape[0])
#                             width = int(detection[2] * frame.shape[1])
#                             height = int(detection[3] * frame.shape[0])
#                             x = int(center_x - width / 2)
#                             y = int(center_y - height / 2)
#                             boxes.append([x, y, width, height])
#                             confidences.append(float(confidence))
#                             class_ids.append(class_id)

#                 indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
#                 for i in range(len(boxes)):
#                     if i in indices:
#                         x, y, width, height = boxes[i]
#                         label = str(classes[class_ids[i]])
#                         cv2.imwrite("Cropped_img.jpeg", cropped_img)
#                         print(label)
#         except Exception as e:
#             print("e", e)
#             pass
#     return frame, cropped_img
# def generate_frames():
#     main_str_url = 'sdffwefd'
#     cap = cv2.VideoCapture(r"rtsp://admin:vinayan@123@192.168.1.108:554/cam/realmonitor?channel=1&subtype=0")
#     fps = 60
#     delay = int(1000 / fps)

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break
#         frame = cv2.resize(frame, desired_frame_size)
#         draw_line(frame, line_y)
#         frame, cropped_img = final_inference(frame)
#         #vehicle = Ppe_Detection_1().detection(frame)
#         #print("Vehicle", vehicle)

#         _, buffer = cv2.imencode('.jpeg', frame)
#         frame_bytes = buffer.tobytes()

#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# @app.route('/api/settings', methods=['GET'])
# def get_settings():
#     settings = Settings.query.first()
#     if settings is not None:
#         return jsonify({
#             'frame_rate': settings.frame_rate,
#             'water_mark': settings.water_mark,
#             'color_mode': settings.color_mode,
#             'resolution': settings.resolution,
#         })
#     else:
#         # If no settings found, create a new record with default values
#         default_settings = Settings()
#         db.session.add(default_settings)
#         db.session.commit()

#         return jsonify({
#             'frame_rate': default_settings.frame_rate,
#             'water_mark': default_settings.water_mark,
#             'color_mode': default_settings.color_mode,
#             'resolution': default_settings.resolution,
#         })

# @app.route('/api/settings', methods=['POST'])
# def update_settings():
#     try:
#         settings = Settings.query.first()

#         if settings is None:
#             # If no settings found, create a new record with default values
#             settings = Settings()

#         settings.frame_rate = request.json.get('frame_rate', settings.frame_rate)
#         settings.water_mark = request.json.get('water_mark', settings.water_mark)
#         settings.color_mode = request.json.get('color_mode', settings.color_mode)
#         settings.resolution = request.json.get('resolution', settings.resolution)

#         db.session.add(settings)
#         db.session.commit()

#         return jsonify({
#             'frame_rate': settings.frame_rate,
#             'water_mark': settings.water_mark,
#             'color_mode': settings.color_mode,
#             'resolution': settings.resolution,
#         })

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500






# # @app.route("/",methods=['GET'])
# # def index():
# #     video_list = get_video_list()
# #     return render_template("index_vid.html", video_list=video_list)

# @app.route("/play_video/<filename>")
# def play_video(filename):
#     return render_template("video.html", filename=filename)

# @app.route("/videos/<filename>")
# def get_video(filename):
#     return send_from_directory(app.static_folder, filename)

# @app.route("/image", methods=['GET'])
# def display_images():
#     image_folder = r"C:\Users\anoop\Documents\sign\venv\flaskreact\24-11-2023"
#     image_files = os.listdir(image_folder)
#     with app.app_context():
#         data = CapturedVehicle.query.all()
#         result = []

#         for entry in data:
#             print(f"Processing entry with ID: {entry.id}")
#             result.append({
#                 'id': entry.id,
#                 'vehicle_image': f'http://localhost:5000/image/{entry.vehicle_image}',
#                 'number_plate_image': f'http://localhost:5000/image/{entry.number_plate_image}',
#                 'created_datetime': entry.created_datetime,
#             })
#     if request.headers.get('Accept') == 'application/json':
#         # If JSON is requested, return JSON
#         return jsonify({'data': result})
#     else:
#         # Otherwise, render the HTML template
#         return render_template("index_record.html", image_files=image_files, data=result)

# @app.route("/image/<filename>")
# def display_image(filename):
#     image_path = os.path.join(app.config['IMAGE_FOLDER'], filename)
#     if os.path.exists(image_path):
#         if request.headers.get('Accept') == 'application/json':
#             # If JSON is requested, return a JSON response
#             return jsonify({'image_url': f'http://localhost:5000/image/{filename}'})
#         else:
#             # Otherwise, serve the image
#             return send_from_directory(app.config['IMAGE_FOLDER'], filename)
#     else:
#         return "404 Not Found"


# @app.route("/signup", methods=["POST"])
# def signup():
#     name = request.json.get("name")
#     email = request.json["email"]
#     password = request.json["password"]
#       # Get the user's name from the request JSON data
#     user_exists = User.query.filter_by(email=email).first() is not None
#     if user_exists:
#         return jsonify({"error": "Email already exists"}), 409
#     hashed_password = bcrypt.generate_password_hash(password)
#     new_user = User(email=email, password=hashed_password, name=name)  # Add name to the User object
#     db.session.add(new_user)
#     db.session.commit()
#     session["user_id"] = new_user.id
#     return jsonify({
#         "id": new_user.id,
#         "name": new_user.name,  # Include the user's name in the response
#         "email": new_user.email
#     })
 
# @app.route("/login", methods=["POST"])
# def login_user():
#     email = request.json["email"]
#     password = request.json["password"]
#     user = User.query.filter_by(email=email).first()
#     if user is None:
#         return jsonify({"error": "Unauthorized Access"}), 401
#     if not bcrypt.check_password_hash(user.password, password):
#         return jsonify({"error": "Unauthorized"}), 401    
#     session["user_id"] = user.id 
#     return jsonify({
#         "id": user.id,
#         "email": user.email
#     })

# @app.route('/')
# def index():
#     return render_template('index.html')


# @app.route('/video_feed')
# def video_feed():
#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
#       # Serialize the data to JSON and send it to the frontend
      
# @app.route('/save-settings', methods=['POST', 'GET'])
# def configuration():
#     if request.method == 'GET':
#         config_data = Configuration.query.first()
#         if config_data is None:
#             config_data = {}
#         else:
#             config_data = {
#                 'location': config_data.location,
#                 'company_name': config_data.company_name,
#                 'duplicate_time_span': config_data.duplicate_time_span,
#                 'device_unique_id': config_data.device_unique_id,
#                 'main_url': config_data.main_url,
#                 'substream_url': config_data.substream_url,
#                 'image_resolution': config_data.image_resolution
#             }
#         return jsonify(config_data)
#     elif request.method == 'POST':
#         try:
#             data = request.get_json()
#             print("Received data:", data)
#             config = Configuration(
#                 location=data.get('location'),
#                 company_name=data.get('company_name'),
#                 duplicate_time_span=data.get('duplicate_time_span'),
#                 device_unique_id=data.get('device_unique_id'),
#                 main_url=data.get('main_url'),
#                 substream_url=data.get('substream_url'),
#                 image_resolution=data.get('image_resolution')
#             )
#             db.session.query(Configuration).delete()
#             db.session.add(config)
#             db.session.commit()
#             return jsonify({'location': data.get('location'),
#                             'company_name': data.get('company_name'),
#                             'duplicate_time_span': data.get('duplicate_time_span'),
#                             'device_unique_id': data.get('device_unique_id'),
#                             'main_url': data.get('main_url'),
#                             'substream_url': data.get('substream_url'),
#                             'image_resolution': data.get('image_resolution')})
            
#             return jsonify({'location': data.get('location'), 'company_name': data.get('company_name'), 'duplicate_time_span': data.get('duplicate_time_span'), 'device_unique_id': data.get('device_unique_id'), 'main_url': data.get('main_url'), 'substream_url': data.get('substream_url'), 'image_resolution': data.get('image_resolution')})
#         except Exception as e:
#             print(f"An error occurred: {e}")
#             return jsonify({'error': 'Internal Server Error'}), 500
#     else:
#         return jsonify({'error': 'Invalid request method'}), 400

# @app.route('/network-settings', methods=['POST', 'GET'])
# def network():
#     if request.method == 'GET':
#         config_data = Network.query.first()
#         if config_data is None:
#             config_data = {}
#         else:
#             config_data = {
#                 'ethernet_ip' : config_data.ethernet_ip,
#                 'router_ip' : config_data.router_ip,
#                 'domain_address' : config_data.domain_address
#             }
#         return jsonify(config_data)
#     elif request.method == 'POST':
#         try:
#             data = request.get_json()
#             config = Network(
                
#                 ethernet_ip = data.get('ethernet_ip'),
#                 router_ip = data.get('router_ip'),
#                 domain_address = data.get('domain_address')
#             )
#             db.session.query(Network).delete()
#             db.session.add(config)
#             db.session.commit()
            
#             return jsonify({'ethernet_ip': data.get('ethernet_ip'),
#                             'router_ip': data.get('router_ip'),
#                             'domain_address' : data.get('domain_address')})
#         except Exception as e:
#             print(f"An error occurred: {e}")
#             return jsonify({'error': 'Internal Server Error'}), 500
        
# def run_flask_app():
#     app.run(host='0.0.0.0', port=5000, debug=True)
          
# if __name__ == "__main__":
#     with app.app_context():
#         db.create_all()
#         print("Database and tables created successfully.")
#     for name in os.listdir(app.config['IMAGE_FOLDER']):
#         if name.endswith('.jpeg') or name.endswith('.png'):
#             path = os.path.join(app.config['IMAGE_FOLDER'], name)
#             insert_image_data(name, path)
#     fetch_and_update_data(datetime.now().strftime("%d-%m-%Y"))
#     app.run(debug=True)
#     Thread(target=app.run, args=('0.0.0.0', 5000)).start()
 
 
# Import necessary modules and classes
from flask import Flask, Response, render_template, jsonify, request, session, send_file, abort,send_from_directory
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,date
from flask import Flask, render_template, send_from_directory
import os
import glob
from flask_cors import CORS
from flask import send_file, url_for, jsonify
from threading import Thread
import numpy as np
import cv2
from models import db, User, Configuration, Network,CapturedVehicle,Video
from detection_cls import Ppe_Detection_1
from multiple_detection_copy import Ppe_Detection
from flask import Flask, Response, render_template, jsonify,request,session,send_file,abort
#C:\flask_dev\flaskreact\app.py
from flask_bcrypt import Bcrypt #pip install Flask-Bcrypt = https://pypi.org/project/Flask-Bcrypt/
from flask_cors import CORS, cross_origin #ModuleNotFoundError: No module named 'flask_cors' = pip install Flask-Cors
from flask import Flask, render_template, send_from_directory, jsonify, send_file,request

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trilok.db'
# Initialize the line parameters (y-coordinate where the line will be drawn)
# You can adjust this value based on your setup
margin = 20
line_y = 250
desired_frame_size = (800, 380)

app = Flask(__name__)
CORS(app, resources={r"/save-settings": {"origins": "http://localhost:3000"}})
CORS(app, supports_credentials=True)
app.config['IMAGE_FOLDER'] = os.path.abspath(r'/home/vinayan/sign/venv/flaskreact/24-11-2023')

app.config['SECRET_KEY'] = 'cairocoders-ednalan'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fla.db'
# app.config['UPLOAD_FOLDER'] = VIDEO_FOLDER
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True
bcrypt = Bcrypt(app)
CORS(app, supports_credentials=True)
db.init_app(app)
#db = SQLAlchemy(app)

VIDEO_FOLDER = r'/home/vinayan/sign/venv/flaskreact/2023-12-04/10_Hour'
def get_video_list():
    video_list = []
    for filename in os.listdir(VIDEO_FOLDER):
        if filename.endswith('.mp4'):
            video_path = os.path.join(VIDEO_FOLDER, filename)
            
            try:
                created_date_time = extract_creation_time(video_path)
            except Exception as e:
                # Handle the exception, log the error, and continue with the next file
                print(f"Error extracting creation time for {filename}: {str(e)}")
                continue

            video_url = f'http://localhost:5000/api/video/{filename}'
            video_list.append({'filename': filename, 'video_url': video_url, 'created_date_time': created_date_time})

            # Save video information to the database
            try:
                video_data = Video(filename=filename, video_url=video_url, created_date_time=created_date_time)
                db.session.add(video_data)
                db.session.commit()
            except Exception as e:
                # Handle the database operation exception, log the error, and continue with the next file
                db.session.rollback()
                print(f"Error saving video data for {filename} to the database: {str(e)}")

    return jsonify(video_list)

def extract_creation_time(video_path):
    # Replace this with your method to extract creation time from the video file
    # For example, you can use a library like moviepy or ffprobe to get the metadata
    # This is just a placeholder, update it based on your needs.
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

@app.route('/api/videos')
def api_get_video_list():
    try:
        return get_video_list()
    except Exception as e:
        # Handle the exception and return an appropriate error response
        return make_response(jsonify({'error': str(e)}), 500)

@app.route('/api/video/<filename>')
def get_video(filename):
    video_path = os.path.join(VIDEO_FOLDER, filename)
    try:
        return send_file(video_path, mimetype='video/mp4')
    except FileNotFoundError:
        # Handle the file not found exception and return a 404 response
        return make_response(jsonify({'error': 'Video not found'}), 404)
    except Exception as e:
        # Handle other exceptions and return an appropriate error response
        return make_response(jsonify({'error': str(e)}), 500)


# db = SQLAlchemy(app)


#db.create_all()
# Provide the absolute path to the videos directory
# videos_directory = os.path.abspath(r"/home/vinayan/sign/venv/flaskreact/2023-12-04")
# app.static_folder = videos_directory

# with app.app_context():
#     existing_files = set((video.folder_path, video.file) for video in Video.query.all())
#     for root, dirs, files in os.walk(videos_directory):
#         for file in files:
#             if file.endswith(".mp4"):
#                 folder_path = root
#                 file_name_with_extension = os.path.basename(file)
#                 file_name, file_extension = os.path.splitext(file_name_with_extension)
#                 file = file_name + '.mp4'
#                 DateTime = datetime.now().strftime('%Y-%m-%d')
#                 created_date_time = date.today()  # Replace this with the actual creation date of the file

#                 if (folder_path, file) not in existing_files:
#                     video = Video(folder_path=folder_path, file=file, DateTime=DateTime, created_date_time=created_date_time)
#                     db.session.add(video)
#                     existing_files.add((folder_path, file))  # Add to the existing files set

#     db.session.commit()
# def get_video_list():
#     video_folder = os.path.join(app.static_folder)
#     videos = []
#     for root, dirs, files in os.walk(video_folder):
#         for file in files:
#             if file.endswith(".mp4"):
#                 video_path = os.path.join(root, file)
#                 videos.append(os.path.relpath(video_path, video_folder))

#     return videos
def fetch_and_update_data(target_image_path):
    with app.app_context():
        entries = CapturedVehicle.query.filter(CapturedVehicle.image_path.like(f"%{target_image_path}%")).all()

        for entry in entries:
            if entry.vehicle_image and entry.vehicle_image.startswith("frame"):
                entry.vehicle_image = send_file(os.path.join(app.config['IMAGE_FOLDER'], entry.image_path, entry.vehicle_image), mimetype='image/jpeg')
            elif entry.number_plate_image and entry.number_plate_image.startswith("plate"):
                entry.number_plate_image = send_file(os.path.join(app.config['IMAGE_FOLDER'], entry.image_path, entry.number_plate_image), mimetype='image/jpeg')
            else:
                print(f"Ignoring entry with ID {entry.id}")
            entry.modified_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db.session.commit()


def insert_image_data(image_name, path):
    date_added = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with app.app_context():
        if image_name.startswith("frame"):
            plate_image_name = image_name.replace("frame", "plate")
            plate_image_path = os.path.join(os.path.dirname(path), plate_image_name)
            if os.path.exists(plate_image_path):
                new_image = CapturedVehicle(
                    vehicle_image=image_name,
                    number_plate_image=plate_image_name,
                    image_path=date_added,
                    created_datetime=date_added,
                    modified_datetime=date_added
                )
                db.session.add(new_image)
            else:
                print(f"Ignoring entry with frame image '{image_name}' as corresponding plate image not found.")
        elif image_name.startswith("plate"):
            frame_image_name = image_name.replace("plate", "frame")
            frame_image_path = os.path.join(os.path.dirname(path), frame_image_name)
            if os.path.exists(frame_image_path):
                new_image = CapturedVehicle(
                    vehicle_image=frame_image_name,
                    number_plate_image=image_name,
                    image_path=date_added,
                    created_datetime=date_added,
                    modified_datetime=date_added
                )
                db.session.add(new_image)
            else:
                print(f"Ignoring entry with plate image '{image_name}' as corresponding frame image not found.")
        db.session.commit()
def draw_line(frame, line_y):
     cv2.line(frame, (0, line_y), (frame.shape[1], line_y), (0, 255, 0), 2)
def is_vehicle_in_roi(x, y, w, h):
    # Check if the bottom of the bounding box is below the ROI line
    return (y + h / 2) > line_y

def save_frame_and_plate(frame, cropped_img, detected_number_plate):
    # Save the frame and number plate image in a folder with the current date
    folder_path = os.path.join(os.getcwd(), current_date)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    timestamp = datetime.datetime.now().strftime("%H-%M-%S")
    frame_filename = os.path.join(folder_path, f"frame_{timestamp}.jpeg")
    plate_filename = os.path.join(folder_path, f"plate_{timestamp}.jpeg")

    cv2.imwrite(frame_filename, frame)
    cv2.imwrite(plate_filename, cropped_img)
    
def final_inference(frame):
    with app.app_context():
        net = cv2.dnn.readNet('ocr-tiny-v3-PI-256_200000.weights', 'ocr-tiny-v3-PI-256.cfg')
        classes = []
        with open("ocr.names", "r") as f:
            classes = [line.strip() for line in f]
        cropped_img = None
        run = Ppe_Detection().detection(frame)
        print("run", run)

        try:
            x, y, w, h, cls, conf = run[0]

            if cls and (y + h / 2) > line_y:
                print("Number Plate detected:", cls)
                cropped_img = frame[y - margin:y + h + margin, x - margin:x + w + margin]
                save_frame_and_plate(frame, cropped_img,cls)  # Save the frame and plate within the app context
                gray_frame = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)
                blob = cv2.dnn.blobFromImage(gray_frame, scalefactor=1/255.0, size=(416, 416), swapRB=True, crop=False)
                net.setInput(blob)
                outs = net.forward(net.getUnconnectedOutLayersNames())
                boxes = []
                confidences = []
                class_ids = []

                for out in outs:
                    for detection in out:
                        scores = detection[5:]
                        class_id = np.argmax(scores)
                        confidence = scores[class_id]

                        if confidence > 0.5:
                            center_x = int(detection[0] * frame.shape[1])
                            center_y = int(detection[1] * frame.shape[0])
                            width = int(detection[2] * frame.shape[1])
                            height = int(detection[3] * frame.shape[0])
                            x = int(center_x - width / 2)
                            y = int(center_y - height / 2)
                            boxes.append([x, y, width, height])
                            confidences.append(float(confidence))
                            class_ids.append(class_id)

                indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
                for i in range(len(boxes)):
                    if i in indices:
                        x, y, width, height = boxes[i]
                        label = str(classes[class_ids[i]])
                        cv2.imwrite("Cropped_img.jpeg", cropped_img)
                        print(label)
        except Exception as e:
            print("e", e)
            pass
    return frame, cropped_img

def generate_frames():
    main_str_url = 'sdffwefd'
    cap = cv2.VideoCapture(r"C:\Users\anoop\Documents\sign\venv\flaskreact\2023-12-07\10_Hour\11.mp4")
    fps = 20
    delay = int(1000 / fps)

    while True:
        
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.resize(frame, desired_frame_size)
        draw_line(frame, line_y)
        frame, cropped_img = final_inference(frame)
        vehicle = Ppe_Detection_1().detection(frame)
        print("Vehicle", vehicle)
        _, buffer = cv2.imencode('.jpeg', frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')



# @app.route("/",methods=['GET'])
# def index():
#     video_list = get_video_list()
#     return render_template("index_vid.html", video_list=video_list)

# @app.route("/play_video/<filename>")
# def play_video(filename):
#     return render_template("video.html", filename=filename)

# @app.route("/videos/<filename>")
# def get_video(filename):
#     return send_from_directory(app.static_folder, filename)

@app.route("/image", methods=['GET'])
def display_images():
    image_folder = r"C:\Users\anoop\Documents\sign\venv\flaskreact\24-11-2023"
    image_files = os.listdir(image_folder)
    with app.app_context():
        data = CapturedVehicle.query.all()
        result = []

        for entry in data:
            print(f"Processing entry with ID: {entry.id}")
            result.append({
                'id': entry.id,
                'vehicle_image': f'http://localhost:5000/image/{entry.vehicle_image}',
                'number_plate_image': f'http://localhost:5000/image/{entry.number_plate_image}',
                'created_datetime': entry.created_datetime,
            })
    if request.headers.get('Accept') == 'application/json':
        # If JSON is requested, return JSON
        return jsonify({'data': result})
    else:
        # Otherwise, render the HTML template
        return render_template("index_record.html", image_files=image_files, data=result)

@app.route("/image/<filename>")
def display_image(filename):
    image_path = os.path.join(app.config['IMAGE_FOLDER'], filename)
    if os.path.exists(image_path):
        if request.headers.get('Accept') == 'application/json':
            # If JSON is requested, return a JSON response
            return jsonify({'image_url': f'http://localhost:5000/image/{filename}'})
        else:
            # Otherwise, serve the image
            return send_from_directory(app.config['IMAGE_FOLDER'], filename)
    else:
        return "404 Not Found"


@app.route("/signup", methods=["POST"])
def signup():
    name = request.json.get("name")
    email = request.json["email"]
    password = request.json["password"]
      # Get the user's name from the request JSON data
    user_exists = User.query.filter_by(email=email).first() is not None
    if user_exists:
        return jsonify({"error": "Email already exists"}), 409
    hashed_password = bcrypt.generate_password_hash(password)
    new_user = User(email=email, password=hashed_password, name=name)  # Add name to the User object
    db.session.add(new_user)
    db.session.commit()
    session["user_id"] = new_user.id
    return jsonify({
        "id": new_user.id,
        "name": new_user.name,  # Include the user's name in the response
        "email": new_user.email
    })
 
@app.route("/login", methods=["POST"])
def login_user():
    email = request.json["email"]
    password = request.json["password"]
    user = User.query.filter_by(email=email).first()
    if user is None:
        return jsonify({"error": "Unauthorized Access"}), 401
    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Unauthorized"}), 401    
    session["user_id"] = user.id 
    return jsonify({
        "id": user.id,
        "email": user.email
    })

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
      # Serialize the data to JSON and send it to the frontend
      
@app.route('/save-settings', methods=['POST', 'GET'])
def configuration():
    if request.method == 'GET':
        config_data = Configuration.query.first()
        if config_data is None:
            config_data = {}
        else:
            config_data = {
                'location': config_data.location,
                'company_name': config_data.company_name,
                'duplicate_time_span': config_data.duplicate_time_span,
                'device_unique_id': config_data.device_unique_id,
                'main_url': config_data.main_url,
                'substream_url': config_data.substream_url,
                'image_resolution': config_data.image_resolution
            }
        return jsonify(config_data)
    elif request.method == 'POST':
        try:
            data = request.get_json()
            print("Received data:", data)
            config = Configuration(
                location=data.get('location'),
                company_name=data.get('company_name'),
                duplicate_time_span=data.get('duplicate_time_span'),
                device_unique_id=data.get('device_unique_id'),
                main_url=data.get('main_url'),
                substream_url=data.get('substream_url'),
                image_resolution=data.get('image_resolution')
            )
            db.session.query(Configuration).delete()
            db.session.add(config)
            db.session.commit()
            return jsonify({'location': data.get('location'),
                            'company_name': data.get('company_name'),
                            'duplicate_time_span': data.get('duplicate_time_span'),
                            'device_unique_id': data.get('device_unique_id'),
                            'main_url': data.get('main_url'),
                            'substream_url': data.get('substream_url'),
                            'image_resolution': data.get('image_resolution')})
            
            return jsonify({'location': data.get('location'), 'company_name': data.get('company_name'), 'duplicate_time_span': data.get('duplicate_time_span'), 'device_unique_id': data.get('device_unique_id'), 'main_url': data.get('main_url'), 'substream_url': data.get('substream_url'), 'image_resolution': data.get('image_resolution')})
        except Exception as e:
            print(f"An error occurred: {e}")
            return jsonify({'error': 'Internal Server Error'}), 500
    else:
        return jsonify({'error': 'Invalid request method'}), 400

@app.route('/network-settings', methods=['POST', 'GET'])
def network():
    if request.method == 'GET':
        config_data = Network.query.first()
        if config_data is None:
            config_data = {}
        else:
            config_data = {
                'ethernet_ip' : config_data.ethernet_ip,
                'router_ip' : config_data.router_ip,
                'domain_address' : config_data.domain_address
            }
        return jsonify(config_data)
    elif request.method == 'POST':
        try:
            data = request.get_json()
            config = Network(
                
                ethernet_ip = data.get('ethernet_ip'),
                router_ip = data.get('router_ip'),
                domain_address = data.get('domain_address')
            )
            db.session.query(Network).delete()
            db.session.add(config)
            db.session.commit()
            
            return jsonify({'ethernet_ip': data.get('ethernet_ip'),
                            'router_ip': data.get('router_ip'),
                            'domain_address' : data.get('domain_address')})
        except Exception as e:
            print(f"An error occurred: {e}")
            return jsonify({'error': 'Internal Server Error'}), 500
        
def run_flask_app():
    app.run(host='0.0.0.0', port=5000, debug=True)      
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("Database and tables created successfully.")
    for name in os.listdir(app.config['IMAGE_FOLDER']):
        if name.endswith('.jpeg') or name.endswith('.png'):
            path = os.path.join(app.config['IMAGE_FOLDER'], name)
            insert_image_data(name, path)
    fetch_and_update_data(datetime.now().strftime("%d-%m-%Y"))
    app.run(debug=True)
    Thread(target=app.run, args=('0.0.0.0', 5000)).start()

# # Import necessary modules and classes
# from flask import Flask, Response, render_template, jsonify, request, session, send_file, abort,send_from_directory
# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime,date
# from flask import Flask, render_template, send_from_directory
# import os
# import glob
# from flask_cors import CORS
# from flask import send_file, url_for, jsonify
# from threading import Thread
# import numpy as np
# import cv2
# from models import db, User, Configuration, Network,CapturedVehicle,Video
# from detection_cls import Ppe_Detection_1
# from multiple_detection_copy import Ppe_Detection
# from flask import Flask, Response, render_template, jsonify,request,session,send_file,abort
# #C:\flask_dev\flaskreact\app.py
# from flask_bcrypt import Bcrypt #pip install Flask-Bcrypt = https://pypi.org/project/Flask-Bcrypt/
# from flask_cors import CORS, cross_origin #ModuleNotFoundError: No module named 'flask_cors' = pip install Flask-Cors
# from flask import Flask, render_template, send_from_directory, jsonify, send_file,request

# # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trilok.db'
# # Initialize the line parameters (y-coordinate where the line will be drawn)
# # You can adjust this value based on your setup
# margin = 20
# line_y = 250
# desired_frame_size = (800, 380)

# app = Flask(__name__)
# CORS(app, resources={r"/save-settings": {"origins": "http://localhost:3000"}})
# CORS(app, supports_credentials=True)
# app.config['IMAGE_FOLDER'] = os.path.abspath(r'/home/vinayan/sign/venv/flaskreact/24-11-2023')
# app.config['SECRET_KEY'] = 'cairocoders-ednalan'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fla.db'
# SQLALCHEMY_TRACK_MODIFICATIONS = False
# SQLALCHEMY_ECHO = True
# bcrypt = Bcrypt(app)
# CORS(app, supports_credentials=True)
# db.init_app(app)

# # db = SQLAlchemy(app)


# #db.create_all()
# # Provide the absolute path to the videos directory
# videos_directory = os.path.abspath(r"/home/vinayan/sign/venv/flaskreact/2023-12-04")
# app.static_folder = videos_directory

# with app.app_context():
#     existing_files = set((video.folder_path, video.file) for video in Video.query.all())
#     for root, dirs, files in os.walk(videos_directory):
#         for file in files:
#             if file.endswith(".mp4"):
#                 folder_path = root
#                 file_name_with_extension = os.path.basename(file)
#                 file_name, file_extension = os.path.splitext(file_name_with_extension)
#                 file = file_name + '.mp4'
#                 DateTime = datetime.now().strftime('%Y-%m-%d')
#                 created_date_time = date.today()  # Replace this with the actual creation date of the file

#                 if (folder_path, file) not in existing_files:
#                     video = Video(folder_path=folder_path, file=file, DateTime=DateTime, created_date_time=created_date_time)
#                     db.session.add(video)
#                     existing_files.add((folder_path, file))  # Add to the existing files set

#     db.session.commit()
# def get_video_list():
#     video_folder = os.path.join(app.static_folder)
#     videos = []
#     for root, dirs, files in os.walk(video_folder):
#         for file in files:
#             if file.endswith(".mp4"):
#                 video_path = os.path.join(root, file)
#                 videos.append(os.path.relpath(video_path, video_folder))

#     return videos
# def fetch_and_update_data(target_image_path):
#     with app.app_context():
#         entries = CapturedVehicle.query.filter(CapturedVehicle.image_path.like(f"%{target_image_path}%")).all()

#         for entry in entries:
#             if entry.vehicle_image and entry.vehicle_image.startswith("frame"):
#                 entry.vehicle_image = send_file(os.path.join(app.config['IMAGE_FOLDER'], entry.image_path, entry.vehicle_image), mimetype='image/jpeg')
#             elif entry.number_plate_image and entry.number_plate_image.startswith("plate"):
#                 entry.number_plate_image = send_file(os.path.join(app.config['IMAGE_FOLDER'], entry.image_path, entry.number_plate_image), mimetype='image/jpeg')
#             else:
#                 print(f"Ignoring entry with ID {entry.id}")
#             entry.modified_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         db.session.commit()


# def insert_image_data(image_name, path):
#     date_added = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     with app.app_context():
#         if image_name.startswith("frame"):
#             plate_image_name = image_name.replace("frame", "plate")
#             plate_image_path = os.path.join(os.path.dirname(path), plate_image_name)
#             if os.path.exists(plate_image_path):
#                 new_image = CapturedVehicle(
#                     vehicle_image=image_name,
#                     number_plate_image=plate_image_name,
#                     image_path=date_added,
#                     created_datetime=date_added,
#                     modified_datetime=date_added
#                 )
#                 db.session.add(new_image)
#             else:
#                 print(f"Ignoring entry with frame image '{image_name}' as corresponding plate image not found.")
#         elif image_name.startswith("plate"):
#             frame_image_name = image_name.replace("plate", "frame")
#             frame_image_path = os.path.join(os.path.dirname(path), frame_image_name)
#             if os.path.exists(frame_image_path):
#                 new_image = CapturedVehicle(
#                     vehicle_image=frame_image_name,
#                     number_plate_image=image_name,
#                     image_path=date_added,
#                     created_datetime=date_added,
#                     modified_datetime=date_added
#                 )
#                 db.session.add(new_image)
#             else:
#                 print(f"Ignoring entry with plate image '{image_name}' as corresponding frame image not found.")
#         db.session.commit()
# def draw_line(frame, line_y):
#      cv2.line(frame, (0, line_y), (frame.shape[1], line_y), (0, 255, 0), 2)
# def is_vehicle_in_roi(x, y, w, h):
#     # Check if the bottom of the bounding box is below the ROI line
#     return (y + h / 2) > line_y

# def save_frame_and_plate(frame, cropped_img, detected_number_plate):
#     # Save the frame and number plate image in a folder with the current date
#     folder_path = os.path.join(os.getcwd(), current_date)

#     if not os.path.exists(folder_path):
#         os.makedirs(folder_path)

#     timestamp = datetime.datetime.now().strftime("%H-%M-%S")
#     frame_filename = os.path.join(folder_path, f"frame_{timestamp}.jpeg")
#     plate_filename = os.path.join(folder_path, f"plate_{timestamp}.jpeg")

#     cv2.imwrite(frame_filename, frame)
#     cv2.imwrite(plate_filename, cropped_img)
    
# def final_inference(frame):
#     with app.app_context():
#         net = cv2.dnn.readNet('ocr-tiny-v3-PI-256_200000.weights', 'ocr-tiny-v3-PI-256.cfg')
#         classes = []
#         with open("ocr.names", "r") as f:
#             classes = [line.strip() for line in f]
#         cropped_img = None
#         run = Ppe_Detection().detection(frame)
#         print("run", run)

#         try:
#             x, y, w, h, cls, conf = run[0]

#             if cls and (y + h / 2) > line_y:
#                 print("Number Plate detected:", cls)
#                 cropped_img = frame[y - margin:y + h + margin, x - margin:x + w + margin]
#                 save_frame_and_plate(frame, cropped_img,cls)  # Save the frame and plate within the app context
#                 gray_frame = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)
#                 blob = cv2.dnn.blobFromImage(gray_frame, scalefactor=1/255.0, size=(416, 416), swapRB=True, crop=False)
#                 net.setInput(blob)
#                 outs = net.forward(net.getUnconnectedOutLayersNames())
#                 boxes = []
#                 confidences = []
#                 class_ids = []

#                 for out in outs:
#                     for detection in out:
#                         scores = detection[5:]
#                         class_id = np.argmax(scores)
#                         confidence = scores[class_id]

#                         if confidence > 0.5:
#                             center_x = int(detection[0] * frame.shape[1])
#                             center_y = int(detection[1] * frame.shape[0])
#                             width = int(detection[2] * frame.shape[1])
#                             height = int(detection[3] * frame.shape[0])
#                             x = int(center_x - width / 2)
#                             y = int(center_y - height / 2)
#                             boxes.append([x, y, width, height])
#                             confidences.append(float(confidence))
#                             class_ids.append(class_id)

#                 indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
#                 for i in range(len(boxes)):
#                     if i in indices:
#                         x, y, width, height = boxes[i]
#                         label = str(classes[class_ids[i]])
#                         cv2.imwrite("Cropped_img.jpeg", cropped_img)
#                         print(label)
#         except Exception as e:
#             print("e", e)
#             pass
#     return frame, cropped_img
# def generate_frames():
#     main_str_url = 'sdffwefd'
#     cap = cv2.VideoCapture("rtsp:/")
#     fps = 24
#     delay = int(1000 / fps)

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break
#         frame = cv2.resize(frame, desired_frame_size)
#         draw_line(frame, line_y)
#         frame, cropped_img = final_inference(frame)
#         #vehicle = Ppe_Detection_1().detection(frame)
#         #print("Vehicle", vehicle)

#         _, buffer = cv2.imencode('.jpeg', frame)
#         frame_bytes = buffer.tobytes()

#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')



# @app.route("/",methods=['GET'])
# def index():
#     video_list = get_video_list()
#     return render_template("index_vid.html", video_list=video_list)

# @app.route("/play_video/<filename>")
# def play_video(filename):
#     return render_template("video.html", filename=filename)

# @app.route("/videos/<filename>")
# def get_video(filename):
#     return send_from_directory(app.static_folder, filename)

# @app.route("/image", methods=['GET'])
# def display_images():
#     image_folder = r"/home/vinayan/sign/venv/flaskreact/24-11-2023"
#     image_files = os.listdir(image_folder)
#     with app.app_context():
#         data = CapturedVehicle.query.all()
#         result = []

#         for entry in data:
#             print(f"Processing entry with ID: {entry.id}")
#             result.append({
#                 'id': entry.id,
#                 'vehicle_image': f'http://localhost:5000/image/{entry.vehicle_image}',
#                 'number_plate_image': f'http://localhost:5000/image/{entry.number_plate_image}',
#                 'created_datetime': entry.created_datetime,
#             })
#     if request.headers.get('Accept') == 'application/json':
#         # If JSON is requested, return JSON
#         return jsonify({'data': result})
#     else:
#         # Otherwise, render the HTML template
#         return render_template("index_record.html", image_files=image_files, data=result)

# @app.route("/image/<filename>")
# def display_image(filename):
#     image_path = os.path.join(app.config['IMAGE_FOLDER'], filename)
#     if os.path.exists(image_path):
#         if request.headers.get('Accept') == 'application/json':
#             # If JSON is requested, return a JSON response
#             return jsonify({'image_url': f'http://localhost:5000/image/{filename}'})
#         else:
#             # Otherwise, serve the image
#             return send_from_directory(app.config['IMAGE_FOLDER'], filename)
#     else:
#         return "404 Not Found"


# @app.route("/signup", methods=["POST"])
# def signup():
#     name = request.json.get("name")
#     email = request.json["email"]
#     password = request.json["password"]
#       # Get the user's name from the request JSON data
#     user_exists = User.query.filter_by(email=email).first() is not None
#     if user_exists:
#         return jsonify({"error": "Email already exists"}), 409
#     hashed_password = bcrypt.generate_password_hash(password)
#     new_user = User(email=email, password=hashed_password, name=name)  # Add name to the User object
#     db.session.add(new_user)
#     db.session.commit()
#     session["user_id"] = new_user.id
#     return jsonify({
#         "id": new_user.id,
#         "name": new_user.name,  # Include the user's name in the response
#         "email": new_user.email
#     })
 
# @app.route("/login", methods=["POST"])
# def login_user():
#     email = request.json["email"]
#     password = request.json["password"]
#     user = User.query.filter_by(email=email).first()
#     if user is None:
#         return jsonify({"error": "Unauthorized Access"}), 401
#     if not bcrypt.check_password_hash(user.password, password):
#         return jsonify({"error": "Unauthorized"}), 401    
#     session["user_id"] = user.id 
#     return jsonify({
#         "id": user.id,
#         "email": user.email
#     })

# # @app.route('/')
# # def index():
# #     return render_template('index.html')


# @app.route('/video_feed')
# def video_feed():
#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
#       # Serialize the data to JSON and send it to the frontend
      
# @app.route('/save-settings', methods=['POST', 'GET'])
# def configuration():
#     if request.method == 'GET':
#         config_data = Configuration.query.first()
#         if config_data is None:
#             config_data = {}
#         else:
#             config_data = {
#                 'location': config_data.location,
#                 'company_name': config_data.company_name,
#                 'duplicate_time_span': config_data.duplicate_time_span,
#                 'device_unique_id': config_data.device_unique_id,
#                 'main_url': config_data.main_url,
#                 'substream_url': config_data.substream_url,
#                 'image_resolution': config_data.image_resolution
#             }
#         return jsonify(config_data)
#     elif request.method == 'POST':
#         try:
#             data = request.get_json()
#             print("Received data:", data)
#             config = Configuration(
#                 location=data.get('location'),
#                 company_name=data.get('company_name'),
#                 duplicate_time_span=data.get('duplicate_time_span'),
#                 device_unique_id=data.get('device_unique_id'),
#                 main_url=data.get('main_url'),
#                 substream_url=data.get('substream_url'),
#                 image_resolution=data.get('image_resolution')
#             )
#             db.session.query(Configuration).delete()
#             db.session.add(config)
#             db.session.commit()
#             return jsonify({'location': data.get('location'),
#                             'company_name': data.get('company_name'),
#                             'duplicate_time_span': data.get('duplicate_time_span'),
#                             'device_unique_id': data.get('device_unique_id'),
#                             'main_url': data.get('main_url'),
#                             'substream_url': data.get('substream_url'),
#                             'image_resolution': data.get('image_resolution')})
            
#             return jsonify({'location': data.get('location'), 'company_name': data.get('company_name'), 'duplicate_time_span': data.get('duplicate_time_span'), 'device_unique_id': data.get('device_unique_id'), 'main_url': data.get('main_url'), 'substream_url': data.get('substream_url'), 'image_resolution': data.get('image_resolution')})
#         except Exception as e:
#             print(f"An error occurred: {e}")
#             return jsonify({'error': 'Internal Server Error'}), 500
#     else:
#         return jsonify({'error': 'Invalid request method'}), 400

# @app.route('/network-settings', methods=['POST', 'GET'])
# def network():
#     if request.method == 'GET':
#         config_data = Network.query.first()
#         if config_data is None:
#             config_data = {}
#         else:
#             config_data = {
#                 'ethernet_ip' : config_data.ethernet_ip,
#                 'router_ip' : config_data.router_ip,
#                 'domain_address' : config_data.domain_address
#             }
#         return jsonify(config_data)
#     elif request.method == 'POST':
#         try:
#             data = request.get_json()
#             config = Network(
                
#                 ethernet_ip = data.get('ethernet_ip'),
#                 router_ip = data.get('router_ip'),
#                 domain_address = data.get('domain_address')
#             )
#             db.session.query(Network).delete()
#             db.session.add(config)
#             db.session.commit()
            
#             return jsonify({'ethernet_ip': data.get('ethernet_ip'),
#                             'router_ip': data.get('router_ip'),
#                             'domain_address' : data.get('domain_address')})
#         except Exception as e:
#             print(f"An error occurred: {e}")
#             return jsonify({'error': 'Internal Server Error'}), 500
        
# def run_flask_app():
#     app.run(host='0.0.0.0', port=5000, debug=True)      
# if __name__ == "__main__":
#     with app.app_context():
#         db.create_all()
#         print("Database and tables created successfully.")
#     for name in os.listdir(app.config['IMAGE_FOLDER']):
#         if name.endswith('.jpeg') or name.endswith('.png'):
#             path = os.path.join(app.config['IMAGE_FOLDER'], name)
#             insert_image_data(name, path)
#     fetch_and_update_data(datetime.now().strftime("%d-%m-%Y"))
#     app.run(debug=True)
#     Thread(target=app.run, args=('0.0.0.0', 5000)).start()        












































    

# # def final_inference(frame):
# #     # Load YOLOv3 config and weights
# #     net = cv2.dnn.readNet('ocr-tiny-v3-PI-256_200000.weights', 'ocr-tiny-v3-PI-256.cfg')

# #     # Load class names (if available)
# #     classes = []
# #     with open("ocr.names", "r") as f:
# #         classes = [line.strip() for line in f]
# #         cropped_img = None  # Initialize cropped_img here
# #         run = Ppe_Detection().detection(frame)
# #         print("run",run)

# #         try:
# #             #run = Ppe_Detection().detection(frame)
# #             x, y, w, h, cls, conf = run[0]


# #             if cls and (y + h / 2) > line_y:
# #                 print("Number Plate detected:", cls)
# #                 cropped_img = frame[y - margin:y + h + margin, x - margin:x + w + margin]
# #                 gray_frame = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)
# #                 blob = cv2.dnn.blobFromImage(gray_frame, scalefactor=1/255.0, size=(416, 416), swapRB=True, crop=False)
# #                 net.setInput(blob)
# #                 outs = net.forward(net.getUnconnectedOutLayersNames())
# #             boxes = []
# #             confidences = []
# #             class_ids = []

# #             for out in outs:
# #                 for detection in out:
# #                     scores = detection[5:]
# #                     class_id = np.argmax(scores)
# #                     confidence = scores[class_id]

# #                     if confidence > 0.5:  # You can adjust this confidence threshold
# #                         center_x = int(detection[0] * frame.shape[1])
# #                         center_y = int(detection[1] * frame.shape[0])
# #                         width = int(detection[2] * frame.shape[1])
# #                         height = int(detection[3] * frame.shape[0])

# #                         # Calculate coordinates for the top-left corner of the bounding box
# #                         x = int(center_x - width / 2)
# #                         y = int(center_y - height / 2)

# #                         boxes.append([x, y, width, height])
# #                         confidences.append(float(confidence))
# #                         class_ids.append(class_id)

# #             # Apply non-maximum suppression to remove overlapping bounding boxes
# #             indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

# #             # Draw bounding boxes on the frame
# #             for i in range(len(boxes)):
# #                 if i in indices:
# #                     x, y, width, height = boxes[i]
# #                     label = str(classes[class_ids[i]])
                    
# #                     cv2.imwrite("Cropped_img.png",cropped_img)
# #                     print(label)

# #                     # print("\n\n")
# #                     confidence = confidences[i]
# #                     #cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 255, 0), 2)
# #                     # cv2.putText(frame, f"{label} {confidence:.2f}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
# #         except Exception as e:
# #             print("e",e)
# #             pass

    
# #     return frame,cropped_img
# #         # Display the result frame

# #         #process the outputs and draw bounding boxes - similar to your previous code)

# # def generate_frames():
# #      # Open a video file or capture video from a camera
# #     cap = cv2.VideoCapture("15.mp4")

# #     # Calculate delay based on desired frame rate (e.g., 30 frames per second)
# #     fps = 20
# #     delay = int(1000 / fps)

# #     while True:
# #         ret, frame = cap.read()
# #         if not ret:
# #             break
# #         # Display the frame


# #         frame = cv2.resize(frame, desired_frame_size)
# #         draw_line(frame, line_y)
# #         frame, cropped_img = final_inference(frame)
# #         # cv2.imshow("Number Plate Detection", frame)
# #         vehicle = Ppe_Detection_1().detection(frame)
# #         print("Vehicle",vehicle)

# #         # if cropped_img is not None and cropped_img.shape[0] > 0 and cropped_img.shape[1] > 0:
# #             # cv2.imshow("Number Plate Detection Cropped", cropped_img)
# #         # if cropped_img:
# #         #     print("Cropped_img",cropped_img)
# #         #     cv2.imwrite("Write.jpg",cropped_img)

# #         # # Break the loop if 'q' key is pressed
# #         # if cv2.waitKey(delay) & 0xFF == ord('q'):
# #         #     break

# #         _, buffer = cv2.imencode('.jpg', frame)
# #         frame = buffer.tobytes()

# #         yield (b'--frame\r\n'
# #                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


# #     # Release the video capture object and close all windows
# #     # cap.release()
# #     # cv2.destroyAllWindows()

# # @app.route('/')
# # def index():
# #     return render_template('index.html')

# # @app.route("/signup", methods=["POST"])
# # def signup():
# #     name = request.json.get("name")
# #     email = request.json["email"]
# #     password = request.json["password"]
# #       # Get the user's name from the request JSON data

# #     user_exists = User.query.filter_by(email=email).first() is not None

# #     if user_exists:
# #         return jsonify({"error": "Email already exists"}), 409

# #     hashed_password = bcrypt.generate_password_hash(password)
# #     new_user = User(email=email, password=hashed_password, name=name)  # Add name to the User object
# #     db.session.add(new_user)
# #     db.session.commit()

# #     session["user_id"] = new_user.id

# #     return jsonify({
# #         "id": new_user.id,
# #         "name": new_user.name,  # Include the user's name in the response
# #         "email": new_user.email
# #     })
 
# # @app.route("/login", methods=["POST"])
# # def login_user():
# #     email = request.json["email"]
# #     password = request.json["password"]
  
# #     user = User.query.filter_by(email=email).first()
  
# #     if user is None:
# #         return jsonify({"error": "Unauthorized Access"}), 401
  
# #     if not bcrypt.check_password_hash(user.password, password):
# #         return jsonify({"error": "Unauthorized"}), 401
      
# #     session["user_id"] = user.id
  
# #     return jsonify({
# #         "id": user.id,
# #         "email": user.email
# #     })

# # @app.route('/dashboard')
# # def video_feed():
# #     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# #       # Serialize the data to JSON and send it to the frontend

# # if __name__ == "__main__":
# #     app.run(debug=True)
# # # import cv2
# # # from flask import Flask, Response, render_template
# # # from flask_cors import CORS
# # # import numpy as np
# # # from multiple_detection_copy import Ppe_Detection
# # # from detection_cls import Ppe_Detection_1

# # # margin = 20
# # # desired_frame_size = (640, 480)
# # # line_y = 350

# # # app = Flask(__name__)
# # # CORS(app)

# # # def draw_line(frame, line_y):
# # #     cv2.line(frame, (0, line_y), (frame.shape[1], line_y), (0, 255, 0), 2)

# # # def final_inference(frame):
# # #     net = cv2.dnn.readNet('ocr-tiny-v3-PI-256_200000.weights', 'ocr-tiny-v3-PI-256.cfg')
# # #     classes = []
# # #     with open("ocr.names", "r") as f:
# # #         classes = [line.strip() for line in f]
# # #         cropped_img = None
# # #         run = Ppe_Detection().detection(frame)
# # #         print("run", run)

# # #         try:
# # #             x, y, w, h, cls, conf = run[0]

# # #             if cls and (y + h / 2) > line_y:
# # #                 print("Number Plate detected:", cls)
# # #                 cropped_img = frame[y - margin:y + h + margin, x - margin:x + w + margin]
# # #                 gray_frame = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)
# # #                 blob = cv2.dnn.blobFromImage(gray_frame, scalefactor=1/255.0, size=(416, 416), swapRB=True, crop=False)
# # #                 net.setInput(blob)
# # #                 outs = net.forward(net.getUnconnectedOutLayersNames())

# # #             boxes = []
# # #             confidences = []
# # #             class_ids = []

# # #             for out in outs:
# # #                 for detection in out:
# # #                     scores = detection[5:]
# # #                     class_id = np.argmax(scores)
# # #                     confidence = scores[class_id]

# # #                     if confidence > 0.5:
# # #                         center_x = int(detection[0] * frame.shape[1])
# # #                         center_y = int(detection[1] * frame.shape[0])
# # #                         width = int(detection[2] * frame.shape[1])
# # #                         height = int(detection[3] * frame.shape[0])

# # #                         x = int(center_x - width / 2)
# # #                         y = int(center_y - height / 2)

# # #                         boxes.append([x, y, width, height])
# # #                         confidences.append(float(confidence))
# # #                         class_ids.append(class_id)

# # #             indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

# # #             for i in range(len(boxes)):
# # #                 if i in indices:
# # #                     x, y, width, height = boxes[i]
# # #                     label = str(classes[class_ids[i]])

# # #                     cv2.imwrite("Cropped_img.png", cropped_img)
# # #                     print(label)

# # #         except Exception as e:
# # #             print("e", e)
# # #             pass

# # #     return frame, cropped_img

# # # def generate_frames():
# # #     cap = cv2.VideoCapture("Highway sounds cars trucks passing by for sleeping relaxing.mp4")
# # #     fps = 20
# # #     delay = int(1000 / fps)

# # #     while True:
# # #         ret, frame = cap.read()
# # #         if not ret:
# # #             break

# # #         frame = cv2.resize(frame, desired_frame_size)
# # #         draw_line(frame, line_y)
# # #         frame, cropped_img = final_inference(frame)
# # #         vehicle = Ppe_Detection_1().detection(frame)
# # #         print("Vehicle", vehicle)

# # #         _, buffer = cv2.imencode('.jpg', frame)
# # #         frame_bytes = buffer.tobytes()

# # #         yield (b'--frame\r\n'
# # #                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# # # @app.route('/')
# # # def index():
# # #     return render_template('index.html')

# # # @app.route('/video_feed')
# # # def video_feed():
# # #     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# # # if __name__ == "__main__":
# # #     app.run(debug=True)












































    

# def final_inference(frame):
#     # Load YOLOv3 config and weights
#     net = cv2.dnn.readNet('ocr-tiny-v3-PI-256_200000.weights', 'ocr-tiny-v3-PI-256.cfg')

#     # Load class names (if available)
#     classes = []
#     with open("ocr.names", "r") as f:
#         classes = [line.strip() for line in f]
#         cropped_img = None  # Initialize cropped_img here
#         run = Ppe_Detection().detection(frame)
#         print("run",run)

#         try:
#             #run = Ppe_Detection().detection(frame)
#             x, y, w, h, cls, conf = run[0]


#             if cls and (y + h / 2) > line_y:
#                 print("Number Plate detected:", cls)
#                 cropped_img = frame[y - margin:y + h + margin, x - margin:x + w + margin]
#                 gray_frame = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)
#                 blob = cv2.dnn.blobFromImage(gray_frame, scalefactor=1/255.0, size=(416, 416), swapRB=True, crop=False)
#                 net.setInput(blob)
#                 outs = net.forward(net.getUnconnectedOutLayersNames())
#             boxes = []
#             confidences = []
#             class_ids = []

#             for out in outs:
#                 for detection in out:
#                     scores = detection[5:]
#                     class_id = np.argmax(scores)
#                     confidence = scores[class_id]

#                     if confidence > 0.5:  # You can adjust this confidence threshold
#                         center_x = int(detection[0] * frame.shape[1])
#                         center_y = int(detection[1] * frame.shape[0])
#                         width = int(detection[2] * frame.shape[1])
#                         height = int(detection[3] * frame.shape[0])

#                         # Calculate coordinates for the top-left corner of the bounding box
#                         x = int(center_x - width / 2)
#                         y = int(center_y - height / 2)

#                         boxes.append([x, y, width, height])
#                         confidences.append(float(confidence))
#                         class_ids.append(class_id)

#             # Apply non-maximum suppression to remove overlapping bounding boxes
#             indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

#             # Draw bounding boxes on the frame
#             for i in range(len(boxes)):
#                 if i in indices:
#                     x, y, width, height = boxes[i]
#                     label = str(classes[class_ids[i]])
                    
#                     cv2.imwrite("Cropped_img.png",cropped_img)
#                     print(label)

#                     # print("\n\n")
#                     confidence = confidences[i]
#                     #cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 255, 0), 2)
#                     # cv2.putText(frame, f"{label} {confidence:.2f}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
#         except Exception as e:
#             print("e",e)
#             pass

    
#     return frame,cropped_img
#         # Display the result frame

#         #process the outputs and draw bounding boxes - similar to your previous code)

# def generate_frames():
#      # Open a video file or capture video from a camera
#     cap = cv2.VideoCapture("15.mp4")

#     # Calculate delay based on desired frame rate (e.g., 30 frames per second)
#     fps = 20
#     delay = int(1000 / fps)

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break
#         # Display the frame


#         frame = cv2.resize(frame, desired_frame_size)
#         draw_line(frame, line_y)
#         frame, cropped_img = final_inference(frame)
#         # cv2.imshow("Number Plate Detection", frame)
#         vehicle = Ppe_Detection_1().detection(frame)
#         print("Vehicle",vehicle)

#         # if cropped_img is not None and cropped_img.shape[0] > 0 and cropped_img.shape[1] > 0:
#             # cv2.imshow("Number Plate Detection Cropped", cropped_img)
#         # if cropped_img:
#         #     print("Cropped_img",cropped_img)
#         #     cv2.imwrite("Write.jpg",cropped_img)

#         # # Break the loop if 'q' key is pressed
#         # if cv2.waitKey(delay) & 0xFF == ord('q'):
#         #     break

#         _, buffer = cv2.imencode('.jpg', frame)
#         frame = buffer.tobytes()

#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


#     # Release the video capture object and close all windows
#     # cap.release()
#     # cv2.destroyAllWindows()

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route("/signup", methods=["POST"])
# def signup():
#     name = request.json.get("name")
#     email = request.json["email"]
#     password = request.json["password"]
#       # Get the user's name from the request JSON data

#     user_exists = User.query.filter_by(email=email).first() is not None

#     if user_exists:
#         return jsonify({"error": "Email already exists"}), 409

#     hashed_password = bcrypt.generate_password_hash(password)
#     new_user = User(email=email, password=hashed_password, name=name)  # Add name to the User object
#     db.session.add(new_user)
#     db.session.commit()

#     session["user_id"] = new_user.id

#     return jsonify({
#         "id": new_user.id,
#         "name": new_user.name,  # Include the user's name in the response
#         "email": new_user.email
#     })
 
# @app.route("/login", methods=["POST"])
# def login_user():
#     email = request.json["email"]
#     password = request.json["password"]
  
#     user = User.query.filter_by(email=email).first()
  
#     if user is None:
#         return jsonify({"error": "Unauthorized Access"}), 401
  
#     if not bcrypt.check_password_hash(user.password, password):
#         return jsonify({"error": "Unauthorized"}), 401
      
#     session["user_id"] = user.id
  
#     return jsonify({
#         "id": user.id,
#         "email": user.email
#     })

# @app.route('/dashboard')
# def video_feed():
#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

#       # Serialize the data to JSON and send it to the frontend

# if __name__ == "__main__":
#     app.run(debug=True)
# # import cv2
# # from flask import Flask, Response, render_template
# # from flask_cors import CORS
# # import numpy as np
# # from multiple_detection_copy import Ppe_Detection
# # from detection_cls import Ppe_Detection_1

# # margin = 20
# # desired_frame_size = (640, 480)
# # line_y = 350

# # app = Flask(__name__)
# # CORS(app)

# # def draw_line(frame, line_y):
# #     cv2.line(frame, (0, line_y), (frame.shape[1], line_y), (0, 255, 0), 2)

# # def final_inference(frame):
# #     net = cv2.dnn.readNet('ocr-tiny-v3-PI-256_200000.weights', 'ocr-tiny-v3-PI-256.cfg')
# #     classes = []
# #     with open("ocr.names", "r") as f:
# #         classes = [line.strip() for line in f]
# #         cropped_img = None
# #         run = Ppe_Detection().detection(frame)
# #         print("run", run)

# #         try:
# #             x, y, w, h, cls, conf = run[0]

# #             if cls and (y + h / 2) > line_y:
# #                 print("Number Plate detected:", cls)
# #                 cropped_img = frame[y - margin:y + h + margin, x - margin:x + w + margin]
# #                 gray_frame = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)
# #                 blob = cv2.dnn.blobFromImage(gray_frame, scalefactor=1/255.0, size=(416, 416), swapRB=True, crop=False)
# #                 net.setInput(blob)
# #                 outs = net.forward(net.getUnconnectedOutLayersNames())

# #             boxes = []
# #             confidences = []
# #             class_ids = []

# #             for out in outs:
# #                 for detection in out:
# #                     scores = detection[5:]
# #                     class_id = np.argmax(scores)
# #                     confidence = scores[class_id]

# #                     if confidence > 0.5:
# #                         center_x = int(detection[0] * frame.shape[1])
# #                         center_y = int(detection[1] * frame.shape[0])
# #                         width = int(detection[2] * frame.shape[1])
# #                         height = int(detection[3] * frame.shape[0])

# #                         x = int(center_x - width / 2)
# #                         y = int(center_y - height / 2)

# #                         boxes.append([x, y, width, height])
# #                         confidences.append(float(confidence))
# #                         class_ids.append(class_id)

# #             indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

# #             for i in range(len(boxes)):
# #                 if i in indices:
# #                     x, y, width, height = boxes[i]
# #                     label = str(classes[class_ids[i]])

# #                     cv2.imwrite("Cropped_img.png", cropped_img)
# #                     print(label)

# #         except Exception as e:
# #             print("e", e)
# #             pass

# #     return frame, cropped_img

# # def generate_frames():
# #     cap = cv2.VideoCapture("Highway sounds cars trucks passing by for sleeping relaxing.mp4")
# #     fps = 20
# #     delay = int(1000 / fps)

# #     while True:
# #         ret, frame = cap.read()
# #         if not ret:
# #             break

# #         frame = cv2.resize(frame, desired_frame_size)
# #         draw_line(frame, line_y)
# #         frame, cropped_img = final_inference(frame)
# #         vehicle = Ppe_Detection_1().detection(frame)
# #         print("Vehicle", vehicle)

# #         _, buffer = cv2.imencode('.jpg', frame)
# #         frame_bytes = buffer.tobytes()

# #         yield (b'--frame\r\n'
# #                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# # @app.route('/')
# # def index():
# #     return render_template('index.html')

# # @app.route('/video_feed')
# # def video_feed():
# #     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# # if __name__ == "__main__":
# #     app.run(debug=True)