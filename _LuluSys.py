import os
import time
import datetime
from datetime import date
from datetime import datetime
from datetime import timedelta

import selenium
from selenium import webdriver
from datetime import datetime
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

import wolframalpha
import urllib.parse

from dotenv import load_dotenv
load_dotenv()

SID = os.getenv('SID')
AUTH = os.getenv('AUTH')
PHONE = os.getenv('PHONE')
ADMIN = os.getenv('ADMIN')


def sendMsg(msg, number):
    client = Client(SID, AUTH)
    message = client.messages \
        .create(
             body=msg,
             from_=PHONE,
             to=number
         )

from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

sendMsg('Initialized!', ADMIN)

@app.route('/lulu', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    incoming_number = request.form['From']
    msg = resp.message()
    responded = False

    if 'wolfram mode' not in incoming_msg and wolframmode == 1:
        question = incoming_msg
        wolframapi = os.getenv('WOLFRAMAPI')
        client = wolframalpha.Client(wolframapi)
        res = client.query(question)
        try:
            txtmsg = next(res.results).text
        except StopIteration:
            txtmsg = "Invalid input."

        msg.body(txtmsg)
        responded = True

    elif 'wolfram mode' in incoming_msg and wolframmode == 1:
        global wolframmode
        wolframmode = 1
        txtmsg = "Wolfram Mode enabled."
        msg.body(txtmsg)
        responded = True

    elif 'wolfram mode' in incoming_msg and wolframmode == 0:
        global wolframmode
        wolframmode = 1
        txtmsg = "Wolfram Mode enabled."
        msg.body(txtmsg)
        responded = True

    elif 'wolfram full' in incoming_msg and responded==False:
    	question = incoming_msg.replace('wolfram full', '')
    	parsed = urllib.parse.quote_plus(question)
    	wolframapi = os.getenv('WOLFRAMAPI')
    	url = 'http://api.wolframalpha.com/v1/simple?appid=' + wolframapi + '&i=' + parsed + '&layout=labelbar&background=283044&foreground=white&timeout=30'

    	imagef = ("image/png", "image/jpeg", "image/jpg", "image/gif")
    	r = requests.head(url)
    	if r.headers["content-type"] in imagef:
            txtmsg = url
            msg.media(url)
            responded = True
    	else:
            txtmsg = "Invalid input."
            msg.body(txtmsg)
            responded = True


    elif 'wolfram long' in incoming_msg and responded==False:
    	question = incoming_msg.replace('wolfram full', '')
    	parsed = urllib.parse.quote_plus(question)
    	wolframapi = os.getenv('WOLFRAMAPI')
    	url = 'http://api.wolframalpha.com/v1/simple?appid=' + wolframapi + '&i=' + parsed + '&layout=labelbar&background=283044&foreground=white&timeout=30'

    	imagef = ("image/png", "image/jpeg", "image/jpg", "image/gif")
    	r = requests.head(url)
    	if r.headers["content-type"] in imagef:
            txtmsg = url
            msg.media(url)
            responded = True
    	else:
            txtmsg = "Invalid input."
            msg.body(txtmsg)
            responded = True


    elif 'wolfram' in incoming_msg and responded==False:
        question = incoming_msg.replace('wolfram', '')
        wolframapi = os.getenv('WOLFRAMAPI')
        client = wolframalpha.Client(wolframapi)
        res = client.query(question)
        try:
            txtmsg = next(res.results).text
        except StopIteration:
            txtmsg = "Invalid input."

        msg.body(txtmsg)
        responded = True

    elif 'bills' in incoming_msg and responded==False:
        today = date.today()
        day = int(today.strftime("%-d"))
        month = int(today.strftime("%-m"))
        year = int(today.strftime("%Y"))

        def automonthly(name, subday, pos, cost):
            subyear = year
            submonth = month

            if month == 2:
                if day >= subday:
                    submonth = month + 1
                elif subday >= 29:
                    tempday = subday
                    subday = 28
                    if day >= subday:
                        submonth = month + 1
                        subday = tempday

            elif month == 1:
                if day >= subday:
                    submonth = month + 1
                    if subday >= 29:
                        subday = 28

            elif day >= subday:
                submonth = month + 1
                if submonth > 12:
                    subyear = year + 1
                    submonth = 1

            subdate = date(subyear, submonth, subday)
            subin = int((subdate - today).total_seconds() / 86400)
            subinw = str(int(subin / 7)) + "|" + str(subin % 7)
            subhum = subdate.strftime("%b %d")

            if pos:
                sign = "+"
            else:
                sign = "-"

            if subin < payday_in:
                upcoming = "*"
            else:
                upcoming = ""

            return subinw + upcoming + " " + name + " (" + sign + "$" + cost + ") on " + subhum

        def autoyearly(name, subday, submonth, pos, cost):
            if month == submonth:
                if day >= subday:
                    subyear = year + 1
                else:
                    subyear = year
            elif month > submonth:
                subyear = year + 1
            else:
                subyear = year

            subdate = date(subyear, submonth, subday)
            subin = int((subdate - today).total_seconds() / 86400)

            subinm = int(subin / 30)
            subinw = (subin - (30 * subinm)) / 7
            subind = (subinw * 7) % 7

            subint = str(subinm) + "|" + str(int(subinw)) + "|" + str(int(subind))
            subhum = subdate.strftime("%b %d")

            if pos:
                sign = "+"
            else:
                sign = "-"

            if subin < payday_in:
                upcoming = "*"
            else:
                upcoming = ""

            return subint + upcoming + " " + name + " (" + sign + "$" + cost + ") on " + subhum

        payday_old = date(2022, 2, 25)
        payday_in = int(14 - ((today - payday_old).total_seconds() / 86400) % 14)
        payday_inw = str(int(payday_in / 7)) + "|" + str(payday_in % 7)
        payday_date = today + timedelta(days=payday_in)
        payday_hum = payday_date.strftime("%b %d")
        payday = payday_inw + " Payday (SCP) on " + payday_hum

        mompay = automonthly("MomPay", 30, True, "50.25")
        madpay = automonthly("MadPay", 3, True, "35")
        friendspoty = autoyearly("FriendSpoty", 31, 12, True, "205")
        parentsvpn = autoyearly("ParentVPN", 24, 1, True, "50")

        iphonepay = automonthly("iPhone", 8, False, "49.91")
        tmobilepay = automonthly("T-Mobile", 7, False, "110.35")
        spotifypay = automonthly("Spotify", 30, False, "17.11")
        icloudpay = automonthly("iCloud", 23, False, "9.99")

        expressvpnpay = autoyearly("ExpVPN", 24, 1, False, "99.95")
        ccpay = autoyearly("AdobeCC", 26, 12, False, "239.88")

        nyuapp = autoyearly("NYU App", 1, 11, True, "CommonApp and Tisch and Diversity")
        journpay = automonthly("JournPay", 1, True, "200")

        txtmsg = ("Here are all of your future income sources and bills.\n\n"
            + "INCOME \n"
            + payday
            + "\n\n"
            + mompay + "\n"
            + madpay + "\n\n"
            + friendspoty + "\n"
            + parentsvpn + "\n\n"
            + "\n~~~~~~~~~~~~~~~~~~~~~"
            + "\n\n"
            + "BILLS \n"
            + iphonepay + "\n"
            + tmobilepay + "\n"
            + spotifypay + "\n"
            + icloudpay + "\n"
            + "\n\n"
            + expressvpnpay + "\n"
            + ccpay + "\n\n"
            + "\n~~~~~~~~~~~~~~~~~~~~~"
            + "\n\n"
            + "TODO \n"
            + journpay + "\n"
            + nyuapp
            )

        msg.body(txtmsg)
        responded = True

    elif 'cat' in incoming_msg and responded==False:
        msg.media('https://cataas.com/cat')
        responded = True

    elif 'the code' in incoming_msg and responded==False and incoming_number != '+18435134441' and incoming_number != '+18435808363':
    	SCREENTIMECODE = os.getenv('SCREENTIMECODE')
    	txtmsg = 'The code is ' + SCREENTIMECODE + '. But if this is Dillon then fuck off.'
    	msg.body(txtmsg)
    	responded = True

    elif 'the code' in incoming_msg and responded==False and incoming_number == '+18435134441':
    	txtmsg = 'Fuck you dillon'
    	msg.body(txtmsg)
    	responded = True

    elif 'time' in incoming_msg and responded==False:
        today = datetime.now()
        txtmsg = today.strftime("%c")
        msg.body(txtmsg)
        responded = True

    elif 'idea' in incoming_msg and responded==False:
    	txtmsg = 'Want to add more things? How about life360 (https://www.home-assistant.io/integrations/life360/#:~:text=From%20the%20configuration%20menu%20select,to%20complete%20the%20set%20up.), DEPLOY TO PRODUCTION (https://flask.palletsprojects.com/en/2.2.x/tutorial/deploy) texting other people, calling myself, setting up an HTTP get request to my website, phone number profiles, push to github, auto update with keyword, update code through texting (like bills, maybe with a database https://pythonbasics.org/flask-sqlalchemy/#:~:text=Step%201%20%2D%20Install%20the%20Flask%2DSQLAlchemy%20extension.&text=Step%202%20%2D%20You%20need%20to,SQLAlchemy%20class%20from%20this%20module.&text=Step%203%20%2D%20Now%20create%20a,for%20the%20database%20to%20use.&text=Step%204%20%2D%20then%20use%20the,an%20object%20of%20class%20SQLAlchemy.), and a phone extension!'
    	msg.body(txtmsg)
    	responded = True

    elif 'lulu' in incoming_msg and responded==False:
    	txtmsg = "Current version v0.4 \n Hi! I'm a bot that was made by Dillon originally for checking banking info, but now way more!!"
    	msg.body(txtmsg)
    	responded = True

    elif not responded:
        msg.body('Invalid input. I can respond to prompts that include "bills", "time", "the code", "lulu", "idea", "wolfram", "*wolfram mode", "wolfram long" or "wolfram full", and "cat".')
    return str(resp)


if __name__ == '__main__':
    app.run()
