import imaplib
import os
import email

from dotenv import load_dotenv
from email.header import decode_header

from app.filters import is_trusted_sender
from app.telegram_client import send_telegram_alert

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")
IMAP_SERVER = os.getenv("IMAP_SERVER")
IMAP_PORT = int(os.getenv("IMAP_PORT"))


def connect_to_mailbox():
    print("SERVER:", IMAP_SERVER)
    print("PORT:", IMAP_PORT)
    print("EMAIL:", EMAIL_ADDRESS)

    mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)

    mail.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

    mail.select("inbox", readonly=True)

    return mail


def decode_mime_words(text):
    if not text:
        return ""

    decoded_parts = decode_header(text)

    decoded_string = ""

    for part, encoding in decoded_parts:

        if isinstance(part, bytes):

            decoded_string += part.decode(
                encoding or "utf-8",
                errors="ignore"
            )

        else:
            decoded_string += part

    return decoded_string


def fetch_unread_emails(mail):

    status, messages = mail.search(None, "UNSEEN")

    email_ids = messages[0].split()

    latest_email_ids = email_ids[-5:]

    for email_id in latest_email_ids:

        status, msg_data = mail.fetch(email_id, "(RFC822)")

        raw_email = msg_data[0][1]

        msg = email.message_from_bytes(raw_email)

        sender = decode_mime_words(msg["From"])

        subject = decode_mime_words(msg["Subject"])


        if not is_trusted_sender(sender):

            print("Skipped untrusted sender:", sender)

            continue

        body = ""

        if msg.is_multipart():

            for part in msg.walk():

                content_type = part.get_content_type()

                if content_type == "text/plain":

                    payload = part.get_payload(decode=True)

                    if payload:

                        body = payload.decode(
                            errors="ignore"
                        )

                        break

        else:

            payload = msg.get_payload(decode=True)

            if payload:

                body = payload.decode(
                    errors="ignore"
                )

        print("---------------")
        print("FROM:", sender)
        print("SUBJECT:", subject)
        print("BODY:", body[:200])

        message = f"""
🔥 NEW EMAIL ALERT 🔥

👤 Sender:
{sender}

📌 Subject:
{subject}

💬 Message:
{body[:200]}

━━━━━━━━━━━━━━
🤖 Email Monitoring Bot
"""

        send_telegram_alert(message)


def close_connection(mail):

    mail.logout()


if __name__ == "__main__":

    mail = connect_to_mailbox()

    fetch_unread_emails(mail)

    close_connection(mail)