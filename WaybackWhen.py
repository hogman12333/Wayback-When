import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import waybackpy
from datetime import datetime, timedelta, timezone
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import concurrent.futures
from collections import deque
import threading

SETTINGS = {
    'archiving_cooldown': 2, # Default cooldown in days
    'urls_per_minute_limit': 15, # Max URLs to archive per minute
    'max_crawler_workers': 15 # Max concurrent workers for website crawling
}

def get_internal_links(base_url):
    """Scrapes a given URL to find all internal links and returns them as a set.

    This function uses a browser-like User-Agent and retry logic for robustness.
    Contributors: Consider enhancing error handling for different HTTP status codes or improving URL normalization.
    """
    links = set()

    # Mimic a common browser User-Agent to avoid being blocked by some websites
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
    }

    # Configure a retry strategy for robust HTTP requests
    # It retries on specific status codes (e.g., 403, 404, 429, 5xx) up to 5 times
    # with an exponential backoff factor.
    retry_strategy = Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=[403, 404, 429, 500, 502, 503, 504],
        allowed_methods=False # Apply retry to all HTTP methods
    )
    # Mount the adapter to the session to enable retries for both http and https
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session = requests.Session()
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    try:
        # Send a GET request to the base_url using the configured session and headers
        # A timeout is set to prevent requests from hanging indefinitely.
        response = session.get(base_url, headers=headers, timeout=15)
        # Raise an HTTPError for bad responses (4xx or 5xx client/server errors)
        response.raise_for_status()

        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        # Extract the domain name from the base_url to identify internal links
        domain = urlparse(base_url).netloc

        # Find all anchor tags (<a>) that have an 'href' attribute
        for anchor in soup.find_all('a', href=True):
            href = anchor['href']

            # Skip links that are fragments, mailto links, javascript, or contain 'action='
            # These are typically not relevant for archiving content.
            if href.startswith(('#', 'mailto:', 'javascript:')) or 'action=' in href:
                continue

            # Resolve relative URLs to absolute URLs
            full_url = urljoin(base_url, href)
            parsed_url = urlparse(full_url)

            # Check if the parsed URL's domain matches the base URL's domain
            # This ensures only internal links are collected.
            if parsed_url.netloc == domain:
                # Construct a clean URL without query parameters or fragments
                clean_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
                links.add(clean_url)

    # Handle specific HTTP errors during the request
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error crawling {base_url}: {e}")
    # Handle general request exceptions (e.g., connection errors, timeouts)
    except requests.exceptions.RequestException as e:
        print(f"Request Error crawling {base_url}: {e}")
    # Catch any other unexpected errors
    except Exception as e:
        print(f"An unexpected error occurred while crawling {base_url}: {e}")

    return links

def should_archive(url, global_archive_action):
    """Determines if a URL should be archived based on a global action or a custom check.

    Contributors: Consider adding more sophisticated checks for archiving, e.g., checking content changes.
    """
    user_agent = "ArchiveRequestBot/1.0" # Define a user agent for Wayback Machine requests
    wayback = waybackpy.Url(url, user_agent) # Initialize WaybackPy URL object

    # If the global action is 'a' (Archive All), immediately return True to archive.
    if global_archive_action == 'a':
        print(f"Global choice: Archiving all for {url}.")
        return True, wayback
    # If the global action is 's' (Skip All), immediately return False to skip.
    elif global_archive_action == 's':
        print(f"Global choice: Skipping all for {url}.")
        return False, wayback

    # If global_archive_action is 'n' (Normal), proceed with the 48-hour check logic.
    while True:
        try:
            # Get the most recent archive record for the URL from Wayback Machine
            newest = wayback.newest()
            # Extract the timestamp of the last archive and make it timezone-aware (UTC)
            # WaybackPy's timestamp is naive but represents UTC, so we make it explicit.
            last_archived_dt = newest.timestamp.replace(tzinfo=timezone.utc)

            # Get the current UTC time for comparison
            current_utc_dt = datetime.now(timezone.utc)
            # Calculate the time difference since the last archive
            time_diff = current_utc_dt - last_archived_dt

            # If the last archive was less than `archiving_cooldown` days ago, skip archiving
            if time_diff < timedelta(days=SETTINGS['archiving_cooldown']):
                print(f"[-] Skipping: {url} (Last archived {time_diff.total_seconds() // 3600:.1f} hours ago)")
                return False, wayback
            # Otherwise, the URL needs archiving
            else:
                print(f"[+] Needs Archive: {url} (Last archived {time_diff.total_seconds() // 3600:.1f} hours ago, > {SETTINGS['archiving_cooldown']*24} hours)")
                return True, wayback

        # Handle cases where no existing archive record is found for the URL
        except waybackpy.exceptions.NoCDXRecordFound:
            print(f"[!] No existing archive found for {url}. Archiving.")
            return True, wayback
        # Handle other unexpected errors during the archive check
        except Exception as e:
            print(f"[!] An error occurred while checking archive for {url}: {e}")
            # Prompt the user to retry or skip the URL in case of an error
            user_choice = input("Type 'retry' to try again or 'skip' to skip this URL: ").strip().lower()
            if user_choice == 'retry':
                print("Retrying in 5 seconds...")
                time.sleep(5) # Wait before retrying the archive check
            elif user_choice == 'skip':
                print(f"Skipping {url} due to user request.")
                return False, wayback # Skip this URL if user chooses to
            else:
                print("Invalid input. Please type 'retry' or 'skip'.")

# A lock to ensure only one thread modifies `last_archive_time` at a time
archive_lock = threading.Lock()
# Timestamp of the last archive request, initialized to 0.0
last_archive_time = 0.0
# Minimum delay required between archive requests to respect rate limits
MIN_ARCHIVE_DELAY_SECONDS = 60 / SETTINGS['urls_per_minute_limit']

def process_link_for_archiving(link, global_archive_action):
    """Checks if a link needs archiving and attempts to save it to Wayback Machine with rate limiting and retries.

    Contributors: Optimizing rate limiting or adding more detailed logging for archive results would be valuable.
    """
    global last_archive_time

    # Determine if the link needs to be saved based on global action or 48-hour rule
    needs_save, wb_obj = should_archive(link, global_archive_action)

    if needs_save:
        retries = 3 # Number of retries for archiving a single link
        while True:
            # Acquire a lock to safely manage the global rate limit timer
            with archive_lock:
                now = time.time() # Current time
                elapsed = now - last_archive_time # Time since the last archive request
                # If the elapsed time is less than the minimum required delay, pause.
                if elapsed < MIN_ARCHIVE_DELAY_SECONDS:
                    sleep_duration = MIN_ARCHIVE_DELAY_SECONDS - elapsed
                    print(f"[RATE LIMIT] Sleeping for {sleep_duration:.2f} seconds before archiving {link}")
                    time.sleep(sleep_duration)

                # Update the last archive time after potentially sleeping
                last_archive_time = time.time()

            try:
                print(f"[+] Archiving: {link}...")
                wb_obj.save() # Attempt to save the URL to Wayback Machine
                return f"Successfully archived: {link}"
            except Exception as e:
                error_message = str(e)
                # Check for a specific rate limit error message from Wayback Machine
                rate_limit_keyword = 'Save request refused by the server. Save Page Now limits saving 15 URLs per minutes.'

                if rate_limit_keyword in error_message:
                    # If rate limit hit, prompt user for action (retry or skip)
                    while True:
                        user_choice = input(f"Wayback Machine rate limit hit for {link}. Type 'R' to retry after 5 minutes or 'S' to skip this URL: ").strip().lower()
                        if user_choice == 'r':
                            print("Pausing for 5 minutes as requested...")
                            time.sleep(300) # Pause for 5 minutes (300 seconds)
                            break # Break from this inner loop to re-attempt archiving
                        elif user_choice == 's':
                            print(f"Skipping {link} as requested.")
                            return f"User skipped archiving due to rate limit: {link}"
                        else:
                            print("Invalid input. Please type 'R' or 'S'.")
                else:
                    # For other errors, decrement retry count and retry if attempts remain
                    retries -= 1
                    if retries > 0:
                        print(f"[!] Could not save {link}: {e}. Retrying ({retries} attempts left)...")
                        time.sleep(2) # Short cooldown before next retry for other errors
                    else:
                        # If no retries left, report failure
                        return f"[!] Failed to archive {link} after multiple attempts: {e}"
    else:
        return f"Skipped: {link}"

def crawl_website(base_url):
    """
    Performs a breadth-first search (BFS) to discover all internal links within a given base URL.
    Uses parallel processing for efficient scraping.

    Contributors: Optimizing the BFS algorithm (e.g., using a faster data structure for visited URLs),
    or improving the parallel processing strategy could be future enhancements.
    """
    # Initialize a deque (double-ended queue) for BFS, starting with the base_url
    queue = deque([base_url])
    # Keep track of visited URLs to avoid redundant processing and infinite loops
    visited_urls = {base_url}
    # Stores all unique internal links discovered during the crawl
    all_unique_internal_links = {base_url}

    # Use ThreadPoolExecutor for parallel processing of `get_internal_links` calls
    # `max_crawler_workers` allows for up to that many concurrent scraping operations.
    with concurrent.futures.ThreadPoolExecutor(max_workers=SETTINGS['max_crawler_workers']) as executor:
        while queue:
            # Define a batch size for processing URLs in parallel
            batch_size = SETTINGS['max_crawler_workers'] # Use max_crawler_workers as batch size
            current_batch_urls = []

            # Populate the batch with URLs from the queue, up to `batch_size`
            while queue and len(current_batch_urls) < batch_size:
                url_to_crawl = queue.popleft() # Get the next URL from the front of the queue
                current_batch_urls.append(url_to_crawl)

            # If the current batch is empty, there are no more URLs to process
            if not current_batch_urls:
                break

            print(f"Processing batch of {len(current_batch_urls)} URLs for crawling.")

            # Submit `get_internal_links` for each URL in the batch to the executor.
            # `executor.map` applies the function to all items in `current_batch_urls` concurrently
            # and returns results in the order the calls were made.
            for new_links_from_url in executor.map(get_internal_links, current_batch_urls):
                for link in new_links_from_url:
                    all_unique_internal_links.add(link) # Add discovered link to the overall set
                    # If the link has not been visited yet, add it to the queue for future crawling
                    if link not in visited_urls:
                        visited_urls.add(link)
                        queue.append(link)

    return all_unique_internal_links

def main():
    """Main function to orchestrate the website crawling and archiving process.

    Contributors: Consider adding command-line argument parsing for URLs, or integrating a configuration file.
    """
    # Prompt the user to enter one or more URLs
    target_urls_input = input("Enter URLs (comma-separated, e.g., https://notawebsite.org/, https://example.com/): ").strip()
    # Split the input string by commas and clean up whitespace, filtering out empty strings
    initial_urls = [url.strip() for url in target_urls_input.split(',') if url.strip()]

    # If no valid URLs were entered, exit the function
    if not initial_urls:
        print("No valid URLs entered.")
        return

    all_discovered_links = set() # Set to store all unique internal links found across all initial URLs
    for url in initial_urls:
        # Basic validation to ensure the URL starts with 'http' or 'https'
        if not url.startswith("http"):
            print(f"Invalid URL format for {url}. Skipping.")
            continue
        print(f"\nStarting crawl for initial URL: {url}")
        # Perform the BFS crawl for each initial URL
        discovered_links_for_url = crawl_website(url)
        # Add all links discovered from the current URL to the master set
        all_discovered_links.update(discovered_links_for_url)

    print(f"Found {len(all_discovered_links)} unique internal links across all initial URLs.")

    # Loop until a valid global archiving action is chosen by the user
    while True:
        global_choice = input(f"Choose global archiving action: 'A' (Archive All), 'N' (Archive Normally - respecting {SETTINGS['archiving_cooldown']*24}h rule), 'S' (Skip All): ").strip().lower()
        if global_choice in ['a', 'n', 's']:
            break # Exit loop if input is valid
        else:
            print("Invalid input. Please enter 'A', 'N', or 'S'.")

    results = [] # List to store the results of archiving attempts
    # Iterate through all discovered unique links (sorted for consistent output)
    for link in sorted(list(all_discovered_links)):
        # Process each link for archiving based on the global choice
        results.append(process_link_for_archiving(link, global_choice))

    # Print a summary of all archiving attempts
    print("\n--- Archiving Summary ---")
    for result in results:
        print(result)

if __name__ == "__main__":
    main()
