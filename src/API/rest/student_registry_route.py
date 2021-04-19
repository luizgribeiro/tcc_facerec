import cv2
import numpy as np 
import base64
from flask_restful import Resource, reqparse
from .helpers.student_registry_args import add_args_keys

class StudentRegistryRoute(Resource):

    def __init__(self, **kwargs):
        self.student_registry_controller = kwargs['student_registry_controller']
        self.frame_controller = kwargs['frame_controller']
        self.face_detector_controller = kwargs['face_detector_controller']

    def post(self):
        
        parser = reqparse.RequestParser()
        add_args_keys(parser)
        args = parser.parse_args()

           
        frame = self.b64_to_frame(args['foto'])            
        face_desc = self.frame_controller.get_face_encodings(frame)

        if face_desc == None:
            return {"response" : "no_faces"}
        elif len(face_desc) > 1:
            return {"response": "multi_faces"}
        else:
            if self.student_registry_controller.add_registry(args, face_desc): 
                self.face_detector_controller.update_known_faces()
                return {"response": "success"}
            else :
                return {"response": "db_insert_error"}


    def b64_to_frame(self, frame_value):

        base64_request_string = frame_value.split(',')[1]
    
        base64_bytes = base64_request_string.encode("utf-8") 
        jpg_file_string = base64.decodestring(base64_bytes) 
        
        nparr = np.fromstring(jpg_file_string, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        return frame