import threading
from uid_gen import uid_gen
from file_transfer import sender as file_sender
from uid_tracker import server as uid_server
from mongo import connector
from uid_tracker import client as ip_finder
from file_transfer import receiver as file_receiver

def start_file_sender():
    print("Starting File Sender...")
    file_sender.start_server()

def start_uid_server():
    print("Starting UID Server...")
    uid_server.start_server()

# Generate UID
uid_gen.generate()

# Start each server in a separate thread
file_sender_thread = threading.Thread(target=start_file_sender)
uid_server_thread = threading.Thread(target=start_uid_server)

file_sender_thread.start()
uid_server_thread.start()

# Gets the file URL and returns the uid if it is found in db
retrived_data = connector.find_data()

if retrived_data:
    ip_found = ip_finder.get_ip(retrived_data["user_id"])

    if ip_found:
        file_receiver.receive_file(ip_found, retrived_data["filename"])