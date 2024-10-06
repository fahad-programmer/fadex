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

## Performance Comparison

We conducted a performance comparison between **Fadex**, **aiohttp**, and **requests** by making 1000 requests to 10 different domains. The results are as follows:

```
Aiohttp Average Time: 1.03 seconds (Successful Requests: 9)
Fadex Average Time: 0.88 seconds (Successful Requests: 10)
Requests Average Time: 0.92 seconds (Successful Requests: 9)

Performance Comparison:
Aiohttp Time: 1.03 seconds
Fadex Time: 0.88 seconds
Requests Time: 0.92 seconds

Winner: Fadex
```

These results show that **Fadex** outperforms both **aiohttp** and **requests** in terms of average response time and the number of successful requests. However, please note that the performance of each library is also dependent on factors such as internet connection stability, which can vary. With a stable internet connection, you can expect even better and more consistent results from **Fadex**.

## Example Code for Performance Comparison

Below is the code used for the performance comparison:

```python
import asyncio
import time
import requests
from fadex import fetch_page_py
import aiohttp

# Function to fetch a page using Fadex
async def fetch_page_with_fadex(url):
    try:
        await fetch_page_py(url)
        return True
    except Exception as e:
        return False

# Function to fetch a page using aiohttp
async def fetch_page_with_aiohttp(url):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                response.raise_for_status()
                return True
        except Exception as e:
            return False

# Function to fetch a page using requests (synchronous)
def fetch_page_with_requests(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return True
    except Exception as e:
        return False

# Function to measure average performance for each library
async def measure_performance_async(urls, async_func):
    total_time = 0
    successful_requests = 0
    for url in urls:
        start_time = time.time()
        success = await async_func(url)
        total_time += time.time() - start_time
        if success:
            successful_requests += 1
    average_time = total_time / len(urls)
    return average_time, successful_requests

def measure_performance_sync(urls, sync_func):
    total_time = 0
    successful_requests = 0
    for url in urls:
        start_time = time.time()
        success = sync_func(url)
        total_time += time.time() - start_time
        if success:
            successful_requests += 1
    average_time = total_time / len(urls)
    return average_time, successful_requests

# Main function to run the tests
async def main():
    # List of URLs for testing
    urls = [
        "http://example.com",
        "http://gigmasters.it",
        "http://httpbin.org",
        "http://jsonplaceholder.typicode.com",
        "http://github.com",
        "http://openai.com",
        "http://stackoverflow.com",
        "http://python.org",
        "http://reddit.com",
        "http://wikipedia.org"
    ]

    num_requests = 1000
    expanded_urls = urls * (num_requests // len(urls))

    # Measure performance for aiohttp
    aiohttp_average_time, aiohttp_success = await measure_performance_async(expanded_urls, fetch_page_with_aiohttp)

    # Measure performance for Fadex
    fadex_average_time, fadex_success = await measure_performance_async(expanded_urls, fetch_page_with_fadex)

    # Measure performance for requests (using asyncio.to_thread to run it asynchronously)
    requests_average_time, requests_success = await asyncio.to_thread(measure_performance_sync, expanded_urls, fetch_page_with_requests)

    # Print the results
    print(f"Aiohttp Average Time: {aiohttp_average_time:.2f} seconds (Successful Requests: {aiohttp_success})")
    print(f"Fadex Average Time: {fadex_average_time:.2f} seconds (Successful Requests: {fadex_success})")
    print(f"Requests Average Time: {requests_average_time:.2f} seconds (Successful Requests: {requests_success})")

    # Compare and determine the winner
    print("\nPerformance Comparison:")
    print(f"Aiohttp Time: {aiohttp_average_time:.2f} seconds")
    print(f"Fadex Time: {fadex_average_time:.2f} seconds")
    print(f"Requests Time: {requests_average_time:.2f} seconds")

    if fadex_average_time < aiohttp_average_time and fadex_average_time < requests_average_time:
        print("\nWinner: Fadex")
    elif aiohttp_average_time < fadex_average_time and aiohttp_average_time < requests_average_time:
        print("\nWinner: aiohttp")
    elif requests_average_time < fadex_average_time and requests_average_time < aiohttp_average_time:
        print("\nWinner: Requests")
    else:
        print("\nIt's a tie between the libraries!")

if __name__ == "__main__":
    asyncio.run(main())
```

## License

This project is licensed under the MIT License.

## Contact

For any questions or feedback, please reach out to [Your Email](mailto:your.email@example.com).
