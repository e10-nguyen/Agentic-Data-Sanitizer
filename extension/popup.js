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

            

            // Send message to content script
            await chrome.tabs.sendMessage(tab.id, { action: 'sanitize' });
            statusDiv.textContent = 'Sanitization in progress...';
        } catch (error) {
            statusDiv.textContent = 'popup.js Error: ' + error.message;
        }
    });
});
