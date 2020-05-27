import face_recognition as face_rec 
import numpy as np

class FaceDetector:

    def __init__(self, db_connection=None):

        #TODO: Load from database known faces

        self.known_face_encodings = []
        self.known_face_names = []


    def load_known_faces(self):
        #TODO: load from database known faces (names and )
        pass


    def detect_faces(self, face_encoding):

        name = "Unkown"

        matches = face_rec.compare_faces(self.known_face_encodings, face_encoding)

        face_distances = face_rec.face_distance(self.known_face_encodings, face_encoding)
        if len(face_distances) != 0:
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = self.known_face_names[best_match_index]

        return name
