my-topic:
    kafka.present:
        - config:
              cleanup.policy: delete
              retention.ms: 604800006

missing-topic:
    kafka.absent: []
