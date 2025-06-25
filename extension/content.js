chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'sanitize') {
        sendResponse({farewell: "goodbye"});
        return true;}
    //     // Get the data to be sanitized
    //     const data = document.body.innerText;
        
    //     // Send data to API server
    //     fetch('http://localhost:3000/api/sanitize', {
    //         method: 'POST',
    //         headers: {
    //             'Content-Type': 'application/json',
    //         },
    //         body: JSON.stringify({ text: data })
    //     })
    //     .then(response => {
    //         if (!response.ok) {
    //             throw new Error('Server returned an error');
    //         }
    //         return response.json();
    //     })
    //     .then(result => {
    //         // Replace the content with sanitized data
    //         document.body.innerHTML = result.sanitizedText;
    //     })
    //     .catch(error => {
    //         console.error('content.js Error:', error);
    //         // Send error back to popup
    //         chrome.runtime.sendMessage({ 
    //             action: 'error', 
    //             message: error.message 
    //         });
    //     });
        
    //     // Acknowledge the message
    //     sendResponse({ success: true });
    // } else {
    //     // Acknowledge other messages
    //     sendResponse({ success: false });
    // }
    // // Return true to indicate async handling
    // return true;
});
