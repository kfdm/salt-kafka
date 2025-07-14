_help:
    @just --list

_salt_call *args:
    sudo salt-call --local -l info {{ args }}

[group('dev')]
format:
    uvx ruff check --fix
    uvx ruff format
