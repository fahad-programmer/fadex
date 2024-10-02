// src/crawler.rs

use crate::parser::{extract_links, sanitize_link};
use tokio::sync::Semaphore;
use std::sync::Arc;
use crossbeam::queue::SegQueue;
use dashmap::DashSet;
use tokio::task;
use lazy_static::lazy_static;
use url::Url;
use reqwest;

// Constants
const MAX_CONCURRENT_TASKS: usize = 100;

// Initialize a global semaphore to limit concurrency
lazy_static! {
    static ref SEMAPHORE: Arc<Semaphore> = Arc::new(Semaphore::new(MAX_CONCURRENT_TASKS));
}

/// Asynchronously crawls web pages starting from the URLs in the queue.
pub async fn crawl(
    queue: Arc<SegQueue<String>>,
    visited: Arc<DashSet<String>>,
    base_url: Url,
) {
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

        // Clone for the task
        let queue_inner = Arc::clone(&queue);
        let visited_inner = Arc::clone(&visited);
        let base_inner = base_url.clone();

        // Spawn the task
        let handle = task::spawn(async move {
            // Fetch the page
            match fetch_page(&url).await {
                Ok(body) => {
                    // Parse HTML
                    let (title, description) = crate::parser::parse_html(&body);

                    // Print the extracted data
                    println!("URL: {}", url);
                    println!("Title: {:?}", title);
                    println!("Description: {:?}", description);

                    // Extract and enqueue links
                    let links = extract_links(&body, &base_inner);
                    for link in links {
                        if let Some(sanitized) = sanitize_link(&link) {
                            if !visited_inner.contains(&sanitized) {
                                queue_inner.push(sanitized);
                            }
                        }
                    }
                }
                Err(e) => {
                    eprintln!("Error fetching {}: {:?}", url, e);
                }
            }
            // Permit is automatically released when `permit` goes out of scope
        });

        handles.push(handle);
    }

    // Await all tasks
    for handle in handles {
        let _ = handle.await;
    }
}

/// Fetches the content of the given URL.
async fn fetch_page(url: &str) -> Result<String, reqwest::Error> {
    let response = reqwest::get(url).await?;
    let content = response.text().await?;
    Ok(content)
}
