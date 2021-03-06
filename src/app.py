from imutils.video import VideoStream
from flask import Response
from flask import Flask
from flask import render_template
from flask import request
from flask_socketio import SocketIO
import threading 
import argparse 
import datetime
import imutils
import time 
import cv2 
from controllers.webcam_controller import WebcamController
from controllers.registry_controller import RegistryController
from controllers.face_detector_controller import FaceDetector
from controllers.face_finder_controller import FaceFinder
from controllers.students_controller import StudentsController
from controllers.db_controller import DataBase
from controllers.face_list_controller import FaceListController
from controllers.attendance_controller import AttendanceController
from models.students import Student
from models.attendance import Attendance

from datetime import datetime

output_frame = None 
lock = threading.Lock() 


app = Flask(__name__)
socketio = SocketIO(app)

DataBase('chamada_facial')


students_cont = StudentsController(Student)
student_registry_cont = RegistryController(students_cont)
attendance_cont = AttendanceController(Attendance)
face_list_cont = FaceListController(app)
face_detector_cont = FaceDetector(face_list_cont, attendance_cont)
face_detector_cont.update_known_faces(students_cont)
face_finder_cont = FaceFinder()

video = WebcamController(face_detector_cont, face_finder_cont, 0)


@app.route("/")
def index():
    return render_template("./index.htm")

@app.route("/cadastro.htm")
def cadastro():
    return render_template("./cadastro.htm")


@app.route("/video_feed")
def video_feed():
    return Response(video.gen_jpg_from_frame(lock), mimetype = "multipart/x-mixed-replace; boundary=frame")


@app.route("/cadastra_estudante", methods=['POST'])
def cadastra_estudante():
    
    face_desc = video.get_face_encodings(lock)

    if face_desc == None:
        return "no faces detected"
    elif len(face_desc) > 1:
        return "multiple faces detected"
    else:
        if student_registry_cont.add_registry(request.json, face_desc):
            face_detector_cont.update_known_faces(students_cont)
            return "face descriptors generated successfully!"
        else:
            return "Unable to register"


@socketio.on('update_atendences')
def update_atendences():
    if face_list_cont.has_detected():
        socketio.emit('updated_list', {'faces': face_list_cont.get_detected_faces()} )
    else:
        #TODO implement a clear alternative
        print('No updates available')



if __name__ == '__main__':

    socketio.run(app)


