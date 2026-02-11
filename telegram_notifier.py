import requests
from config import config

def send_telegram_message(message: str) -> bool:
    """
    Sends a message via the Telegram Bot API using credentials from config.
    """
    if not config.SEND_TELEGRAM:
        print("[TELEGRAM] Notifications disabled (SEND_TELEGRAM=False)")
        return False
        
    if not config.TELEGRAM_BOT_TOKEN or not config.TELEGRAM_CHAT_ID:
        print("[TELEGRAM ERROR] Missing Token or Chat ID in .env")
        return False
        
    url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendMessage"
    
    payload = {
        "chat_id": config.TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            print(f"[TELEGRAM] Notification successfully sent to {config.TELEGRAM_CHAT_ID}")
            return True
        else:
            print(f"[TELEGRAM ERROR] HTTP Error {response.status_code}: {response.text}")
            return False
    except Exception as e:
        print(f"[TELEGRAM ERROR] Exception during sending: {e}")
        return False

def get_display_name(hostname, mac=None):
    """
    Returns the alias if it exists, otherwise the original hostname.
    Priority: MAC alias > Hostname alias > Hostname
    """
    if mac and mac in config.ALIASES:
        return config.ALIASES[mac]
    return config.ALIASES.get(hostname, hostname)

def notify_device_join(hostname, ip, mac):
    if mac in config.EXCLUDED_MACS:
        alias = config.EXCLUDED_MACS[mac]
        print(f"[SCAN] Notification ignored for {hostname} ({mac} - {alias}) - MAC excluded.")
        return False
    display_name = get_display_name(hostname, mac)
    message = f"🆕 {display_name}"
    return send_telegram_message(message)

def notify_device_leave(hostname, ip, mac):
    if mac in config.EXCLUDED_MACS:
        alias = config.EXCLUDED_MACS[mac]
        print(f"[SCAN] Notification ignored for {hostname} ({mac} - {alias}) - MAC excluded.")
        return False
    display_name = get_display_name(hostname, mac)
    message = f"❌ {display_name}"
    return send_telegram_message(message)

def notify_initial_scan(devices):
    """Sends a summary of all online devices detected during the first scan."""
    # Filter out excluded MACs
    filtered_devices = [d for d in devices if d['mac'] not in config.EXCLUDED_MACS]
    
    if not filtered_devices:
        return send_telegram_message("🔍 <b>Initial scan:</b> No devices detected (or all are excluded).")
    
    device_list = []
    for d in filtered_devices:
        display_name = get_display_name(d['hostname'], d['mac'])
        device_list.append(f"• {display_name}")
    
    summary = "\n".join(device_list)
    message = f"🔍 <b>Online devices:</b>\n\n{summary}"
    return send_telegram_message(message)
