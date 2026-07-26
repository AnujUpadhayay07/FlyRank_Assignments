from psycopg import Connection


class UserRepository:

    def __init__(self, conn: Connection):
        self.conn = conn

    def create_user(self, user):

        with self.conn.cursor() as cur:

            cur.execute(
                """
                INSERT INTO users (username, email, password_hash)
                VALUES (%s, %s, %s)
                RETURNING id;
                """,
                (
                    user["username"],
                    user["email"],
                    user["password_hash"]
                )
            )

            user_id = cur.fetchone()[0]

        self.conn.commit()

        return {
            "id": user_id,
            "username": user["username"],
            "email": user["email"]
        }

    def find_by_email(self, email):

        with self.conn.cursor() as cur:

            cur.execute(
                """
                SELECT id, username, email, password_hash
                FROM users
                WHERE email = %s;
                """,
                (email,)
            )

            row = cur.fetchone()

        if row is None:
            return None

        return {
            "id": row[0],
            "username": row[1],
            "email": row[2],
            "password_hash": row[3]
        }

    def find_by_id(self, user_id):

        with self.conn.cursor() as cur:

            cur.execute(
                """
                SELECT id, username, email
                FROM users
                WHERE id = %s;
                """,
                (user_id,)
            )

            row = cur.fetchone()

        if row is None:
            return None

        return {
            "id": row[0],
            "username": row[1],
            "email": row[2]
        }
