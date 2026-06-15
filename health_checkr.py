#Health Checker - monitors URLs and post alerts to Teams
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from datetime import datetime

targets = [
    {"name": "Google", "url": "https://www.google.com"},
    {"name": "GitHub", "url": "https://www.github.com"},
    {"name": "Fake Website", "url": "https://fakefakefakefakewebsite.com"}
]
WEBHOOK_URL = "https://cebupacificairph.webhook.office.com/webhookb2/2b14a23f-23f5-41a6-9e4a-d63939fab78c@fab3949d-3cb0-4097-802f-053ad7075219/IncomingWebhook/3a7d4b16a86241699bf049f1634ffdf4/5b208123-43c0-466b-81a4-13522b75b69f/V225GKWIbpi1QxsPK-TYX6Bdws4TrkS-1TulbokVh4qW01"
SLOW_THRESHOLD = 2.0


def send_teams_message(message):
    payload = {"text": message}
    requests.post(WEBHOOK_URL, json=payload, verify=False)


def check_target(target):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        response = requests.get(target["url"], verify = False, timeout = 5)
        elapsed = response.elapsed.total_seconds()

        if response.status_code == 200 and elapsed < SLOW_THRESHOLD:
            status = "🟢 HEALTHY"

        elif response.status_code == 200 and elapsed > SLOW_THRESHOLD:
            status = "🟡 BAGAL TEH"

        else:
            status = "🔴 UNHEALTHY"

        detail = f"{response.status_code} | {elapsed: .2f}s"


    except requests.exceptions.RequestException as e:
            status = "🔴 DOWN"
            detail = "could not connect"

    return timestamp, status, detail

def log_result(timestamp, name, status, detail):
    with open("health_log.txt", "a", encoding="utf-8") as f:
        f.write(f"{timestamp} | {name} | {status} | {detail}\n")

for target in targets:
    timestamp, status, detail = check_target(target)
    print(f"{target['name']} | {status} | {detail}")
    log_result(timestamp, target['name'], status, detail)
    if "🟢" not in status:
        send_teams_message(f"{target['name']} | {status} | {detail}")



