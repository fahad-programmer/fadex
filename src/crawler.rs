// src/crawler.rs

use reqwest::Client;
use std::sync::Arc;
use dashmap::DashSet;
use crossbeam::queue::SegQueue;
use tokio::sync::Semaphore;
use tokio::task;
use lazy_static::lazy_static;
use url::Url;
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

const MAX_CONCURRENT_TASKS: usize = 100;

lazy_static! {
    static ref SEMAPHORE: Arc<Semaphore> = Arc::new(Semaphore::new(MAX_CONCURRENT_TASKS));
}

/// Asynchronously fetches the content of the given URL.
pub async fn fetch_page(url: &str) -> Result<String, FetchError> {
    let response = CLIENT.get(url).send().await?;
    let content = response.text().await?;
    Ok(content)
}

/// Asynchronously crawls web pages starting from the URLs in the queue.
pub async fn crawl(
    queue: Arc<SegQueue<String>>,
    visited: Arc<DashSet<String>>,
    base_url: Url,
) -> Result<(), FetchError> {
    let mut handles = Vec::new();

    loop {
        // Attempt to dequeue a URL
        let url_option = queue.pop();
        let url = match url_option {
            Some(url) => url,
            None => {
                // Queue is empty; check if all permits are available
                if SEMAPHORE.available_permits() == MAX_CONCURRENT_TASKS {
                    break;
                }
                tokio::time::sleep(tokio::time::Duration::from_millis(100)).await;
                continue;
            }
        };

        // Check and insert into visited
        if !visited.insert(url.clone()) {
            continue; // Already visited
        }

        // Acquire semaphore permit
        let _permit = SEMAPHORE.clone().acquire_owned().await.unwrap();

        // Clone references for the async task
        let queue_inner = Arc::clone(&queue);
        let visited_inner = Arc::clone(&visited);
        let base_inner = base_url.clone();

        // Spawn the task
        let handle = task::spawn(async move {
            // Fetch the page
            match fetch_page(&url).await {
                Ok(body) => {
                    // Parse HTML
                    let (title, description) = crate::parser::get_meta_and_title(&body);

                    // Print the extracted data
                    println!("URL: {}", url);
                    println!("Title: {:?}", title);
                    println!("Description: {:?}", description);

                    // Extract and enqueue links
                    let links = crate::parser::extract_links(&body, &base_inner);
                    for link in links {
                        if let Some(sanitized) = crate::parser::sanitize_link(&link) {
                            if !visited_inner.contains(&sanitized) {
                                queue_inner.push(sanitized);
                            }
                        }
                    }
                }
                Err(e) => {
                    eprintln!("Error fetching {}: {}", url, e);
                }
            }
            // Permit is automatically released when `_permit` goes out of scope
        });

        handles.push(handle);
    }

    // Await all tasks
    for handle in handles {
        let _ = handle.await;
    }

    Ok(())
}
