import hashlib
import os
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes
from django.conf import settings

def md5_encrypt(password):
    md5 = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    md5.update(password.encode('utf-8'))
    return md5.hexdigest()

def generate_rsa_keypair():
    if os.path.exists('private_key.pem') and os.path.exists('public_key.pem'):
        print("密钥对已存在，无需重新生成。")
        return

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()

    with open('private_key.pem', 'wb') as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))

    with open('public_key.pem', 'wb') as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ))

    print("已生成并保存新的密钥对。")
    return private_key, public_key

def rsa_encrypt(public_key, password):
    encrypted = public_key.encrypt(
        password.encode('utf-8'),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted

def rsa_decrypt(private_key, encrypted_password):
    decrypted = private_key.decrypt(
        encrypted_password,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted.decode('utf-8')

def rsa_encrypt_password(password):
    with open('public_key.pem', 'rb') as f:
        public_key = serialization.load_pem_public_key(
            f.read(),
            backend=default_backend()
        )
    encrypted_password = rsa_encrypt(public_key, password)
    return encrypted_password

def rsa_decrypt_password(encrypted_password):
    if isinstance(encrypted_password, str):
        encrypted_password = base64.b64decode(encrypted_password.encode('utf-8'))

    with open('private_key.pem', 'rb') as f:
        private_key = serialization.load_pem_private_key(
            f.read(),
            password=None,
            backend=default_backend()
        )
    decrypted_password = rsa_decrypt(private_key, encrypted_password)
    return decrypted_password

# 在启动时检查并生成密钥对
generate_rsa_keypair()

def encrypt_password(password):
    md5_password = md5_encrypt(password)
    encrypted_password = rsa_encrypt_password(md5_password)
    return base64.b64encode(encrypted_password).decode('utf-8')


def verify_encrypted_password(base64_encoded_password, base64_encoded_stored_password):
    # 解码 Base64 编码
    encrypted_password = base64.b64decode(base64_encoded_password)
    encrypted_stored_password = base64.b64decode(base64_encoded_stored_password)

    # 使用私钥解密
    with open('private_key.pem', 'rb') as f:
        private_key = serialization.load_pem_private_key(
            f.read(),
            password=None,
            backend=default_backend()
        )

    # 解密密码
    decrypted_password = rsa_decrypt(private_key, encrypted_password)
    decrypted_stored_password = rsa_decrypt(private_key, encrypted_stored_password)

    # 比较哈希值
    return decrypted_password == decrypted_stored_password
