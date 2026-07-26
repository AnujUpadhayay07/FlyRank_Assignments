from repositories.repository_interface import PatientRepository

class MemoryRepository(PatientRepository):

    def __init__(self):
        self.patients = []
        self.next_id = 1

    def get_all(self):
        return self.patients

    def create(self, patient):
        patient = patient.copy()  # Avoid modifying the original dictionary
        patient["id"] = self.next_id
        self.next_id += 1

        self.patients.append(patient)
        return patient
