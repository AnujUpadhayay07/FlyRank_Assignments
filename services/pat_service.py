class PatientService:

    def __init__(self, repository):

        self.repository = repository

    def get_patients(self):

        return self.repository.get_all()

    def create_patient(self, patient):

        return self.repository.create(patient)
