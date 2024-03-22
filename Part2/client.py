from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import dh
from gmpy2 import mpz, c_div
import os

parameters = dh.generate_parameters(generator=2, key_size=2048)
numbers = parameters.parameter_numbers()

p = mpz(numbers.p)
q = c_div(p - 1, 2)

def string_to_int(pwd):
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(pwd.encode())
    hashed_bytes = digest.finalize()

    hashed_int = int.from_bytes(hashed_bytes, byteorder='big')

    s = 2+(hashed_int % (q-2))
    return s