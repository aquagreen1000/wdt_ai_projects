import unittest
from account_backend import AccountManager

class TestAccountManager(unittest.TestCase):
    def setUp(self):
        self.am = AccountManager()

    def test_create_account_success(self):
        success, msg = self.am.create_account("user1", 1000)
        self.assertTrue(success)
        self.assertIn("Account created successfully", msg)

    def test_create_account_duplicate(self):
        self.am.create_account("user1", 1000)
        success, msg = self.am.create_account("user1", 500)
        self.assertFalse(success)
        self.assertIn("already exists", msg)

    def test_create_account_negative_deposit(self):
        success, msg = self.am.create_account("user2", -100)
        self.assertFalse(success)
        self.assertIn("must not be negative", msg)

    def test_deposit_and_withdraw_success(self):
        self.am.create_account("user1", 1000)
        success, msg = self.am.deposit("user1", 500)
        self.assertTrue(success)
        self.assertIn("Deposit of $500.00 successful", msg)

        success, msg = self.am.withdraw("user1", 200)
        self.assertTrue(success)
        self.assertIn("Withdrawal of $200.00 successful", msg)

    def test_deposit_invalid_user(self):
        success, msg = self.am.deposit("nouser", 100)
        self.assertFalse(success)
        self.assertIn("user 'nouser' not found", msg)

    def test_deposit_negative_amount(self):
        self.am.create_account("user1", 1000)
        success, msg = self.am.deposit("user1", -10)
        self.assertFalse(success)
        self.assertIn("Deposit amount must be positive", msg)

    def test_withdraw_insufficient_funds(self):
        self.am.create_account("user1", 100)
        success, msg = self.am.withdraw("user1", 200)
        self.assertFalse(success)
        self.assertIn("insufficient funds", msg)

    def test_withdraw_invalid_user(self):
        success, msg = self.am.withdraw("nouser", 100)
        self.assertFalse(success)
        self.assertIn("user 'nouser' not found", msg)

    def test_withdraw_negative_amount(self):
        self.am.create_account("user1", 1000)
        success, msg = self.am.withdraw("user1", -10)
        self.assertFalse(success)
        self.assertIn("Withdrawal amount must be positive", msg)

    def test_buy_shares_sufficient_funds(self):
        self.am.create_account("user1", 2000)
        success, msg = self.am.buy_shares("user1", "AAPL", 5)
        self.assertTrue(success)
        self.assertIn("Bought 5 shares of AAPL", msg)

    def test_buy_shares_insufficient_funds(self):
        self.am.create_account("user1", 100)
        success, msg = self.am.buy_shares("user1", "AAPL", 5)
        self.assertFalse(success)
        self.assertIn("insufficient funds", msg)

    def test_buy_shares_invalid_user(self):
        success, msg = self.am.buy_shares("nouser", "AAPL", 5)
        self.assertFalse(success)
        self.assertIn("user 'nouser' not found", msg)

    def test_buy_shares_unknown_symbol(self):
        self.am.create_account("user1", 1000)
        success, msg = self.am.buy_shares("user1", "XYZ", 5)
        self.assertFalse(success)
        self.assertIn("Unknown share symbol", msg)

    def test_buy_shares_invalid_quantity(self):
        self.am.create_account("user1", 1000)
        success, msg = self.am.buy_shares("user1", "AAPL", 0)
        self.assertFalse(success)
        self.assertIn("must be positive", msg)

    def test_sell_shares_sufficient(self):
        self.am.create_account("user1", 2000)
        self.am.buy_shares("user1", "AAPL", 5)
        success, msg = self.am.sell_shares("user1", "AAPL", 3)
        self.assertTrue(success)
        self.assertIn("Sold 3 shares of AAPL", msg)

    def test_sell_shares_insufficient(self):
        self.am.create_account("user1", 2000)
        self.am.buy_shares("user1", "AAPL", 1)
        success, msg = self.am.sell_shares("user1", "AAPL", 5)
        self.assertFalse(success)
        self.assertIn("insufficient shares", msg)

    def test_sell_shares_invalid_user(self):
        success, msg = self.am.sell_shares("nouser", "AAPL", 1)
        self.assertFalse(success)
        self.assertIn("user 'nouser' not found", msg)

    def test_sell_shares_unknown_symbol(self):
        self.am.create_account("user1", 2000)
        self.am.buy_shares("user1", "AAPL", 5)
        # manually add an unknown holding to simulate
        self.am._users["user1"].holdings["XYZ"] = 1
        success, msg = self.am.sell_shares("user1", "XYZ", 1)
        self.assertFalse(success)
        self.assertIn("Unknown share symbol", msg)

    def test_sell_shares_invalid_quantity(self):
        self.am.create_account("user1", 2000)
        self.am.buy_shares("user1", "AAPL", 5)
        success, msg = self.am.sell_shares("user1", "AAPL", 0)
        self.assertFalse(success)
        self.assertIn("must be positive", msg)

    def test_portfolio_value_calculation(self):
        self.am.create_account("user1", 1000)
        self.am.buy_shares("user1", "AAPL", 2)  # 2*150=300
        value = self.am.get_portfolio_value("user1")
        expected = (1000 - 300) + (2*150)  # cash + holdings
        self.assertAlmostEqual(value, expected)

    def test_profit_loss_calculation(self):
        self.am.create_account("user1", 1000)
        self.am.buy_shares("user1", "AAPL", 2)  # spent 300
        profit_loss = self.am.get_profit_loss("user1")
        expected_profit_loss = self.am.get_portfolio_value("user1") - 1000
        self.assertAlmostEqual(profit_loss, expected_profit_loss)

    def test_holdings_update(self):
        self.am.create_account("user1", 1000)
        self.am.buy_shares("user1", "AAPL", 3)
        self.am.buy_shares("user1", "TSLA", 1)
        holdings = self.am.get_holdings("user1")
        self.assertEqual(holdings.get("AAPL"), 3)
        self.assertEqual(holdings.get("TSLA"), 1)
        self.am.sell_shares("user1", "AAPL", 2)
        holdings_after = self.am.get_holdings("user1")
        self.assertEqual(holdings_after.get("AAPL"), 1)

    def test_transaction_history(self):
        self.am.create_account("user1", 1000)
        self.am.deposit("user1", 500)
        self.am.withdraw("user1", 200)
        self.am.buy_shares("user1", "AAPL", 2)
        self.am.sell_shares("user1", "AAPL", 1)
        history = self.am.get_transaction_history("user1")
        self.assertTrue(len(history) >= 5)  # At least 5 transactions
        types = [t["type"] for t in history]
        self.assertIn("deposit", types)
        self.assertIn("withdrawal", types)
        self.assertIn("buy", types)
        self.assertIn("sell", types)

if __name__ == '__main__':
    unittest.main()
