# Pytest Commands Guide

This guide provides various useful commands for running the SV Students Recommend automation test suite using Pytest.

## Basic Execution

*   **Run all tests (API and UI):**
    ```bash
    pytest
    ```
    *Note: This will use the default configuration in `pytest.ini`.*

*   **Run a specific test file:**
    ```bash
    pytest tests/ui/test_auth_ui.py
    ```

*   **Run a specific test function inside a file:**
    ```bash
    pytest tests/api/test_auth_api.py::test_login_success
    ```

## Running Tests by Markers

Markers allow you to categorize tests (e.g., `sanity`, `regression`, `smoke`, `errors_handling`).

*   **Run only Sanity tests:**
    ```bash
    pytest -m sanity
    ```

*   **Run only Regression tests:**
    ```bash
    pytest -m regression
    ```

*   **Run tests that validate Error Handling:**
    ```bash
    pytest -m errors_handling
    ```

*   **Run all tests EXCEPT smoke tests:**
    ```bash
    pytest -m "not smoke"
    ```

## Playwright UI Specific Commands

*   **Run UI tests in Headed mode (visible browser):**
    ```bash
    pytest --headed
    ```
    
*   **Run tests in a specific browser (e.g., Firefox, WebKit):**
    ```bash
    pytest --browser firefox --browser webkit
    ```

*   **Slow down test execution (useful for debugging visually):**
    ```bash
    pytest --headed --slowmo 1000  # Slows down by 1000 milliseconds
    ```

## Advanced Execution & Reporting

*   **Run tests in parallel (Requires `pytest-xdist` plugin):**
    ```bash
    pytest -n 4  # Runs on 4 CPU cores
    pytest -n auto # Automatically detects and uses all available cores
    ```

*   **Stop execution after the first failure:**
    ```bash
    pytest -x
    ```

*   **Generate an HTML Report:**
    ```bash
    pytest --html=report.html --self-contained-html
    ```
    *The `pytest.ini` file in this project is already configured to automatically generate this report on every run.*

*   **Increase verbosity (see detailed test names and results):**
    ```bash
    pytest -v
    ```
    *This is also pre-configured in `pytest.ini`.*
