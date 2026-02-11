import os
from dotenv import load_dotenv

import json

# Load .env file
load_dotenv()

class Config:
    SCAN_INTERVAL = int(os.getenv("SCAN_INTERVAL", 15))
    NETWORK_RANGE = os.getenv("NETWORK_RANGE", "192.168.1.0/24")
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
    SEND_TELEGRAM = os.getenv("SEND_TELEGRAM", "False").lower() == "true"
    # Load aliases
    ALIASES = {}
    if os.path.exists("aliases.json"):
        try:
            with open("aliases.json", "r", encoding="utf-8") as f:
                raw_aliases = json.load(f)
                # Normalize keys: lowercase and strip potential typos like trailing colons
                ALIASES = {}
                for k, v in raw_aliases.items():
                    clean_key = k.strip().lower().rstrip(':')
                    ALIASES[clean_key] = v
        except Exception as e:
            print(f"Error loading aliases.json: {e}")

    # Load excluded MACs
    EXCLUDED_MACS = {}
    if os.path.exists("excluded_macs.json"):
        try:
            with open("excluded_macs.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    EXCLUDED_MACS = data
                elif isinstance(data, list):
                    EXCLUDED_MACS = {mac: "Excluded" for mac in data}
                else:
                    print("Warning: excluded_macs.json should be a list or a dictionary.")
        except Exception as e:
            print(f"Error loading excluded_macs.json: {e}")

config = Config()
