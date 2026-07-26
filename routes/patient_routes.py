from flask import request, jsonify

def register_routes(app, service):

    @app.route("/patients", methods=["GET"])
    def get_patients():
        return jsonify(service.get_patients())

    @app.route("/patients", methods=["POST"])
    def create_patient():
        patient = request.get_json()
        result = service.create_patient(patient)
        return jsonify(result), 201