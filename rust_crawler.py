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
