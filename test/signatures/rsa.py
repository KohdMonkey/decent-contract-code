from cryptography.hazmat.backends import default_backend  
from cryptography.hazmat.primitives import serialization  
from cryptography.hazmat.primitives.asymmetric import rsa 
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from pyrfc3339 import generate
from web3 import Web3

KEYSIZEBITS = 2048

# KEYSIZEBYTES = 128 # 1024 bits
KEYSIZEBYTES = 256 # 2048 bits


#source: https://gist.github.com/ostinelli/aeebf4643b7a531c248a353cee8b9461
def save_file(filename, content):  
    # save file helper
    f = open(filename, "wb")  
    f.write(content) 
    f.close()  


def generate_keys():      
    
    # generate private key & write to disk  
    private_key = rsa.generate_private_key(  
        public_exponent=65537,  
        key_size=KEYSIZEBITS,  
        backend=default_backend()  
    )  
    pem = private_key.private_bytes(  
        encoding=serialization.Encoding.PEM,  
        format=serialization.PrivateFormat.PKCS8,  
        encryption_algorithm=serialization.NoEncryption()  
    )  
    save_file("private.pem", pem)  
    
    # generate public key  
    public_key = private_key.public_key()  
    pem = public_key.public_bytes(  
        encoding=serialization.Encoding.PEM,  
        format=serialization.PublicFormat.SubjectPublicKeyInfo  
    )  
    save_file("public.pem", pem)  


def load_privatekey():
    with open("private.pem", "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
        )
        return private_key
    return None


def load_publickey():
    with open("public.pem", "rb") as key_file:
        publickey = serialization.load_pem_public_key(
            key_file.read()
        )
        return publickey


def sign_message(private_key: rsa.RSAPrivateKey, message: bytes):
    signature = private_key.sign(
        message,
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    return signature


def test_sign():
    publickey = load_publickey()

    pubNum = publickey.public_numbers()
    exponent = pubNum.e
    modulus = pubNum.n
    print('exponent:', Web3.toHex((exponent).to_bytes(KEYSIZEBYTES, byteorder='big')))
    print('modulus:', Web3.toHex((modulus).to_bytes(KEYSIZEBYTES, byteorder='big')))
    print()

    message = b'hello world'
    print('message:', Web3.toHex(message))  
    print()

    privatekey = load_privatekey()
    signature = sign_message(privatekey, message)
    print('signature: ', Web3.toHex(signature))

# generate_keys()
test_sign()
