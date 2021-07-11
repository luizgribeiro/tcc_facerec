from flask import Flask, request
from flask_restful import Api
from flask_socketio import SocketIO
from flask_cors import CORS

from websocket.video_route import  VideoRoute
from rest.student_registry_route import StudentRegistryRoute

#controllers
from controllers.frame_controller import FrameController
from controllers.registry_controller import RegistryController
from controllers.face_detector_controller import FaceDetector
from controllers.face_finder_controller import FaceFinder
from controllers.students_controller import StudentsController
from controllers.face_list_controller import FaceListController
from controllers.attendance_controller import AttendanceController


from infra.db import DataBase
from dotenv import dotenv_values
import logging
logging.getLogger('socketio').setLevel(logging.ERROR)
logging.getLogger('engineio').setLevel(logging.ERROR)
config = dotenv_values(".env")
       
if __name__ == '__main__':

    try: 

        #database setup
        DataBase(config)
        
        #controllers setup
        students_cont = StudentsController()
        attendance_cont = AttendanceController()
        student_registry_cont = RegistryController(students_cont)
        face_list_cont = FaceListController()
        face_detector_cont = FaceDetector(face_list_cont, attendance_cont, students_cont)
        face_detector_cont.update_known_faces()
        face_finder_cont = FaceFinder()
        frame_cont = FrameController(face_detector_cont, face_finder_cont)


        #api setup
        app = Flask(__name__)
        CORS(app)

        #websocket api routes setup
        socketio = SocketIO(app, cors_allowed_origins="*", logger=False, engineio_logger=False)
        video_route = VideoRoute(frame_cont, socketio)

        #REST api routes setup
        api = Api(app)

        api.add_resource(StudentRegistryRoute, '/student_registry', resource_class_kwargs={
            'student_registry_controller': student_registry_cont,
            'frame_controller' : frame_cont,
            'face_detector_controller': face_detector_cont
            })


        socketio.run(app, host='0.0.0.0', port=5000)


    except Exception as e:
        print(e)
        exit(-1)
