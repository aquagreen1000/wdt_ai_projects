from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Transaction:
    timestamp: datetime
    type: str  # "deposit", "withdrawal", "buy", "sell"
    symbol: Optional[str]
    quantity: Optional[int]
    amount: float


class UserAccount:
    def __init__(self, username: str, initial_deposit: float):
        self.username = username
        self.cash_balance = initial_deposit
        self.initial_deposit = initial_deposit
        self.holdings: Dict[str, int] = {}
        self.transactions: List[Transaction] = []


# Test implementation for get_share_price
# Returns fixed prices for AAPL, TSLA, GOOGL, raises ValueError for unknown symbol

def get_share_price(symbol: str) -> float:
    prices = {
        "AAPL": 150.0,
        "TSLA": 700.0,
        "GOOGL": 2800.0
    }
    if symbol not in prices:
        raise ValueError(f"Unknown share symbol: {symbol}")
    return prices[symbol]


class AccountManager:
    def __init__(self):
        self._users: Dict[str, UserAccount] = {}

    def create_account(self, username: str, initial_deposit: float) -> Tuple[bool, str]:
        if username in self._users:
            return False, f"Account creation failed: username '{username}' already exists."
        if initial_deposit < 0:
            return False, "Initial deposit must not be negative."
        user = UserAccount(username, initial_deposit)
        user.transactions.append(Transaction(
            timestamp=datetime.now(),
            type="deposit",
            symbol=None,
            quantity=None,
            amount=initial_deposit
        ))
        self._users[username] = user
        return True, f"Account created successfully for user '{username}' with initial deposit ${initial_deposit:.2f}."

    def deposit(self, username: str, amount: float) -> Tuple[bool, str]:
        user = self._users.get(username)
        if not user:
            return False, f"Deposit failed: user '{username}' not found."
        if amount <= 0:
            return False, "Deposit amount must be positive."
        user.cash_balance += amount
        user.transactions.append(Transaction(
            timestamp=datetime.now(),
            type="deposit",
            symbol=None,
            quantity=None,
            amount=amount
        ))
        return True, f"Deposit of ${amount:.2f} successful. New balance: ${user.cash_balance:.2f}."

    def withdraw(self, username: str, amount: float) -> Tuple[bool, str]:
        user = self._users.get(username)
        if not user:
            return False, f"Withdrawal failed: user '{username}' not found."
        if amount <= 0:
            return False, "Withdrawal amount must be positive."
        if user.cash_balance < amount:
            return False, f"Withdrawal failed: insufficient funds. Current balance: ${user.cash_balance:.2f}."
        user.cash_balance -= amount
        user.transactions.append(Transaction(
            timestamp=datetime.now(),
            type="withdrawal",
            symbol=None,
            quantity=None,
            amount=amount
        ))
        return True, f"Withdrawal of ${amount:.2f} successful. New balance: ${user.cash_balance:.2f}."

    def buy_shares(self, username: str, symbol: str, quantity: int) -> Tuple[bool, str]:
        if quantity <= 0:
            return False, "Quantity to buy must be positive."
        user = self._users.get(username)
        if not user:
            return False, f"Buy failed: user '{username}' not found."
        try:
            price_per_share = get_share_price(symbol)
        except ValueError as e:
            return False, str(e)
        total_cost = price_per_share * quantity
        if user.cash_balance < total_cost:
            return False, f"Buy failed: insufficient funds. Required ${total_cost:.2f}, available ${user.cash_balance:.2f}."
        user.cash_balance -= total_cost
        user.holdings[symbol] = user.holdings.get(symbol, 0) + quantity
        user.transactions.append(Transaction(
            timestamp=datetime.now(),
            type="buy",
            symbol=symbol,
            quantity=quantity,
            amount=total_cost
        ))
        return True, f"Bought {quantity} shares of {symbol} at ${price_per_share:.2f} each for a total of ${total_cost:.2f}."

    def sell_shares(self, username: str, symbol: str, quantity: int) -> Tuple[bool, str]:
        if quantity <= 0:
            return False, "Quantity to sell must be positive."
        user = self._users.get(username)
        if not user:
            return False, f"Sell failed: user '{username}' not found."
        owned_quantity = user.holdings.get(symbol, 0)
        if owned_quantity < quantity:
            return False, f"Sell failed: insufficient shares. Owned {owned_quantity}, trying to sell {quantity}."
        try:
            price_per_share = get_share_price(symbol)
        except ValueError as e:
            return False, str(e)
        total_revenue = price_per_share * quantity
        user.cash_balance += total_revenue
        user.holdings[symbol] = owned_quantity - quantity
        if user.holdings[symbol] == 0:
            del user.holdings[symbol]
        user.transactions.append(Transaction(
            timestamp=datetime.now(),
            type="sell",
            symbol=symbol,
            quantity=quantity,
            amount=total_revenue
        ))
        return True, f"Sold {quantity} shares of {symbol} at ${price_per_share:.2f} each for a total of ${total_revenue:.2f}."

    def get_portfolio_value(self, username: str) -> float:
        user = self._users.get(username)
        if not user:
            return 0.0
        total_value = user.cash_balance
        for symbol, qty in user.holdings.items():
            try:
                price = get_share_price(symbol)
                total_value += price * qty
            except ValueError:
                # Ignore missing prices
                pass
        return total_value

    def get_profit_loss(self, username: str) -> float:
        user = self._users.get(username)
        if not user:
            return 0.0
        portfolio_value = self.get_portfolio_value(username)
        return portfolio_value - user.initial_deposit

    def get_holdings(self, username: str) -> Dict[str, int]:
        user = self._users.get(username)
        if not user:
            return {}
        return dict(user.holdings)

    def get_transaction_history(self, username: str) -> List[Dict[str, Any]]:
        user = self._users.get(username)
        if not user:
            return []
        history = []
        for t in user.transactions:
            history.append({
                "timestamp": t.timestamp.isoformat(),
                "type": t.type,
                "symbol": t.symbol,
                "quantity": t.quantity,
                "amount": t.amount
            })
        return history
