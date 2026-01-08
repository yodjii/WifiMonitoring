# 📡 Network Monitoring

A lightweight and elegant solution to monitor devices connected to your local network in real-time, with instant Telegram notifications.

This project focuses on observing network availability, collecting connectivity data, and identifying potential disconnections or instability in a simple and practical way without relying on heavy monitoring tools.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg?style=for-the-badge&logo=python&logoColor=white)
![Status](https://img.shields.io/badge/Status-Stable-green.svg?style=for-the-badge)

## Why this project exists

This project was created to answer a very concrete need:  
monitor Wi-Fi connectivity reliability and detect connection drops without relying on heavy monitoring tools.

The goals were to:
- observe network behavior over time
- detect disconnections or instability
- build a simple, readable monitoring tool
- keep the implementation lightweight and focused

---

## Use cases

- Monitoring Wi-Fi stability on a workstation or server
- Detecting recurring network disconnections
- Collecting connectivity data for diagnostics
- Supporting troubleshooting of unreliable networks
- Learning and experimenting with system monitoring in Python

---

## ✨ Features

- 🔍 **Automatic Network Scan**: Detects new devices and disconnections on your LAN.
- ⏱️ **Adjustable Interval**: Configure the scan frequency to suit your needs (e.g., every 15 seconds).
- 💬 **Telegram Notifications**: Receive real-time alerts when a device joins or leaves the network.
- 🏷️ **Alias Management**: Replace cryptic hostnames with readable names (e.g., `Flo's iPhone`).
- 🚫 **Selective Exclusion**: Ignore notifications for specific devices (like routers or servers) via an exclusion list.
- 📊 **Startup Summary**: A summary of all online devices right at launch.

## Voluntary limitations

This project was intentionally kept simple. It does not include:

* Advanced network diagnostics
* Visualization dashboards
* Alerting or notification mechanisms
* Persistent data storage

These choices were made to stay focused on the core goal: detecting Networking connectivity issues in a lightweight and reliable way.

## Possible improvements

* Persistent logging or database storage
* Network metrics visualization
* Other Alerting system (email, SMS, etc.)
* Containerization with Docker

## 🚀 Installation

### 1. Clone the project
```bash
git clone https://github.com/yodjii/WifiMonitoring.git
cd WifiMonitoring
```

### 2. Environment Setup
Create a virtual environment and install dependencies:
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Variable Configuration
Create a `.env` file in the root directory (use `.env.example` if available):
```env
SCAN_INTERVAL=15
NETWORK_RANGE=192.168.1.0/24
TELEGRAM_BOT_TOKEN=YOUR_BOT_TOKEN
TELEGRAM_CHAT_ID=YOUR_CHAT_ID
SEND_TELEGRAM=True
```

## ⚙️ Advanced Configuration

### 📛 Aliases (`aliases.json`)
Map custom names to detected hostnames (copy `aliases.json.example` to `aliases.json`):
```json
{
    "iphone-de-Nicolas.home": "📱 Nicolas's iPhone",
    "livebox.home": "🌐 Internet Box"
}
```

### 🔕 Exclusion (`excluded_macs.json`)
Prevent specific devices from triggering notifications (copy `excluded_macs.json.example` to `excluded_macs.json`):
```json
{
    "48:29:52:c2:32:57": "Unknown Device",
    "AA:BB:CC:DD:EE:FF": "NAS Server"
}
```

## 🛠️ Usage

Simply run the main script:
```bash
python main.py
```

> [!TIP]
> On Windows, you can use the provided `run_wifi_monitor.bat` file to launch monitoring with a single double-click.

## 📝 Notes
- The script uses `ping` and `arp` commands to detect devices without requiring complex administrator privileges.
- Ensure your firewall allows ICMP (ping) requests.

## ⚖️ Legal Warning

This project is intended for strictly **personal and educational** use on a network you own or for which you have received explicit monitoring authorization.

- **Private Network**: Use on your own home network is legal and recommended for security.
- **Third-Party Networks**: Using this tool on a network that does not belong to you without authorization is illegal (e.g., Art. 323-1 of the French Penal Code).
- **GDPR**: MAC addresses and hostnames are personal data. Be sure to respect the privacy of your guests.

*The author declines all responsibility in the event of malicious use or use not complying with current legislation.*

---
*Developed with ❤️ for a better-monitored network.*
