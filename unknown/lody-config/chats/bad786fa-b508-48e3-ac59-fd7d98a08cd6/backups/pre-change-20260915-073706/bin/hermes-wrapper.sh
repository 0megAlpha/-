#!/usr/bin/env bash
unset PYTHONPATH
unset PYTHONHOME
exec "/usr/local/lib/hermes-agent/venv/bin/python" "/usr/local/lib/hermes-agent/hermes" "$@"
