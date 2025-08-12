"""Playwright configuration for library card workflow tests."""

# Playwright configuration for library card workflow
config = {
    "testDir": "./tests",
    "timeout": 30000,  # 30 seconds per test
    "expect": {"timeout": 5000},  # 5 seconds for assertions
    "fullyParallel": False,  # Don't run tests in parallel (they share services)
    "forbidOnly": True,  # Fail if test.only is left in code
    "retries": 1,  # Retry failed tests once
    "workers": 1,  # Single worker to avoid port conflicts
    "reporter": [["list"], ["html"]],
    "use": {
        "baseURL": "http://localhost:8000",
        "trace": "on-first-retry",
        "screenshot": "only-on-failure",
    },
    "projects": [
        {
            "name": "chromium",
            "use": {"browserName": "chromium"},
        }
    ],
}