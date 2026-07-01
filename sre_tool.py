import requests
import json
import urllib3
import argparse
import logging
import subprocess


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from datetime import datetime
from utils import send_teams_message, WEBHOOK_URL, SLOW_THRESHOLD, targets, api_targets, logger


def check_targets(targets):
    report = ""
    for target in targets:
        attempts = 0
        success = False
        while attempts < 3 and not success:
            attempts += 1
            try:
                response = requests.get(target, verify=False)
                if response.status_code == 200 and response.elapsed.total_seconds() < SLOW_THRESHOLD:
                    status = "UP"
                    success = True
                    report = report + f'{target} | {status} , {response.status_code} {response.elapsed.total_seconds()}s \n'
                elif response.status_code == 200 and response.elapsed.total_seconds() > SLOW_THRESHOLD:
                    status = "SLOW"
                    success = True
                    report = report + f'{target} | {status} , {response.status_code} {response.elapsed.total_seconds()}s \n'
                else:
                    status = "DOWN"
                    success = False
                    if attempts == 3:
                        report = report + f'{target} + | {status}\n'


            except requests.exceptions.RequestException as e:
                status = "ERROR"
                success = False
                if attempts == 3:
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

def check_api(targets, expected_field, expected_value):
    report = ""
    for target in targets:
        try:
                webresponse = requests.get(target, verify = False)
                data = webresponse.json()
                if expected_field in data and data[expected_field] == expected_value:
                    status = "UP"
                elif data == {}:
                    status = "ERROR - did not return anything"
                else:
                    status = "DOWN"
        except requests.exceptions.RequestException:
            status = "ERROR"
        report += f'{target} | {status} \n'
    return report

def ping_report(targets):
    report = ""
    for target in targets:
        target = target.replace("https://", "")
        result = subprocess.run(['ping', '-n', '1', target], capture_output=True, text=True)
        if result.returncode == 0:
            for line in result.stdout.split("\n"):
                if "time=" in line:
                    response_time = line.split("time=")[1].split(" ")[0]
            report += f'{target} is pingable with response time of {response_time}\n'
        else:
            report += f'{target} is not pingable. Aurnaur. \n'
    return report




parser = argparse.ArgumentParser()
parser.add_argument("--check", action = "store_true")
parser.add_argument("--logs", action = "store_true")
parser.add_argument("--report", action = "store_true")
parser.add_argument("--teams", action = "store_true")
parser.add_argument("--api", action = "store_true")
parser.add_argument("--ping", action="store_true")
args = parser.parse_args()

if args.check:
    report = check_targets(targets)
    for line in report.strip().split("\n"):
        if "ERROR" in line:
            logger.error(line)
        else:
            logger.info(line)
    if args.teams:
        send_teams_message(report)
if args.logs:
    tally, start, end, loglist = log_analyser()
    for line in loglist.strip().split("\n"):
        if "ERROR" in line:
            logger.error(line)
        else:
            logger.info(line)
    if args.teams:
        send_teams_message(loglist)
if args.report:
    report = check_targets(targets)
    tally, start, end, loglist = log_analyser()
    logger.info(build_shift_report(report, tally, start, end))
    if args.teams:
        logger.info("Sending to teams")
        send_teams_message(build_shift_report(report, tally, start, end))
if args.api:
    report = check_api(api_targets, "completed", False)
    for line in report.strip().split("\n"):
        if "DOWN" in line or "ERROR" in line:
            logger.error(line)
        else:
            logger.info(line)
    if args.teams:
        send_teams_message(report)
if args.ping:
    report = ping_report(targets)
    for line in report.strip().split("\n"):
        if "Aurnaur" in line:
            logger.error(line)
        else:
            logger.info(line)
    if args.teams:
        send_teams_message(report)






