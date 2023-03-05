from jwt import PyJWT

import pytest

from jwts import (
    JWTDecodeClaims,
    JWTDecodeException,
    JWTDecoder,
    JWTEncodeClaims,
    JWTEncoder,
    PlainAlgorithms,
    PlainIdentity,
)


@pytest.fixture
def plain_identity() -> PlainIdentity:
    return PlainIdentity(
        secret_key_loader=lambda: "some key", algorithm=PlainAlgorithms.HS256
    )


@pytest.fixture
def encoder(plain_identity: PlainIdentity) -> JWTEncoder:
    return JWTEncoder(
        identity=plain_identity,
        py_jwt=PyJWT(),  # type: ignore
        claims=JWTEncodeClaims(),
    )


@pytest.fixture
def decoder(plain_identity: PlainIdentity) -> JWTDecoder:
    return JWTDecoder(
        identity=plain_identity,
        py_jwt=PyJWT(),  # type: ignore
        claims=JWTDecodeClaims(require=[]),
    )


def test_create_token(
    encoder: JWTEncoder, test_data: dict[str, str | bool]
) -> None:
    token = encoder.encode(test_data)
    assert isinstance(token, str)


def test_decode_valid_token(
    encoder: JWTEncoder, decoder: JWTDecoder, test_data: dict[str, str | bool]
) -> None:
    token = encoder.encode(test_data)
    decoded_data = decoder.decode(token)

    assert decoded_data["payload"] == test_data


def test_decode_token_with_not_enouth_segments(
    decoder: JWTDecoder, test_data: dict[str, str | bool]
) -> None:
    with pytest.raises(JWTDecodeException):
        decoder.decode("asdasdnas")


def test_decode_token_with_bad_encoding(
    decoder: JWTDecoder, test_data: dict[str, str | bool]
) -> None:
    with pytest.raises(JWTDecodeException):
        decoder.decode("asdadasda.asdasdadasd.asdasdasdad")


def test_decode_token_with_different_secret_key(
    decoder: JWTDecoder,
    plain_identity: PlainIdentity,
    test_data: dict[str, str | bool],
) -> None:
    different_service = JWTEncoder(
        PlainIdentity(
            secret_key_loader=plain_identity.secret_key_loader,
            algorithm=PlainAlgorithms.HS384,
        ),
        py_jwt=PyJWT(),  # type: ignore
        claims=JWTEncodeClaims(),
    )
    invalid_token = different_service.encode(test_data)
    with pytest.raises(JWTDecodeException):
        decoder.decode(invalid_token)


def test_decode_token_with_different_algorithm(
    decoder: JWTDecoder,
    plain_identity: PlainIdentity,
    test_data: dict[str, str | bool],
) -> None:
    different_service = JWTEncoder(
        PlainIdentity(
            secret_key_loader=plain_identity.secret_key_loader,
            algorithm=PlainAlgorithms.HS384,
        ),
        py_jwt=PyJWT(),  # type: ignore
        claims=JWTEncodeClaims(),
    )
    invalid_token = different_service.encode(test_data)
    with pytest.raises(JWTDecodeException):
        decoder.decode(invalid_token)
