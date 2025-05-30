"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def handle_hello():
    # This is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {"hello": "world",
                     "family": members}
    return jsonify(response_body), 200

@app.route('/members', methods=['POST'])
def add_new_member():
    data = request.get_json()

    if not data:
        return jsonify({'err': 'No se ha podido añadir' }), 400
    
    jackson_family.add_member(data)
    return jsonify({'msg': 'Familiar añadido'}), 201

@app.route('/members/<int:id>', methods=['GET'])
def get_family_member(id):
    member = jackson_family.get_member(id)

    return jsonify(member)



@app.route('/members/<int:id>', methods=['DELETE'])
def delete_family_member(id):
    member_in_db = jackson_family.get_member(id)

    if not member_in_db:
        return jsonify({'err': 'No se ha podido eliminar al usuario :('}), 404
    
    jackson_family.delete_member(id)
    return jsonify({'msg': 'Miembro eliminado :)'}), 200

    

# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
