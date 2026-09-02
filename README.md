# pw-june30-python

Python port of the [pw-june30](../pw-june30) TypeScript Playwright course suite, using
[`tamash-playwright`](https://pypi.org/project/tamash-playwright/) for self-healing locators and
a step-by-step HTML report. 33 source files ported: 22 UI test files, 24 test functions total
(OrangeHRM flows, frames, alerts, shadow DOM, drag & drop, mouse actions, file uploads, POM,
custom fixtures, Excel-driven data-driven testing, network capture, route mocking) and 11 API
test files, 42 test functions total (Basic/OAuth2/Digest auth, Members CRUD, file upload, error
handling).

## Setup

```sh
python -m venv .venv
.venv\Scripts\pip install pytest pytest-playwright pytest-html python-dotenv openpyxl tamash-playwright
.venv\Scripts\python -m playwright install chromium
```

(`pyproject.toml` lists the same dependencies for reference — this project has no installable
package of its own, `pages`/`fixtures`/`DataUtils` are plain directories pytest resolves via its
own rootdir-based imports, so there's nothing to `pip install -e .` here.)

Copy `.env.example` to `.env` and fill in an AI provider key (see the
[`tamash-playwright` README](https://pypi.org/project/tamash-playwright/) for how to get a free
Ollama Cloud key — fastest way to get started). `APP_BASE_URL` and `API_BASE_URL` are already set
to sensible defaults.

## Project structure

```
pages/        Page Object Model classes (BasePage, LoginPage, DashboardPage, PIMPage,
              AddEmployeePage, PersonalDetailsPage) — port of pom/*.ts
fixtures/     pytest fixtures — port of fixtures/*.ts:
                base_fixtures.py      independent base_page/login_page/dashboard_page/
                                      user_credentials fixtures (port of basetest.ts)
                base_app_fixtures.py  grouped App/AppData SimpleNamespace fixtures, including
                                      Excel-driven test data (port of baseAppTest.ts)
DataUtils/    excel_data_util.py — openpyxl port of ExcelDataUtil.ts
testdata/     users.json — copied as-is from the TS suite
FileData/     demo.txt, employees.xlsx — copied as-is from the TS suite
tests/        22 UI tests (numbered to match their TS source file, e.g. test_10_* ports
              10HandlingElementsInFrame.spec.ts)
tests/api/    11 API tests (test_api_01_* .. test_api_11_*), using the api_request_context
              fixture — see "API tests" below
conftest.py   wires in tamash-playwright's self-healing `page` fixture, plus base_url/
              api_base_url/browser_type_launch_args
```

`tests/3PlaywrightAdvantagesAndArchitecture.spec.ts` and `tests/5xpathselector.spec.ts` were not
ported — both are pure comment/notes files in the TS source with no executable test.

## Running tests

```sh
# everything
.venv\Scripts\python -m pytest

# UI tests only
.venv\Scripts\python -m pytest tests/ --ignore=tests/api

# API tests only (needs the local API server — see below)
.venv\Scripts\python -m pytest tests/api

# a single file
.venv\Scripts\python -m pytest tests/test_17_pom_basic.py -s
```

Every run generates two complementary HTML reports (configured in `pyproject.toml`'s `addopts`,
no extra flags needed):

- **`tamash-report.html`** — the self-healing-aware step report: every Playwright action/
  assertion/fixture, in order, with duration, healed-selector detail (provider, tokens used,
  what it recovered to), and a screenshot on unrecovered failures. Shows *what Playwright did*.
- **`report.html`** (pytest-html) — the standard pytest report, including the full traceback and
  value diff for any failed `assert` (e.g. `assert 3 == 999`). Shows *why an assertion failed*.

These two are intentionally complementary, not redundant — see "Why some checks use plain
`assert`" below for why a single report can't cover both jobs.

## API tests

`tests/api/` needs a local API server running at `http://localhost:5002` (override via
`API_BASE_URL` in `.env`). These tests use the `api_request_context` fixture — a
`tamash-playwright`-wrapped, standalone `APIRequestContext` (no browser at all). It's named
`api_request_context` rather than TS Playwright Test's `request`: pytest already has its own
built-in `request` fixture (test/fixture introspection metadata, a completely different thing),
and pytest-playwright's Python package — unlike its TS counterpart — doesn't ship any
request-context fixture of its own to override.

This server persists data across runs. Every test that creates a "Member" uses a per-run unique
name (either a millisecond timestamp or random letters, depending on the file) rather than the
TS original's fixed names — without that, a second run hits a 409 Conflict from the previous
run's leftover data. Names must be letters-only (spaces are fine, digits are not): this server's
own validation rejects a numeric suffix with `"Name should only contain Alphabets"`, discovered
by testing it directly.

## Why some checks use plain `assert`

Every UI assertion uses `tamash_playwright.expect()` (a drop-in for `playwright.sync_api.expect()`
that also records the check as a report step). API test assertions are a mix, and it's
principled, not inconsistent:

- `expect(response).to_be_ok()` is used wherever a check only cares "did this succeed" — it's
  real, documented Playwright API (`APIResponseAssertions` has exactly `to_be_ok()` /
  `not_to_be_ok()`), so it shows up in `tamash-report.html` like any other assertion.
- Plain `assert` is used wherever a check needs a *specific* value: an exact status code
  (`APIResponseAssertions` has no exact-code matcher — `to_be_ok()` would silently accept a
  regression from 404 to 403), or a JSON body field / header / response text (plain Python
  values, not a `Locator`/`Page`/`APIResponse`, so `expect()` rejects them outright —
  `playwright.sync_api.expect('hello')` raises `ValueError: Unsupported type`).

This is a real Python-vs-TypeScript API difference, not a style choice: TS's `expect()` is Jest's
general-purpose assertion library with Playwright matchers layered on top, so it accepts *any*
value. Python's `expect()` is narrowly typed to `Locator`/`Page`/`APIResponse` only. Two of the 93
`assert` statements in this suite are in a UI test (`test_11_alert_handling.py`, checking
`dialog.message` — `Dialog` isn't one of those three types either); the rest are in `tests/api/`.

`tamash-playwright` deliberately never closes this gap with a custom assertion helper (e.g.
`assert_that(x, y)`) — that would force test code to deviate from standard Playwright/Python just
to get report coverage, which is out of scope for what this package is for (healing + reporting
via standard Playwright APIs only, nothing invented).

## Other known, deliberate deviations from the TS source

- `test_07_apsrtc_get_ac_bus_count.py` keeps the TS original's hardcoded `"July 24"` date as-is —
  a real, inherited fragility (this will fail once that date picker entry stops existing) rather
  than something this port introduced.
- `test_21_mock_response.py` omits the TS original's trailing `page.pause()` — that opens the
  interactive Playwright Inspector and blocks forever waiting for a human, which would hang any
  automated run.
- `.first` / `.last` don't get healing or reporting (a `tamash-playwright` limitation, not
  specific to this suite): they're Python properties, not method calls, so there's no way to
  patch the `Locator` they return without globally patching Playwright's own `Locator` class.
  `test_14_mouse_actions.py`'s hover test uses `.nth(0)` instead for exactly this reason — same
  result, and a real method call that gets full healing and reporting.
