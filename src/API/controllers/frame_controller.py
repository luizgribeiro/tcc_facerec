import cv2
from controllers.face_finder_controller import FaceFinder
from controllers.face_detector_controller import FaceDetector

class FrameController:

    def __init__(self, face_detector, face_finder):
        self.face_finder = face_finder 
        self.face_detector = face_detector


    def convert_frame(self, frame):
        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


    def rescale_detected_faces(self, face_locations, face_names, frame):
        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            if name == 'Unknown':
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            else:
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
                name = name.split('-')[1]
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        return frame


    def process_frame(self, frame):
        
        try:
            face_locations, face_encodings = self.face_finder.find_faces(frame)
 
            if face_locations != None:
                detected_faces = [self.face_detector.detect_faces(f_enc) for f_enc in face_encodings]
                processed_frame = self.rescale_detected_faces(face_locations,
                                                              detected_faces,
                                                              frame
                                                            )
                return processed_frame, detected_faces

            else:
                return frame, None
        except Exception as e:
                raise e
      
            
    def gen_jpg_string_from_frame(self, frame):

        if frame is  None:
            return None
        else:
            (flag, encoded_image) = cv2.imencode(".jpg", frame)

            if not flag:
                raise Exception('[ERROR]: frame encoding failure')
        
        return encoded_image.tostring()


    def get_face_encodings(self, frame):
        
        _ , face_encodings = self.face_finder.find_faces(frame)

        if face_encodings is None:
            return None 
        else:
            return face_encodings
