#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export COMPOSE_PROJECT_NAME="${COMPOSE_PROJECT_NAME:-n8n-function-vm2}"
BASE="${1:-http://127.0.0.1:18201}"
chmod +x poc.py

down() {
  echo "== docker compose down -v =="
  docker compose down -v --remove-orphans || true
}

echo "== docker compose down (clean volume) =="
docker compose down -v --remove-orphans || true

echo "== docker compose up (n8nio/n8n:2.42.0, loopback :18201) =="
up_ok=0
for attempt in $(seq 1 8); do
  if docker compose up -d --build; then
    up_ok=1
    break
  fi
  echo "IOC compose-up-retry attempt=$attempt"
  sleep 15
done
if [[ "$up_ok" != 1 ]]; then
  echo "FAIL N8N-FUNCTION-VM2 docker compose up" | tee poc-last-run.txt
  docker compose logs --tail=80 n8n || true
  down
  exit 1
fi

echo "== wait for n8n readiness + REST on ${BASE} =="
ok=0
for i in $(seq 1 90); do
  live="$(curl -s -o /tmp/n8n-function-vm2-health -w '%{http_code}' --max-time 5 "$BASE/healthz" || true)"
  ready="$(curl -s -o /tmp/n8n-function-vm2-ready -w '%{http_code}' --max-time 5 "$BASE/healthz/readiness" || true)"
  settings="$(curl -s -o /tmp/n8n-function-vm2-settings -w '%{http_code}' --max-time 5 "$BASE/rest/settings" || true)"
  if [[ "$ready" == "200" && "$settings" == "200" ]]; then
    echo "IOC n8n-up healthz=$live readiness=$ready settings=$settings"
    ok=1
    break
  fi
  echo "IOC wait i=$i healthz=$live readiness=$ready settings=$settings"
  sleep 3
done
if [[ "$ok" != 1 ]]; then
  echo "FAIL N8N-FUNCTION-VM2 n8n REST did not become ready on $BASE" | tee poc-last-run.txt
  docker compose logs --tail=80 n8n || true
  down
  exit 1
fi

echo "== poc.py =="
set +e
python3 poc.py "$BASE" | tee poc-last-run.txt
rc=${PIPESTATUS[0]}
set -e
if [[ "$rc" != 0 ]]; then
  echo "== n8n logs (tail) ==" | tee -a poc-last-run.txt
  docker compose logs --tail=80 n8n | tee -a poc-last-run.txt || true
fi
down
exit "$rc"
