// src/parser.rs

use scraper::{Html, Selector};
use url::Url;

/// Parses the HTML content and extracts the title and meta description.
pub fn parse_html(html: &str) -> (Option<String>, Option<String>) {
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
