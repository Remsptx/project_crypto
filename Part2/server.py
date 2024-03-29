from flask import Flask, request
from cryptography.hazmat.primitives.asymmetric import dh
import csv

app = Flask(__name__)

# Generate server's private key using a 2048-bit group from RFC 3526
parameters = dh.generate_parameters(generator=2, key_size=2048)
server_private_key = parameters.generate_private_key()
s = server_private_key.private_numbers().x
q = parameters.parameter_numbers().p

def write_to_server_file(username, salt):
    """Write username and salt to server.csv."""
    with open("server.csv", "a", newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username, salt])

@app.route('/oprf', methods=['POST'])
def oprf():
    """Receive C from client, compute R = C^s, and return R."""
    data = request.json
    username = data['username']
    C = int(data['C'])
    
    R = pow(C, s, 2*q + 1)  # Compute R = C^s mod 2q+1
    
    # Write the username and server's secret exponent (acting as salt) to file
    write_to_server_file(username, s)
    return {"R": R}, 200

if __name__ == '__main__':
    app.run(debug=True)
