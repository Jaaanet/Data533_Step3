# # %%
# import unittest
# from budgetbuddy.core.models import UserProfile, Income, Expense

# class TestUserProfile(unittest.TestCase):
#     @classmethod
#     def setUpClass(cls):
#         cls.tx1 = Income("2025-12-02", 1000, "job")
#         cls.tx2 = Expense("2025-12-08", 25, "lunch")
#         cls.tx3 = Expense("2025-12-13", 600, "christmas shopping")
#         cls.tx4 = Income("2025-12-16", 1500, "job")

#     @classmethod
#     def tearDownClass(cls):
#         pass

#     def setUp(self):
#         self.user = UserProfile("Rachel")
#         self.user.add_transactions(self.tx1)
#         self.user.add_transactions(self.tx2)
#         self.user.add_transactions(self.tx3)
#         self.user.add_transactions(self.tx4)

#     def tearDown(self):
#         pass

# #first test case
#     def test_list_transactions(self):
#         txs = self.user.list_transactions()
#         #assertions
#         self.assertEqual(len(txs), 4)
#         self.assertGreater(txs[1].amount, 100)
#         self.assertIs(txs[3], self.tx4)
#         self.assertTrue(txs[0].category == "job")

# #second test case
#     def test_recent_transactions(self):
#         recent = self.user.recent_transactions(12, 2025, 3)
#         #assertions
#         self.assertEqual(len(recent), 3)
#         self.assertNotIn(self.tx1, recent)
#         self.assertLess(recent[2].amount, 1500)
#         self.assertIs(recent[-1], self.tx4)


# unittest.main(argv=[''], verbosity=2, exit=False)

# tests/test_models.py

import unittest

from budgetbuddy.core.models import UserProfile, Income, Expense


class TestUserProfile(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        # Create a profile with a known set of transactions
        self.profile = UserProfile("janet")

        self.t1 = Income("2025-01-01", 500.0, "Salary", "January pay")
        self.t2 = Expense("2025-01-05", 25.0, "Food", "Snacks")
        self.t3 = Income("2025-02-10", 1500.0, "Salary", "Bonus")
        self.t4 = Expense("2025-03-01", 60.0, "Transport", "Bus pass")

        for tx in [self.t1, self.t2, self.t3, self.t4]:
            self.profile.add_transaction(tx)

    def tearDown(self):
        pass

    def test_list_transactions(self):
        txs = self.profile.list_transactions()

        self.assertEqual(len(txs), 4)
        self.assertIn(self.t1, txs)
        self.assertIn(self.t2, txs)
        self.assertIn(self.t3, txs)
        self.assertIn(self.t4, txs)

    # def test_recent_transactions(self):
    #     recent = self.profile.recent_transactions(3)

    #     self.assertLessEqual(len(recent), 3)
    #     for tx in recent:
    #         self.assertIn(tx, self.profile.transactions)

    #     amounts = [tx.amount for tx in recent]
    #     self.assertTrue(all(a >= 0 for a in amounts))
    #     self.assertTrue(500.0 in amounts or 1500.0 in amounts)

    ## the updated methods from above
    def test_recent_transactions(self):
        """recent_transactions(month, year, n) returns at most n records from that year/month."""
        # Call with explicit month, year, n
        recent = self.profile.recent_transactions(1, 2025, 3)

        # At most 3 transactions are returned
        self.assertLessEqual(len(recent), 3)

        # All are from this profile
        for tx in recent:
            self.assertIn(tx, self.profile.transactions)

        # Amounts are all non-negative
        amounts = [tx.amount for tx in recent]
        self.assertTrue(all(a >= 0 for a in amounts))

        # At least one of our known transactions from Jan 2025 appears
        self.assertTrue(any(tx.date.startswith("2025-01") for tx in recent))


if __name__ == "__main__":
    unittest.main()
