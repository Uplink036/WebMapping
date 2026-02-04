"""Web interface for bounding box plugin."""

def boundingbox_section() -> str:
    """Generate HTML section for bounding box functionality."""
    return '''
    <div class="plugin-section">
        <h2>Bounding Box Screenshots</h2>
        <button onclick="loadRandomScreenshot('bbox')">Load Random Bbox Screenshot</button>
        <div id="bbox-screenshot-container">
            <p>Click the button to load a random bbox screenshot</p>
        </div>
        <input type="text" id="bbox-url" placeholder="Enter URL" style="width: 300px; padding: 8px; margin: 5px;">
        <button onclick="captureBoundingBox()">Capture Bounding Box</button>
        <div id="bbox-result">
            <p>Enter a URL to capture its bounding box screenshot</p>
        </div>
        <script>
            function loadRandomScreenshot(type) {
                const container = document.getElementById(type + '-screenshot-container');
                const timestamp = new Date().getTime();
                fetch('/api/random_screenshot?screenshot_type=' + type + '&t=' + timestamp)
                    .then(response => {
                        if (response.ok) {
                            container.innerHTML = '<img src="/api/random_screenshot?screenshot_type=' + type + '&t=' + timestamp + '" style="max-width: 80%; border: 1px solid #ccc; margin: 20px 0;" alt="Random ' + type + ' Screenshot">';
                        } else {
                            container.innerHTML = '<p>No ' + type + ' screenshots available</p>';
                        }
                    });
            }
            function captureBoundingBox() {
                const url = document.getElementById('bbox-url').value;
                if (!url) {
                    alert('Please enter a URL');
                    return;
                }
                document.getElementById('bbox-result').innerHTML = '<p>Capturing bounding box...</p>';
                fetch('/api/capture_bbox', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({url: url})
                })
                .then(response => response.json())
                .then(data => {
                    document.getElementById('bbox-result').innerHTML = '<p>' + data.message + '</p>';
                })
                .catch(error => {
                    document.getElementById('bbox-result').innerHTML = '<p>Error: ' + error + '</p>';
                });
            }
        </script>
    </div>
    '''
