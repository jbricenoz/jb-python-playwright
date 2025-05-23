# Playwright Python Automation Framework

This repository contains a robust, modular Playwright automation framework for the Magento e-commerce demo site, built with Python and Pytest for reliable end-to-end testing.

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

## Project Structure

```
.
├── .github/                     # GitHub Actions workflows and templates
│   └── workflows/
│       └── playwright-crossbrowser.yml  # CI/CD pipeline configuration
├── components/                  # Page Object Models (POM) organized by feature
│   ├── checkout/               # Checkout related page objects
│   │   └── checkout_page.py
│   ├── home/                    # Home page components
│   │   ├── header_content.py
│   │   ├── homepage.py
│   │   ├── nav_sections.py
│   │   └── panel_navbar.py
│   ├── orders/                  # Orders related page objects
│   │   └── orders_returns.py
│   └── product/                 # Product related page objects
│       └── product_page.py
├── data/                        # Test data files
│   └── sample_test_data.csv     # Sample test data in CSV format
├── e2e/                         # End-to-end test cases
│   ├── test_cart_management.py
│   ├── test_checkout_flow.py
│   ├── test_homepage.py
│   ├── test_homepage_elements.py
│   └── test_orders_returns.py
├── fixtures/                    # Pytest fixtures
│   └── pw_fixture.py           # Playwright browser and context fixtures
├── reports/                     # Test execution reports
│   ├── playwright_report.html
│   └── playwright_report.json
├── service/                     # Service modules
│   ├── csv_service.py          # CSV data handling
│   ├── email_service.py        # Email notifications
│   └── webhook_reporter.py     # Webhook reporting
├── tests/                       # Test data and test cases
│   ├── bugs.csv
│   └── tests.csv
├── .gitignore
├── CHANGELOG.md
├── LICENSE
├── playwright.config.py         # Playwright configuration
├── pw.sh                       # Helper script for running tests
├── pytest.ini                  # Pytest configuration
└── requirements.txt            # Python dependencies
```

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

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git (for version control)
- Node.js (required for Playwright)

### 1. Clone the Repository

```bash
git clone https://github.com/jbricenoz/jb-python-playwright.git
cd jb-python-playwright
```

### 2. Set Up Python Virtual Environment

```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

### 3. Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install Python dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install

# Install Playwright dependencies
playwright install-deps
```

### 4. Verify Installation

```bash
# Check Python version
python --version

# Check pip version
pip --version

# Verify Playwright installation
playwright --version
```

## Running Tests

### Basic Test Execution

Run all tests:
```bash
./pw.sh
```

Run tests in headed mode (visible browser):
```bash
./pw.sh --headed
```

Run tests in a specific browser:
```bash
./pw.sh --browser=firefox  # or chromium, webkit
```

### Running Specific Tests

Run a single test file:
```bash
pytest e2e/test_homepage.py -v
```

Run tests with a specific marker:
```bash
pytest -m smoke -v
```

Run tests matching a specific pattern:
```bash
pytest -k "test_search" -v
```

### Test Reports

HTML and JSON reports are automatically generated in the `reports/` directory after each test run.

To view the HTML report:
```bash
open reports/playwright_report.html  # On macOS
# or
start reports/playwright_report.html  # On Windows
```

## Advanced Configuration

### Environment Variables

You can customize test execution using environment variables:

```bash
# Set base URL for tests
export BASE_URL="https://example.com"

# Run in headless mode
export HEADLESS="true"

# Set browser (chromium, firefox, webkit)
export BROWSER="firefox"

# Set timeout (ms)
export PLAYWRIGHT_TIMEOUT=30000

# Set number of parallel workers
export PLAYWRIGHT_WORKERS=4
```

### Playwright Configuration

Edit `playwright.config.py` to modify default settings:

```python
# Browser configuration
browser = {
    'browser': os.getenv('BROWSER', 'chromium'),
    'headless': os.getenv('HEADLESS', 'true').lower() == 'true',
    'slow_mo': int(os.getenv('PLAYWRIGHT_SLOWMO', '0')),
}

# Test configuration
test_config = {
    'base_url': os.getenv('BASE_URL', 'https://example.com'),
    'timeout': int(os.getenv('PLAYWRIGHT_TIMEOUT', '30000')),
    'retries': int(os.getenv('PLAYWRIGHT_RETRIES', '1')),
}

# Reporting configuration
reporting = {
    'trace': os.getenv('PLAYWRIGHT_TRACE', 'retain-on-failure'),
    'video': os.getenv('PLAYWRIGHT_VIDEO', 'retain-on-failure'),
    'screenshot': os.getenv('PLAYWRIGHT_SCREENSHOT', 'only-on-failure'),
}
```

## Parallel Test Execution

Run tests in parallel using pytest-xdist:

```bash
# Run tests with 4 parallel workers
./pw.sh -n 4

# Run tests in parallel with specific browser and headed mode
./pw.sh --browser=firefox --headed -n 3
```

Set the number of workers using environment variable:
```bash
export PLAYWRIGHT_WORKERS=4
./pw.sh
```

## Troubleshooting

### Common Issues

1. **Browser not found**
   ```
   Error: Browser not found. Did you install the browser?
   ```
   Solution: Run `playwright install` to install all required browsers.

2. **Missing dependencies**
   ```
   OSError: [Errno 8] Exec format error
   ```
   Solution: Make sure you have all system dependencies installed. On Ubuntu/Debian:
   ```bash
   sudo apt-get install -y libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libpango-1.0-0 libcairo2 libasound2 libatspi2.0-0
   ```

3. **Slow test execution**
   - Run in headless mode for faster execution
   - Reduce the number of parallel workers if system resources are limited
   - Use `--workers auto` to automatically detect the optimal number of workers

4. **Test failures**
   - Run with `--headed` to see the browser UI
   - Enable video recording with `--video on`
   - Capture trace with `--trace on`
   - Check the HTML report for detailed failure information

## CI/CD Integration

This project includes a GitHub Actions workflow (`.github/workflows/playwright-crossbrowser.yml`) that runs tests on push and pull requests. The workflow:

1. Sets up Python and Node.js
2. Installs dependencies
3. Runs tests across multiple browsers
4. Uploads test artifacts (reports, traces, videos)
5. Fails the build if tests fail

To customize the workflow, edit the YAML file in `.github/workflows/`.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
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
