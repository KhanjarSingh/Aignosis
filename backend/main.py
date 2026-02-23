from fastapi import FastAPI,HTTPException
from fastapi.responses import StreamingResponse
import os
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

app = FastAPI()

STORAGE_DIR = "storage"
PRIVATE_KEY_PATH = os.path.join(STORAGE_DIR, "private_key_test.pem")

# PRIVATE_KEY_PATH = "private_key_test.pem"

@app.get("/")
def check():
    return ("Server is Running perfectly")



def load_private_key():
    with open(PRIVATE_KEY_PATH, "rb") as f:
        pem = f.read()
    return serialization.load_pem_private_key(pem, password=None)


def decrypt_rsa_password(key_path: str):
    priv = load_private_key()
    with open(key_path, "rb") as f:
        enc = f.read()
        password = priv.decrypt(
            enc,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
        print(f"[+] RSA-decrypted password length: {len(password)} bytes")
        return password


def decrypt_video(password: bytes,video_path: str):
    with open(video_path, "rb") as f:
        full = f.read()

    salt = full[:16]
    nonce = full[16:28]
    ciphertext = full[28:]
    print("[+] Salt:", len(salt))
    print("[+] Nonce:", len(nonce))
    print("[+] Ciphertext:", len(ciphertext))

    # Derive AES-256 key from password
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )

    aes_key = kdf.derive(password)
    print(f"[+] Derived AES key length: {len(aes_key)} bytes")

    aesgcm = AESGCM(aes_key)
    try:
        decrypted = aesgcm.decrypt(nonce, ciphertext, None)
        return decrypted
    except Exception as e:
        print("[-] AES decryption failed:", e)
        return
    

def video_stream_generator(data: bytes, chunk_size: int = 1024 * 1024):
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]


@app.get("/video/stream")
def stream_video(uid: str, tid: str):
    ENCRYPTED_VIDEO_PATH = os.path.join(STORAGE_DIR,f"{uid}_{tid}_encrypted.bin")
    ENCRYPTED_AES_KEY_BIN = os.path.join(STORAGE_DIR,f"{uid}_{tid}_encrypted_key.bin")
    if not os.path.exists(ENCRYPTED_VIDEO_PATH) or not os.path.exists(ENCRYPTED_AES_KEY_BIN):
        raise HTTPException(status_code=404, detail="Encrypted files not found")
    
    password = decrypt_rsa_password(ENCRYPTED_AES_KEY_BIN)
    decrypted_video = decrypt_video(password,ENCRYPTED_VIDEO_PATH)

    return StreamingResponse(
        video_stream_generator(decrypted_video),
        # [decrypted_video],
        media_type="video/mp4"
    )
