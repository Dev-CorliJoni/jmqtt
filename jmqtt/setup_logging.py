import logging

NAMESPACE = "jmqtt"
logging.getLogger(NAMESPACE).addHandler(logging.NullHandler())


def get_logger(name):
    return logging.getLogger(f"{NAMESPACE}.{name}")
