from mongo import connector
from uid_tracker import client as ip_finder
from file_transfer import receiver as file_receiver


# Gets the file URL and returns the uid if it is found in db
retrived_data = connector.find_data(input("Enter the URL of the file: "))

if retrived_data:
    ip_found = ip_finder.get_ip(retrived_data["user_id"])

    if ip_found:
        file_receiver.receive_file(ip_found, retrived_data["filename"])