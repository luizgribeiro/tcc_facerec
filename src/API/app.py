from flask import Flask
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



####### Old code #######
'''
#video = WebcamController(face_detector_cont, face_finder_cont, 0)


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
        return "no_faces"
    elif len(face_desc) > 1:
        return "multi_faces"
    else:
        if student_registry_cont.add_registry(request.json, face_desc):
            face_detector_cont.update_known_faces(students_cont)
            return "success"
        else:
            return "Unable to register"


@socketio.on('update_atendences')
def update_atendences():
    if face_list_cont.has_detected():
        socketio.emit('updated_list', {'faces': face_list_cont.get_detected_faces()} )
    else:
        #TODO implement a clear alternative
        print('No updates available')
'''
