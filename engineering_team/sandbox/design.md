# Detailed Design for Trading Simulation Account Management System

---

## Overview

This system will provide the functionalities of user account management, handling deposits and withdrawals of funds, buying and selling shares with quantity constraints, portfolio valuation, transaction history reporting, and validation against invalid operations (negative balances etc). The system will also use a provided `get_share_price(symbol)` function to get current prices of shares. The UI will display operation results with clear messages and success/failure status, implemented using Gradio version 6.

---

## Modules & Responsibilities

- `account_backend.py` — **Backend module**  
  Implements the core logic for accounts, transactions, validations, portfolio calculations.

- `app_frontend.py` — **Frontend module**  
  Implements Gradio UI showing forms and outputs for interactions, uses backend functions.

- `test_backend.py` — **Unit tests module**  
  Implements `unittest` tests covering all backend functionalities, checks correctness and validation.

---

# Module: `account_backend.py`

### Classes

#### 1. `AccountManager`

Manages accounts and user operations.

- **Attributes:**
  - `_users: Dict[str, UserAccount]` — dictionary mapping username to UserAccount instance.

- **Methods:**

```python
def create_account(self, username: str, initial_deposit: float) -> Tuple[bool, str]
```
Create new user account with initial deposit. Return (success, message).

```python
def deposit(self, username: str, amount: float) -> Tuple[bool, str]
```
Deposit funds into user account.

```python
def withdraw(self, username: str, amount: float) -> Tuple[bool, str]
```
Withdraw funds from user account, fail if insufficient funds.

```python
def buy_shares(self, username: str, symbol: str, quantity: int) -> Tuple[bool, str]
```
Record purchase of shares, fail if insufficient funds to cover cost.

```python
def sell_shares(self, username: str, symbol: str, quantity: int) -> Tuple[bool, str]
```
Record sale of shares, fail if not enough shares owned.

```python
def get_portfolio_value(self, username: str) -> float
```
Calculate total current portfolio value (cash + shares at current price).

```python
def get_profit_loss(self, username: str) -> float
```
Calculate profit or loss relative to initial deposit.

```python
def get_holdings(self, username: str) -> Dict[str, int]
```
Return current holdings by symbol and quantity.

```python
def get_transaction_history(self, username: str) -> List[Dict[str, Any]]
```
Return list of user's transactions with details (type, symbol, quantity, amount, time).

---

#### 2. `UserAccount`

Represents individual user account storing balances and transactions.

- **Attributes:**
  - `username: str`
  - `cash_balance: float`
  - `initial_deposit: float`
  - `holdings: Dict[str, int]` — shares owned by symbol
  - `transactions: List[Transaction]`

- **No public methods exposed directly; managed via AccountManager**

---

#### 3. `Transaction`

Data class representing a transaction.

- **Attributes:**
  - `timestamp: datetime`
  - `type: str` — "deposit", "withdrawal", "buy", "sell"
  - `symbol: Optional[str]`
  - `quantity: Optional[int]`
  - `amount: float`

---

### Function Signature for Provided API

```python
def get_share_price(symbol: str) -> float
```

- Returns current price for symbol.
- Test implementation returns fixed prices for "AAPL", "TSLA", "GOOGL".

---

# Module: `app_frontend.py`

### Responsibilities

- Implement UI forms and display for:
  - Create account
  - Deposit funds
  - Withdraw funds
  - Buy shares
  - Sell shares
  - Show portfolio value and profit/loss
  - Show holdings
  - Show transaction history

- Display success/failure messages with status after actions.

- Use Gradio 6.x APIs.

---

### Components to Implement

- Initialization of `AccountManager` instance.

- Gradio Interface(s):

```python
def create_account_ui() -> gr.Interface
```
Form for username and initial deposit, submits to backend.

```python
def deposit_ui() -> gr.Interface
```
Form for username and deposit amount.

```python
def withdraw_ui() -> gr.Interface
```
Form for username and withdraw amount.

```python
def buy_ui() -> gr.Interface
```
Form for username, symbol, quantity.

```python
def sell_ui() -> gr.Interface
```
Form for username, symbol, quantity.

```python
def portfolio_ui() -> gr.Interface
```
Display portfolio value and profit/loss for username.

```python
def holdings_ui() -> gr.Interface
```
Display current holdings for username.

```python
def transactions_ui() -> gr.Interface
```
Display transaction history for username.

---

### Gradio 6 Guidance

- Use the updated `gr.Interface` or `gr.Blocks` construct depending on the UI layout.

- Define inputs with `gr.Textbox()`, `gr.Number()`, `gr.Dropdown()`, etc.

- For outputs, use `gr.Textbox()`, `gr.Dataframe()`, or `gr.Label()`.

- Use explicit `submit` buttons with `.click()` event to connect UI inputs to backend functions.

- Backend functions should return a tuple `(message: str, status: bool)` where the status controls UI display (e.g., color or icon for success/failure).

- No global state outside the `AccountManager` instance.

---

# Module: `test_backend.py`

### Responsibilities

- Use Python `unittest` module.

- Test cases to cover:

  - Account creation success and failure (e.g. duplicate usernames).

  - Deposits and withdrawals, including invalid withdrawals (overdraft).

  - Buying shares with enough and insufficient funds.

  - Selling shares with enough and insufficient stock.

  - Portfolio value calculation correctness.

  - Profit/Loss correctness.

  - Holdings correctness after transactions.

  - Transaction history correctness and completeness.

- Use mocking or test fixed prices in `get_share_price`.

---

### Example Test Case Functions Signatures

```python
def test_create_account_success(self) -> None
def test_create_account_duplicate(self) -> None
def test_deposit_and_withdraw_success(self) -> None
def test_withdraw_insufficient_funds(self) -> None
def test_buy_shares_sufficient_funds(self) -> None
def test_buy_shares_insufficient_funds(self) -> None
def test_sell_shares_sufficient(self) -> None
def test_sell_shares_insufficient(self) -> None
def test_portfolio_value_calculation(self) -> None
def test_profit_loss_calculation(self) -> None
def test_holdings_update(self) -> None
def test_transaction_history(self) -> None
```

---

# Assignment of Work

| Engineer          | Responsibilities                                     | Deliverables                                  |
|-------------------|-----------------------------------------------------|-----------------------------------------------|
| **backend_engineer** | Implement `account_backend.py` with all classes and backend logic. Implement `get_share_price` stub as described. | Complete backend module with all class and method signatures, backend logic. |
| **frontend_engineer** | Implement `app_frontend.py` with the Gradio 6 UI as described.    | Gradio app with all user interface forms and displays, wired to backend. |
| **test_engineer**    | Implement `test_backend.py` using unittest covering all backend functionality and edge cases. | Comprehensive unit tests covering backend including validations and calculations.|

---

# Summary

- **Backend module**: AccountManager main class holding user data and logic (create, deposit, withdraw, buy, sell, get portfolio, profit/loss, holdings, transactions). 
- **Frontend module**: Gradio 6 UI with forms per action, reports result messages + success/failure visually.
- **Test module**: unittest tests verifying core functionality and edge cases.
- Clear interaction boundaries; all code in same directory.
- No external dependencies beyond gradio and standard library.
- Use backend Python code purely for logic; frontend focuses on UI with results reporting.

This design fully meets the requirements and provides a clear path for implementation by the three engineers.