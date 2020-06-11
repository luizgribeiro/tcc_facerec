import cv2
from controllers.face_finder_controller import FaceFinder
from controllers.face_detector_controller import FaceDetector
import logging

class WebcamController:

    def __init__(self, video_source=0, face_detector=FaceDetector(), face_finder=FaceFinder()):

        self.vid = cv2.VideoCapture(video_source)

        if self.vid.isOpened():
            self._width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
            self._height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
        else:
            logging.error("Unable to open video source")
            raise ValueError("Unable to open video source", video_source)
    
        self.face_finder = face_finder 
        self.face_detector = face_detector

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
 
            if ret:
                #detecting faces
                if face_locations != None:
                    detected_faces = []
                    for encoding in face_encodings:
                        detected_faces.append(self.face_detector.detect_faces(encoding))
                        
                    detected_frame = self.rescale_detected_faces(face_locations, 
                                                                detected_faces,
                                                                frame)
                    return (ret, detected_frame)
                else:
                    return (ret, frame)
            else:
                return (ret, None)
        except Exception as e:
                raise e
            
    def gen_jpg_from_frame(self, lock):

        while True:
            lock.acquire()

            ret, frame = self.get_processed_frame()

            lock.release()

            if frame is  None:
                return (ret, None)
            else:
                (flag, encodedImage) = cv2.imencode(".jpg", frame)

                if not flag:
                    return (ret, None)
                
  
            yield b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n'
     


    def get_face_encodings(self, lock):
        lock.acquire()

        ret, frame = self.vid.read()

        lock.release()

        if ret is None:
            return None 
        else:
            face_locations, face_encodings = self.face_finder.find_faces(frame)

        if face_encodings is None:
            return None 
        else:
            return face_encodings
