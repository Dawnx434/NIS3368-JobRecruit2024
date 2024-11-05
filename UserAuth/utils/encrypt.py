import hashlib
import os
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from django.conf import settings
from django.core.exceptions import ValidationError

# # 使用 SHA256 哈希算法进行加密
# def sha256_encrypt(password):
#     sha256 = hashlib.sha256(settings.SECRET_KEY.encode('utf-8'))
#     sha256.update(password.encode('utf-8'))
#     return sha256.hexdigest()

# # 生成 RSA 密钥对
# def generate_rsa_keypair():
#     if os.path.exists('private_key.pem') and os.path.exists('public_key.pem'):
#         print("密钥对已存在，无需重新生成。")
#         return
#
#     private_key = rsa.generate_private_key(
#         public_exponent=65537,
#         key_size=2048,
#         backend=default_backend()
#     )
#     public_key = private_key.public_key()
#
#     with open('private_key.pem', 'wb') as f:
#         f.write(private_key.private_bytes(
#             encoding=serialization.Encoding.PEM,
#             format=serialization.PrivateFormat.TraditionalOpenSSL,
#             encryption_algorithm=serialization.NoEncryption()
#         ))
#
#     with open('public_key.pem', 'wb') as f:
#         f.write(public_key.public_bytes(
#             encoding=serialization.Encoding.PEM,
#             format=serialization.PublicFormat.SubjectPublicKeyInfo,
#         ))
#
#     print("已生成并保存新的密钥对。")
#     return private_key, public_key

# # 使用公钥加密密码
# def rsa_encrypt(public_key, password):
#     encrypted = public_key.encrypt(
#         password.encode('utf-8'),
#         padding.OAEP(
#             mgf=padding.MGF1(algorithm=hashes.SHA256()),
#             algorithm=hashes.SHA256(),
#             label=None
#         )
#     )
#     return encrypted

# 使用私钥解密密码
def rsa_decrypt(private_key, encrypted_stored_password):
    try:
        decrypted = private_key.decrypt(
            encrypted_stored_password,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return decrypted
    except ValueError as e:
        print("Decryption failed:", e)
        print("Private Key:", private_key)
        print("Encrypted Stored Password:", encrypted_stored_password)
        print("Encrypted Stored Password (Base64):", base64.b64encode(encrypted_stored_password).decode())
        raise ValidationError("解密失败，请联系管理员")


# # 加载公钥并加密密码
# def rsa_encrypt_password(password):
#     with open('public_key.pem', 'rb') as f:
#         public_key = serialization.load_pem_public_key(
#             f.read(),
#             backend=default_backend()
#         )
#     encrypted_password = rsa_encrypt(public_key, password)
#     return encrypted_password

# 加载私钥并解密密码
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
# generate_rsa_keypair()

# # 使用 SHA256 加密并生成密文
# def encrypt_password(password):
#     sha256_password = sha256_encrypt(password)
#     encrypted_password = rsa_encrypt_password(sha256_password)
#     return base64.b64encode(encrypted_password).decode('utf-8')

# 验证加密的密码
def verify_encrypted_password(base64_encoded_password, base64_encoded_stored_password):
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
