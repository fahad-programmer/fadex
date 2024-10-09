import time
from fadex import get_meta_and_title, extract_links
from lxml import html as lxml_html
import requests

def fetch_html(url):
    print(f"Fetching HTML content for {url}...")
    response = requests.get(url)
    print(f"Content fetched for {url}.")
    return response.text

def benchmark_fadex(html, iterations):
    total_time = 0
    print("Starting Fadex benchmark...")
    for i in range(iterations):
        if i % 100 == 0:
            print(f"Fadex iteration {i}/{iterations}")
        start = time.time()
        links = extract_links(html)
        total_time += time.time() - start
    print("Fadex benchmark complete.")
    return total_time / iterations

def benchmark_lxml(html, iterations):
    total_time = 0
    print("Starting lxml benchmark...")
    for i in range(iterations):
        if i % 100 == 0:
            print(f"lxml iteration {i}/{iterations}")
        start = time.time()
        tree = lxml_html.fromstring(html)
        links = tree.xpath('//a/@href')
        total_time += time.time() - start
    print("lxml benchmark complete.")
    return total_time / iterations

# URLs of websites with complex HTML structures
urls = [
    "https://www.nytimes.com",  # Complex structure with multiple nested elements
    "https://www.bbc.com",      # Extensive multimedia content and interactive components
    "https://www.amazon.com",   # Dynamic content and numerous nested HTML tags
    "https://www.reddit.com",   # Infinite scroll and diverse embedded elements
    "https://www.aliexpress.com",  # Heavy use of JavaScript and multiple HTML layers
]

iterations = 1000  # Number of iterations per URL
fadex_total_time = 0
lxml_total_time = 0

for url in urls:
    html = fetch_html(url)
    print(f"Benchmarking Fadex for {url}...")
    fadex_total_time += benchmark_fadex(html, iterations)
    print(f"Benchmarking lxml for {url}...")
    lxml_total_time += benchmark_lxml(html, iterations)

# Calculate average time across all URLs and iterations
fadex_avg_time = fadex_total_time / len(urls)
lxml_avg_time = lxml_total_time / len(urls)

print("\n--- Benchmark Results ---")
print(f"Average Fadex Time: {fadex_avg_time} seconds")
print(f"Average lxml Time: {lxml_avg_time} seconds")

# Determine the winner
if fadex_avg_time < lxml_avg_time:
    print("Winner: Fadex")
else:
    print("Winner: lxml")
