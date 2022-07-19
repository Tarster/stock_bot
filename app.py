from urllib import response
from flask import Flask, request
from twilio.rest import Client
from marketstack import get_stock_price
import sys
paths = [r'C:\TCS\stock_bot\env']
sys.path.append(paths)
import apikey


app = Flask(__name__)

# fetch or replace with your own credentials
ACCOUNT_ID = apikey.TWILIO_ACCOUNT
TWILIO_TOKEN = apikey.TWILIO_TOKEN
TWILIO_NUMBER = apikey.TWILIO_NUMBER

client = Client(ACCOUNT_ID, TWILIO_TOKEN)


def process_message(message: str):
    response = ""
    if message == "Hi":
        response = "Hello, welcome to the stock market bot!"
        response += "Type 'sym:<stock_symbol>' to get the stock price."
    elif 'sym:' in message:
        data = message.split(":")[1]
        last_price = str(get_stock_price(data)["last_price"])
        if last_price.isnumeric():
            response = "The stock price of " + data +" is: $" + last_price
        else:
            response = last_price
    else:
        response = "Please type 'Hi' to get started"
    return response


def send_message(message:str, recipient:str):
    client.messages.create(to=recipient, body=message, from_=TWILIO_NUMBER)


@app.route("/")
def hello():
    return {"Result": "You successfully created the first route!"}


@app.route("/webhook", methods=["POST"])
def webhook():
    message = request.form['Body']
    sender = request.form['From']
    response = process_message(message)
    send_message(response , sender)
    return "OK", 200
