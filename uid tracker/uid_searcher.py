import socket
import json

# Function to search for a device with a specific user ID
def find_device_with_user_id(user_id):
    # Broadcast address to send messages to all devices in the network
    broadcast_address = '255.255.255.255'  # Replace this with your broadcast address if needed
    port = 50000

    # Create a UDP socket for communication
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Allow broadcasting
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # Create a message with the user ID to be sent as a JSON object
    message = json.dumps({'user_id': user_id}).encode('utf-8')

    # Send the message to the broadcast address
    sock.sendto(message, (broadcast_address, port))
    print(f"Searching for user ID '{user_id}' on the network...")

    # Set a timeout to stop waiting for responses after a certain time
    sock.settimeout(5)

    try:
        while True:
            # Receive responses from devices
            data, addr = sock.recvfrom(1024)
            response = data.decode('utf-8')

            if response == 'FOUND':
                print(f"Device with user ID '{user_id}' found at {addr[0]}")
                break
    except socket.timeout:
        print("No device with the requested user ID was found on the network.")
    finally:
        # Close the socket after the operation is complete
        sock.close()

if __name__ == "__main__":
    # Ask the user for the user ID to search for
    user_id = input("Enter the user ID to search for: ")
    find_device_with_user_id(user_id)
