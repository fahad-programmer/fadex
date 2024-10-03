# benchmark_comparison.py

import asyncio
import time
import fadex
import bs_crawler

# Define test cases
TEST_CASES = [
    {
        "description": "Simple HTML with few elements",
        "html": """
        <html>
            <body>
                <div class="container">
                    <p class="text">Hello World!</p>
                    <p class="text">Another paragraph.</p>
                    <div class="container">
                        <span class="highlight">Highlighted Text</span>
                    </div>
                    <a href="https://example.com" class="link">Example Link</a>
                    <a href="https://another.com">Another Link</a>
                </div>
            </body>
        </html>
        """,
        "tag_class_pairs": [
            ("p", "text"),
            ("a", None),
            ("div", "container"),
            ("span", "highlight"),
        ]
    },
    # Add more test cases as needed
]

# Number of iterations for each function
ITERATIONS = 10000

async def benchmark_fadex(html, tag, class_name):
    start_time = time.perf_counter()
    elements = fadex.get_elements_py(html, tag, class_name)
    # Optionally, you can process 'elements' if needed
    end_time = time.perf_counter()
    return end_time - start_time

def benchmark_bs(html, tag, class_name):
    start_time = time.perf_counter()
    elements = bs_crawler.get_elements_bs(html, tag, class_name)
    # Optionally, you can process 'elements' if needed
    end_time = time.perf_counter()
    return end_time - start_time

async def run_benchmark():
    results = []

    for test in TEST_CASES:
        description = test["description"]
        html = test["html"]
        print(f"\nTest Case: {description}")

        for tag, class_name in test["tag_class_pairs"]:
            print(f"\nBenchmarking tag='{tag}' with class='{class_name}'")

            # Benchmark fadex
            fadex_times = []
            for _ in range(ITERATIONS):
                elapsed = await benchmark_fadex(html, tag, class_name)
                fadex_times.append(elapsed)
            fadex_avg = sum(fadex_times) / ITERATIONS

            # Benchmark Beautiful Soup
            bs_times = []
            for _ in range(ITERATIONS):
                elapsed = benchmark_bs(html, tag, class_name)
                bs_times.append(elapsed)
            bs_avg = sum(bs_times) / ITERATIONS

            # Store results
            results.append({
                "description": description,
                "tag": tag,
                "class_name": class_name,
                "fadex_avg": fadex_avg,
                "bs_avg": bs_avg,
            })

            # Print results
            print(f"fadex Average Time over {ITERATIONS} iterations: {fadex_avg:.6f} seconds")
            print(f"Beautiful Soup Average Time over {ITERATIONS} iterations: {bs_avg:.6f} seconds")

            # Determine which is faster
            if fadex_avg < bs_avg:
                percentage = ((bs_avg - fadex_avg) / bs_avg) * 100
                print(f"Result: fadex is faster than Beautiful Soup by {percentage:.2f}%")
            elif fadex_avg > bs_avg:
                percentage = ((fadex_avg - bs_avg) / fadex_avg) * 100
                print(f"Result: Beautiful Soup is faster than fadex by {percentage:.2f}%")
            else:
                print("Result: Both implementations have the same average execution time.")

    # Optionally, process 'results' further or save to a file

if __name__ == "__main__":
    asyncio.run(run_benchmark())
