# Agentic Data Sanitizer
UCLA MEng Capstone 2025

# Collaboration with iDox.ai
Ethan Nguyen, Colton Rowe, Yijie Lu, and Gongzhi Wang

## Setup and Running

### 1. Install Server Dependencies

```bash
pip install -r server/requirements.txt
```

### 2. Start the Server

```bash
python server/app.py
```

The server will run on `http://localhost:3000`. You can access the API documentation at:
- Swagger UI: `http://localhost:3000/docs`
- ReDoc: `http://localhost:3000/redoc`

### 3. Load the Chrome Extension

1. Open Chrome and navigate to `chrome://extensions/`
2. Enable "Developer mode" in the top right
3. Click "Load unpacked" and select the `extension/` directory

### 4. Using the Extension

1. Click the extension icon in Chrome's toolbar
2. Click the "Sanitize Data" button in the popup
3. The extension will send the current page content to the server for sanitization
4. The sanitized content will replace the original content on the page