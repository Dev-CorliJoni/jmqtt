from __future__ import annotations

from jmqtt import MQTTBuilderV3, MQTTBuilderV5, client_identity


def test_effective_client_id_is_exposed_v3(monkeypatch):
    monkeypatch.setattr(
        client_identity.facts,
        "collect_device_facts",
        lambda: ("serial-client", []),
    )

    expected_client_id = client_identity.client_id.build_auto_client_id(
        app_name="agent",
        instance_id="worker1",
        serial_number="serial-client",
        connections=[],
    )

    connection = MQTTBuilderV3("localhost", "agent").instance_id("worker1").build()
    assert connection.client_id == expected_client_id


def test_effective_client_id_is_exposed_v5(monkeypatch):
    monkeypatch.setattr(
        client_identity.facts,
        "collect_device_facts",
        lambda: ("serial-client", []),
    )

    expected_client_id = client_identity.client_id.build_auto_client_id(
        app_name="agent",
        instance_id="worker2",
        serial_number="serial-client",
        connections=[],
    )

    connection = MQTTBuilderV5("localhost", "agent").instance_id("worker2").build()
    assert connection.client_id == expected_client_id
