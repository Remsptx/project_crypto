from flask import Flask, request, jsonify, make_response
import tink
from flask_cors import CORS
from tink import aead
from tink import tink_config
from tink import secret_key_access
import json
app = Flask(__name__)
CORS(app)


# write key in a file
aead.register()
with open('key.json', 'r') as file:
  keyset = json.load(file)
serialized_keyset = json.dumps(keyset)
keyset_handle = tink.json_proto_keyset_format.parse(serialized_keyset, secret_key_access.TOKEN )
primitive = keyset_handle.primitive(aead.Aead)

@app.route('/')
def home():
    return "hello world"


@app.route('/encrypt', methods=['POST'])
def encrypt():    
    id= request.json.get('id')
    hash = request.json.get('hash')
    if hash:
        # crypt the text using the key
        encrypted_hash = primitive.encrypt(hash.encode(), id.encode())
        cyphertext = encrypted_hash.hex()
        return jsonify({'encrypted_hash': cyphertext}),200
    else:
        return jsonify({'error': 'No data provided'}), 400

@app.route('/decrypt', methods=['POST'])
def decrypt():

    id= request.json.get('id')
    encrypted_hash = request.json.get('encrypted_hash')
    if encrypted_hash:
        
        # decrypt the text using the key
        decrypted_hash = str(primitive.decrypt(bytes.fromhex(encrypted_hash), id.encode()))
        decrypted_hash = decrypted_hash.split("\'")[1]
        return jsonify({'hash': decrypted_hash}),200
    else:
        return jsonify({'error': 'No encrypted data provided'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
