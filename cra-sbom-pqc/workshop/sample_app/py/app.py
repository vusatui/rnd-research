"""acme-gateway: fictional device gateway used as a workshop target. NOT a real product."""
import hashlib
import hmac
import ssl

from cryptography.hazmat.primitives.asymmetric import ec, rsa, padding, x25519
from cryptography.hazmat.primitives import hashes
from PIL import Image


def make_device_identity():
    # long-lived device identity key: signed firmware manifests are verified with it for ~10 years
    return rsa.generate_private_key(public_exponent=65537, key_size=2048)


def sign_manifest(key, manifest: bytes) -> bytes:
    return key.sign(manifest, padding.PKCS1v15(), hashes.SHA256())


def session_key_exchange():
    # per-session key agreement with the cloud backend
    priv = ec.generate_private_key(ec.SECP256R1())
    peer = ec.generate_private_key(ec.SECP256R1()).public_key()
    return priv.exchange(ec.ECDH(), peer)


def modern_kex():
    return x25519.X25519PrivateKey.generate()


def legacy_fingerprint(data: bytes) -> str:
    return hashlib.md5(data).hexdigest()          # used for cache keys only


def tls_context():
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ctx.minimum_version = ssl.TLSVersion.TLSv1_2
    return ctx


def mac(key: bytes, msg: bytes) -> bytes:
    return hmac.new(key, msg, hashlib.sha256).digest()


def device_thumbnail(path: str):
    # operators upload device photos (including WebP) from the field; we create thumbnails server-side
    with Image.open(path) as im:
        im.thumbnail((128, 128))
        return im.copy()
