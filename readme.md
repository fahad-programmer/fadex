Here's your documentation reformatted to match the style you provided for **Pyhoroscope**. The structure includes headers, badges, and sections, and it maintains clarity and organization for easy navigation.

```html
<div align="center" id="top"> 
  <img src="https://your-image-link-here.png" alt="Fadex" />

  &#xa0;

  <!-- <a href="https://your-demo-link-here">Demo</a> -->
</div>

<h1 align="center">Fadex</h1>

<p align="center">
  <img alt="Github top language" src="https://img.shields.io/github/languages/top/your-username/fadex?color=56BEB8">
  <img alt="Github language count" src="https://img.shields.io/github/languages/count/your-username/fadex?color=56BEB8">
  <img alt="Repository size" src="https://img.shields.io/github/repo-size/your-username/fadex?color=56BEB8">
  <img alt="License" src="https://img.shields.io/github/license/your-username/fadex?color=56BEB8">
  <img alt="Github issues" src="https://img.shields.io/github/issues/your-username/fadex?color=56BEB8" />
  <img alt="Github forks" src="https://img.shields.io/github/forks/your-username/fadex?color=56BEB8" />
  <img alt="Github stars" src="https://img.shields.io/github/stars/your-username/fadex?color=56BEB8" />
</p>

<p align="center">
  <a href="#dart-about">About</a> &#xa0; | &#xa0; 
  <a href="#sparkles-features">Features</a> &#xa0; | &#xa0;
  <a href="#rocket-technologies">Technologies</a> &#xa0; | &#xa0;
  <a href="#white_check_mark-requirements">Requirements</a> &#xa0; | &#xa0;
  <a href="#checkered_flag-starting">Starting</a> &#xa0; | &#xa0;
  <a href="#test_tube-how-to-use">How TO</a> &#xa0; | &#xa0;
  <a href="#hammer_and_wrench-functionalities">Functions</a> &#xa0; | &#xa0;
  <a href="#memo-license">License</a> &#xa0; | &#xa0;
  <a href="https://github.com/your-username" target="_blank">Author</a>
</p>

<br>

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

Before starting :checkered_flag:, ensure you have [Python](https://python.org) and [Rust](https://www.rust-lang.org/) installed.

## :checkered_flag: Starting ##

```bash
# Clone this project
$ git clone https://github.com/your-username/fadex

# Access
$ cd fadex

# Install dependencies
$ pip install -r requirements.txt

# Run the project (if applicable)
$ python your_script.py
```

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

Made with :heart: by <a href="https://github.com/your-username" target="_blank">Your Name</a>

&#xa0;

<a href="#top">Back to top</a>
```

### Notes:
- Replace placeholders like `your-image-link-here`, `your-username`, and `Your Name` with your actual links and names.
- The structure is consistent with the **Pyhoroscope** example, ensuring clarity and ease of navigation.
- Feel free to modify any section to better fit your project needs!