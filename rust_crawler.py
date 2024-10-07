# test_html_functions.py

import fadex  # Make sure to replace this with your actual Rust module name
from urllib.parse import urlparse

# Sample HTML content for testing
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="description" content="Sample description for testing.">
    <title>Sample Title</title>
</head>
<body>
    <h1 id="context-region-dialog-title">Navigate back to</h1>
    <div id="context-region-dialog" aria-modal="true">
        <div class="Overlay-header">
            <div class="Overlay-headerContentWrap">
                <div class="Overlay-titleWrap">
                    <h1 class="Overlay-title">Sample Overlay Title</h1>
                </div>
            </div>
        </div>
    </div>
    <a href="http://example.com">Example Link</a>
</body>
</html>
"""

# Test get_meta_and_title function
def test_get_meta_and_title():
    title, description = fadex.get_meta_and_title_py(html_content)
    assert title == "Sample Title", f"Expected 'Sample Title', got {title}"
    assert description == "Sample description for testing.", f"Expected 'Sample description for testing.', got {description}"
    print("test_get_meta_and_title passed!")

# Test extract_links function
def test_extract_links():
    base_url = urlparse("http://localhost")
    links = fadex.extract_links_py(html_content)
    assert links == ["http://example.com"], f"Expected ['http://example.com'], got {links}"
    print("test_extract_links passed!")

def test_element_id():
    element = fadex.get_elements_py(html_content,"Overlay-header")
    print(element)

# Run all tests
if __name__ == "__main__":
    test_get_meta_and_title()
    test_extract_links()
    test_element_id()
