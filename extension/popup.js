document.addEventListener('DOMContentLoaded', function() {
    const sanitizeButton = document.getElementById('sanitizeButton');
    const statusDiv = document.getElementById('status');

    sanitizeButton.addEventListener('click', async () => {
        try {
            const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
            if (!tab) {
                statusDiv.textContent = 'No active tab found';
                return;
            }

            // Get the text from the content script.
            statusDiv.textContent = 'Retrieving text...';
            const text = await chrome.tabs.sendMessage(tab.id, { action: 'getbody' });

            // Send the text to be sanitized.
            statusDiv.textContent = 'Sanitization in progress...';
            const response = await chrome.runtime.sendMessage({ action: 'sanitize', text: text.body });

            // Updates the HTML of the page.
            statusDiv.textContent = 'Updating HTML';
            chrome.tabs.sendMessage(tab.id, { action: 'updateHTML', html: response.sanitizedText });

            // Display the sanitized text.
            statusDiv.textContent = 'Redaction complete.';

        } catch (error) {
            statusDiv.textContent = 'popup.js Error: ' + error.message + "\nTry reloading the page or type in a URL.";
        }
    });
});
