import cv2
from controllers.face_finder_controller import FaceFinder
from controllers.face_detector_controller import FaceDetector
import logging

class WebcamController:

    def __init__(self, video_source=0):

        self.vid = cv2.VideoCapture(video_source)

        if self.vid.isOpened():
            self._width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
            self._height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
        else:
            logging.error("Unable to open video source")
            raise ValueError("Unable to open video source", video_source)
    
        self.face_finder = FaceFinder()
        self.face_detector = FaceDetector()

    def get_width(self):
        return self._width
    
    def get_height(self):
        return self._height


    def convert_frame(self, frame):
        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


    #TODO: Separate and draw squares
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
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)


        return frame
    
    def get_processed_frame(self):
        
        try:
            ret, frame = self.vid.read()
            face_locations, face_encodings = self.face_finder.find_faces(frame)
            print(type(face_locations))
            if ret:
                #detecting faces
                if face_locations != None:
                    detected_faces = []
                    for encoding in face_encodings:
                        detected_faces.append(self.face_detector.detect_faces(encoding))
                        
                    detected_frame = self.rescale_detected_faces(face_locations, 
                                                                detected_faces,
                                                                frame)
                    return (ret, self.convert_frame(detected_frame))
                else:
                    return (ret, self.convert_frame(frame))
            else:
                return (ret, None)
        except Exception as e:
                raise e
            
            
