## :dart: About ##
**Fadex** is a powerful Python module that provides robust web scraping functionalities, including fetching web pages, extracting metadata, and parsing HTML content. Built with a Rust backend using PyO3, it is optimized for performance and ease of use in web scraping tasks.

## :sparkles: Features ##

:heavy_check_mark: Fetch web pages asynchronously;\
:heavy_check_mark: Extract metadata including title and description;\
:heavy_check_mark: Sanitize and extract all href links from HTML;\
:heavy_check_mark: Fetch elements by ID and class efficiently;

## Installing

Use the following command in your terminal to install the module.
```bash
$ pip install fadex
```

## :rocket: Technologies ##

The following tools were used in this project:

- [Python](https://python.org)
- [Rust](https://www.rust-lang.org/)
- [PyO3](https://pyo3.rs/v0.15.0/)

## :white_check_mark: Requirements ##

Before starting :checkered_flag:, ensure you have [Python](https://python.org) installed.


## :test_tube: How To Use ##

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
url = "http://example.com"
asyncio.run(fetch_page(url))
```

## :hammer_and_wrench: Functionalities

- Fetch metadata (title and description):
  ```python
  title, description = get_meta_and_title_py(html_content)
  ```

- Extract links from HTML:
  ```python
  links = extract_links_py(html_content)
  ```

- Fetch elements by ID:
  ```python
  elements = find_element_by_id_py(html_content, "your-id")
  ```

- Fetch elements by class:
  ```python
  elements = get_elements_py(html_content, "your-class")
  ```

## :memo: License ##

This project is licensed under the MIT License. For more details, see the [LICENSE](LICENSE.md) file.

Made with :heart: by <a href="https://github.com/fahad-programmer" target="_blank">Fahad Malik</a>

&#xa0;

<a href="#top">Back to top</a>
```
