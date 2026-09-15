from __future__ import annotations

import smtplib
from email.message import EmailMessage
from pathlib import Path

from .config import EMAIL_ADDRESS, EMAIL_APP_PASSWORD, EMAIL_SMTP_SERVER, USE_EMAIL


def send_email(subject: str, text_body: str, html_body: str) -> None:
    if not (EMAIL_ADDRESS and EMAIL_SMTP_SERVER and EMAIL_APP_PASSWORD):
        raise RuntimeError(
            "Email configuration is incomplete. Set EMAIL_ADDRESS, EMAIL_SMTP_SERVER, and EMAIL_APP_PASSWORD."
        )

    msg = EmailMessage()
    print(f"Sending email to {EMAIL_ADDRESS} with subject: {subject}")
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = EMAIL_ADDRESS
    msg["Subject"] = subject
    msg.set_content(text_body)
    msg.add_alternative(html_body, subtype="html")

    with smtplib.SMTP(EMAIL_SMTP_SERVER, 587) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_APP_PASSWORD)
        server.send_message(msg)


def send_message(subject: str, text_body: str, html_body: str) -> None:
    if USE_EMAIL:
        print(f"Sending email with subject: {subject} because USE_EMAIL is True")
        send_email(subject, text_body, html_body)
        return

    print(f"Writing message to test_message.txt with subject: {subject} because USE_EMAIL is False")
    output_path = Path("test_message.txt")
    output_path.write_text(
        f"From: {EMAIL_ADDRESS}\n"
        f"To: {EMAIL_ADDRESS}\n"
        f"Subject: {subject}\n"
        f"Body:\n{text_body}\n",
        encoding="utf-8",
    )


def write_html_output(filename: str, content: str, output_dir: str = "output") -> None:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    (output_path / filename).write_text(f"<html><body>{content}</body></html>", encoding="utf-8")
