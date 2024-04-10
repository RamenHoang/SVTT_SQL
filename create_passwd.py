from hashlib import sha3_256
from .app.config import secret_key, algorithm

SECRET_KEY = secret_key
ALGORITHM = algorithm

passwd = input("Type password: ")
print(sha3_256(bytes(passwd, 'utf-8')).hexdigest())