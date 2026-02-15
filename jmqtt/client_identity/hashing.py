from __future__ import annotations

import base64
import hashlib
import math


def build_deterministic_id(seed: str, length: int = 16, namespace: str | None = None) -> str:
    """
    Build a deterministic lowercase token from a seed.

    Output alphabet: base32 lowercase `[a-z2-7]`.
    """
    if not isinstance(seed, str) or seed.strip() == "":
        raise ValueError("seed must be a non-empty string")
    if namespace is not None and (not isinstance(namespace, str) or namespace.strip() == ""):
        raise ValueError("namespace must be a non-empty string when provided")
    if length < 1:
        raise ValueError("length must be >= 1")

    content = seed.strip()
    if namespace is not None:
        content = f"{namespace.strip()}\x1f{content}"

    digest_size = max(10, math.ceil(length * 5 / 8))
    raw = hashlib.blake2s(content.encode("utf-8"), digest_size=digest_size).digest()
    encoded = base64.b32encode(raw).decode("ascii").rstrip("=").lower()
    return encoded[:length]
