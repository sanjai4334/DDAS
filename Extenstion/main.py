from mongo import connector
from uid_tracker import client as ip_finder
from file_transfer import receiver as file_receiver
from file_downloader import downloader 
from flask import Flask, request, jsonify
from flask_cors import CORS
from plyer import notification  # Import plyer notification

app = Flask(__name__)
CORS(app)

@app.route('/receive-url', methods=['POST'])
def receive_url():
    data = request.json
    url = data.get('url')
    print("Received URL:", url)
    
    # Send notification for receiving URL
    notification.notify(
        title="URL Received",
        message=f"Received URL: {url}",
        timeout=5
    )

    # Example response; you can customize this based on your needs
    retrived_data = connector.find_data(url)

    if retrived_data:
        ip_found = ip_finder.get_ip(retrived_data["user_id"])
        
        # Notify about IP finding
        notification.notify(
            title="User Found",
            message=f"User with ID {retrived_data['user_id']} found on network.",
            timeout=5
        )

        if ip_found:
            file_receiver.receive_file(ip_found, retrived_data["filename"])
            response_message = "File Downloaded from the network successfully!"
            
            # Notify about file download
            notification.notify(
                title="Download Complete",
                message=response_message,
                timeout=5
            )

    else:
        downloader.download(url)
        response_message = "File Downloaded from the server successfully!"
        
        # Notify about server download
        notification.notify(
            title="Download Complete",
            message=response_message,
            timeout=5
        )
    
    return jsonify({"status": "success", "message": response_message}), 200

if __name__ == "__main__":
    app.run(debug=True, port=5003)  # Port changed to 5003
