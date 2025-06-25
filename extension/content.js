// Gets the body of the page
chrome.runtime.onMessage.addListener(
    (request, sender, sendResponse) => {
        if (request.action === "getbody") {
            sendResponse({body: document.body.innerHTML});
        }
        return true;
    }
);

// Updates the HTML of the page
chrome.runtime.onMessage.addListener(
    (request, sender, sendResponse) => {
        if (request.action === "updateHTML") {
            document.body.innerHTML = request.html;
        }
    }
);