from __future__ import annotations

from typing import List

from .facts import Connection, CONN_MAC, CONN_BT, collect_device_facts
from .hashing import build_compact_token
from .validation import validate_client_id_component

DEFAULT_MAX_CLIENT_ID_LENGTH = 23


def resolve_device_fingerprint(serial_number: str | None, connections: List[Connection]) -> str:
    """
    Build a stable device fingerprint seed from runtime facts.

    Priority:
    1) serial number
    2) first stable connection by type priority: mac > bluetooth
    3) hostname fallback
    """
    if isinstance(serial_number, str) and serial_number.strip() != "":
        return f"sn:{serial_number.strip().lower()}"

    for kind, value in sorted(
        connections,
        key=lambda x: ((0 if x[0] == CONN_MAC else 1 if x[0] == CONN_BT else 2), x[1]),
    ):
        if isinstance(value, str) and value.strip() != "":
            return f"{kind}:{value.strip().lower()}"

    try:
        import socket

        host = socket.gethostname().strip().lower()
        if host:
            return f"host:{host}"
    except Exception:
        pass

    return "host:unknown"


def build_auto_client_id(
    app_name: str,
    instance_id: str | None = None,
    *,
    max_length: int = DEFAULT_MAX_CLIENT_ID_LENGTH,
    serial_number: str | None = None,
    connections: List[Connection] | None = None,
) -> str:
    """
    Build a deterministic MQTT client ID.

    Seed composition:
    - `device_fingerprint + app_name + instance_id` (if instance is set)
    - `device_fingerprint + app_name` (if instance is not set)
    """
    app_name_norm = validate_client_id_component(app_name, "app_name")
    instance_norm = None
    if instance_id is not None:
        instance_norm = validate_client_id_component(instance_id, "instance_id")

    if max_length < 8:
        raise ValueError("max_length must be >= 8")

    if serial_number is None and connections is None:
        serial_number, connections = collect_device_facts()
    elif connections is None:
        connections = []

    fingerprint = resolve_device_fingerprint(serial_number, connections)

    seed = f"{fingerprint}\x1f{app_name_norm}"
    if instance_norm is not None:
        seed = f"{seed}\x1f{instance_norm}"

    hash_length = min(12, max(8, max_length - 4))
    suffix = build_compact_token(seed, length=hash_length, namespace="mqtt-client")

    prefix_budget = max_length - len(suffix) - 1
    if prefix_budget <= 0:
        return suffix[:max_length]

    prefix = app_name_norm[:prefix_budget]
    if prefix == "":
        return suffix[:max_length]

    return f"{prefix}-{suffix}"[:max_length]


__all__ = ["DEFAULT_MAX_CLIENT_ID_LENGTH", "resolve_device_fingerprint", "build_auto_client_id"]
