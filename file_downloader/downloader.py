# download_module.py
import requests
from urllib.parse import urlsplit
import os

def download(url: str) -> None:
    """
    Download a file from a URL and save it with the same name as in the URL.

    :param url: The URL of the file to download.
    """
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Check for HTTP errors

        # Extract filename from URL
        filename = os.path.basename(urlsplit(url).path)

        if not filename:
            filename = 'downloaded_file'  # Default filename if extraction fails

        with open(filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        print(f"File downloaded successfully and saved to {filename}")

    except requests.RequestException as e:
        print(f"An error occurred: {e}")
