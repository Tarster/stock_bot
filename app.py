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

def is_number_digit(number:str):
    if number is None:
        return False
    try:
        if number.isdigit():
            return True
        else:
            number_list= number.split(".")
    except Exception as _:
        return False
    
    if len(number_list) == 2 and number_list[0].isdigit() and number_list[1].isdigit():
        return True
    else:
        return False


def process_message(message: str):
    response = ""
    if message == "Hi":
        response = "Hello, welcome to the stock market bot!"
        response += "Type 'sym:<stock_symbol>' to get the stock price."
    elif 'sym:' in message.lower():
        data = message.split(":")[1]
        last_price = str(get_stock_price(data.upper())["last_price"])
        if is_number_digit(last_price):
            response = "The stock price of " + data.upper() +" is: $" + last_price
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
