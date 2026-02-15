from ..mqtt_connections import MQTTConnectionV5
from .mqtt_builder_base import MqttBuilder


class MQTTBuilderV5(MqttBuilder[MQTTConnectionV5]):
    def __init__(self, host: str, app_name: str):
        """
        Initialize an MQTT v5 builder.

        :param host: Broker hostname or IPv4/IPv6 literal.
        :param app_name: Stable application name used for deterministic client IDs.
                         Allowed characters: letters, digits, `-`.
                         If the same app runs multiple times on one broker, call
                         `instance_id(...)` to avoid client-id collisions.
        """
        super().__init__(host, app_name, connector=MQTTConnectionV5)
