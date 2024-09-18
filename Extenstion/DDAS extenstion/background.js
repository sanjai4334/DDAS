// Listener for when a download is about to begin
chrome.downloads.onDeterminingFilename.addListener((downloadItem, suggest) => {
  console.log(`Blocking download: ${downloadItem.url}`);
  // Cancel all downloads
  suggest({ cancel: true });
  
  // Optionally, send the URL to your application for logging
  if (downloadItem.url) {
    sendUrlToApplication(downloadItem.url);
  }
});

function sendUrlToApplication(url) {
  const applicationUrl = "http://localhost:5003/receive-url"; // Your application endpoint

  fetch(applicationUrl, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ url })
  })
  .then(response => response.json())
  .then(data => {
    console.log('Server response:', data);
    showNotification(data.message); // Display the message from the server
  })
  .catch(error => {
    console.error('Error:', error.message);
    showNotification(`Error: ${error.message}`); // Show error in notification
  });
}

function showNotification(message) {
  chrome.notifications.create({
    type: 'basic',
    iconUrl: 'icon128.png', // Ensure this file exists in your extension directory
    title: 'Download Blocked',
    message: message
  });
}
