# tests/test_csvio.py

import unittest
import csv
from pathlib import Path

from budgetbuddy.data import csvio
from budgetbuddy.core.models import UserProfile, Income, Expense


class TestCsvIO(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Use a shared CSV path name (files created per test)
        cls.csv_path = Path("test_profile.csv")
        cls.invalid_csv_path = Path("test_invalid_amount.csv")

    @classmethod
    def tearDownClass(cls):
        # Clean up any CSV files left over
        if cls.csv_path.exists():
            cls.csv_path.unlink()
        if cls.invalid_csv_path.exists():
            cls.invalid_csv_path.unlink()

    def setUp(self):
        # Fresh profile for each test
        self.profile = UserProfile("janet")
        self.profile.add_transaction(
            Income("2025-01-01", 100.0, "Salary", "January pay")
        )
        self.profile.add_transaction(
            Expense("2025-01-02", 25.0, "Food", "Snacks")
        )

        # Ensure CSV files do not exist at the start of each test
        if self.csv_path.exists():
            self.csv_path.unlink()
        if self.invalid_csv_path.exists():
            self.invalid_csv_path.unlink()

    def tearDown(self):
        # Remove CSV files created by a test
        if self.csv_path.exists():
            self.csv_path.unlink()
        if self.invalid_csv_path.exists():
            self.invalid_csv_path.unlink()

    def test_export_profile_to_csv_creates_file_and_rows(self):
        """Exporting a profile should create a CSV with one row per transaction."""
        csvio.export_profile_to_csv(self.profile, self.csv_path)

        # File should exist
        self.assertTrue(self.csv_path.exists())

        # Read back the CSV and check content
        with self.csv_path.open("r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        # We added 2 transactions
        self.assertEqual(len(rows), 2)
        # Check that the first row matches the first transaction
        self.assertEqual(rows[0]["date"], "2025-01-01")
        self.assertEqual(float(rows[0]["amount"]), 100.0)
        self.assertEqual(rows[0]["category"], "Salary")
        self.assertEqual(rows[0]["type"].lower(), "income")

    def test_import_transactions_missing_file_does_not_crash(self):
        """
        Calling import_transactions_from_csv on a non-existent file
        should not crash and should not change the profile.
        """
        original_count = len(self.profile.transactions)

        missing_path = "this_file_does_not_exist.csv"

        # Ensure it does not raise and does not modify the profile
        csvio.import_transactions_from_csv(self.profile, missing_path)

        self.assertEqual(len(self.profile.transactions), original_count)
        self.assertEqual(self.profile.name, "janet")
        self.assertGreaterEqual(original_count, 2)
        self.assertTrue(all(tx.amount >= 0 for tx in self.profile.transactions))

    def test_import_transactions_skips_invalid_amount_row(self):
        """
        Rows with invalid amount values should be skipped and not added
        as transactions in the profile.
        """
        # Create a CSV with one invalid and one valid row
        with self.invalid_csv_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["date", "amount", "category", "description", "type"])
            writer.writerow(["2025-01-01", "not-a-number", "Food", "Bad row", "expense"])
            writer.writerow(["2025-01-02", "50.0", "Food", "Valid row", "expense"])

        original_count = len(self.profile.transactions)

        csvio.import_transactions_from_csv(self.profile, self.invalid_csv_path)

        # Only the valid row should be added
        self.assertEqual(len(self.profile.transactions), original_count + 1)
        last_tx = self.profile.transactions[-1]
        self.assertEqual(last_tx.amount, 50.0)
        self.assertEqual(last_tx.category, "Food")
        self.assertEqual(last_tx.description, "Valid row")


if __name__ == "__main__":
    unittest.main()
