from repositories.repository_interface import PatientRepository

class PostgresRepository(PatientRepository):

    def __init__(self, conn):
        self.conn = conn

    def get_all(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT id, name, age, disease FROM patients")
            rows = cur.fetchall()

        patients = []

        for row in rows:
            patients.append({
                "id": row[0],
                "name": row[1],
                "age": row[2],
                "disease": row[3]
            })

        return patients

    def create(self, patient):
        with self.conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO patients (name, age, disease)
                VALUES (%s, %s, %s)
                RETURNING id;
                """,
                (
                    patient["name"],
                    patient["age"],
                    patient["disease"],
                ),
            )

            patient_id = cur.fetchone()[0]

        self.conn.commit()

        return {
            "id": patient_id,
            **patient
        }