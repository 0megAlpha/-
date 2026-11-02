#!/bin/bash
HOST="${VPS_BRIDGE_DEFAULT_HOST:-localhost}"; USER="${VPS_BRIDGE_DEFAULT_USER:-root}"; KEY="${VPS_BRIDGE_SSH_KEY:-}"
exec_remote(){ if [ -n "$KEY" ];then ssh -i "$KEY" -o StrictHostKeyChecking=no "$USER@$HOST" "$1";else ssh -o StrictHostKeyChecking=no "$USER@$HOST" "$1";fi; }
case "$1" in exec) exec_remote "$2";; scp) scp "$2" "$USER@$HOST:$3";; docker) exec_remote "docker $2";; tmux) exec_remote "tmux $2";; *) echo "usage: bridge.sh {exec|scp|docker|tmux}";; esac
