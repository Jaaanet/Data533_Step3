# tests/test_main.py

import io
import os
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from budgetbuddy.ui.main import BudgetBuddyApp
from budgetbuddy.core.models import UserProfile


class TestBudgetBuddyApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Ensure guide.txt exists in the same directory as main.py so
        show_guide() has something to print.
        """
        from budgetbuddy.ui import main as main_mod

        cls.ui_dir = os.path.dirname(main_mod.__file__)
        cls.guide_path = os.path.join(cls.ui_dir, "guide.txt")

        if not os.path.exists(cls.guide_path):
            with open(cls.guide_path, "w", encoding="utf-8") as f:
                f.write("=== BudgetBuddy Guide ===\nThis is a test guide.\n")

    @classmethod
    def tearDownClass(cls):
        # We leave guide.txt in place since the real app uses it.
        pass

    def setUp(self):
        # Patch load_profiles so __init__ doesn't touch disk
        patcher = patch("budgetbuddy.ui.main.repository.load_profiles", return_value={})
        self.mock_load = patcher.start()
        self.addCleanup(patcher.stop)

        self.app = BudgetBuddyApp()

    def tearDown(self):
        # Any per-test cleanup can go here (none needed now)
        pass

    def test_show_guide_prints_text(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            self.app.show_guide()
        out = buf.getvalue()

        self.assertIn("Guide", out)
        self.assertIn("BudgetBuddy", out)
        self.assertGreater(len(out.strip()), 0)
        self.assertNotIn("Guide file not found", out)

    def test_create_profile_flow_adds_profile(self):
        # Simulate typing "janet" and patch save_profiles so we don't write JSON
        with patch("builtins.input", side_effect=["janet"]), \
             patch("budgetbuddy.ui.main.repository.save_profiles") as mock_save:

            self.app.create_profile_flow()

        self.assertIn("janet", self.app.profiles)
        self.assertIsInstance(self.app.profiles["janet"], UserProfile)
        self.assertEqual(self.app.profiles["janet"].name, "janet")
        self.assertTrue(mock_save.called)

    def test_record_income_flow_valid_amount_adds_transaction(self):
        app = BudgetBuddyApp()
        profile = UserProfile("janet")

        # Simulate user input:
        # date, amount, category, description
        inputs = ["2025-01-01", "100.5", "Salary", "January pay"]
        with patch("builtins.input", side_effect=inputs), \
             patch("sys.stdout", new_callable=io.StringIO) as fake_out:

            app.record_income_flow(profile)

        # Check that a transaction was added
        self.assertEqual(len(profile.transactions), 1)
        tx = profile.transactions[0]
        self.assertEqual(tx.amount, 100.5)
        self.assertEqual(tx.category, "Salary")
        self.assertIn("Income recorded.", fake_out.getvalue())

    def test_record_income_flow_invalid_amount_shows_error_and_skips(self):
        app = BudgetBuddyApp()
        profile = UserProfile("janet")

        # Invalid amount "abc"
        inputs = ["2025-01-01", "abc"]
        # Note: after the invalid amount, the function returns early
        with patch("builtins.input", side_effect=inputs), \
             patch("sys.stdout", new_callable=io.StringIO) as fake_out:

            app.record_income_flow(profile)

        output = fake_out.getvalue()
        self.assertIn("not a valid number", output)
        self.assertEqual(len(profile.transactions), 0)

    def test_change_year_flow_invalid_year_keeps_current(self):
        app = BudgetBuddyApp()
        original_year = app.current_year

        # First input: printed current year (no input)
        # Second input: user types "abcd" (invalid)
        with patch("builtins.input", side_effect=["abcd"]), \
             patch("sys.stdout", new_callable=io.StringIO) as fake_out:

            app.change_year_flow()

        output = fake_out.getvalue()
        self.assertIn("Invalid year", output)
        # Year should not have changed
        self.assertEqual(app.current_year, original_year)


if __name__ == "__main__":
    unittest.main()
