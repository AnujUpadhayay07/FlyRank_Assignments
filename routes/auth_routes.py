from flask import request, jsonify


def register_auth_routes(app, service):

    @app.route("/register", methods=["POST"])
    def register():

        user = request.get_json()

        response, status = service.register_user(user)

        return jsonify(response), status

    @app.route("/login", methods=["POST"])
    def login():

        credentials = request.get_json()

        response, status = service.login_user(credentials)

        return jsonify(response), status
