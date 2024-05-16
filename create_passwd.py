from hashlib import sha3_256

SECRET_KEY = 'BN3298'
ALGORITHM = 'HS256'

passwd = input("Type password: ")
print(sha3_256(bytes(passwd, 'utf-8')).hexdigest())