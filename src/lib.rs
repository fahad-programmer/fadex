// src/lib.rs

use pyo3::exceptions;
use pyo3::prelude::*;
use pyo3_asyncio::tokio::future_into_py;
use thiserror::Error;

// Declare the modules
mod crawler;
mod parser;

// Define a custom error type for better error handling
#[derive(Error, Debug)]
pub enum FetchError {
    #[error("Request error: {0}")]
    RequestError(#[from] reqwest::Error),

    #[error("URL parsing error: {0}")]
    UrlParseError(#[from] url::ParseError),
}

/// Parses the HTML content and extracts the title and meta description.
#[pyfunction]
fn get_meta_and_title_py(html: &str) -> PyResult<(Option<String>, Option<String>)> {
    let (title, description) = parser::get_meta_and_title(html);
    Ok((title, description))
}

/// Extracts and sanitizes all href links from the HTML content.
#[pyfunction]
fn extract_links_py(html: &str) -> PyResult<Vec<String>> {
    let links = parser::extract_links(html);
    Ok(links)
}

/// Sanitizes and validates a single URL.
#[pyfunction]
fn sanitize_link_py(link: &str) -> PyResult<Option<String>> {
    let sanitized = parser::sanitize_link(link);
    Ok(sanitized)
}

/// Finds an HTML element by its `id` and returns its text content.
#[pyfunction]
fn find_element_by_id_py(html: &str, id: &str) -> PyResult<Option<String>> {
    let element = parser::find_element_by_id(html, id);
    Ok(element)
}

/// Asynchronously fetches the content of a web page.
#[pyfunction]
fn fetch_page_py(py: Python, url: String) -> PyResult<PyObject> {
    // Define the async task
    let async_fetch = async move {
        match crawler::fetch_page(&url).await {
            Ok(content) => Ok(content),
            Err(e) => Err(exceptions::PyIOError::new_err(format!(
                "Failed to fetch page: {}",
                e
            ))),
        }
    };

    // Convert the async task to a Python awaitable
    let py_future = future_into_py(py, async_fetch)?;

    Ok(py_future.into())
}


#[pyfunction]
fn get_elements_py(html: &str, class: &str) -> PyResult<Vec<String>> {
    let elements = parser::get_elements_by_cls(html, class);
    Ok(elements)
}

/// A Python module implemented in Rust.
#[pymodule]
fn fadex(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(get_meta_and_title_py, m)?)?;
    m.add_function(wrap_pyfunction!(extract_links_py, m)?)?;
    m.add_function(wrap_pyfunction!(sanitize_link_py, m)?)?;
    m.add_function(wrap_pyfunction!(find_element_by_id_py, m)?)?;
    m.add_function(wrap_pyfunction!(fetch_page_py, m)?)?;
    m.add_function(wrap_pyfunction!(get_elements_py, m)?)?;
    Ok(())
}
