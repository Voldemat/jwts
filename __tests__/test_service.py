import pytest

from jwts import (
    JWTDecodeClaims,
    JWTDecoder,
    JWTEncodeClaims,
    JWTEncoder,
    JWTTokenPairIssuer,
    PlainAlgorithms,
    PlainIdentity,
    decode_access_token,
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
def token_pair_issuer(
    encoder: JWTEncoder, decoder: JWTDecoder
) -> JWTTokenPairIssuer:
    return JWTTokenPairIssuer(
        encoder=encoder,
        decoder=decoder,
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
    access_token_headers = decoder.get_headers(access_token)
    assert (
        access_token_headers.get("grant_type", None) == "access"
    ), access_token_headers
    decoder.decode(refresh_token)
    refresh_token_headers = decoder.get_headers(refresh_token)
    assert (
        refresh_token_headers.get("grant_type", None) == "refresh"
    ), refresh_token_headers

    new_access_token = token_pair_issuer.refresh(refresh_token)
    decoder.decode(new_access_token)
    new_access_token_headers = decoder.get_headers(new_access_token)
    assert (
        new_access_token_headers.get("grant_type", None) == "access"
    ), new_access_token_headers
    decode_access_token(decoder, new_access_token)
