
class StudentsController:

    def __init__(self, db_students):
        self.db_students = db_students 


    def fetch_students_info(self):
        return self.db_students.objects.all()

    def get_student_ids(self):
        return [ stu.student_id for stu in self.fetch_students_info() ]

    def get_student_names(self):
        return [ stu.full_name for stu in self.fetch_students_info() ]
    
    def get_student_emails(self):
        return [ stu.email for stu in self.fetch_students_info() ]

    def get_student_facedesc(self):
        return [ stu.face_encodings for stu in self.fetch_students_info() ]

    def add_student(self, student_data, face_descriptors):
        self.db_students(student_data['matricula'],
                         student_data['email'],
                         student_data['nome'],
                         [desc for desc in face_descriptors[0]]
                        ).save()

