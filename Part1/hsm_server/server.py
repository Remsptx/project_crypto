from flask import Flask, request, jsonify, make_response
import tink
from flask_cors import CORS
from tink import aead
from tink import tink_config
from tink.proto import tink_pb2
import json
app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Home</title>
    </head>
    <body>
        <h1>It works</h1>
    </body>
    </html>
    """
    return make_response(html_content)

    
@app.route('/encrypt', methods=['POST'])
def encrypt():

# Récupérer l'identifiant de la personne qui veut se connecter
    id = request.json.get('id')
    # Enregistrer les configurations de Tink
    tink_config.register()

    # Enregistrer les plugins pour les opérations de chiffrement/déchiffrement AEAD
    aead.register()

    # Générer une nouvelle clé avec le modèle AES256_GCM
    key_template = tink_pb2.AesGcmKeyTemplates.AES256_GCM
    keyset_handle = tink.KeysetHandle.generate_new(key_template)

    # Écrire la clé dans un fichier
    with open("keyset.json", "w") as keyset_file:
        key_dict_json = {id: tink.CleartextKeysetHandle.serialize(keyset_handle)}
        json.dump(key_dict_json, keyset_file)
   
    hash = request.json.get('hash')
    if hash:
        # Obtenir l'primitive Aead à partir de la clé
        aead_primitive = aead.KeysetHandle.get_primitive(keyset_handle)
        # Chiffrer le texte en clair
        encrypted_hash = aead_primitive.encrypt(hash.encode(), id.encode())

        return jsonify({'encrypted_hash': encrypted_hash.decode()})
    else:
        return jsonify({'error': 'No data provided'}), 400

@app.route('/decrypt', methods=['POST'])
def decrypt():

    # Lire les clés depuis le fichier JSON
    with open("keyset.json", "r") as keyset_file:
        key_dict_json = json.load(keyset_file)

    key_id = request.json.get('id')
    

    encrypted_hash = request.json.get('encrypted_hash')
    if encrypted_hash:
        if key_id in key_dict_json: 
        # on récupère la  clé correspondant à l'identifiant
            serialized_keyset_handle = key_dict_json[key_id]
            keyset_handle = tink.CleartextKeysetHandle.deserialize(serialized_keyset_handle)
        # Obtenir l'primitive Aead à partir de la clé
            aead_primitive = aead.KeysetHandle.get_primitive(keyset_handle)
         # Déchiffrer le texte chiffré
            decrypted_hash = aead_primitive.decrypt(encrypted_hash, key_id.encode()).decode()
            return jsonify({'hash': decrypted_hash})
        else:
            return jsonify({'error': 'Key not found'}), 404
    else:
        return jsonify({'error': 'No encrypted data provided'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
