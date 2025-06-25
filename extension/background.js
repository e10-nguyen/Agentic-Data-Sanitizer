// Listen for extension installation
chrome.runtime.onInstalled.addListener(() => {
    console.log('Agentic Data Sanitizer extension installed');
});

// Handle messages from content scripts
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'error') {
        console.error('Content script error:', request.message);
        sendResponse({ handled: true });
    }
    return true;
});

// Handle external messages
chrome.runtime.onMessageExternal.addListener((request, sender, sendResponse) => {
    console.log('Received external message:', request);
    sendResponse({ received: true });
    return true;
});

// Handle tab updates
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    if (changeInfo.status === 'complete') {
        console.log('Tab updated:', tab.url);
    }
});

// Handle tab updates
chrome.tabs.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'sanitize') {
        console.error('Sanitization in progress:', request.message);
    }
    return true;
});
