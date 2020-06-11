from pymongo.write_concern import WriteConcern
from pymodm import EmbeddedMongoModel, MongoModel, fields
from .students import Student

class Atendence(MongoModel):
    student_id = fields.ReferenceField(Student)
    date = fields.DateTimeField(verbose_name="data da presenca", mongo_name="data_presenca")

    class Meta:
        collection_name = 'atendence'