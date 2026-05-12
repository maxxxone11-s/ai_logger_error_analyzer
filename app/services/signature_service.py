def build_signature(message: str, source: str | None) -> str:
    return f"{message}:{source}"