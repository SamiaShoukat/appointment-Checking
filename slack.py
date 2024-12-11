import logging
logging.basicConfig(level=logging.DEBUG)

import os
import time
import ssl
from dotenv import load_dotenv

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

load_dotenv()

slack_token = os.environ['SLACK_TOKEN']
context = ssl._create_unverified_context()
DEFAULT_APPOINTMENT_OPEN_MSG = """ APPOINTMENT OPEN !!!! \n\n BOOK NOW : https://service2.diplo.de/rktermin/extern/appointment_showForm.do?locationCode=isla&realmId=108&categoryId=1600"""

class SlackNotificationError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

def send_message(channel,message):
    try:
        client = WebClient(token=slack_token, ssl=context)
        client.chat_postMessage(
            channel=channel,
            text=message
        )
    except SlackApiError as e:
        logging.error("Slack API Error: %s - Channel: %s, Message: %s", e, channel, message)
        raise SlackNotificationError('Sending message failed') from e 

def send_appointment_notification(message = DEFAULT_APPOINTMENT_OPEN_MSG):
    try:
        channel = os.environ['SLACK_APPOINTMENT_NOTIFIER_CHANNEL']
        send_message(channel,message)
    except Exception as e:
        logging.error("Sending appointment notification failed: %s", e)
        raise SlackNotificationError('Sending appointment notification failed')

def send_health_check(iterations = 0, latest_options = []):
    try:
        channel = os.environ['SLACK_HEALTH_CHECK_CHANNEL']
        message = f"Health Update \n Iterations : {iterations} \n Latest Options : {latest_options}"
        send_appointment_notification(f"HC : {iterations}")
        send_message(channel,message)
    except Exception as e:
        logging.error("Sending health check failed: %s", e)
        raise SlackNotificationError('Sending health check failed')

def cold_start_notification(latest_options):
    try:
        send_appointment_notification(message="cold start check")
        send_health_check(iterations=0, latest_options=latest_options)
    except SlackNotificationError as e:
        print(e)
        raise 


if __name__ == "__main__":
    #cold_start_notification(["option1","option2"])
    #send_appointment_notification()
    send_health_check()