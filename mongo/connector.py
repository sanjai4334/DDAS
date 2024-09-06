from pymongo import MongoClient
import requests
import mimetypes
from urllib.parse import urlparse, unquote

# MongoDB connection URL
db_url = "mongodb+srv://user1:karan@cluster1.bozbp.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1"

def get_file_info(url):
    try:
        # Send a HEAD request to get metadata without downloading the file
        response = requests.head(url, allow_redirects=True)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Extract relevant information from the headers
            content_type = response.headers.get('Content-Type', 'Unknown')
            content_length = response.headers.get('Content-Length', 'Unknown')
            last_modified = response.headers.get('Last-Modified', 'Unknown')
            etag = response.headers.get('ETag', 'Unknown')
            content_disposition = response.headers.get('Content-Disposition', 'Unknown')
            cache_control = response.headers.get('Cache-Control', 'Unknown')
            expires = response.headers.get('Expires', 'Unknown')
            final_url = response.url

            # Infer the file extension from the content type if possible
            extension = mimetypes.guess_extension(content_type.split(';')[0].strip())
            extension = extension if extension else 'Unknown'

            # Extract filename from Content-Disposition header if available
            filename = 'Unknown'
            if content_disposition and ('attachment' in content_disposition or 'inline' in content_disposition):
                filename = content_disposition.split('filename=')[-1].strip('"').strip("'")
                filename = unquote(filename)  # Decode URL-encoded filename

            # If filename is still 'Unknown', infer it from the URL path
            if filename == 'Unknown':
                parsed_url = urlparse(final_url)
                filename = parsed_url.path.split('/')[-1]
                filename = unquote(filename)  # Decode URL-encoded filename

            # Print file metadata (optional)
            print(f"File URL: {final_url}")
            print(f"Filename: {filename}")
            # print(f"Content Type: {content_type}")
            print(f"Content Length: {content_length} bytes")
            # print(f"File Extension: {extension}")
            # print(f"Last Modified: {last_modified}")
            print(f"ETag: {etag}")
            # print(f"Content-Disposition: {content_disposition}")
            # print(f"Cache-Control: {cache_control}")
            # print(f"Expires: {expires}")

            # Return metadata as a dictionary
            return {
                'url': final_url,
                'filename': filename,
                'content_type': content_type,
                'content_length': content_length,
                'extension': extension,
                'last_modified': last_modified,
                'etag': etag,
                'content_disposition': content_disposition,
                'cache_control': cache_control,
                'expires': expires
            }

        else:
            print(f"Failed to retrieve information. HTTP Status Code: {response.status_code}")
            return None

    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def check_if_file_exists(collection, file_info):
    """
    Check if the file already exists in the collection.
    """
    # Check for a document with the same URL or filename
    existing_file = collection.find_one({
        'url': file_info['url'],  # Check by URL
        # You can add more fields to match, such as 'filename': file_info['filename']
    })

    if existing_file:
        print("Alert: This file is already present in the database.")
        return True  # File exists
    else:
        print("This is a new file. Proceeding with the save.")
        return False  # File does not exist


if __name__ == "__main__":
    # Example URL
    url = input("Enter the URL of the file: ")

    # Get file information
    file_info = get_file_info(url)

    # Connect to MongoDB and check if file exists
    if file_info:
        # Step 1: Create a MongoDB client
        client = MongoClient(db_url)

        try:
            # Step 2: Connect to the database
            db = client.get_database('DDAS')  # Replace 'test_database' with your desired database name

            # Step 3: Define a collection
            file_metadata_collection = db['FileMetadata']

            # Step 4: Check if file already exists
            if not check_if_file_exists(file_metadata_collection, file_info):
                # Step 5: Save the file information to the database if it does not exist
                result = file_metadata_collection.insert_one(file_info)
                print(f"Document saved with ID: {result.inserted_id}")

        except Exception as e:
            print(f"Error connecting to the DB or saving document: {e}")

        finally:
            # Close the connection
            client.close()
