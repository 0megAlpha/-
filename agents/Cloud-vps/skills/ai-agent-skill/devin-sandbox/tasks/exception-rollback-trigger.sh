export LANG=zh_TW.UTF-8
trap "echo DEVIN_STOP" SIGTERM SIGINT
while true; do
  sleep 60
done
