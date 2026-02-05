"""Web interface for screenshot plugin."""


def screenshot_section() -> str:
    """Generate HTML section for screenshot functionality."""
    return """
    <div class="plugin-section">
        <h2>Clean Screenshots</h2>
        <button onclick="loadRandomScreenshot('clean')">Load Random Clean Screenshot</button>
        <div id="clean-screenshot-container">
            <p>Click the button to load a random clean screenshot</p>
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
        </script>
    </div>
    """
