# Data533_Step3 - BudgetBuddy: Integration Testing & Continuous Integration (CI/CD)
Here is the integration test for our budgetbuddy project step3

This repository contains the **Step 3 deliverables** for the BudgetBuddy project.  
In this stage, we implemented:

- **Exception and error handling** throughout the data and UI modules  
- **A complete suite of unit tests** for every function  
- **Continuous Integration (CI)** using GitHub Actions  
- **Coverage reporting** via `coverage.py` to ensure at least **75% coverage**

This README documents the setup, testing process, CI workflow, and coverage results.

---

## Project Structure



BudgetBuddy Step 3/  
|  
|-- budgetbuddy/  
|   | -- core/  
|   | -- data/  
|   |-- ui/  
|  
|-- tests/  
|   |-- test_budget.py  
|   |-- test_csvio.py  
|   |-- test_repository.py  
|   |-- test_models.py  
|   |-- test_summary.py  
|   |-- test_main.py  
|  
|-- .github/workflows/python-tests.yml     ← GitHub Actions CI workflow  
|-- coverageSummary.txt                    ← Coverage results  
|-- README.md  




---

## 1 Exception & Error Handling

For Step 3, multiple functions across the project were extended with **robust exception handling**.

### Six methods with exception handling

| Module | Method | Exception Type | Purpose |
|--------|--------|----------------|---------|
| `csvio.py` | `import_transactions_from_csv()` | `FileNotFoundError` | Handles missing CSV file |
| `csvio.py` | `import_transactions_from_csv()` | `ValueError` | Handles malformed numeric fields |
| `repository.py` | `load_profiles()` | **`ProfileDataError` (user-defined)** | Raised for corrupted JSON |
| `repository.py` | `save_profiles()` | `IOError` | Handles file write issues |
| `ui/main.py` | `_open_profile_flow()` | `KeyError` | Invalid profile selection |
| `ui/main.py` | `_input_amount()` | `ValueError` | Non-numeric input |

### User-defined exception

```python
class ProfileDataError(Exception):
    """Raised when profile JSON data is corrupted or unreadable."""
```

## 2 Unit Testing & Test Suite
All modules are thoroughly tested in the tests/ subpackage.

Run all tests:
```
python -m unittest discover -s tests -p "test_*.py"
```

## 3 Coverage (coverage.py)

We use coverage.py to measure test coverage.
```
coverage run -m unittest discover -s tests -p "test_*.py"
coverage report
```

A full report is in the `coverageSummary.txt` file.
