my-topic:
    kafka.present:
        - config:
              cleanup.policy: delete
              retention.ms: {{salt['kafka.timedelta_ms']('2d')}}
              retention.bytes: {{ "1GB" | human_to_bytes }}

missing-topic:
    kafka.absent: []
