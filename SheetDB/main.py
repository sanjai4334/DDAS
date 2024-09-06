import os.path
import requests
import mimetypes
from urllib.parse import urlparse, unquote
import platform
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import socket
import time

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SAMPLE_SPREADSHEET_ID = "1kUiulAeHaQ-PvrKmKTlkWp7n4Kc1LzT8akxlNLGIyTo"

def get_file_info(url):
    try:
        parsed_url = urlparse(url)
        hostname = parsed_url.hostname if parsed_url.hostname else 'Unknown'
        system_name = platform.node()
        response = requests.head(url, allow_redirects=True)

        if response.status_code == 200:
            content_type = response.headers.get('Content-Type', 'Unknown')
            content_length = response.headers.get('Content-Length', 'Unknown')
            last_modified = response.headers.get('Last-Modified', 'Unknown')
            etag = response.headers.get('ETag', 'Unknown')
            content_disposition = response.headers.get('Content-Disposition', 'Unknown')
            cache_control = response.headers.get('Cache-Control', 'Unknown')
            expires = response.headers.get('Expires', 'Unknown')
            final_url = response.url

            extension = mimetypes.guess_extension(content_type.split(';')[0].strip())
            extension = extension if extension else 'Unknown'

            filename = 'Unknown'
            if 'attachment' in content_disposition or 'inline' in content_disposition:
                filename = content_disposition.split('filename=')[-1].strip('"').strip("'")
                filename = unquote(filename)

            if filename == 'Unknown':
                filename = parsed_url.path.split('/')[-1]
                filename = unquote(filename)

            return [system_name, hostname, get_public_ip(), get_local_ip(), final_url, filename, content_type, content_length, extension, last_modified, etag, content_disposition, cache_control, expires]
        else:
            print(f"Failed to retrieve information. HTTP Status Code: {response.status_code}")
            return None

    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        return response.json()['ip']
    except Exception as e:
        print(f"Error retrieving public IP: {e}")
        return 'Unknown'

def get_local_ip():
    try:
        return socket.gethostbyname(socket.gethostname())
    except Exception as e:
        print(f"Error retrieving local IP: {e}")
        return 'Unknown'

def get_current_ip_info():
    return get_public_ip(), get_local_ip()

def read_existing_ips(sheet_service, spreadsheet_id, cell_range):
    try:
        result = sheet_service.values().get(
            spreadsheetId=spreadsheet_id,
            range=cell_range
        ).execute()
        values = result.get('values', [])
        
        if values:
            return values[0]  # Assuming the cell range contains one row of data
        else:
            return ['Unknown', 'Unknown']
    except Exception as e:
        print(f"Error reading existing IPs from Google Sheet: {e}")
        return ['Unknown', 'Unknown']

def update_google_sheet(sheet_service, spreadsheet_id, cell_range, values):
    try:
        sheet_service.values().update(
            spreadsheetId=spreadsheet_id,
            range=cell_range,
            valueInputOption="RAW",
            body={"values": [values]}
        ).execute()
        print(f"Updated cell range {cell_range} with new values: {values}")
    except Exception as e:
        print(f"Error updating Google Sheet: {e}")

def monitor_ip_and_update_sheet(sheet_service, spreadsheet_id, cell_range, interval=5):
    public_ip, local_ip = get_current_ip_info()
    
    print(f"Initial Public IP: {public_ip}, Local IP: {local_ip}")
    
    while True:
        time.sleep(interval)
        
        new_public_ip, new_local_ip = get_current_ip_info()
        
        # Read existing IPs from the sheet
        existing_ips = read_existing_ips(sheet_service, spreadsheet_id, cell_range)
        
        # Update if there are changes
        if new_public_ip != existing_ips[0] or new_local_ip != existing_ips[1]:
            print("------------------------------------")
            print(f"IP addresses changed: Public IP: {new_public_ip}, Local IP: {new_local_ip}")
            update_google_sheet(sheet_service, spreadsheet_id, cell_range, [new_public_ip, new_local_ip])
        
        print("------------------------------------")
        print(f"Current Public IP: {new_public_ip}, Local IP: {new_local_ip}")

def main():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("sheets", "v4", credentials=creds)
        sheet = service.spreadsheets()

        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="Sheet1!A1:Z1").execute()
        values = result.get("values", [])

        if not values:
            headers = ["System Name", "Hostname", "Public IP", "Local IP", "URL", "Filename", "Content Type", "Content Length", "File Extension", "Last Modified", "ETag", "Content-Disposition", "Cache-Control", "Expires"]
            sheet.values().update(
                spreadsheetId=SAMPLE_SPREADSHEET_ID,
                range="Sheet1!A1",
                valueInputOption="RAW",
                body={"values": [headers]}
            ).execute()
            print("Headers added to the Google Sheet.")

        url = input("Enter the URL of the file: ")
        file_info = get_file_info(url)

        if file_info:
            sheet.values().append(
                spreadsheetId=SAMPLE_SPREADSHEET_ID,
                range="Sheet1!A2",
                valueInputOption="RAW",
                body={"values": [file_info]}
            ).execute()
            print("Data successfully appended to Google Sheet.")
        else:
            print("No data to append.")
        
        cell_range = 'C2:D2'  # Update this to the appropriate range where IP addresses are stored
        monitor_ip_and_update_sheet(sheet, SAMPLE_SPREADSHEET_ID, cell_range)

    except HttpError as err:
        print(err)

if __name__ == "_main_":
    main()