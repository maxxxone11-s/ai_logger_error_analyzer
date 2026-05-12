from app.services.signature_service import build_signature

def test_build_signature():
    signature = build_signature(
        message="TypeError: NoneType object is not iterable",
        source="demo_client/main.py"
    )

    assert signature == "TypeError: NoneType object is not iterable:demo_client/main.py"