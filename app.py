from flask import Flask, request, jsonify
from flask import Flask, request, render_template,jsonify
from flask_cors import CORS
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

app = Flask(__name__)

ENCRYPT_URL = 'http://localhost:5000/encrypt'
DECRYPT_URL = 'http://localhost:5000/decrypt'
dbFile = 'credentials.json'
database = []

hasher = argon2.PasswordHasher(hash_len=256)

def load_json_file(jsonfile):
    with open(jsonfile, 'r') as file:
        data = json.load(file)
    for entry in data:
        user = {'id': entry['id'], 'pwd': entry['pwd']}
        database.append(user)
    return database
def (update_jsonfile):


@app.route('/register', methods=['POST'])
def register():
    # Get informations and load the dbfile in database
    data = request.json
    id = request.json['id']
    pwd= request.json['pwd']
    load_json_file(dbfile)

    if id in [x[0] for x in database]:
        return jsonify({'message': 'User already exists'}), 200
    # Hash password
    hash_pwd = hasher.hash(pwd)
    # Encrypt password
    return jsonify({'message': 'User registered successfully'}), 201

    # Store in json file

    return jsonify({'message': 'User registered successfully'}), 201
@app.route('/login', methods=['POST'])
def login():
    # Get informations and load the dbfile in database
    data = request.json
    id= request.json['id']
    pwd= request.json['pwd']
    load_json_file(dbfile)

    # Check is the user is registered
    if id not in [x[0] for x in database]:
        return jsonify({'message': 'User not found'}), 200

    encrypted_hash = (x[1] for x in database if x[0] == id)
    if encrypted_hash is None:
        return jsonify({'message' : 'Error during password recovery' }), 200

    body = {
        'id': id,
        'encrypted_hash': encrypted_hash
        }
    response = requests.post(DECRYPT_URL, json=body)
    hashToVerify = response.json().get('hash')
    # Verify password
    if password == decrypted_password:
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port = 5000)
