

class Updater(object):

    def __init__(self):
        self.alert_recipients = []
        self.server = None  # e.g. prometheus
        self.database = None  # e.g. ResearchAnalytics
        self.url = None  # e.g. councils.clark.edu
        self.courses = []

    def council_course(self, course_number, default_role_id, default_enrollment_type):
        ...

