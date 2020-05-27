from pymongo.write_concern import WriteConcern
from pymodm import EmbeddedMongoModel, MongoModel, fields

class Atendence(MongoModel):
    student_id = fields.ReferenceField(Student)
    date = fields.DateTimeField(verbose_name="data da presenca", mongo_name="data_presenca")
