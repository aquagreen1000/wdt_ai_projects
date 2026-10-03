import gradio as gr
from account_backend import AccountManager

# The UI is a thin demo layer over the real account logic. The backend handles
# validation, balances, holdings, and transaction history; Gradio simply exposes
# those operations as browser-friendly forms and tables.
manager = AccountManager()

# Define the color palette as hex strings
color_palette = {
    "primary": "#ecad0a",
    "secondary": "#209dd7",
    "tertiary": "#753991",
    "gray_light": "#e0e0e0",
    "gray_dark": "#505050"
}

# Helper to format success/failure message with color

def format_message(msg: str, success: bool) -> str:
    color = color_palette['primary'] if success else "#d9534f"  # red color for failure
    return f"<div style='color:{color}; font-weight: bold;'>{msg}</div>"


def create_account(username: str, initial_deposit: float):
    success, msg = manager.create_account(username.strip(), initial_deposit)
    return format_message(msg, success)


def deposit(username: str, amount: float):
    success, msg = manager.deposit(username.strip(), amount)
    return format_message(msg, success)


def withdraw(username: str, amount: float):
    success, msg = manager.withdraw(username.strip(), amount)
    return format_message(msg, success)


def buy_shares(username: str, symbol: str, quantity: int):
    symbol = symbol.strip().upper()
    success, msg = manager.buy_shares(username.strip(), symbol, quantity)
    return format_message(msg, success)


def sell_shares(username: str, symbol: str, quantity: int):
    symbol = symbol.strip().upper()
    success, msg = manager.sell_shares(username.strip(), symbol, quantity)
    return format_message(msg, success)


def show_portfolio(username: str):
    username = username.strip()
    if not username:
        return "<div style='color:#d9534f;font-weight:bold;'>Please enter a username.</div>", ""
    portfolio_val = manager.get_portfolio_value(username)
    profit_loss = manager.get_profit_loss(username)
    profit_loss_color = color_palette['primary'] if profit_loss >= 0 else "#d9534f"
    if username not in manager._users:
        return (f"<div style='color:#d9534f;font-weight:bold;'>User '{username}' not found.</div>", "")

    msg_html = (f"<div style='font-weight:bold; color:{color_palette['secondary']}'>"
                f"Portfolio Value: ${portfolio_val:.2f}</div>"
                f"<div style='font-weight:bold; color:{profit_loss_color}'>"
                f"Profit/Loss: ${profit_loss:.2f}</div>")
    return msg_html, ""


def show_holdings(username: str):
    username = username.strip()
    if username not in manager._users:
        return f"<div style='color:#d9534f; font-weight:bold;'>User '{username}' not found.</div>", None
    holdings = manager.get_holdings(username)
    if not holdings:
        return f"<div style='color:{color_palette['gray_dark']}; font-weight:bold;'>No holdings for user '{username}'.</div>", None
    import pandas as pd
    df = pd.DataFrame([{"Symbol": symbol, "Quantity": qty} for symbol, qty in holdings.items()])
    return f"<div style='color:{color_palette['secondary']}; font-weight:bold;'>Holdings for '{username}':</div>", df


def show_transactions(username: str):
    username = username.strip()
    if username not in manager._users:
        return f"<div style='color:#d9534f; font-weight:bold;'>User '{username}' not found.</div>", None
    history = manager.get_transaction_history(username)
    if not history:
        return f"<div style='color:{color_palette['gray_dark']}; font-weight:bold;'>No transactions found for user '{username}'.</div>", None
    import pandas as pd
    df = pd.DataFrame(history)
    # Show columns in order and readable format
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df[['timestamp', 'type', 'symbol', 'quantity', 'amount']]
    df.columns = ["Timestamp", "Type", "Symbol", "Quantity", "Amount"]
    return f"<div style='color:{color_palette['secondary']}; font-weight:bold;'>Transaction History for '{username}':</div>", df


with gr.Blocks() as app:
    gr.Markdown("# Trading Simulation Account Management System", elem_id="header")

    with gr.Tab("Create Account"):
        username_input = gr.Textbox(label="Username", placeholder="Enter username")
        initial_deposit_input = gr.Number(label="Initial Deposit", value=1000.0, precision=2)
        create_btn = gr.Button("Create Account", variant="primary")
        create_output = gr.HTML()
        create_btn.click(create_account, inputs=[username_input, initial_deposit_input], outputs=create_output)

    with gr.Tab("Deposit Funds"):
        username_deposit = gr.Textbox(label="Username", placeholder="Enter username")
        amount_deposit = gr.Number(label="Deposit Amount", value=100.0, precision=2)
        deposit_btn = gr.Button("Deposit", variant="primary")
        deposit_output = gr.HTML()
        deposit_btn.click(deposit, inputs=[username_deposit, amount_deposit], outputs=deposit_output)

    with gr.Tab("Withdraw Funds"):
        username_withdraw = gr.Textbox(label="Username", placeholder="Enter username")
        amount_withdraw = gr.Number(label="Withdrawal Amount", value=50.0, precision=2)
        withdraw_btn = gr.Button("Withdraw", variant="primary")
        withdraw_output = gr.HTML()
        withdraw_btn.click(withdraw, inputs=[username_withdraw, amount_withdraw], outputs=withdraw_output)

    with gr.Tab("Buy Shares"):
        username_buy = gr.Textbox(label="Username", placeholder="Enter username")
        symbol_buy = gr.Textbox(label="Stock Symbol", placeholder="Enter symbol e.g. AAPL")
        quantity_buy = gr.Number(label="Quantity", value=1, precision=0)
        buy_btn = gr.Button("Buy", variant="primary")
        buy_output = gr.HTML()
        buy_btn.click(buy_shares, inputs=[username_buy, symbol_buy, quantity_buy], outputs=buy_output)

    with gr.Tab("Sell Shares"):
        username_sell = gr.Textbox(label="Username", placeholder="Enter username")
        symbol_sell = gr.Textbox(label="Stock Symbol", placeholder="Enter symbol e.g. AAPL")
        quantity_sell = gr.Number(label="Quantity", value=1, precision=0)
        sell_btn = gr.Button("Sell", variant="primary")
        sell_output = gr.HTML()
        sell_btn.click(sell_shares, inputs=[username_sell, symbol_sell, quantity_sell], outputs=sell_output)

    with gr.Tab("Portfolio & Profit/Loss"):
        username_portfolio = gr.Textbox(label="Username", placeholder="Enter username")
        portfolio_btn = gr.Button("Show Portfolio")
        portfolio_msg = gr.HTML()
        portfolio_value = gr.Textbox(label="", interactive=False, visible=False)
        portfolio_btn.click(show_portfolio, inputs=username_portfolio, outputs=[portfolio_msg, portfolio_value])

    with gr.Tab("Holdings"):
        username_holdings = gr.Textbox(label="Username", placeholder="Enter username")
        holdings_btn = gr.Button("Show Holdings")
        holdings_msg = gr.HTML()
        holdings_table = gr.Dataframe(headers=None, datatype=["str", "number"], interactive=False)
        holdings_btn.click(show_holdings, inputs=username_holdings, outputs=[holdings_msg, holdings_table])

    with gr.Tab("Transactions"):
        username_transactions = gr.Textbox(label="Username", placeholder="Enter username")
        transactions_btn = gr.Button("Show Transactions")
        transactions_msg = gr.HTML()
        transactions_table = gr.Dataframe(headers=None, datatype=["str", "str", "str", "number", "number"], interactive=False)
        transactions_btn.click(show_transactions, inputs=username_transactions, outputs=[transactions_msg, transactions_table])


if __name__ == "__main__":
    app.launch()
