#!/bin/bash
# Run Playwright+pytest tests and launch a live server to view the HTML report

pytest "$@"

REPORT_PATH="reports/playwright_report.html"
JSON_REPORT_PATH="reports/playwright_report.json"

# Function to find a free port between 8000-9000
find_free_port() {
  for port in $(seq 8888 9000); do
    if ! lsof -i :$port >/dev/null 2>&1; then
      echo $port
      return
    fi
  done
  # fallback: random port
  echo 0
}

PORT=8888
if lsof -i :$PORT >/dev/null 2>&1; then
  PORT=$(find_free_port)
fi

# Start FastAPI webhook_reporter in background (port 8000)
WEBHOOK_PORT=8000
uvicorn service.webhook_reporter:app --host 0.0.0.0 --port $WEBHOOK_PORT &
WEBHOOK_PID=$!
sleep 2 # Give FastAPI a moment to start

echo "\nFastAPI Webhook Reporter running at: http://localhost:$WEBHOOK_PORT"
echo "  - GET  /report (view JSON report)"
echo "  - POST /send-report (send JSON report to webhook)"

if [ -f "$REPORT_PATH" ]; then
  echo "\nPlaywright HTML report available at: http://localhost:$PORT/playwright_report.html"
  # Start the static server in the background
  python3 -m http.server $PORT --directory reports &
  SERVER_PID=$!
  # Open the report in the default browser (macOS)
  open "http://localhost:$PORT/playwright_report.html"
  # Wait for user to press any key to stop both servers
  echo "\nPress any key to stop the report and webhook servers..."
  read -n 1 -s
  kill $SERVER_PID
  kill $WEBHOOK_PID

else
  echo "Report not found: $REPORT_PATH"
  kill $WEBHOOK_PID
fi
