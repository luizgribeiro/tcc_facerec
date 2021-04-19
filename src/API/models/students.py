from pymongo.write_concern import WriteConcern
from pymodm import MongoModel, fields

class Student(MongoModel):
    student_id = fields.IntegerField(primary_key=True, verbose_name="matricula", mongo_name="_id")
    email = fields.EmailField(verbose_name="email", mongo_name="email")
    full_name = fields.CharField(verbose_name="nome completo", mongo_name="nome")
    face_encodings = fields.ListField(verbose_name="face encodings", mongo_name="face_encodings")

    class Meta:
        collection_name = 'student'