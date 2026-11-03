#!/usr/bin/env bash
# lockdown plan|apply|confirm|rollback  （apply 後 5 分鐘內沒 confirm 會自動還原）
set -uo pipefail
IFACE=$(ip route get 1.1.1.1 2>/dev/null | awk '{for(i=1;i<=NF;i++) if($i=="dev"){print $(i+1);exit}}')
SSHP=$(sshd -T 2>/dev/null | awk '/^port /{print $2;exit}'); SSHP=${SSHP:-22}
case "${1:-plan}" in
  plan)
    echo "SSH port: $SSHP / 對外網卡: $IFACE"
    echo "--- 目前對外監聽 ---"; ss -tlnpH | awk '$4 ~ /^(0\.0\.0\.0|\[::\]|\*):/ {print $4, $6}'
    echo "--- Docker 對外發佈 ---"; docker ps --format '{{.Names}}  {{.Ports}}' 2>/dev/null | grep -E '0\.0\.0\.0|::'
    echo "套用: lockdown apply" ;;
  apply)
    command -v ufw >/dev/null || apt-get install -y ufw
    ufw --force reset; ufw default deny incoming; ufw default allow outgoing
    ufw allow "$SSHP/tcp"; ufw allow in on tailscale0; ufw --force enable
    iptables -N DOCKER-USER 2>/dev/null
    iptables -C DOCKER-USER -i "$IFACE" -m conntrack --ctstate NEW -j DROP 2>/dev/null || iptables -I DOCKER-USER -i "$IFACE" -m conntrack --ctstate NEW -j DROP
    systemd-run --on-active=300 --unit=lockdown-rollback /usr/local/bin/lockdown rollback
    echo "已套用。請另開一個 ssh 視窗確認連得上，再執行: lockdown confirm" ;;
  confirm) systemctl stop lockdown-rollback.timer 2>/dev/null; echo "已確認，保留規則" ;;
  rollback) ufw --force disable; iptables -D DOCKER-USER -i "$IFACE" -m conntrack --ctstate NEW -j DROP 2>/dev/null; echo "已還原" ;;
esac
