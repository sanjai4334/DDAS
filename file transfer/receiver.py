import socket
import os

# Define server address and port
SERVER_HOST = input("Enter the server IP: ")  # Replace with the server's IP address
SERVER_PORT = 5001
BUFFER_SIZE = 4096  # Buffer size for receiving data
SAVE_DIR = 'received_files'  # Directory to save the received files

def receive_file():
    # Create a socket object
    client_socket = socket.socket()

    # Connect to the server
    client_socket.connect((SERVER_HOST, SERVER_PORT))
    print(f"[+] Connected to {SERVER_HOST}:{SERVER_PORT}")

    # Request the filename from the user
    filename_to_request = input("Enter the filename you want to receive (with extension): ")

    # Send the filename to the server
    client_socket.send(filename_to_request.encode())

    # Receive the metadata: filename and file size
    metadata = client_socket.recv(BUFFER_SIZE).decode().split('\n')
    if metadata[0].startswith('ERROR'):
        print(metadata[0])
        client_socket.close()
        return

    server_filename = metadata[0]
    filesize = int(metadata[1])

    # Acknowledge metadata reception
    client_socket.send(b'ACK')

    # Ensure the directory exists
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)

    # Define the path to save the received file
    save_path = os.path.join(SAVE_DIR, server_filename)

    # Open the file in binary mode
    with open(save_path, 'wb') as file:
        bytes_received = 0
        while bytes_received < filesize:
            # Receive data from the server
            bytes_read = client_socket.recv(BUFFER_SIZE)
            if not bytes_read:
                # File transmitting is done
                break
            # Write the received data to the file
            file.write(bytes_read)
            bytes_received += len(bytes_read)

    print(f"[+] File received successfully and saved as {save_path}.")

    # Close the client socket
    client_socket.close()

# Receive the file
receive_file()
