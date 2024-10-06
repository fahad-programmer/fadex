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

    num_requests = 10
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
