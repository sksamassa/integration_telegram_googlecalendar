import requests
import datetime 
import json
import re 
from dotenv import load_dotenv
import os

from scheduler import book_timeslot

# Load environment variables
load_dotenv() 
api_key = os.getenv("API_KEY")

def check_email(email):
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if(re.search(regex,email)):  
        print("Valid Email") 
        return True
    else:  
        print("Invalid Email")  
        return False

def getLastMessage():
    url = f"https://api.telegram.org/bot{api_key}/getUpdates"
    response = requests.get(url)
    data = response.json()
    last_msg = data['result'][-1]['message']['text']
    chat_id = data['result'][-1]['message']['chat']['id']
    update_id = data['result'][-1]['update_id']
    return last_msg, chat_id, update_id

def sendMessage(chat_id, text_message):
    url = f'https://api.telegram.org/bot{api_key}/sendMessage?text={text_message}&chat_id={chat_id}'
    response = requests.get(url)
    return response

def sendInlineMessageForService(chat_id):
    text_message = 'Hi! I\'m RemindoBot, your assistant.\n\n/start-to start chatting with the bot\n/cancel-to stop chatting with the bot.\n\nFor more information please contact sksamassa@gmail.com'
    keyboard = {'keyboard': [[{'text': 'Set Event'}]]}
    key = json.dumps(keyboard)
    url = f'https://api.telegram.org/bot{api_key}/sendmessage?chat_id={chat_id}&text={text_message}&reply_markup={key}'
    response = requests.get(url)
    return response

def run():
    update_id_for_booking_of_time_slot = ''
    prev_last_msg, chat_id, prev_update_id = getLastMessage()
    while True:
        current_last_msg, chat_id, current_update_id = getLastMessage()
        if prev_last_msg == current_last_msg and current_update_id == prev_update_id:
            print('continue')
            continue
        else:
            if current_last_msg == '/start':
                sendInlineMessageForService(chat_id)   
            if current_last_msg == 'Set Event':
                sendMessage(chat_id, "Please enter the event name and its date and time (e.g., 'Birthday 2024-05-20 14:00'):")
            if re.match(r'^\w+\s+\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}$', current_last_msg):
                event_description, event_datetime = current_last_msg.split(maxsplit=1)
                event_datetime = datetime.datetime.strptime(event_datetime, "%Y-%m-%d %H:%M")
                update_id_for_booking_of_time_slot = current_update_id
                sendMessage(chat_id, "Please enter your email address:")
            if check_email(current_last_msg):
                if update_id_for_booking_of_time_slot != current_update_id and update_id_for_booking_of_time_slot != '':
                    update_id_for_booking_of_time_slot = ''
                    booking_time = event_datetime.strftime("%H:%M")
                    booking_date = event_datetime.strftime("%Y-%m-%d")
                    response = book_timeslot(event_description, booking_time, current_last_msg, booking_date)
                    if response:
                        sendMessage(chat_id, f"Appointment is booked. See you at {booking_time}")
                    else:
                        sendMessage(chat_id, "Please try another timeslot and try again tomorrow")
        prev_last_msg = current_last_msg
        prev_update_id = current_update_id

if __name__ == "__main__":
    run()