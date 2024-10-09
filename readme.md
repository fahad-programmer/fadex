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
from fadex import fetch_page

async def fetch_page_py(url):
    try:
        content = await fetch_page(url)
        print("Page content fetched successfully:")
        print(content)
    except Exception as e:
        print(f"Failed to fetch page: {e}")

# Example usage
url = "http://gigmasters.it"
asyncio.run(fetch_page_py(url))
```

## :hammer_and_wrench: Functionalities

- Fetch metadata (title and description):
  ```python
  title, description = get_meta_and_title_py(html_content)
  ```

#### `get_meta_and_title(html: str) -> Tuple[Optional[str], Optional[str]]`

- Fetch elements by ID:
  ```python
  elements = find_element_by_id_py(html_content, "your-id")
  ```

- Fetch elements by class:
  ```python
  elements = get_elements_py(html_content, "your-class")
  ```

#### `extract_links(html: str) -> List[str]`

This project is licensed under the MIT License. For more details, see the [LICENSE](LICENSE.md) file.

Made with :heart: by <a href="https://github.com/fahad-programmer" target="_blank">Fahad Malik</a>

#### `fetch_page(url: str) -> Awaitable[str]`

Asynchronously fetches the content of a web page.

- **Parameters:**
  - `url`: A string containing the URL of the page to fetch.
- **Returns:**
  - A string containing the content of the fetched page.

#### `find_element_by_id(html: str, id: str) -> List[str]`

Fetches the elements that have the specified id in the html content.

- **Parameters:**
  - `html`: A string containing the html content.
  - `id` : The id of which u want elements for.
- **Returns:**
  - A list of elements usually one that have the same id as given in param.

#### `get_elements_by_cls(html: str, class: str) -> List[str]`

Fetches the elements that have the specified class in the html content.

- **Parameters:**
  - `html`: A string containing the html content.
  - `class` : The class of which you want elements for.
- **Returns:**
  - A list of elements that have the same class as given in param.


## Performance Comparison

We conducted a performance comparison between **Fadex**, **BeautifulSoup**, and **lxml** by extracting the metadata (title and description) and extracting all links from 10 popular websites. The results are as follows:

### Metadata Extraction Performance

<a href="#top">Back to top</a>
```
