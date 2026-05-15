import os

from dotenv import load_dotenv

load_dotenv()

trusted_senders = os.getenv(
    "TRUSTED_SENDERS",
    ""
).split(",")


def is_trusted_sender(sender):

    for trusted in trusted_senders:

        if trusted.strip() in sender:

            return True

    return False