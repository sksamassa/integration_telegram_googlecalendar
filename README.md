# Integration of Google Calendar and Telegram
This repository contains a Python script that integrates Google Calendar with a Telegram bot, allowing users to schedule events directly from their Telegram chats.

## Features
**Google Calendar Integration:** Users can schedule events by interacting with the Telegram bot, and the events are automatically added to their Google Calendar.
**Interactive Bot:** The Telegram bot provides a user-friendly interface for setting event details such as title, date, time, and description.
**Error Handling:** The system handles errors gracefully and provides feedback to users in case of invalid inputs or scheduling conflicts.

## Prerequisites
Before running the script, ensure you have the following prerequisites installed:
* Python 3.x
* Required Python libraries:
  * **google-api-python-client**
  * **google-auth**
  * **google-auth-oauthlib**
  * **google-auth-httplib2**
  * **requests**
* Telegram Bot API key
* Google Calendar API credentials (client ID and client secret)

## Setup
**1. Clone the Repository:**
`git clone https://github.com/your_username/google-calendar-telegram-bot.git`
**2. Install Dependencies:**
`pip install -r requirements.txt`
**3. Set Up Google Calendar API:**
* Enable the **Google Calendar API** for your Google account.
* Create **OAuth 2.0** credentials (client ID and client secret) and download the JSON file containing these credentials.
* Save the JSON file as **credentials.json** in the root directory of the repository.

## Set Environment Variables(optional):
* Create a **.env** file in the root directory.
* Define the **API_KEY** variable with your Telegram bot API key.

## Usage
**1. Run the Bot:**
`python main.py`
**2. Start Chatting:**
* Search for your bot's username on Telegram and start a chat.
* Use the `/start` command to initiate the conversation with the bot.
**3. `Set Event`:**
* Send the Set Event command to the bot to schedule a new event.
* Follow the prompts to enter the event details, including *title*, *date*, *time*, and *description*.
**4. Confirmation:**
Once the event is successfully booked, you will receive a confirmation message with the event details and a link to the event in your Google Calendar.

## License
This project is licensed under the **MIT License**. Feel free to modify and distribute it as needed.
