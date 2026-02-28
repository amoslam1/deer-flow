#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOG_ROOT="$ROOT/logs"

# Load env files for API keys and other app settings.
set -a
[ -f "$ROOT/.env" ] && source "$ROOT/.env"
[ -f "$ROOT/backend/.env" ] && source "$ROOT/backend/.env"
set +a

mkdir -p "$LOG_ROOT/archive"

cleanup() {
  echo ""
  echo "Stopping local debug services..."
  pkill -f "langgraph dev" 2>/dev/null || true
  pkill -f "uvicorn src.gateway.app:app" 2>/dev/null || true
  pkill -f "next dev" 2>/dev/null || true
  nginx -c "$ROOT/docker/nginx/nginx.local.conf" -p "$ROOT" -s quit 2>/dev/null || true
  sleep 1
  pkill -9 nginx 2>/dev/null || true
  echo "Done."
  exit 0
}

trap cleanup INT TERM

echo "=========================================="
echo "  DeerFlow Local Debug Startup"
echo "=========================================="
echo "Root: $ROOT"
echo "GEMINI_BASE_URL: ${GEMINI_BASE_URL:-https://generativelanguage.googleapis.com}"
echo "GEMINI_IMAGE_MODEL: ${GEMINI_IMAGE_MODEL:-gemini-3-pro-image-preview}"
echo "GEMINI_VIDEO_MODEL: ${GEMINI_VIDEO_MODEL:-veo-3.1-generate-preview}"
echo "LOG_LEVEL: ${LOG_LEVEL:-DEBUG}"
echo ""

echo "Starting LangGraph..."
(
  cd "$ROOT/backend"
  LOG_LEVEL="${LOG_LEVEL:-DEBUG}" NO_COLOR=1 \
    uv run langgraph dev --server-log-level "${LANGGRAPH_SERVER_LOG_LEVEL:-debug}" \
    --no-browser --allow-blocking --no-reload 2>&1 \
    | python3 "$ROOT/scripts/tee_daily_log.py" langgraph --log-root "$LOG_ROOT"
) &

sleep 2

echo "Starting Gateway..."
(
  cd "$ROOT/backend"
  uv run uvicorn src.gateway.app:app --host 0.0.0.0 --port 8001 --reload \
    --log-level "${UVICORN_LOG_LEVEL:-debug}" 2>&1 \
    | python3 "$ROOT/scripts/tee_daily_log.py" gateway --log-root "$LOG_ROOT"
) &

sleep 2

echo "Starting Frontend..."
(
  cd "$ROOT/frontend"
  pnpm run dev 2>&1 \
    | python3 "$ROOT/scripts/tee_daily_log.py" frontend --log-root "$LOG_ROOT"
) &

sleep 2

echo "Starting Nginx..."
(
  cd "$ROOT"
  nginx -g "daemon off;" -c "$ROOT/docker/nginx/nginx.local.conf" -p "$ROOT" 2>&1 \
    | python3 "$ROOT/scripts/tee_daily_log.py" nginx --log-root "$LOG_ROOT"
) &

echo ""
echo "Services started:"
echo "  App:       http://localhost:2026"
echo "  LangGraph: http://localhost:2024"
echo "  Gateway:   http://localhost:8001"
echo ""
echo "Logs:"
echo "  $LOG_ROOT/langgraph.log"
echo "  $LOG_ROOT/gateway.log"
echo "  $LOG_ROOT/frontend.log"
echo "  $LOG_ROOT/nginx.log"
echo ""
echo "Press Ctrl+C to stop."

wait
