import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import numpy as np
import face_recognition
from time import sleep

class App:
    def __init__(self, window, window_title, delay=15, video_source=0):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source
        self.delay = delay

        self.face_finder = FaceFinder()

        #open video source
        self.vid = VideoCapture(video_source)

        ##Button for snapshot
        self.btn_snapshot = tkinter.Button(window, text="Snapshot", width=50, command=self.snapshot)
        self.btn_snapshot.pack(anchor=tkinter.CENTER, expand=True)

        

        #Create a canvas for the video
        self.canvas = tkinter.Canvas(window, width=self.vid.width, height=self.vid.height)
        self.canvas.pack()

        self.update()

        self.window.mainloop()



    def update(self):
        ret, frame = self.vid.get_frame()

        faces_frame = self.face_finder.detect_faces(frame)

        rgb_faces_frame = self.vid.convert_frame(faces_frame)
        
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(rgb_faces_frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor = tkinter.NW )
        self.window.after(self.delay, self.update)
        

    def snapshot(self):
        ret, frame = self.vid.get_frame()

        if ret:
            cv2.imwrite("frame-teste.jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))



class VideoCapture:
    def __init__(self, video_source=0):
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
           raise ValueError("Unable to open video source", video_source)
    #get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

    def get_frame(self):

        ret, frame = self.vid.read()
        if self.vid.isOpened():
            if ret:
                return (ret, frame)
            else:
                return (ret, None)
        else:
            raise "No video Stream available"

        ret, frame = self.vid.read()
       

    def convert_frame(self, frame):
        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


class FaceFinder:
    def __init__(self):
        print('Face finder created!')


        # Load a sample picture and learn how to recognize it.
        obama_image = face_recognition.load_image_file("obama.jpg")
        obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

        # Load a second sample picture and learn how to recognize it.
        biden_image = face_recognition.load_image_file("biden.jpg")
        biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

        # Create arrays of known face encodings and their names
        self.known_face_encodings = [
            obama_face_encoding,
            biden_face_encoding
        ]
        self.known_face_names = [
            "Barack Obama",
            "Joe Biden"
        ]

    def detect_faces(self, cv_frame):

        face_locations = []
        face_encodings = []
        face_names = []


        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(cv_frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if True:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)


            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                name = "Unknown"

                # # If a match was found in known_face_encodings, just use the first one.
                # if True in matches:
                #     first_match_index = matches.index(True)
                #     name = known_face_names[first_match_index]

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = self.known_face_names[best_match_index]

                face_names.append(name)

        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(cv_frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(cv_frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(cv_frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)


        return cv_frame


App(tkinter.Tk(), "Tkinter and OpenCV")