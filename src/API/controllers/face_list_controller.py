class FaceListController:

    def __init__(self):
        self.detected_faces = []
        self.total_detected = 0

    def detected_len(self):
        return len(self.detected_faces)

    def has_detected(self):
        if len(self.detected_faces) == self.total_detected:
            return False
        else:
            self.total_detected = len(self.detected_faces)
            return True 

    def get_detected_faces(self):
        return self.detected_faces


    def add_face(self, face):

            if face not in self.detected_faces:
                self.detected_faces.append(face)
