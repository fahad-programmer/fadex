from bs4 import BeautifulSoup
from lxml import etree
from io import StringIO
import timeit
from fadex import get_elements_by_cls

def generate_html(num_sections=100, num_divs_per_section=100, target_class="target"):
    """
    Generates a large HTML document with specified numbers of sections and divs.
    
    :param num_sections: Number of <section> tags.
    :param num_divs_per_section: Number of <div> tags per <section>.
    :param target_class: The class name to assign to some <div> tags.
    :return: A string containing the generated HTML.
    """
    html = ["<html><head><title>Test Document</title></head><body>"]
    
    for i in range(num_sections):
        html.append(f"<section id='section-{i}'>")
        for j in range(num_divs_per_section):
            # Assign the target class to every 10th div for testing
            if j % 10 == 0:
                html.append(f"<div class='{target_class}'>Content {i}-{j}</div>")
            else:
                html.append(f"<div class='other'>Content {i}-{j}</div>")
        html.append("</section>")
    
    html.append("</body></html>")
    return "\n".join(html)

def extract_with_bs4(html, class_name):
    """
    Extracts all elements with the specified class using BeautifulSoup.
    
    :param html: The HTML content as a string.
    :param class_name: The class name to search for.
    :return: A list of matching BeautifulSoup elements.
    """
    soup = BeautifulSoup(html, 'html.parser')
    return soup.find_all(class_=class_name)

def extract_with_lxml(html, class_name):
    """
    Extracts all elements with the specified class using lxml.
    
    :param html: The HTML content as a string.
    :param class_name: The class name to search for.
    :return: A list of matching lxml elements.
    """
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(html), parser)
    # Using XPath to find all elements with the specified class
    xpath_query = f"//*[@class='{class_name}']"
    return tree.xpath(xpath_query)

def benchmark_functions(html, class_name, number=10):
    """
    Benchmarks the extraction functions using timeit.
    
    :param html: The HTML content as a string.
    :param class_name: The class name to search for.
    :param number: Number of times to execute each function.
    :return: None (prints the results).
    """
    # Define the setup code for timeit
    setup_code = f"""
from __main__ import extract_with_bs4, extract_with_lxml, get_elements_by_cls
html = {repr(html)}
class_name = {repr(class_name)}
"""
    # Define the code snippets to benchmark
    bs4_code = "extract_with_bs4(html, class_name)"
    lxml_code = "extract_with_lxml(html, class_name)"
    fadex_code = "get_elements_by_cls(html, class_name)"
    
    # Time the BeautifulSoup extraction
    bs4_time = timeit.timeit(bs4_code, setup=setup_code, number=number)
    
    # Time the lxml extraction
    lxml_time = timeit.timeit(lxml_code, setup=setup_code, number=number)
    
    # Time the fadex extraction
    fadex_time = timeit.timeit(fadex_code, setup=setup_code, number=number)
    
    # Compute average times
    bs4_avg = bs4_time / number
    lxml_avg = lxml_time / number
    fadex_avg = fadex_time / number
    
    print(f"Benchmark Results over {number} runs:")
    print(f"BeautifulSoup: {bs4_time:.6f} seconds total, {bs4_avg:.6f} seconds per run")
    print(f"lxml:          {lxml_time:.6f} seconds total, {lxml_avg:.6f} seconds per run")
    print(f"fadex:         {fadex_time:.6f} seconds total, {fadex_avg:.6f} seconds per run")

def main():
    # Generate a large HTML document
    html = generate_html(num_sections=100, num_divs_per_section=100, target_class="target")
    
    # Specify the class to search for
    target_class = "target"
    
    # Number of benchmark runs
    number = 10
    
    # Run the benchmark
    benchmark_functions(html, target_class, number=number)

if __name__ == "__main__":
    main()
