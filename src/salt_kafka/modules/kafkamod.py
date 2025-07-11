import logging
import datetime
import re

log = logging.getLogger(__name__)

try:
    from confluent_kafka.admin import (
        AdminClient,
        NewTopic,
        ConfigResource,
        ConfigEntry,
        ResourceType,
        AlterConfigOpType,
    )
except ImportError:
    log.warning("Cannot find confluent_kafka")

__virtualname__ = "kafka"
__context__ = {}
__salt__ = {}


def __virtual__():
    return True


def _config(key):
    if key not in __context__:
        __context__[key] = __salt__["config.option"](f"kafka.{key}")
    return __context__[key]


def _client():
    if "_client" not in __context__:
        __context__["_client"] = AdminClient(
            {
                "bootstrap.servers": _config("bootstrap.servers"),
            }
        )
    return __context__["_client"]


TIMEDELTA_VARS = {
    "weeks": "w",
    "days": "d",
    "hours": "h",
    "minutes": "m",
    "seconds": "s",
    "milliseconds": "ms",
    "microseconds": "us",
}
TIMEDELTA_RE = re.compile(
    "".join([f"((?P<{k}>\d+?){TIMEDELTA_VARS[k]})?" for k in TIMEDELTA_VARS])
)


def timedelta_ms(value: str) -> int:
    """
    Parse a timedelta into milliseconds as used by Kafka
    """
    parsed = TIMEDELTA_RE.match(value).groupdict()
    parts = {p: int(parsed[p]) for p in parsed if parsed[p] is not None}
    td = datetime.timedelta(**parts)
    return int(td.total_seconds() * 1000)


def list_topics():
    response = _client().list_topics(timeout=10)
    return response.topics


def create_topic(name, num_partitions=3, replication_factor=1, config=None):
    request = NewTopic(name, num_partitions, replication_factor)
    if config is not None:
        request.config = config

    response = _client().create_topics([request])
    changes = {topic: response[topic].result() is None for topic in response}
    log.info("create_topic %s", changes)
    return changes[name]


def delete_topic(name):
    response = _client().delete_topics([name])
    changes = {topic: response[topic].result() is None for topic in response}
    log.info("delete_topics %s", response)
    return changes[name]


def describe_topic(name):
    request = [ConfigResource(ResourceType.TOPIC, name)]
    log.info("describe_topics %s", request)
    response = _client().describe_configs(request)
    changes = {}

    for topic in response:
        changes[topic.name] = {}
        for config in response[topic].result().values():
            changes[topic.name][config.name] = config.value

    return changes[name]


def update_topic(name, config: dict):
    client = _client()
    print("new_config", config)

    new_config = [
        ConfigEntry(
            name=key,
            value=str(config[key]),
            incremental_operation=AlterConfigOpType.SET,
        )
        for key in config
    ]
    request = [ConfigResource(ResourceType.TOPIC, name, incremental_configs=new_config)]

    response = client.incremental_alter_configs(request)
    for cr in response:
        if response[cr].result() is None:
            return {ce.name: ce.value for ce in cr.incremental_configs}
