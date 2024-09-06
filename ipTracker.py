import requests
import socket
import time

def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        return response.json()['ip']
    except Exception as e:
        return None

def get_local_ip():
    try:
        return socket.gethostbyname(socket.gethostname())
    except Exception as e:
        return None

def monitor_ip(interval=5):
    current_public_ip = get_public_ip()
    current_local_ip = get_local_ip()
    
    print(f"Initial Public IP: {current_public_ip}")
    print(f"Initial Local IP: {current_local_ip}")
    
    while True:
        time.sleep(interval)
        
        new_public_ip = get_public_ip()
        new_local_ip = get_local_ip()
        
        if new_public_ip != current_public_ip:
            print(f"Public IP changed: {new_public_ip}")
            current_public_ip = new_public_ip
        
        if new_local_ip != current_local_ip:
            print(f"Local IP changed: {new_local_ip}")
            current_local_ip = new_local_ip

if __name__ == "__main__":
    monitor_ip()
