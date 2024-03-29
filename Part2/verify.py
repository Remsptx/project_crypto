import csv
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import dh

# Initialize DH parameters for the 2048-bit group from RFC 3526
parameters = dh.generate_parameters(generator=2, key_size=2048, backend=default_backend())
q = parameters.parameter_numbers().p

def hash_to_group(password):
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(password.encode())
    hashed = int.from_bytes(digest.finalize(), byteorder='big')
    # Adjust hashing to group range [2, q] and compute H(P)
    s = 2 + hashed % (q - 2)
    return pow(s, 2, 2*q + 1)

def read_csv_to_dict(filename):
    with open(filename, mode='r') as infile:
        reader = csv.reader(infile)
        return {rows[0]: rows[1:] for rows in reader}

def verify():
    server_data = read_csv_to_dict("server.csv")
    client_data = read_csv_to_dict("client.csv")
    
    for username, client_info in client_data.items():
        password, K_client = client_info
        K_client = int(K_client)  # Convert K from string to int
        
        if username in server_data:
            salt = int(server_data[username][0])
            H_P = hash_to_group(password)
            expected_K = pow(H_P, salt, 2*q + 1)
            
            if expected_K == K_client:
                print(f"Verification for {username}: PASSED")
            else:
                print(f"Verification for {username}: FAILED - Expected K '{expected_K}', got '{K_client}'")
        else:
            print(f"Username {username} not found in server data.")

if __name__ == '__main__':
    verify()
