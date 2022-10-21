import os
from twilio.rest import Client

from dotenv import load_dotenv

load_dotenv()
SID = os.getenv('SID')
AUTH = os.getenv('AUTH')
PHONE = os.getenv('PHONE')
ADMIN = os.getenv('ADMIN')

client = Client(SID, AUTH)

msg = input("Enter your text message to admin: ")

message = client.messages \
    .create(
         body=msg
         from_=PHONE,
         to=ADMIN
     )
