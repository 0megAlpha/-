#!/usr/bin/env bash
# portctl open|close <port> [tcp|udp] | portctl list
set -uo pipefail
IFACE=$(ip route get 1.1.1.1 2>/dev/null | awk '{for(i=1;i<=NF;i++) if($i=="dev"){print $(i+1);exit}}')
SSHP=$(sshd -T 2>/dev/null | awk '/^port /{print $2;exit}'); SSHP=${SSHP:-22}
act=${1:-list}; port=${2:-}; proto=${3:-tcp}
[ "$act" = close ] && [ "$port" = "$SSHP" ] && { echo "拒絕關閉 SSH port $SSHP"; exit 1; }
case "$act" in
  open)  ufw allow "$port/$proto"; iptables -C DOCKER-USER -i "$IFACE" -p "$proto" -m conntrack --ctorigdstport "$port" -j ACCEPT 2>/dev/null || iptables -I DOCKER-USER 1 -i "$IFACE" -p "$proto" -m conntrack --ctorigdstport "$port" -j ACCEPT ;;
  close) ufw delete allow "$port/$proto"; iptables -D DOCKER-USER -i "$IFACE" -p "$proto" -m conntrack --ctorigdstport "$port" -j ACCEPT 2>/dev/null ;;
  list)  ufw status numbered; echo; ss -tlnpH | awk '{print $4, $6}' ;;
  *) echo "用法: portctl open|close <port> [tcp|udp] | portctl list" ;;
esac
