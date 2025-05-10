# Playwright Python Automation Framework

This repository contains a robust, modular Playwright automation framework for the Magento e-commerce demo site.

---

## Features
- **Modular project structure** for scalability and maintainability
- **Page Object Model (POM)** for reusable, organized UI automation
- **Pytest** integration for test running and fixtures
- **Service modules** for data and utility operations
- **CSV-driven test data** for easy test parametrization
- **Email notification utility** for reporting
- **Ready for CI/CD** with GitHub Actions

---

## Project Structure Explained

- `e2e/` — End-to-end test cases using Playwright and Pytest
- `components/` — Page Object classes, organized by feature/section
  - `home/` — Home page components (e.g., `homepage.py`, `header_content.py`, `nav_sections.py`)
- `data/` — Test data files (e.g., CSV files for test input)
- `fixtures/` — Pytest fixtures for browser/session/test setup
- `service/` — Utility modules for:
  - **CSVService**: Read/write CSV test data
  - **EmailService**: Send emails (e.g., for notifications or reports)
- `.github/` — Issue/PR templates and GitHub Actions workflows for CI
- `playwright.config.py` — Project-level config for Playwright and Pytest
- `requirements.txt` — All Python dependencies

---

## Email Sending (Local SMTP, No Config Required)

The framework includes a simple `EmailService` for sending emails via a local SMTP server on `localhost` (no authentication required). This works out-of-the-box on both Ubuntu and macOS if a local SMTP server is running.

**Recommended for development/testing:**
- Use [MailHog](https://github.com/mailhog/MailHog) (cross-platform, no config, captures all test emails in a web UI)

#### Quick Start with MailHog

**macOS:**
```bash
brew install mailhog
mailhog
```

**Ubuntu:**
```bash
sudo apt-get install golang-go # if Go is not installed
go install github.com/mailhog/MailHog@latest
~/go/bin/MailHog
```

MailHog listens on `localhost:1025` (SMTP) and shows a web UI at [http://localhost:8025](http://localhost:8025).

#### Usage Example
```python
from service.email_service import EmailService

email_service = EmailService(smtp_server="localhost", smtp_port=1025)  # For MailHog
email_service.send_email(
    subject="Test Email",
    body="This is a test email.",
    recipients=["your@email.com"],
    sender="Tester <your@email.com>"
)
```

#### Troubleshooting
- Make sure MailHog (or another SMTP server) is running on the correct port.
- For real email delivery, use an actual SMTP server (e.g., Gmail SMTP, company mail relay) and configure `smtp_server`/`smtp_port` as needed.
- No changes to `/etc/hosts` or environment variables are required for local dev/testing.
- All errors will be printed to the console for easy debugging.

---

## How to Use This Framework

### 1. Setup Environment

```bash
# create a directory for the project (Optional)
mkdir my_workspace
cd my_workspace
# clone the repository
git clone https://github.com/jbricenoz/jb-python-playwright.git
# cd into the project directory
cd jb-python-playwright
# create a virtual environment and activate it
python3 -m venv venv
source venv/bin/activate
# upgrade pip
pip install --upgrade pip
# install dependencies
pip install -r requirements.txt
# install playwright
playwright install
```

### 2. Configure Playwright (Optional & Advanced)
- Edit `playwright/playwright.config.py` to change base URL, browser, headless mode, timeouts, retries, trace, video, screenshot, parallel workers, or output directories.
- You can override config via environment variables or pytest CLI options:
  - `BASE_URL`, `BROWSER`, `HEADLESS`, `PLAYWRIGHT_TIMEOUT`, `PLAYWRIGHT_RETRIES`, `PLAYWRIGHT_WORKERS`, `PLAYWRIGHT_TRACE`, `PLAYWRIGHT_VIDEO`, `PLAYWRIGHT_SCREENSHOT`, `PLAYWRIGHT_SLOWMO`
- Supported browsers: `chromium` (Chrome/Edge), `firefox`, `webkit` (Safari), `chrome`, `edge`, `safari` (aliases). **IE11 is not natively supported by Playwright; use Selenium or a cloud/grid provider for legacy browser testing.**
- Advanced options:
  - `--retries`: Number of retries for flaky tests
  - `--workers`: Number of parallel workers
  - `--trace`: Trace mode (`on`, `off`, `retain-on-failure`)
  - `--video`: Video recording (`on`, `off`, `retain-on-failure`)
  - `--screenshot`: Take screenshots (`on`, `off`, `only-on-failure`)
  - `--slowmo`: Slow down Playwright operations (ms)
  - `--headed`: Run browser in headed mode

**Example CLI usage:**

### Run All Tests in All Browsers (Parallel)
Run all tests in Chromium, Firefox, and WebKit in parallel (headed mode):
```sh
./pw.sh --headed -n 3
```
- `--headed`: Run browsers with UI visible.
- `-n 3`: Run tests in parallel using 3 workers (pytest-xdist required).

### Run in a Single Browser
Specify a browser (chromium, firefox, or webkit):
```sh
./pw.sh --headed --browser=firefox
```

### Run Headless
Remove `--headed` or add `--headless`:
```sh
./pw.sh --headless -n 3
```

### Run Only Marked Tests
To run only tests with a specific marker (e.g., homepage):
```sh
./pw.sh -m homepage --headed -n 3
```

### How to run this test file:

```sh
# Run all homepage tests (with output)
pytest -v e2e/test_homepage.py

# Run only homepage tests with 'homepage' marker
pytest -m homepage e2e/test_homepage.py

# Run all smoke tests
pytest -m smoke

# To see print output, use:
pytest -s e2e/test_homepage.py

# Run with Playwright browser options (examples):
pytest e2e/test_homepage.py --browser=firefox --headless
pytest e2e/test_homepage.py --browser=webkit --trace=on --video=on
pytest e2e/test_homepage.py --workers=2 --retries=1
```

### Reports
- HTML and JSON reports are generated in the `reports/` directory.
- After a run, open the HTML report:
  - Open the link shown in the terminal, e.g.:
    - `file:///.../playwright/reports/playwright_report.html`
    - Or: `http://localhost:8889/playwright_report.html` if the server is running

---

## Parallel Test Execution & Worker Configuration

This project supports parallel test execution using **pytest-xdist**. You can control the number of parallel workers in several ways:

### 1. Command Line (`-n` flag)
Run tests in parallel by specifying the number of workers:
```sh
./pw.sh --headed -n 4
```
This runs tests in 4 parallel processes.

### 2. CLI Option (`--workers`)
If your CLI and config support it, you can use:
```sh
./pw.sh --headed --workers=4
```

### 3. Environment Variable
Set the number of workers via an environment variable:
```sh
export PLAYWRIGHT_WORKERS=4
./pw.sh --headed
```

### 4. pytest.ini (Default for All Runs)
Set a default number of workers for all runs by adding this to `pytest.ini`:
```ini
[pytest]
addopts = -n 3
```

### How It Works
- Each worker is a separate process and can run tests in a different browser if you use browser parametrization (as this project does).
- If you have 3 browsers and 3 workers, each worker can run one browser in parallel.
- If you have more tests than workers, workers will pick up new tests as they finish.

### Summary Table
| Method                        | How to Use                                      |
|-------------------------------|-------------------------------------------------|
| CLI flag                      | `./pw.sh --headed -n 4`                         |
| CLI option (if supported)     | `./pw.sh --headed --workers=4`                  |
| Environment variable          | `export PLAYWRIGHT_WORKERS=4; ./pw.sh ...`      |
| pytest.ini (default for all)  | `[pytest]\naddopts = -n 3`                      |

---

## Webhook & API Integration for Reports

This project provides a FastAPI server for programmatic access to Playwright JSON reports and webhook integration. The server is started automatically by `pw.sh` after each test run.

### Access the JSON Report
- URL: `http://localhost:8000/report`
- Returns the latest Playwright JSON report (all results).
- To get only failures:
  - `http://localhost:8000/report?only_failures=true`

### Send the Report to a Webhook
- URL: `http://localhost:8000/send-report`
- Method: POST
- Content-Type: application/json
- Body example:
```json
{
  "webhook_url": "<YOUR_WEBHOOK_URL>",
  "message": "Playwright Test Report",
  "only_failures": false
}
```
- Example using curl:
```sh
curl -X POST "http://localhost:8000/send-report" \
  -H "Content-Type: application/json" \
  -d '{"webhook_url": "https://hooks.slack.com/services/XXX/YYY/ZZZ"}'
```
- The webhook will receive a JSON payload with the test results.

### Notes
- The FastAPI server runs on port 8000 by default (see `pw.sh`).
- Both the HTML report and FastAPI server are live after each run until you press a key to stop them.
- You can integrate with Slack, Teams, Discord, or any webhook-compatible service.

---

# Run in Firefox, headless, with trace and video recording, and 1 retry for failures
pytest e2e/ --browser=firefox --headless --retries=1 --trace=on --video=on --timeout=60000

# Run in Safari (WebKit)
pytest e2e/ --browser=webkit

# Run in Chrome (Chromium)
pytest e2e/ --browser=chromium

# Run with 4 parallel workers and screenshots on every failure
pytest e2e/ --workers=4 --screenshot=only-on-failure
```

### 3. Add or Update Test Data
- Place your CSV test data in the `data/` folder.
- Example: `data/sample_test_data.csv` with columns like `test_case_id`, `search_term`, etc.

### 4. Write or Update Tests
- Create new test scripts in the `e2e/` folder.
- Import and use page objects from `components/` for clean, maintainable tests.
- Use `CSVService` to drive data-driven tests.

### 5. Run the Tests
```bash
pytest e2e/
```
- Use CLI options to customize (e.g., `pytest e2e/ --browser=firefox --headless`)

### 6. Continuous Integration
- Tests run automatically on every push/PR via GitHub Actions.
- See `.github/workflows/playwright-tests.yml` for workflow details.

---

## Example: Data-Driven Test
```python

def test_search_with_csv_data(homepage, csv_service):
    test_data = csv_service.read_csv('sample_test_data.csv')
    home = HomePage(homepage)
    home.goto()
    for entry in test_data:
        home.search(entry['search_term'])
        # Add assertions based on entry['expected_result']
```

---

## License
MIT
