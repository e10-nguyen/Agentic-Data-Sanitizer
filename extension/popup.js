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

            const response = await chrome.runtime.sendMessage({ action: 'sanitize', text: "This is example text. (123) 456-7890."});
            statusDiv.textContent = 'Sanitized text: ' + response.sanitizedText;
        } catch (error) {
            statusDiv.textContent = 'popup.js Error: ' + error.message;
        }
    });
});
