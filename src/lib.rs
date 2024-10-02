// src/lib.rs

use pyo3::prelude::*;
use pyo3::exceptions;
use pyo3_asyncio::tokio::future_into_py;
use url::Url;

// Declare the modules
mod crawler;
mod parser;

/// Parses the HTML content and extracts the title and meta description.
#[pyfunction]
fn parse_html_py(html: &str) -> PyResult<(Option<String>, Option<String>)> {
    let (title, description) = parser::parse_html(html);
    Ok((title, description))
}

/// Extracts and sanitizes all href links from the HTML content.
#[pyfunction]
fn extract_links_py(html: &str, base_url: &str) -> PyResult<Vec<String>> {
    let base = Url::parse(base_url).map_err(|e| {
        exceptions::PyValueError::new_err(format!("Invalid base URL: {}", e))
    })?;
    let links = parser::extract_links(html, &base);
    Ok(links)
}

/// Sanitizes and validates a single URL.
#[pyfunction]
fn sanitize_link_py(link: &str) -> PyResult<Option<String>> {
    let sanitized = parser::sanitize_link(link);
    Ok(sanitized)
}

/// Asynchronously crawls web pages starting from a given URL.
#[pyfunction]
fn crawl_py(py: Python, start_url: String, base_url: String) -> PyResult<PyObject> {
    // Convert base_url string to Url
    let base = Url::parse(&base_url).map_err(|e| {
        exceptions::PyValueError::new_err(format!("Invalid base URL: {}", e))
    })?;

    // Initialize visited set and queue
    let visited = std::sync::Arc::new(dashmap::DashSet::new());
    let queue = std::sync::Arc::new(crossbeam::queue::SegQueue::new());
    queue.push(start_url.clone());

    // Clone references for the async task
    let visited_clone = std::sync::Arc::clone(&visited);
    let queue_clone = std::sync::Arc::clone(&queue);
    let base_clone = base.clone();

    // Define the async task
    let async_crawl = async move {
        crawler::crawl(queue_clone, visited_clone, base_clone).await;
        Ok(()) // Ensure the async block returns Result<(), PyErr>
    };

    // Convert the async task to a Python awaitable
    let py_async_crawl = future_into_py(py, async_crawl)?;

    Ok(py_async_crawl.into())
}

/// A Python module implemented in Rust.
#[pymodule]
fn fadex(_py: Python, m: &PyModule) -> PyResult<()> {  // Ensure the module name is 'fadex'
    m.add_function(wrap_pyfunction!(parse_html_py, m)?)?;
    m.add_function(wrap_pyfunction!(extract_links_py, m)?)?;
    m.add_function(wrap_pyfunction!(sanitize_link_py, m)?)?;
    m.add_function(wrap_pyfunction!(crawl_py, m)?)?;
    Ok(())
}
