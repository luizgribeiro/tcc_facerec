import face_recognition as face_rec 
import numpy as np
from datetime import datetime

class FaceDetector:

    def __init__(self, face_list_cont, attend_cont):
        self.students_descs = {}
        self.face_list_cont = face_list_cont
        self.attend_cont = attend_cont
        

    def update_known_faces(self, db_student_data):

        first_name = [ name.split()[0] for name in db_student_data.get_student_names() ]
        students_ids = [ identification for identification in db_student_data.get_student_ids()]
        face_descs = [ np.array(desc) for desc in db_student_data.get_student_facedesc() ]


        if len(first_name) == len(students_ids) and len(first_name) == len(face_descs):
            list_id = [
                        f'{students_ids[i]} - {first_name[i]}' 
                        for i in range(len(first_name))
                      ]
        else:
            raise "Inconsistence in student names and ids"
        

        for i in range(len(first_name)):
            self.students_descs[list_id[i]] = face_descs[i]

    def detect_faces(self, face_encoding):

        name = "Unkown"

        all_face_encodings = [ enc for enc in self.students_descs.values()]
        all_student_ids = [ident for ident in self.students_descs.keys()]
        matches = face_rec.compare_faces(all_face_encodings, face_encoding)

        
        face_distances = face_rec.face_distance(all_face_encodings, face_encoding)
        if len(face_distances) != 0:
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = all_student_ids[best_match_index]

        #updating detections locally and on db
        if name != "Unkown":
            
            if name not in self.face_list_cont.get_detected_faces():
            
                matricula = name.split()[0]
                self.attend_cont.add_attendance({ 'matricula': matricula,
                                                  'data_hora': datetime.now()
                                                })
            self.face_list_cont.add_face(name)
        
        return name
