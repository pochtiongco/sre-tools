import requests
import json
import urllib3
import argparse


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from datetime import datetime

with open("config.json", "r") as f:
    config = json.load(f)

WEBHOOK_URL = config["webhook_url"]
SLOW_THRESHOLD = config["slow_threshold"]
targets = config["targets"]

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
    loglist = ""
    with open('fake_app.log', 'r') as log:
        for line in log:
            loglist += line
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

    return tally, start, end, loglist

def build_shift_report(report, tally, start, end):
    update = (f'(Results of the health checker: \n {report} \n Total tally of logs: {tally} \n Start time of issue: {start} \n End time of issue: {end}')
    return update

def send_teams_message(message):
    payload = {"text": message}
    requests.post(WEBHOOK_URL, json=payload, verify=False)


parser = argparse.ArgumentParser()
parser.add_argument("--check", action = "store_true")
parser.add_argument("--logs", action = "store_true")
parser.add_argument("--report", action = "store_true")
parser.add_argument("--teams", action = "store_true")
args = parser.parse_args()

if args.check:
    report = check_targets(targets)
    print(report)
    if args.teams:
        send_teams_message(report)
if args.logs:
    tally, start, end, loglist = log_analyser()
    print(loglist)
    if args.teams:
        send_teams_message(loglist)
if args.report:
    report = check_targets(targets)
    tally, start, end, loglist = log_analyser()
    print(build_shift_report(report, tally, start, end))
    if args.teams:
        send_teams_message(build_shift_report(report, tally, start, end))










