import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from datetime import datetime

WEBHOOK_URL = "https://cebupacificairph.webhook.office.com/webhookb2/2b14a23f-23f5-41a6-9e4a-d63939fab78c@fab3949d-3cb0-4097-802f-053ad7075219/IncomingWebhook/3a7d4b16a86241699bf049f1634ffdf4/5b208123-43c0-466b-81a4-13522b75b69f/V225GKWIbpi1QxsPK-TYX6Bdws4TrkS-1TulbokVh4qW01"
SLOW_THRESHOLD = 2.0
targets = ["https://www.google.com", "https://www.youtube.com", "https://fakefakefakeuurl.com"]


def check_targets(targets):
    report = ""
    for target in targets:
            try:
                response =  requests.get(target, verify = False)
                if response.status_code == 200 and response.elapsed.total_seconds() < SLOW_THRESHOLD:
                        status = "UP"
                        report = report + f'{target} | {status} , {response.status_code} {response.elapsed.total_seconds()}s \n'
                elif response.status_code == 200 and response.elapsed.total_seconds() > SLOW_THRESHOLD:
                        status = "SLOW"
                        report = report + f'{target} | {status} , {response.status_code} {response.elapsed.total_seconds()}s \n'
                else:
                    status = "DOWN"
                    report = report + f'{target} + | {status}\n'

            except requests.exceptions.RequestException as e:
                status = "ERROR"
                report = report + f'{target} | {status} \n'

    return report

def log_analyser():
    tally = {'INFO': 0, 'WARNING': 0, 'ERROR': 0}
    start = ""
    end = ""
    with open('.venv/fake_app.log', 'r') as log:
        for line in log:
            logline = line.strip().split(" ",3)
            if logline[2] == 'INFO':
                tally['INFO'] += 1
            elif logline[2] == 'WARNING':
                if logline[2] == 'WARNING' and tally['WARNING'] == 0 and tally['ERROR'] == 0:
                    start = logline[0] + " " + logline[1]
                else:
                    pass
                tally['WARNING'] +=1
            else:

                if logline[2] == 'ERROR' and tally['WARNING'] == 0 and tally['ERROR'] == 0:
                    start = logline[0] + " " + logline[1]
                else:
                    pass
                tally['ERROR'] += 1
                end = logline[0] + " " + logline[1]

    return tally, start, end

def build_shift_report(report, tally, start, end):
    update = (f'(Results of the health checker: \n {report} \n Total tally of logs: {tally} \n Start time of issue: {start} \n End time of issue: {end}')
    return update

report = check_targets(targets)
tally, start, end = log_analyser()
print(build_shift_report(report, tally, start, end))





