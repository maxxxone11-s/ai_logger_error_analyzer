from app.services.signature_sevice import build_signature

def test_build_signature():
    result = build_signature("error", "api")

    assert result == "error:api"