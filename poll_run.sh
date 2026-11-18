#!/bin/bash
# Poll satu Actions run tiap 5 menit sampai completed (maks ~2.5 jam).
# Pakai: poll_run.sh <run_id> <logfile>
RUN_ID=$1
LOG=$2
echo "poll start $(TZ=Asia/Jakarta date '+%Y-%m-%d %H:%M WIB') run=$RUN_ID" > "$LOG"
for i in $(seq 1 30); do
  python3 ~/workspace/tools/gh_api_full.py GET "/repos/hozin-king/twrp-duchamp-builder/actions/runs/$RUN_ID" /tmp/twrp_poll_status.json >/dev/null 2>&1
  S=$(python3 -c "import json;d=json.load(open('/tmp/twrp_poll_status.json'));print(d.get('status'),d.get('conclusion'))" 2>/dev/null)
  echo "$(TZ=Asia/Jakarta date '+%H:%M WIB') check $i: $S" >> "$LOG"
  if echo "$S" | grep -q "completed"; then
    echo "FINAL: $S" >> "$LOG"
    exit 0
  fi
  sleep 300
done
echo "poll timeout after 30 checks" >> "$LOG"
exit 2
