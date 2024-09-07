import threading
from uid_gen import uid_gen
from file_transfer import sender as file_sender
from uid_tracker import server as uid_server

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

# Optionally, join threads if you want the main program to wait for them to finish
file_sender_thread.join()
uid_server_thread.join()
