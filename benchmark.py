# benchmark.py

import asyncio
import time
import fadex  # Your Rust-based module
import bs_crawler  # The Beautiful Soup implementation

URL = "https://realpython.com/beautiful-soup-web-scraper-python/"
ITERATIONS = 10  # Number of times to run each function for averaging

async def benchmark_fadex(url: str, iterations: int):
    """
    Benchmarks the Rust-based fadex implementation.
    
    :param url: The URL to fetch and parse.
    :param iterations: Number of iterations to run.
    :return: Average execution time in seconds.
    """
    total_time = 0.0
    for _ in range(iterations):
        start_time = time.perf_counter()
        
        # Fetch page asynchronously using fadex
        content = await fadex.fetch_page_py(url)
        
        # Parse title and description
        title, description = fadex.get_meta_and_title_py(content)
        
        end_time = time.perf_counter()
        iteration_time = end_time - start_time
        total_time += iteration_time
        print(f"[fadex] Iteration Time: {iteration_time:.4f} seconds")
    
    average_time = total_time / iterations
    print(f"[fadex] Average Time over {iterations} iterations: {average_time:.4f} seconds\n")
    return average_time

async def benchmark_bs(url: str, iterations: int):
    """
    Benchmarks the Beautiful Soup implementation.
    
    :param url: The URL to fetch and parse.
    :param iterations: Number of iterations to run.
    :return: Average execution time in seconds.
    """
    total_time = 0.0
    for _ in range(iterations):
        start_time = time.perf_counter()
        
        # Fetch page asynchronously using aiohttp
        content = await bs_crawler.fetch_page_bs(url)
        
        # Parse title and description using Beautiful Soup
        title, description = bs_crawler.get_meta_and_title_bs(content)
        
        end_time = time.perf_counter()
        iteration_time = end_time - start_time
        total_time += iteration_time
        print(f"[Beautiful Soup] Iteration Time: {iteration_time:.4f} seconds")
    
    average_time = total_time / iterations
    print(f"[Beautiful Soup] Average Time over {iterations} iterations: {average_time:.4f} seconds\n")
    return average_time

async def main():
    print(f"Benchmarking URL: {URL}\n")
    print(f"Running {ITERATIONS} iterations for each implementation...\n")
    
    # Benchmark fadex
    avg_fadex = await benchmark_fadex(URL, ITERATIONS)
    
    # Benchmark Beautiful Soup
    avg_bs = await benchmark_bs(URL, ITERATIONS)
    
    # Compare results
    print("Benchmark Results:")
    print(f"Average Time - fadex: {avg_fadex:.4f} seconds")
    print(f"Average Time - Beautiful Soup: {avg_bs:.4f} seconds")
    
    if avg_fadex < avg_bs:
        print("\nResult: fadex is faster than Beautiful Soup by {:.2f}%".format(((avg_bs - avg_fadex) / avg_bs) * 100))
    elif avg_fadex > avg_bs:
        print("\nResult: Beautiful Soup is faster than fadex by {:.2f}%".format(((avg_fadex - avg_bs) / avg_fadex) * 100))
    else:
        print("\nResult: Both implementations have the same average execution time.")

if __name__ == "__main__":
    asyncio.run(main())
