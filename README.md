# salt-kafka

Kafka tools for Salt

[![PyPI - Version](https://img.shields.io/pypi/v/salt-kafka)](https://pypi.org/project/salt-kafka/)
[![Gitea Stars](https://img.shields.io/gitea/stars/kfdm/salt-kafka?gitea_url=https://codeberg.org)](https://codeberg.org/kfdm/salt-kafka)

## Engine

`kafka_consumer` can be used to map Kafka topics to a Salt topic to be used in automation.

```yaml
# From Salt Master config

engines:
  - kafka_consumer:
      broker: kafka.example.com:9094
      subscribe:
        # Format is <kafka-topic> / <salt-topic>
        push-repo: kafka/repo
        push-package: kafka/container
```
