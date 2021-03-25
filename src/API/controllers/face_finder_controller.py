import face_recognition as face_rec 
import cv2

class FaceFinder:

    def __init__(self):
        
        pass 


    def find_faces(self, cv_frame):
        
        face_locations = []
        face_encodings = []

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(cv_frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        face_locations = face_rec.face_locations(rgb_small_frame)
        face_encodings = face_rec.face_encodings(rgb_small_frame, face_locations)

        if len(face_locations) != 0:
            return (face_locations, face_encodings)
        else:
            return (None, None)
