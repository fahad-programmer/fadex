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

/// Extracts all href links from the given HTML content.
pub fn extract_links(html: &str, base_url: &Url) -> Vec<String> {
    let document = Html::parse_document(html);
    let selector = Selector::parse("a[href]").unwrap();
    let mut links = Vec::new();

    for element in document.select(&selector) {
        if let Some(href) = element.value().attr("href") {
            // Attempt to resolve the href against the base URL
            if let Ok(mut resolved_url) = base_url.join(href) {
                // Remove fragment to avoid duplicates
                resolved_url.set_fragment(None);

                // Only include http and https schemes
                match resolved_url.scheme() {
                    "http" | "https" => {
                        links.push(resolved_url.to_string());
                    },
                    _ => (), // Skip other schemes like mailto, javascript, etc.
                }
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
    // parse the html document
    let document = Html::parse_document(html);

    // Create a css selector for the id 
    let selector  = Selector::parse(&format!("#{}", id)).ok()?;

    // Select the first element that matches the selector
    let element = document.select(&selector).next()?;

    // Extract and concatenate the text content of the element
    Some(element.text().collect::<Vec<_>>().concat())
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

pub fn get_elements(html: &str, tag: &str, class: Option<&str>) -> Vec<String> {
    let document = Html::parse_document(html);

    //Build the css selector based on wheather a class is provided or not
    let selector_string = match class {
        Some(cls) => format!("{}[class=\"{}\"]", tag, cls),
        None => tag.to_string()
    };

    let selector = match Selector::parse(&selector_string) {
        Ok(sel) => sel,
        Err(_) => return Vec::new(), //Return empty vector if selector is invalid
    };

    document.select(&selector)
        .map(|element| element.html())
        .collect()
}