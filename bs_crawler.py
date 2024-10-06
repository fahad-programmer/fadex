import asyncio
import time
from fadex import fetch_page_py, get_meta_and_title_py, extract_links_py
from bs4 import BeautifulSoup
from lxml import html as lxml_html
from urllib.parse import urljoin, urlparse

# Function to extract metadata using Fadex
def extract_metadata_with_fadex(html_content):
    try:
        title, description = get_meta_and_title_py(html_content)
        return True, title, description
    except Exception as e:
        return False, None, None

# Function to extract metadata using BeautifulSoup
def extract_metadata_with_beautifulsoup(html_content):
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        title = soup.title.string if soup.title else None
        description = None
        meta_tag = soup.find('meta', attrs={'name': 'description'})
        if meta_tag:
            description = meta_tag.get('content')
        return True, title, description
    except Exception as e:
        return False, None, None

# Function to extract metadata using lxml
def extract_metadata_with_lxml(html_content):
    try:
        tree = lxml_html.fromstring(html_content)
        title = tree.find('.//title').text if tree.find('.//title') is not None else None
        description = None
        meta = tree.xpath('//meta[@name="description"]')
        if meta and 'content' in meta[0].attrib:
            description = meta[0].attrib['content']
        return True, title, description
    except Exception as e:
        return False, None, None

# Function to extract links using Fadex
def extract_links_with_fadex(html_content, base_url):
    try:
        links = extract_links_py(html_content, base_url)
        return True, links
    except Exception as e:
        return False, []

# Function to extract links using BeautifulSoup
def extract_links_with_beautifulsoup(html_content, base_url):
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        links = [urljoin(base_url, a['href']) for a in soup.find_all('a', href=True)]
        return True, [link for link in links if urlparse(link).scheme in ["http", "https"]]
    except Exception as e:
        return False, []

# Function to extract links using lxml
def extract_links_with_lxml(html_content, base_url):
    try:
        tree = lxml_html.fromstring(html_content)
        links = [urljoin(base_url, link) for link in tree.xpath('//a/@href')]
        return True, [link for link in links if urlparse(link).scheme in ["http", "https"]]
    except Exception as e:
        return False, []

# Function to measure average performance for each library
def measure_metadata_performance(html_contents, extract_func, iterations=5):
    total_time = 0
    successful_extracts = 0
    for _ in range(iterations):
        for html_content in html_contents:
            start_time = time.time()
            success, title, description = extract_func(html_content)
            total_time += time.time() - start_time
            if success:
                successful_extracts += 1
    average_time = total_time / (len(html_contents) * iterations)
    return average_time, successful_extracts

# Function to measure link extraction performance for each library
def measure_link_extraction_performance(html_contents, base_urls, extract_func, iterations=5):
    total_time = 0
    successful_extracts = 0
    for _ in range(iterations):
        for html_content, base_url in zip(html_contents, base_urls):
            start_time = time.time()
            success, links = extract_func(html_content, base_url)
            total_time += time.time() - start_time
            if success:
                successful_extracts += 1
    average_time = total_time / (len(html_contents) * iterations)
    return average_time, successful_extracts

# Main function to run the tests
async def main():
    # List of popular URLs for testing
    urls = [
        "https://www.google.com",
        "https://www.wikipedia.org",
        "https://www.github.com",
        "https://www.reddit.com",
        "https://www.stackoverflow.com",
        "https://www.nytimes.com",
        "https://www.bbc.com",
        "https://www.amazon.com",
        "https://www.apple.com",
        "https://www.microsoft.com"
    ]

    # Fetch page content using Fadex
    html_contents = []
    for url in urls:
        try:
            content = await fetch_page_py(url)
            html_contents.append(content)
        except Exception as e:
            print(f"Failed to fetch page from {url}: {e}")

    # Define number of iterations for performance measurement
    iterations = 10

    # Measure performance for Fadex (metadata extraction)
    fadex_meta_average_time, fadex_meta_success = measure_metadata_performance(
        html_contents, extract_metadata_with_fadex, iterations
    )

    # Measure performance for BeautifulSoup (metadata extraction)
    bs_meta_average_time, bs_meta_success = measure_metadata_performance(
        html_contents, extract_metadata_with_beautifulsoup, iterations
    )

    # Measure performance for lxml (metadata extraction)
    lxml_meta_average_time, lxml_meta_success = measure_metadata_performance(
        html_contents, extract_metadata_with_lxml, iterations
    )

    # Measure performance for Fadex (link extraction)
    fadex_links_average_time, fadex_links_success = measure_link_extraction_performance(
        html_contents, urls, extract_links_with_fadex, iterations
    )

    # Measure performance for BeautifulSoup (link extraction)
    bs_links_average_time, bs_links_success = measure_link_extraction_performance(
        html_contents, urls, extract_links_with_beautifulsoup, iterations
    )

    # Measure performance for lxml (link extraction)
    lxml_links_average_time, lxml_links_success = measure_link_extraction_performance(
        html_contents, urls, extract_links_with_lxml, iterations
    )

    # Print the results for metadata extraction
    print(f"Fadex Metadata Extraction Average Time: {fadex_meta_average_time:.2f} seconds (Successful Extracts: {fadex_meta_success})")
    print(f"BeautifulSoup Metadata Extraction Average Time: {bs_meta_average_time:.2f} seconds (Successful Extracts: {bs_meta_success})")
    print(f"lxml Metadata Extraction Average Time: {lxml_meta_average_time:.2f} seconds (Successful Extracts: {lxml_meta_success})")

    # Print the results for link extraction
    print(f"Fadex Link Extraction Average Time: {fadex_links_average_time:.2f} seconds (Successful Extracts: {fadex_links_success})")
    print(f"BeautifulSoup Link Extraction Average Time: {bs_links_average_time:.2f} seconds (Successful Extracts: {bs_links_success})")
    print(f"lxml Link Extraction Average Time: {lxml_links_average_time:.2f} seconds (Successful Extracts: {lxml_links_success})")

    # Compare and determine the winner for metadata extraction
    print("\nPerformance Comparison for Metadata Extraction:")
    print(f"Fadex Time: {fadex_meta_average_time:.2f} seconds")
    print(f"BeautifulSoup Time: {bs_meta_average_time:.2f} seconds")
    print(f"lxml Time: {lxml_meta_average_time:.2f} seconds")

    if lxml_meta_average_time < fadex_meta_average_time and lxml_meta_average_time < bs_meta_average_time:
        print("\nWinner for Metadata Extraction: lxml")
    elif fadex_meta_average_time < lxml_meta_average_time and fadex_meta_average_time < bs_meta_average_time:
        print("\nWinner for Metadata Extraction: Fadex")
    elif bs_meta_average_time < lxml_meta_average_time and bs_meta_average_time < fadex_meta_average_time:
        print("\nWinner for Metadata Extraction: BeautifulSoup")
    else:
        print("\nIt's a tie for Metadata Extraction!")

    # Compare and determine the winner for link extraction
    print("\nPerformance Comparison for Link Extraction:")
    print(f"Fadex Time: {fadex_links_average_time:.2f} seconds")
    print(f"BeautifulSoup Time: {bs_links_average_time:.2f} seconds")
    print(f"lxml Time: {lxml_links_average_time:.2f} seconds")

    if lxml_links_average_time < fadex_links_average_time and lxml_links_average_time < bs_links_average_time:
        print("\nWinner for Link Extraction: lxml")
    elif fadex_links_average_time < lxml_links_average_time and fadex_links_average_time < bs_links_average_time:
        print("\nWinner for Link Extraction: Fadex")
    elif bs_links_average_time < lxml_links_average_time and bs_links_average_time < fadex_links_average_time:
        print("\nWinner for Link Extraction: BeautifulSoup")
    else:
        print("\nIt's a tie for Link Extraction!")

if __name__ == "__main__":
    asyncio.run(main())