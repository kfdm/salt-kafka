# salt-kafka

Kafka tools for Salt

[![PyPI - Version](https://img.shields.io/pypi/v/salt-kafka)](https://pypi.org/project/salt-kafka/)
[![Gitea Stars](https://img.shields.io/gitea/stars/kfdm/salt-kafka?gitea_url=https://codeberg.org)](https://codeberg.org/kfdm/salt-kafka)

## Installation

Can be installed via `pip` or the Pip version distributed in Salt onedir installs.
Salt extensions need to be installed to any `salt-minion` where they may run.

```shell
# Example for Salt onedir
/opt/saltstack/salt/salt-pip install salt-kafka

# Can be installed via Salt commands
salt '*' pip.install salt-kafka
```

or Via a salt state

```yaml
salt-minion:
  service.running:
    - enable: true
  # Install any OS requirements
  pkg.installed:
    - aggregate: True
    - pkgs:
        - python3-docker
        - python3-setproctitle
  # Install any pip packages
  pip.installed:
    - pkgs:
        - salt-kafka
```

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

## States

```yaml
# Example minion config
kafka.bootstrap.servers: "kafka.example.com:9094"
```

```yaml
# Example kafka.sls
my-topic:
    kafka.present:
        - config:
              cleanup.policy: delete
              retention.ms: {{salt['kafka.timedelta_ms']('2d')}}
              retention.bytes: {{ "1GB" | human_to_bytes }}

missing-topic:
    kafka.absent: []
```

See the Upstream Kafka documentation at <http://kafka.apache.org/documentation.html#topicconfigs> for valid config options.
