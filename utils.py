import logging
import os

import requests
import urllib3
from datetime import datetime
import json
import logging

logging.basicConfig(
    level = logging.INFO,
    format = '%(asctime)s | %(levelname)s | %(message)s')


logger = logging.getLogger("sre_tool")

with open("config.json", "r") as f:
    config = json.load(f)


WEBHOOK_URL = os.environ.get("TEAMS_WEBHOOK_URL")
SLOW_THRESHOLD = config["slow_threshold"]
targets = config["targets"]
api_targets = config["api_targets"]

def send_teams_message(message):
    #payload = {"text": message}
    payload = {
        "type": "message",
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": {
                    "type": "AdaptiveCard",
                    "body": [
                        {
                            "type": "TextBlock",
                            "text": message
                        }
                    ],
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "version": "1.2"
                }
            }
        ]
    }
    response = requests.post(WEBHOOK_URL, json=payload, verify=False)
