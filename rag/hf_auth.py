import os

_TOKEN_KEYS = (
    "HF_TOKEN",
    "HUGGINGFACE_HUB_TOKEN",
    "HF_API_TOKEN",
)


def resolve_hf_token() -> str | None:
    """HF Spaces secret, alternate env names, or huggingface_hub login token."""
    for key in _TOKEN_KEYS:
        value = os.environ.get(key)
        if value and value.strip():
            return value.strip()
    try:
        from huggingface_hub import get_token

        token = get_token()
        if token and str(token).strip():
            return str(token).strip()
    except Exception:
        pass
    return None


def require_hf_token() -> str:
    token = resolve_hf_token()
    if token:
        os.environ.setdefault("HF_TOKEN", token)
        return token
    raise RuntimeError(
        "No Hugging Face token found. In Space Settings → Repository secrets, "
        "add a secret named exactly HF_TOKEN (write token from huggingface.co/settings/tokens), "
        "then Factory restart the Space."
    )
