# bs_crawler.py

from bs4 import BeautifulSoup

def get_elements_bs(html: str, tag: str, class_name: str = None) -> list:
    """
    Extracts all HTML elements matching a specified tag and optional class using Beautiful Soup.

    :param html: The HTML content to parse.
    :param tag: The HTML tag to search for (e.g., 'div', 'a', 'span').
    :param class_name: The class name to filter elements. If None, returns all elements with the specified tag.
    :return: A list of strings, each representing the outer HTML of a matched element.
    """
    soup = BeautifulSoup(html, 'html.parser')
    
    if class_name:
        elements = soup.find_all(tag, class_=class_name)
    else:
        elements = soup.find_all(tag)
    
    return [str(element) for element in elements]
