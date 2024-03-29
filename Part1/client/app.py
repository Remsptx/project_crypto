from flask import Flask, request, jsonify
from flask import Flask, request, render_template,jsonify
from flask_cors import CORS
from argon2 import PasswordHasher
import json
import csv
import requests
app = Flask(__name__)
CORS(app)

ENCRYPT_URL = 'http://localhost:5000/encrypt'
DECRYPT_URL = 'http://localhost:5000/decrypt'
dbFile = 'credentials.json'
database = []

hasher = PasswordHasher(hash_len=256)

def load_json_file(jsonfile):
    with open(jsonfile, 'r') as file:
        data = json.load(file)
    for entry in data:
        user = {'id': entry['id'], 'pwd': entry['pwd']}
        database.append(user)
    return database
def update_json_file(bodyJson):
    id = bodyJson.get('id')
    pwd = bodyJson.get('pwd')

    with open(dbFile, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([id, pwd])

@app.route('/registerPage')
def registerPage():
    return render_template('register.html')

@app.route('/loginPage')
def loginPage():
    return render_template('login.html')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['POST'])
def register():
    # Get informations and load the dbfile in database
    data = request.json
    id = request.json['id']
    pwd= request.json['pwd']
    load_json_file(dbFile)

    if id in [x[0] for x in database]:
        return jsonify({'message': 'User already exists'}), 401
    # Hash password
    hash = hasher.hash(pwd)
    # Encrypt password
    body = {
        'id': id,
        'hash': hash
        }
    response = requests.post(ENCRYPT_URL, json=body)
    encrypted_hash = response.json().get('encrypted_hash')
    #Store encrypted password in the csv using a json file
    bodyJson = {
        'id': id,
        'pwd': encrypted_hash
        }
    update_json_file(bodyJson)

    return jsonify({'message': 'User registered successfully'}), 201
@app.route('/login', methods=['POST'])
def login():
    # Get informations and load the dbfile in database
    data = request.json
    id= request.json['id']
    pwd= request.json['pwd']
    load_json_file(dbFile)

    # Check if the user is registered
    if id not in [x[0] for x in database]:
        return jsonify({'message': 'User not found'}), 401

    encrypted_hash = (x[1] for x in database if x[0] == id)
    if encrypted_hash is None:
        return jsonify({'message' : 'Error during password recovery' }), 401
    
    body = {
        'id': id,
        'encrypted_hash': encrypted_hash
        }
    response = requests.post(DECRYPT_URL, json=body)
    decrypted_hash = response.json().get('hash')
    # Verify password (pwd is the password in plain that the user entered, decrypted_hash is the hash of the real password stored in the database)
    if hasher.verify(pwd, decrypted_hash):
        return jsonify({'message': 'Login successful !'}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port = 3000)
