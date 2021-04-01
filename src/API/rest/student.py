from flask_restful import Resource 


class Student(Resource):

  def get(self):
    return "Dados dos estudantes retornados"

  def post(self):
    return "Dados do estudante cadastrado"

  '''
  def put(self):
    return "Dados do estudante alterados"

  def delete(self):
    return "Dados do est

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


