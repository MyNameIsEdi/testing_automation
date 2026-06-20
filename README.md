
<div align="center">

# 🏢 SV Students Recommend - QA Automation

**A robust, production-grade test automation framework utilizing Playwright and Pytest to validate End-to-End (E2E) UI flows and REST APIs.**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org)
[![Playwright](https://img.shields.io/badge/Playwright-45ba4b?style=flat-square&logo=playwright&logoColor=white)](https://playwright.dev/python/)
[![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?style=flat-square&logo=pytest&logoColor=white)](https://docs.pytest.org/en/latest/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![CI](https://img.shields.io/badge/CI-GitHub_Actions-2088FF?style=flat-square&logo=github-actions&logoColor=white)](https://github.com/features/actions)

<br/>

![Project Screenshot](assets/screenshots/playwright-report-preview.png)

</div>

---

## What is this project?

This repository contains the complete quality assurance suite for the **SV Students Recommend** platform. It is designed to simulate real user interactions and validate backend logic simultaneously. 

The framework is built on **Playwright for Python**, leveraging its native auto-waiting capabilities to eliminate flaky tests. It utilizes the **Page Object Model (POM)** architecture for maximum code reuse and integrates tightly with `pytest` for streamlined execution, rich HTML reporting, and CI/CD readiness.

---

## ✨ Features

|      | Feature                           | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| ---- | --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 🎭 | **E2E UI Testing**                | Full user journey coverage simulating clicks, form submissions, and layout validations using Playwright's role-based locators. |
| 📡 | **REST API Testing**              | Direct backend validation testing CRUD operations and endpoint security using Bearer token authentication. |
| 🏛️ | **Page Object Model**             | Clean, maintainable architecture separating page interactions from test logic for scaling the test suite easily. |
| 🐛 | **Advanced Debugging**            | Auto-generates detailed HTML reports and trace viewers (DOM snapshots, network requests) automatically on test failures. |
| 🔄 | **Auth State Reuse**              | Captures and reuses login states across tests to bypass repetitive authentication, vastly speeding up test execution. |

---

## 🔗 Production & Demo Accounts

The application being tested is live. You can explore the system or run tests against the live environment.

* **Live Web App:** [https://sv-students-recommend.onrender.com/](https://sv-students-recommend.onrender.com/)
* **API Swagger Docs:** [https://sv-students-recommend.onrender.com/docs](https://sv-students-recommend.onrender.com/docs)

**Pre-configured Demo Credentials:**
| Role | Email | Password |
| --- | --- | --- |
| Admin | `hagai@svcollege.co.il` | `test1234` |
| Standard User | `student@example.com` | `test1234` |

*(Note: Automated registration tests should use dynamic emails, e.g., `test_<random>@example.com`, to prevent data collisions)*.

---

## 🚀 Quick Start (Local Setup)

To run the automation framework on your local machine:

1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   cd <project_directory>
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   playwright install  # Installs required browser binaries
   ```
3. **Environment Setup:**
   Copy the `.env.example` file to `.env` and fill in your API URLs and credentials (ensure `.env` is ignored in Git).

---

## 🧪 Running the Tests

The test suite uses `pytest` and `pytest-playwright` fixtures to manage browser contexts seamlessly. Ensure your local or remote server is up before executing.

* **Run the entire suite:**
  ```bash
  pytest
  ```
* **Run tests in headed mode (watch the browser visibly):**
  ```bash
  pytest --headed --slowmo 1000
  ```
* **Run only the sanity suite:**
  ```bash
  pytest -m sanity
  ```
* **Generate and view an HTML report:**
  ```bash
  pytest --html=report.html
  ```

---

## 🛠️ Team Workflow & Branching

To maintain a clean and stable codebase, our team adheres to a lightweight feature-branch workflow:

* **Protected Main Branch:** The `main` branch is always stable. No direct commits are allowed.
* **Feature Branches:** Create a short-lived branch for every new task using the format `feature/<task-name>` or `bugfix/<issue>`.
* **Atomic Commits:** Keep commits small and focused on one logical change.
* **Pull Requests (PRs):** Open a PR for review. At least one teammate must approve the code before it can be merged.
* **Merge Strategy:** We use **Squash & Merge** to maintain a clean Git history, automatically deleting the branch afterward.
