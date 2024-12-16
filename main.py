import datetime
import os
import time
import checker
import mailer
import slack
from seleniumbase import Driver
from dotenv import load_dotenv

load_dotenv()
LAST_EMAIL = datetime.datetime.now()

data = []
iteration = 1
latest_options = []

def init_request(driver):
    global latest_options
    global data

    timestamp = datetime.datetime.now()
    error, result, options = checker.check(driver)
    status = ''
    if error:
        status = 'error'
    elif result:
        status = 'active'
    else:
        status = 'inactive'
    data.append({'status': status, 'timestamp': timestamp})
    latest_options = options

def take_action():
    global EMAIL_AFTER
    global LAST_EMAIL
    global data
    global iteration
    global latest_options

    try:
        status = data[-1]['status']
        if status != 'inactive':
            if status == 'active':
                print('Appointment Open !')
                slack.send_appointment_notification()
                # mailer.send_mail()
            elif status == 'error':
                print('Error Occured in Checker')
                slack.send_appointment_notification(message= "Health Check: Waiting for the opening")
                # mailer.send_mail('ERROR : checker.py Failure', 'Something went wrong in the checker.py. Kindly check!')
        elif datetime.datetime.now() > LAST_EMAIL + datetime.timedelta(minutes=int(os.environ.get('EMAIL_AFTER_MIN'))):
            print('Sending Health Check')
            slack.send_health_check(iteration,latest_options)
            data = []
            LAST_EMAIL = datetime.datetime.now()

    except Exception as e :
        print(f"Error Occured in Sending Message {e}")
        try:
            slack.send_appointment_notification(message= "ERROR : Sending Slack Notification Failed")
        except Exception as e :
            print("Error - Take Action")
            # mailer.send_mail('ERROR : Critical Failure', 'Something went wrong . HURRY CHECK !!!')

def cold_start_checks():
    slack.cold_start_notification(latest_options=latest_options)
    # mailer.send_mail(subject='COLD START EMAIL CHECK !',contents='Testing if the email sender is working correctly')

def main():
    i = 1
    global iteration
    driver = Driver(uc=True, incognito=True, headless=True)
    while True:
        print('Cycle ' + str(i) + ':', datetime.datetime.now())
        init_request(driver)
        take_action()
        if i == 1:
            cold_start_checks()
        time.sleep(int(os.environ.get('CHECK_AFTER_SEC')))
        i += 1
        iteration += 1

if __name__ == '__main__':
    main()