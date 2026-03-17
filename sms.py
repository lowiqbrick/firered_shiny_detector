import os
from twilio.rest import Client


class SMSSender:
    def __init__(self):
        self.account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
        self.auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
        self.from_address = os.environ.get("TWILIO_NUMBER")
        self.to_address = os.environ.get("MY_NUMBER")
        self.client = Client(self.account_sid, self.auth_token)

    def send(self, message: str):
        self.client.messages.create(
            body=message, from_=self.from_address, to=self.to_address
        )


if __name__ == "__main__":
    # costs cuple cents
    sender = SMSSender()
    sender.send("message from me to me")
