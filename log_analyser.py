import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

WEBHOOK_URL = "https://cebupacificairph.webhook.office.com/webhookb2/2b14a23f-23f5-41a6-9e4a-d63939fab78c@fab3949d-3cb0-4097-802f-053ad7075219/IncomingWebhook/3a7d4b16a86241699bf049f1634ffdf4/5b208123-43c0-466b-81a4-13522b75b69f/V225GKWIbpi1QxsPK-TYX6Bdws4TrkS-1TulbokVh4qW01"


def parse_log(filename):
    entries = []
    with open(filename, "r", encoding = "utf-8") as f:
        for line in f:
            parts = line.strip().split(" ", 3)
            timestamp = parts[0] + " " + parts[1]
            level = parts[2]
            message = parts[3]

            entry = {
                "timestamp": timestamp,
                "level": level,
                "message": message
            }

            entries.append(entry)

        return entries

results = parse_log("fake_app.log")
for r in results:
    print(r)

def summarize(entries):
    counts = {"INFO": 0, "WARNING": 0, "ERROR": 0}

    for entry in entries:
        level = entry["level"]
        counts[level] += 1

    return counts

counts = summarize(results)
print(counts)

def find_incident_window(entries):
    start = None
    end = None

    for entry in entries:
        if entry["level"] in ("WARNING", "ERROR") and start is None:
            start = entry

        if entry["level"] == "ERROR":
            end = entry

    return start, end

start, end = find_incident_window(results)
print("Start:", start)
print("End:", end)

def build_reports(entries):
    counts = summarize(entries)
    start,end = find_incident_window(entries)

    report=f"""Incident Summary
    
First sign of trouble: {start['timestamp']} - {start['message']}

Last error: {end['timestamp']} - {end['message']}


Total errors: {counts['ERROR']}

Total warnings: {counts['WARNING']}
    """

    return report

report = build_reports(results)
print(report)

def send_teams_message(message):
    payload = {"text": message}
    requests.post(WEBHOOK_URL, json=payload, verify=False)

send_teams_message(report)