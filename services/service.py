import os
import bcrypt
import jwt

from datetime import datetime, timedelta


class AuthService:

    def __init__(self, repository):
        self.repository = repository

    def register_user(self, user):

        # Validate input
        if not user.get("username"):
            return {"error": "Username is required"}, 400

        if not user.get("email"):
            return {"error": "Email is required"}, 400

        if not user.get("password"):
            return {"error": "Password is required"}, 400

        # Check if email already exists
        existing_user = self.repository.find_by_email(user["email"])

        if existing_user:
            return {"error": "Email already exists"}, 409

        # Hash password
        hashed_password = bcrypt.hashpw(
            user["password"].encode("utf-8"),
            bcrypt.gensalt()
        )

        new_user = {
            "username": user["username"],
            "email": user["email"],
            "password_hash": hashed_password.decode("utf-8")
        }

        created_user = self.repository.create_user(new_user)

        return {
            "message": "User registered successfully",
            "user": created_user
        }, 201

    def login_user(self, credentials):

        # Validate input
        if not credentials.get("email"):
            return {"error": "Email is required"}, 400

        if not credentials.get("password"):
            return {"error": "Password is required"}, 400

        # Find user
        user = self.repository.find_by_email(credentials["email"])

        if user is None:
            return {"error": "Invalid email or password"}, 401

        # Verify password
        password_correct = bcrypt.checkpw(
            credentials["password"].encode("utf-8"),
            user["password_hash"].encode("utf-8")
        )

        if not password_correct:
            return {"error": "Invalid email or password"}, 401

        # Generate JWT
        payload = {
            "user_id": user["id"],
            "email": user["email"],
            "exp": datetime.utcnow() + timedelta(hours=1)
        }

        token = jwt.encode(
            payload,
            os.getenv("JWT_SECRET"),
            algorithm="HS256"
        )

        return {
            "message": "Login successful",
            "token": token,
            "user": {
                "id": user["id"],
                "username": user["username"],
                "email": user["email"]
            }
        }, 200