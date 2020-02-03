import requests
from datetime import datetime
from dotenv import load_dotenv
import os

#Open the .env file in the directory and get the secret for IFTTT
project_folder = os.path.expanduser('~/IPchanges')
load_dotenv(os.path.join(project_folder, '.env'))
SECRET_KEY = os.getenv('IFTTT_SECRET')

#Convert current time and date to what we want it to be
now = datetime.now()
script_time = now.strftime("%d/%m/%Y %H:%M:%S")

#Sending the POST to IFTTT
def webhook_ifttt(new_ip, old_ip, date_time):

    headers={
        "Content-Type": "application/json"
    }
    body={
        "value1": new_ip,
        "value2": old_ip,
        "value3": date_time
    }
    trigger = requests.post('https://maker.ifttt.com/trigger/ip_changed/with/key/{}'.format(SECRET_KEY), json=body, headers=headers)

    return trigger

#Getting the IP adress from ipify.org
live_ip = requests.get("https://api.ipify.org").text

#Open the current_ip.txt file and check if the saved IP is different from the one we got from ipify
if os.path.exists("current_ip.txt"):
    with open("current_ip.txt", "r+") as f:
        stored_ip = f.read()
        f.seek(0)
        if stored_ip:
            if stored_ip != live_ip:
                webhook_ifttt(live_ip, stored_ip, script_time)
                f.write(live_ip)
                f.truncate()
        else:
            f.write(live_ip)
else:
    f = open("current_ip.txt", "w")
    f.write(live_ip)


f.close()

