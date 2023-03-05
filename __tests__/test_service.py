import pytest

from jwts import (
    JWTDecodeClaims,
    JWTDecoder,
    JWTEncodeClaims,
    JWTEncoder,
    JWTTokenPairIssuer,
    PlainAlgorithms,
    PlainIdentity,
)


@pytest.fixture
def identity() -> PlainIdentity:
    return PlainIdentity(
        secret_key_loader=lambda: "asdad213",
        algorithm=PlainAlgorithms.HS256,
    )


@pytest.fixture
def encoder(identity: PlainIdentity) -> JWTEncoder:
    return JWTEncoder(
        identity=identity,
        claims=JWTEncodeClaims(),
    )


@pytest.fixture
def decoder(identity: PlainIdentity) -> JWTDecoder:
    return JWTDecoder(
        identity=identity,
        claims=JWTDecodeClaims(require=[]),
    )


@pytest.fixture
def token_pair_issuer(encoder: JWTEncoder) -> JWTTokenPairIssuer:
    return JWTTokenPairIssuer(
        encoder=encoder,
        access_token_claims=JWTEncodeClaims(),
        refresh_token_claims=JWTEncodeClaims(),
    )


def test_create_token_pair(
    token_pair_issuer: JWTTokenPairIssuer,
    decoder: JWTDecoder,
) -> None:
    access_token, refresh_token = token_pair_issuer.create_pair(
        {"some": "payload"}
    )
    decoder.decode(access_token)
    decoder.decode(refresh_token)
