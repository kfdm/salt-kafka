_help:
    @just --list

_salt_call *args:
    sudo salt-call --local -l info {{ args }}

[group('state.apply')]
@forward *args:
    just _salt_call state.apply kafka.forward {{ args }}

[group('state.apply')]
@reverse *args:
    just _salt_call state.apply kafka.reverse {{ args }}

[group('module')]
list:
    just _salt_call kafka.list_topics

[group('module')]
describe topic='test':
    just _salt_call kafka.describe_topics {{ topic }}

[group('dev')]
format:
    uvx ruff check --fix
    uvx ruff format
