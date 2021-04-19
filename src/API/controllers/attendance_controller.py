from models.attendance import Attendance

class AttendanceController:

    def __init__(self):
        self.db_attendances = Attendance


    def fetch_attendances(self):
        return self.db_attendances.objects.all()

    def add_attendance(self, attend_data):
        self.db_attendances(attend_data['matricula'],
                            attend_data['data_hora']
                            ).save()