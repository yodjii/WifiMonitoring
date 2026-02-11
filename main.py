import time
from config import config
from scanner import scan_network
import os
from telegram_notifier import notify_device_join, notify_device_leave, notify_initial_scan, get_display_name

def clear_screen():
    # For Windows
    if os.name == 'nt':
        _ = os.system('cls')
    # For macOS and Linux (here, primarily windows is expected)
    else:
        _ = os.system('clear')

def log_progress(message):
    print(f"  > {message}", flush=True)

def main():
    print(f"Starting Wifi Monitoring on {config.NETWORK_RANGE}...", flush=True)
    print(f"Scan interval: {config.SCAN_INTERVAL} seconds", flush=True)
    
    # Dictionary to track devices: {mac: {ip, hostname}}
    known_devices = {}
    is_initial_scan = True
    
    try:
        while True:
            print(f"\nScanning network...", flush=True)
            devices = scan_network(config.NETWORK_RANGE, callback=log_progress)
            
            # Map current devices by MAC address
            current_devices = {d['mac']: {'ip': d['ip'], 'hostname': d['hostname']} for d in devices}
            
            # Identify changes
            if is_initial_scan:
                notify_initial_scan(devices)
            else:
                # New devices
                for mac, info in current_devices.items():
                    if mac not in known_devices:
                        msg = f"\n[NEW DEVICE] {info['hostname']} ({info['ip']}) joined the network!"
                        print(msg, flush=True)
                        notify_device_join(info['hostname'], info['ip'], mac)
                
                # Disappeared devices
                for mac, info in known_devices.items():
                    if mac not in current_devices:
                        msg = f"\n[DISCONNECTED] {info['hostname']} ({info['ip']}) left the network."
                        print(msg, flush=True)
                        notify_device_leave(info['hostname'], info['ip'], mac)
            
            print(f"\n--- Scan result at {time.strftime('%Y-%m-%d %H:%M:%S')} ---", flush=True)
            print(f"{'IP Address':<15} {'MAC Address':<20} {'Hostname/Alias':<30}", flush=True)
            print("-" * 65, flush=True)
            
            if not devices:
                print("No devices found.", flush=True)
            else:
                for device in devices:
                    display_name = get_display_name(device['hostname'], device['mac'])
                    print(f"{device['ip']:<15} {device['mac']:<20} {display_name:<30}", flush=True)
            
            # Update state for next scan
            known_devices = current_devices
            is_initial_scan = False
            
            print(f"\nNext scan in {config.SCAN_INTERVAL} seconds...", flush=True)
            time.sleep(config.SCAN_INTERVAL)
            
    except KeyboardInterrupt:
        print("\nStopping Wifi Monitoring...")

if __name__ == "__main__":
    main()
