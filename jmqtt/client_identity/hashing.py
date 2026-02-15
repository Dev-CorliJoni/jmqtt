from __future__ import annotations

import base64
import hashlib
import math


def _compose_content(seed: str, namespace: str | None) -> str:
    if not isinstance(seed, str) or seed.strip() == "":
        raise ValueError("seed must be a non-empty string")
    if namespace is not None and (not isinstance(namespace, str) or namespace.strip() == ""):
        raise ValueError("namespace must be a non-empty string when provided")

    content = seed.strip()
    if namespace is not None:
        content = f"{namespace.strip()}\x1f{content}"
    return content


def build_compact_token(seed: str, length: int = 16, namespace: str | None = None) -> str:
    """
    Deterministic compact token using base32 lowercase `[a-z2-7]`.

    Suitable when a strict, lowercase identifier alphabet is desired.
    """
    if length < 1:
        raise ValueError("length must be >= 1")

    content = _compose_content(seed, namespace)
    digest_size = max(10, math.ceil(length * 5 / 8))
    raw = hashlib.blake2s(content.encode("utf-8"), digest_size=digest_size).digest()
    encoded = base64.b32encode(raw).decode("ascii").rstrip("=").lower()
    return encoded[:length]


def build_urlsafe_token(seed: str, length: int = 32, namespace: str | None = None) -> str:
    """
    Deterministic URL-safe token using base64url `[A-Za-z0-9-_]`.

    Suitable for general unique identifiers with higher character density.
    """
    if length < 1:
        raise ValueError("length must be >= 1")

    content = _compose_content(seed, namespace)
    digest_size = max(16, math.ceil(length * 3 / 4))
    raw = hashlib.blake2s(content.encode("utf-8"), digest_size=digest_size).digest()
    encoded = base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")
    return encoded[:length]


__all__ = ["build_compact_token", "build_urlsafe_token"]
