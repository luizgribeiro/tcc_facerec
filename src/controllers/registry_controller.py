class RegistryController:

    def __init__(self, student_controller):
        #dependency injection: needs student from DB to add registry
        self.student_controller = student_controller


    def add_registry(self, student_data, face_descriptors):

        
        if self.validate_info(student_data):
            self.student_controller.add_student(student_data, face_descriptors)
            return True
        else:
            return False

  
    def validate_info(self, student_data):

        for info in student_data.values():
            if info == None or info == "":
                return "invalid data"
        
        student_ids = self.student_controller.get_student_ids() 
        student_emails = self.student_controller.get_student_emails()

        if (student_data['matricula'] in student_ids 
            or student_data['email'] in student_emails):
            return False
        else:
            return True

