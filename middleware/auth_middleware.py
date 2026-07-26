import os
import jwt

from functools import wraps
from flask import request, jsonify, g


def token_required(auth_service):

    def wrapper(func):

        @wraps(func)
        def verify_token(*args, **kwargs):

            header = request.headers.get("Authorization")

            if header is None:
                return jsonify({"error": "Authorization header missing"}), 401

            parts = header.split()

            if len(parts) != 2 or parts[0] != "Bearer":
                return jsonify({"error": "Invalid Authorization header"}), 401

            token = parts[1]

            try:
                decoded = jwt.decode(
                    token,
                    os.getenv("JWT_SECRET"),
                    algorithms=["HS256"]
                )

                current_user = auth_service.repository.find_by_id(
                    decoded["user_id"]
                )

                if current_user is None:
                    return jsonify({"error": "User not found"}), 401

                g.current_user = current_user

            except jwt.ExpiredSignatureError:
                return jsonify({"error": "Token expired"}), 401

            except jwt.InvalidTokenError:
                return jsonify({"error": "Invalid token"}), 401

            return func(*args, **kwargs)

        return verify_token

    return wrapper
