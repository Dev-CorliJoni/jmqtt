from __future__ import annotations

import re

_CLIENT_ID_COMPONENT_PATTERN = re.compile(r"^[A-Za-z0-9-]+$")


def validate_client_id_component(value: str, field: str) -> str:
    """
    Validate app/instance components used for MQTT client-id derivation.

    Rules:
    - non-empty string
    - only letters, digits and '-'
    - normalized to lowercase
    """
    if not isinstance(value, str):
        raise ValueError(f"{field} is invalid: value must be a string.")

    normalized = value.strip()
    if normalized == "":
        raise ValueError(f"{field} is invalid: value must not be empty.")

    if _CLIENT_ID_COMPONENT_PATTERN.fullmatch(normalized) is None:
        raise ValueError(f"{field} is invalid: only letters, digits and '-' are allowed.")

    return normalized.lower()
