"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")
members = [{
    "first_name": "John",
    "age": 33,
    "lucky_numbers": [7, 13, 22]
}, {
    "first_name": "Jane",
    "age": 35,
    "lucky_numbers": [10, 14, 3]
}, {
    "first_name": "Jimmy",
    "age": 5,
    "lucky_numbers": [1]
}]

for member in members:
    jackson_family.add_member(member)

print(jackson_family)


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():
    try:
        # this is how you can use the Family datastructure by calling its methods
        members = jackson_family.get_all_members()
        response_body = members

        return jsonify(response_body), 200
    except:
        return jsonify({
            "message": "No se pudo obtener la informacion"
        }),500

@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    try:
        member = jackson_family.get_member(member_id)
        if member:
            return jsonify(member),200
        
        return jsonify({
            "message": "No se encontro el usuario"
        }),404

    except Exception as e:
        return jsonify(),500

@app.route('/member', methods=['POST'])
def add_member():
    try:
        body = request.json
        if body.get("id") is None:
            member = {
                "first_name": body["first_name"],
                "age": body["age"],
                "lucky_numbers": body["lucky_numbers"]
            }
        else:
            member = {
                "id": body["id"],
                "first_name": body["first_name"],
                "age": body["age"],
                "lucky_numbers": body["lucky_numbers"]
            }
        
        added = jackson_family.add_member(member)
        if added:
            return jsonify(),200
        return jsonify(), 500
    
    except Exception as e:
        print(e.args[0])
        return jsonify({
            "message": "Ha ocurrido un error"
        }),400

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    success = jackson_family.delete_member(member_id)
    if success:
        return jsonify({
        "done": True
        }),200
    
    return jsonify({
    "done": False
    }),404

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
