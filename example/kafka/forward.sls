my-topic:
    kafka.present:
        - config:
              cleanup.policy: delete
              retention.ms: {{salt['kafka.timedelta_ms']('7d')}}

missing-topic:
    kafka.absent: []
