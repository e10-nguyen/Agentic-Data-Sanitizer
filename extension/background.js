// Listen for extension installation
chrome.runtime.onInstalled.addListener(() => {
    console.log('Agentic Data Sanitizer extension installed');
});

// Right now the server is locally hosted, this can be replaced with a remote server later.
const server = 'http://localhost:3000/api/sanitize';

// Handle messages from content scripts
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'error') {
        console.error('Content script error:', request.message);
        sendResponse({ handled: true });
    }
    if (request.action === 'sanitize') {
        fetch(server, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: request.text })
        })
        .then(r => r.json())
        .then(response => {
            console.log('Sanitized text received from server:', response.sanitizedText);
            sendResponse({ sanitizedText: response.sanitizedText });
        })
        .catch(error => {
            console.error('Error communicating with server:', error);
            sendResponse({ handled: false });
        })
    }
    return true;
});