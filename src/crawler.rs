// src/crawler.rs

use reqwest::Client;
use lazy_static::lazy_static;
use thiserror::Error;

#[derive(Error, Debug)]
pub enum FetchError {
    #[error("Request error: {0}")]
    RequestError(#[from] reqwest::Error),

    #[error("URL parsing error: {0}")]
    UrlParseError(#[from] url::ParseError),
}

lazy_static! {
    static ref CLIENT: Client = Client::new();
}

/// Asynchronously fetches the content of the given URL.
pub async fn fetch_page(url: &str) -> Result<String, FetchError> {
    let response = CLIENT.get(url).send().await?;
    let content = response.text().await?;
    Ok(content)
}


