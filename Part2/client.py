import requests
import csv
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.backends import default_backend

SERVER_URL = 'http://localhost:5000/oprf'

# Initialize DH parameters for the 2048-bit group
parameters = dh.generate_parameters(generator=2, key_size=2048, backend=default_backend())
q = parameters.parameter_numbers().p

def hash_to_group(password):
    """Hashes password to an integer in the group range, and compute H(P)."""
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(password.encode())
    hashed = int.from_bytes(digest.finalize(), byteorder='big')
    # Adjust hashing to group range [2, q] and compute H(P)
    s = 2 + hashed % (q - 2)
    return pow(s, 2, 2*q + 1)

def write_to_client_file(username, password, K):
    """Writes username, password, and OPRF key K to client.csv."""
    with open("client.csv", "a", newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username, password, K])

def oprf_client(username, password):
    """Performs OPRF operation with the server and logs details."""
    client_private_key = parameters.generate_private_key()
    r = client_private_key.private_numbers().x
    H_P = hash_to_group(password)
    C = pow(H_P, r, 2*q + 1)  # Compute C = H(P)^r mod 2q+1

    # Sending request to the server
    response = requests.post(SERVER_URL, json={"username": username, "C": C})
    if response.status_code == 200:
        R = response.json()['R']
        # Compute z = r^-1 in group and K = R^z
        z = pow(r, -1, q)
        K = pow(int(R), z, 2*q + 1)  # Ensure R is an integer
        
        # Writing results to client.csv
        write_to_client_file(username, password, K)
        print(f"Computed OPRF Key K for {username}: {K}")
    else:
        print(f"Error from server: {response.status_code}")

if __name__ == "__main__":
    # Example usage
    username = "user1"
    password = "password123"
    oprf_client(username, password)
