from cryptography.hazmat.primitives.asymmetric import ec, rsa
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    NoEncryption,
    PrivateFormat,
    PublicFormat,
)

from jwt import PyJWT

from jwts import (
    JWTEncodeClaims,
    JWTEncoder,
    PemAlgorithms,
    PemIdentity,
    PlainAlgorithms,
    PlainIdentity,
)


def test_all_plain_algorithms(test_data: dict[str, str | bool]) -> None:
    for algorithm in PlainAlgorithms:
        try:
            JWTEncoder(
                PlainIdentity(
                    secret_key_loader=lambda: "some key", algorithm=algorithm
                ),
                py_jwt=PyJWT(),  # type: ignore
                claims=JWTEncodeClaims(),
            ).encode(test_data)
        except Exception as e:
            raise Exception(f"{algorithm} not valid. Error: {e}") from e


def test_RS_and_PS_identities(test_data: dict[str, str | bool]) -> None:
    rsa_private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    rsa_public_key: rsa.RSAPublicKey = rsa_private_key.public_key()

    private_key: bytes = rsa_private_key.private_bytes(
        Encoding.PEM, PrivateFormat.PKCS8, NoEncryption()
    )
    public_key: bytes = rsa_public_key.public_bytes(
        Encoding.PEM, PublicFormat.SubjectPublicKeyInfo
    )
    for algorithm in filter(
        lambda alg: "RS" in alg.value or "PS" in alg.value, PemAlgorithms
    ):
        try:
            service = JWTEncoder(
                PemIdentity(
                    public_key_loader=lambda: public_key,
                    private_key_loader=lambda: private_key,
                    algorithm=algorithm,
                ),
                py_jwt=PyJWT(),  # type: ignore
                claims=JWTEncodeClaims(),
            )
            service.encode(test_data)
        except Exception as e:
            raise Exception(f"{algorithm} not valid. Error: {e}") from e


def test_ES_identities(test_data: dict[str, str | bool]) -> None:
    es_private_key = ec.generate_private_key(ec.SECP192R1())
    es_public_key: ec.EllipticCurvePublicKey = es_private_key.public_key()

    public_key: bytes = es_public_key.public_bytes(
        encoding=Encoding.PEM,
        format=PublicFormat.SubjectPublicKeyInfo,
    )

    private_key: bytes = es_private_key.private_bytes(
        encoding=Encoding.PEM,
        format=PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=NoEncryption(),
    )

    for algorithm in filter(lambda alg: "ES" in alg.value, PemAlgorithms):
        try:
            service = JWTEncoder(
                PemIdentity(
                    public_key_loader=lambda: public_key,
                    private_key_loader=lambda: private_key,
                    algorithm=algorithm,
                ),
                py_jwt=PyJWT(),  # type: ignore
                claims=JWTEncodeClaims(),
            )
            service.encode(test_data)
        except Exception as e:
            raise Exception(f"{algorithm} not valid. Error: {e}") from e


def test_EdDSA_identitie(test_data: dict[str, str | bool]) -> None:
    es_private_key: Ed25519PrivateKey = Ed25519PrivateKey.generate()
    es_public_key: Ed25519PublicKey = es_private_key.public_key()

    public_key: bytes = es_public_key.public_bytes(
        encoding=Encoding.PEM,
        format=PublicFormat.SubjectPublicKeyInfo,
    )

    private_key: bytes = es_private_key.private_bytes(
        encoding=Encoding.PEM,
        format=PrivateFormat.PKCS8,
        encryption_algorithm=NoEncryption(),
    )
    service = JWTEncoder(
        PemIdentity(
            public_key_loader=lambda: public_key,
            private_key_loader=lambda: private_key,
            algorithm=PemAlgorithms.EdDSA,
        ),
        py_jwt=PyJWT(),  # type: ignore
        claims=JWTEncodeClaims(),
    )
    service.encode(test_data)
