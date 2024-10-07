// src/parser.rs
use scraper::{Html, Selector};
use url::Url;

/// Parses the HTML content and extracts the title and meta description.
pub fn get_meta_and_title(html: &str) -> (Option<String>, Option<String>) {
    let document = Html::parse_document(html);

    // Extract title
    let title_selector = Selector::parse("title").unwrap();
    let title = document
        .select(&title_selector)
        .next()
        .map(|elem| elem.text().collect::<Vec<_>>().concat());

    // Extract meta description
    let meta_selector = Selector::parse(r#"meta[name="description"]"#).unwrap();
    let description = document
        .select(&meta_selector)
        .next()
        .and_then(|elem| elem.value().attr("content").map(|s| s.to_string()));

    (title, description)
}


pub fn extract_links(html: &str) -> Vec<String> {
    let document = Html::parse_document(html);
    let selector = Selector::parse("a[href]").unwrap();
    let mut links = Vec::new();

    for element in document.select(&selector) {
        if let Some(href) = element.value().attr("href") {
            // Only include http and https schemes
            if href.starts_with("http://") || href.starts_with("https://") {
                links.push(href.to_string());
            }
        }
    }

    links
}

/// Sanitizes and validates a URL string.
pub fn sanitize_link(link: &str) -> Option<String> {
    match Url::parse(link) {
        Ok(url) => match url.scheme() {
            "http" | "https" => Some(url.to_string()),
            _ => None,
        },
        Err(_) => None,
    }
}

/// Finds an HTML element by its `id` and returns its text content.
///
/// # Arguments
///
/// * `html` - A string slice containing the HTML content.
/// * `id` - A string slice that holds the `id` of the desired element.
///
/// # Returns
///
/// * `Option<String>` - Returns `Some(text)` if the element is found, otherwise `None`.
pub fn find_element_by_id(html: &str, id: &str) -> Option<String> {
    // Parse the HTML document
    let document = Html::parse_document(html);

    // Create a CSS selector for the id
    let selector = Selector::parse(&format!("#{}", id)).ok()?;

    // Select the first element that matches the selector
    let element = document.select(&selector).next()?;

    // Return the HTML content of the element
    Some(element.html())
}

/// Parses the HTML content and extracts all elements matching the given tag and optional class.
///
/// # Arguments
///
/// * `html` - A string slice containing the HTML content.
/// * `tag` - A string slice that holds the name of the HTML tag to search for.
/// * `class` - An optional string slice that holds the class name to filter elements.
///
/// # Returns
///
/// * `Vec<String>` - A vector of strings, each containing the outer HTML of a matched element.
pub fn get_elements_by_cls(html: &str, class: &str) -> Vec<String> {
    // Parse the HTML document
    let document = Html::parse_document(html);

    // Build the CSS selector for the class
    let selector_string = format!(".{}", class);

    // Parse the selector, return empty vector if it's invalid
    let selector = match Selector::parse(&selector_string) {
        Ok(sel) => sel,
        Err(e) => {
            eprintln!("Error parsing selector: {}", e);
            return Vec::new();
        }
    };

    // Select the elements that match the selector and collect the HTML of each element
    document.select(&selector)
        .map(|element| element.html())
        .collect()
}

