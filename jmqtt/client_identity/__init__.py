"""
Client identity helpers grouped by concern.

Submodules:
- `facts`: runtime device facts collection (serial/mac/bluetooth)
- `validation`: validation of app/instance identity components
- `hashing`: deterministic token building
- `client_id`: MQTT client-id composition logic
"""

from . import facts, validation, hashing, client_id

__all__ = ["facts", "validation", "hashing", "client_id"]
