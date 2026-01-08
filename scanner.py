import subprocess
import socket
import re
from concurrent.futures import ThreadPoolExecutor, TimeoutError

def get_hostname(ip):
    """Attempts to get hostname with a 1-second timeout."""
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(socket.gethostbyaddr, ip)
        try:
            return future.result(timeout=1.0)[0]
        except (TimeoutError, Exception):
            return "Unknown"

def ping_ip(ip):
    """Returns True if IP responds to ping."""
    try:
        # -n 1: 1 packet, -w 100: 100ms timeout (very short for LAN)
        result = subprocess.run(["ping", "-n", "1", "-w", "100", ip], 
                               stdout=subprocess.DEVNULL, 
                               stderr=subprocess.DEVNULL)
        return result.returncode == 0
    except Exception:
        return False

def get_arp_table():
    try:
        # Try different encodings for Windows
        try:
            output = subprocess.check_output(["arp", "-a"]).decode('cp1252')
        except UnicodeDecodeError:
            output = subprocess.check_output(["arp", "-a"]).decode('utf-8', errors='ignore')
            
        # Matches IP and MAC in the arp -a output. 
        # We look for the pattern: IP address followed by MAC address.
        # This version is more flexible with the 'dynamic/dynamique' label.
        pattern = r"(\d+\.\d+\.\d+\.\d+)\s+([0-9a-f-]{17})"
        matches = re.findall(pattern, output, re.IGNORECASE)
        
        # We only want 'dynamic' or 'dynamique' entries to avoid broadcast/multicast IPs
        # But for simplicity, we can also just filter out known static/multicast ranges
        devices = {}
        for ip, mac in matches:
            # Simple check: skip broadcast and multicast
            if not (ip.endswith(".255") or ip.startswith("224.") or ip.startswith("239.") or ip == "255.255.255.255"):
                devices[ip] = mac.replace('-', ':').lower()
        return devices
    except Exception:
        return {}

def scan_network(network_range, callback=None):
    # Assume network_range is like 192.168.1.0/24
    match = re.match(r"(\d+\.\d+\.\d+)\.", network_range)
    if not match:
        if callback: callback(f"Invalid range: {network_range}")
        return []
        
    base_ip = match.group(1)
    ips = [f"{base_ip}.{i}" for i in range(1, 255)]
    
    if callback:
        callback(f"Pinging {len(ips)} addresses on {base_ip}.0/24...")

    # Use ThreadPoolExecutor to limit concurrency
    with ThreadPoolExecutor(max_workers=50) as executor:
        executor.map(ping_ip, ips)
    
    if callback:
        callback("Reading ARP table...")
        
    arp_table = get_arp_table()
    devices = []
    
    # We only care about devices in the requested base_ip range
    relevant_ips = [ip for ip in arp_table.keys() if ip.startswith(base_ip)]
    
    if callback:
        callback(f"Found {len(relevant_ips)} active devices. Resolving hostnames...")
        
    for ip in relevant_ips:
        mac = arp_table[ip]
        hostname = get_hostname(ip)
        devices.append({
            'ip': ip,
            'mac': mac,
            'hostname': hostname
        })
            
    return devices
