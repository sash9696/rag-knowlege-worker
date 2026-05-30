import os

_TOKEN_KEYS = (
    "HF_TOKEN",
    "HUGGINGFACE_HUB_TOKEN",
    "HF_API_TOKEN",
)


def normalize_hf_token(raw: str) -> str:
    """Strip quotes and accidental 'HF_TOKEN=...' paste from Space secret value."""
    value = raw.strip().strip('"').strip("'")
    if value.upper().startswith("HF_TOKEN="):
        value = value.split("=", 1)[1].strip()
    return value


def resolve_hf_token() -> str | None:
    """HF Spaces secret, alternate env names, or huggingface_hub login token."""
    for key in _TOKEN_KEYS:
        raw = os.environ.get(key)
        if not raw:
            continue
        token = normalize_hf_token(raw)
        if token:
            return token
    try:
        from huggingface_hub import get_token

        token = get_token()
        if token:
            token = normalize_hf_token(str(token))
            if token:
                return token
    except Exception:
        pass
    return None


def require_hf_token() -> str:
    token = resolve_hf_token()
    if token:
        os.environ["HF_TOKEN"] = token
        return token
    raise RuntimeError(
        "HF token not visible in this container. Open Settings → Secrets → Replace "
        "HF_TOKEN with only the hf_… string (no HF_TOKEN= prefix), then Factory restart."
    )


def log_token_diagnostics() -> None:
    """Startup lines in Space logs (never prints the token)."""
    hf_keys = sorted(
        k for k in os.environ if k.startswith(("HF_", "HUGGINGFACE_")) and "SECRET" not in k
    )
    print(f"[Knowledge Worker] HF-related env keys: {hf_keys or '(none)'}")

    raw = os.environ.get("HF_TOKEN")
    if raw is None:
        print("[Knowledge Worker] HF_TOKEN env: missing")
    elif not raw.strip():
        print("[Knowledge Worker] HF_TOKEN env: empty string (re-save secret value)")
    else:
        token = normalize_hf_token(raw)
        print(
            f"[Knowledge Worker] HF_TOKEN env: len={len(raw)}, "
            f"looks_valid={token.startswith('hf_')}"
        )

    print(f"[Knowledge Worker] resolve_hf_token: {'ok' if resolve_hf_token() else 'missing'}")
