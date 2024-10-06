# Fadex Documentation

## Overview

**Fadex** is a Python module that provides powerful web scraping functionalities, including fetching web pages, extracting metadata, and parsing HTML content.

## Installation

You can easily install Fadex using pip:

```bash
pip install fadex
```

## Usage

### Basic Example

To fetch the content of a web page asynchronously, you can use the `fetch_page` function:

```python
import asyncio
from fadex import fetch_page_py

async def fetch_page(url):
    try:
        content = await fetch_page_py(url)
        print("Page content fetched successfully:")
        print(content)
    except Exception as e:
        print(f"Failed to fetch page: {e}")

# Example usage
url = "http://gigmasters.it"
asyncio.run(fetch_page(url))
```

## API Reference

### Functions

#### `get_meta_and_title_py(html: str) -> Tuple[Optional[str], Optional[str]]`

Parses the HTML content and extracts the title and meta description.

- **Parameters:**
  - `html`: A string containing the HTML content.
- **Returns:**
  - A tuple containing:
    - `title`: An optional string representing the page title.
    - `description`: An optional string representing the meta description.

#### `extract_links_py(html: str, base_url: str) -> List[str]`

Extracts and sanitizes all href links from the HTML content.

- **Parameters:**
  - `html`: A string containing the HTML content.
  - `base_url`: A string representing the base URL to resolve relative links.
- **Returns:**
  - A list of sanitized URLs extracted from the HTML.

#### `sanitize_link_py(link: str) -> Optional[str]`

Sanitizes and validates a single URL.

- **Parameters:**
  - `link`: A string representing the URL to sanitize.
- **Returns:**
  - An optional string that contains the sanitized URL if valid, or `None` if invalid.

#### `find_element_by_id_py(html: str, id: str) -> Optional[str]`

Finds an HTML element by its `id` and returns its text content.

- **Parameters:**
  - `html`: A string containing the HTML content.
  - `id`: A string representing the `id` of the desired element.
- **Returns:**
  - An optional string with the text content of the found element, or `None` if not found.

#### `fetch_page_py(url: str) -> Awaitable[str]`

Asynchronously fetches the content of a web page.

- **Parameters:**
  - `url`: A string containing the URL of the page to fetch.
- **Returns:**
  - A string containing the content of the fetched page.

#### `crawl_py(start_url: str, base_url: str) -> Awaitable[None]`

Asynchronously crawls web pages starting from a given URL.

- **Parameters:**
  - `start_url`: A string representing the URL to start crawling from.
  - `base_url`: A string representing the base URL for resolving links.
- **Returns:**
  - None (the function executes asynchronously).

#### `get_elements_py(html: str, tag: str, class: Optional[str]) -> List[str]`

Extracts all elements matching the given tag and optional class.

- **Parameters:**
  - `html`: A string containing the HTML content.
  - `tag`: A string representing the name of the HTML tag to search for.
  - `class`: An optional string representing the class name to filter elements.
- **Returns:**
  - A list of strings, each containing the outer HTML of matched elements.

## Error Handling

Fadex includes error handling to manage various issues that may occur during web scraping operations. If an error arises, appropriate exceptions will be raised with descriptive messages.

## License

This project is licensed under the MIT License.

## Contact

For any questions or feedback, please reach out to [Your Email](mailto:your.email@example.com).

---

Feel free to customize any parts of this documentation to better fit your project or personal style. If you need further adjustments or additions, just let me know!