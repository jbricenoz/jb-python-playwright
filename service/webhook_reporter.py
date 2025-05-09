from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from pathlib import Path
import json
import requests
from typing import Optional

app = FastAPI()

REPORT_PATH = Path(__file__).parent.parent / "reports" / "playwright_report.json"

class WebhookPayload(BaseModel):
    webhook_url: str
    message: Optional[str] = None
    only_failures: bool = False


def load_report():
    if not REPORT_PATH.exists():
        return None
    with open(REPORT_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def format_report(report, only_failures=False):
    summary = report.get("summary", {})
    tests = report.get("tests", [])
    if only_failures:
        tests = [t for t in tests if t.get("outcome") == "failed"]
    return {
        "summary": summary,
        "tests": tests
    }


def send_webhook(webhook_url, payload):
    headers = {"Content-Type": "application/json"}
    resp = requests.post(webhook_url, json=payload, headers=headers, timeout=10)
    return resp.status_code, resp.text


@app.post("/send-report")
def send_report(payload: WebhookPayload, background_tasks: BackgroundTasks):
    report = load_report()
    if not report:
        return JSONResponse(status_code=404, content={"error": "Report not found"})
    formatted = format_report(report, only_failures=payload.only_failures)
    message = payload.message or ("Playwright Test Report" if not payload.only_failures else "Playwright Test Failure Report")
    data = {
        "text": message,
        "report": formatted
    }
    background_tasks.add_task(send_webhook, payload.webhook_url, data)
    return {"status": "Report is being sent", "webhook_url": payload.webhook_url}


@app.get("/report")
def get_report(only_failures: bool = False):
    report = load_report()
    if not report:
        return JSONResponse(status_code=404, content={"error": "Report not found"})
    return format_report(report, only_failures=only_failures)
