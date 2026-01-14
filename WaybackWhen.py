# Install required Python packages
!pip install requests beautifulsoup4 waybackpy selenium webdriver-manager

# Install google-chrome-stable for better compatibility with ChromeDriver
!wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
!echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | tee /etc/apt/sources.list.d/google-chrome.list
!apt-get update && apt-get install -y google-chrome-stable

import requests
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning
from urllib.parse import urljoin, urlparse, parse_qs, urlencode, urlunparse # Added urlunparse
from collections import OrderedDict # Import OrderedDict for sorted query parameters
import waybackpy
from datetime import datetime, timedelta, timezone
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import concurrent.futures
from collections import deque
import threading
import warnings
from IPython.display import clear_output # Import clear_output for console management

# Import selenium components
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService # Import ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By # Import By for CAPTCHA detection
from selenium.common.exceptions import TimeoutException, WebDriverException # Import TimeoutException and WebDriverException

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

# Define Settings Dictionary
SETTINGS = {
    'archiving_cooldown': 7, # Default cooldown in days
    'urls_per_minute_limit': 15, # Max URLs to archive per minute
    'max_crawler_workers': 0, # Max concurrent workers for website crawling (0 for unlimited) - affects RAM usage massively
    'archiving_retries': 5, # Max retries for archiving a single link
    'default_archiving_action': 'n' # Default archiving action: 'n' (Normal), 'a' (Archive All), 's' (Skip All)
}

# Define a threading.local() object at the module level for WebDriver instances
_thread_local = threading.local()
clear_output(wait=True)
# Function to set up and return a headless Chrome WebDriver
def get_driver():
    options = Options()
    options.add_argument("--headless") # Run Chrome in headless mode
    options.add_argument("--no-sandbox") # Bypass OS security model, required for Colab
    options.add_argument("--disable-dev-shm-usage") # Overcome limited resource problems
    options.add_argument("--disable-gpu") # Added for headless stability
    # Explicitly set the binary location for google-chrome-stable
    options.binary_location = '/usr/bin/google-chrome'
    # Optionally, add a user-agent to mimic a regular browser
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    # Initialize ChromeDriver using webdriver_manager to handle downloads and setup
    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_page_load_timeout(240) # Set page load timeout to 240 seconds (4 minutes)
    driver.command_executor.set_timeout(300) # Set command executor timeout to 300 seconds (5 minutes)
    return driver



# Configure a retry strategy once, to be used for each new session
retry_strategy = Retry(
    total=5,
    backoff_factor=1,
    status_forcelist=[403, 404, 429, 500, 502, 503, 504],
    allowed_methods=False # Apply retry to all HTTP methods
)
adapter = HTTPAdapter(max_retries=retry_strategy)

# Global dictionary to store the last access time for each domain
# Removed: last_domain_access_time = {}
# Lock to manage concurrent access to last_domain_access_time
# Removed: domain_cooldown_lock = threading.Lock()

# Define irrelevant extensions and path segments globally
IRRELEVANT_EXTENSIONS = ('.pdf', '.zip', '.tar', '.gz', '.rar', '.7z', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.mp4', '.avi', '.mov', '.mp3', '.wav', '.flac', '.iso', '.exe', '.dmg', '.pkg', '.apk')
IRRELEVANT_PATH_SEGMENTS = ('/cdn-cgi/', '/assets/', '/uploads/', '/wp-content/', '/wp-includes/', '/themes/', '/plugins/', '/node_modules/', '/static/', '/javascript/', '/css/', '/img/')

def normalize_url(url):
    """Normalizes a URL for consistent comparison and deduplication."""
    parsed_url = urlparse(url)

    # Lowercase scheme and netloc for consistency
    scheme = parsed_url.scheme.lower()
    netloc = parsed_url.netloc.lower()

    # Remove fragments
    path = parsed_url.path

    # Remove trailing slashes from path, but keep for root '/'
    if path.endswith('/') and path != '/':
        path = path.rstrip('/')

    # Sort query parameters for consistent URLs
    query_params = parse_qs(parsed_url.query)

    # Remove common tracking parameters
    tracking_params = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content', 'gclid', 'fbclid', 'ref', 'src', 'cid', 'referrer']
    for param in tracking_params:
        query_params.pop(param, None)

    # Reconstruct query string with sorted parameters
    sorted_query_params = OrderedDict(sorted(query_params.items()))
    query = urlencode(sorted_query_params, doseq=True)

    return urlunparse((scheme, netloc, path, parsed_url.params, query, ''))


def get_internal_links(base_url, driver): # Modified to accept a driver object
    """Scrapes a given URL to find all internal links and returns them as a set.

    This function uses a browser-like User-Agent and retry logic for robustness.
    Contributors: Consider enhancing error handling for different HTTP status codes or improving URL normalization.
    """
    links = set()

    # Extract the domain from the base_url
    parsed_base_url = urlparse(base_url)
    domain = parsed_base_url.netloc

    retries = SETTINGS.get('crawler_retries', 3) # Use a setting for crawler retries, default to 3
    attempt = 0
    while attempt < retries:
        try:
            # Navigate to the base_url using Selenium
            driver.get(base_url)

            # CAPTCHA Detection
            captcha_indicators = [
                (By.ID, 'g-recaptcha'),
                (By.CLASS_NAME, 'g-recaptcha'),
                (By.XPATH, "//iframe[contains(@src, 'google.com/recaptcha')]")
            ]
            captcha_detected = False
            for by_type, value in captcha_indicators:
                if driver.find_elements(by_type, value):
                    captcha_detected = True
                    break

            if captcha_detected:
                while True:
                    print(f"[CAPTCHA DETECTED] for {base_url}.\nPlease solve the CAPTCHA manually in the browser if it becomes visible.\nType 'continue' to resume crawling or 'skip' to skip this URL:")
                    user_choice = input().strip().lower()
                    if user_choice == 'continue':
                        print("Attempting to continue after manual intervention...")
                        break # Break the loop to re-attempt processing the page
                    elif user_choice == 'skip':
                        print(f"Skipping {base_url} due to CAPTCHA.")
                        return links # Return empty set if CAPTCHA detected and skipped
                    else:
                        print("Invalid input. Please type 'continue' or 'skip'.")

            # Parse the HTML content of the page using BeautifulSoup from driver.page_source
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            # Extract the domain name from the base_url to identify internal links
            # domain = parsed_base_url.netloc # Already defined above

            # Find all anchor tags (<a>) that have an 'href' attribute
            for anchor in soup.find_all('a', href=True):
                href = anchor['href']

                # REMOVED: Skip links that are fragments, mailto links, javascript, or contain 'action='
                # These are typically not relevant for archiving content.
                # if href.startswith(('#', 'mailto:', 'javascript:')) or 'action=' in href:
                #    continue

                # --- NEW FILTERING STEPS ---
                # REMOVED: Skip links if their href ends with any irrelevant extension
                # if any(href.lower().endswith(ext) for ext in IRRELEVANT_EXTENSIONS):
                #     continue

                # REMOVED: Skip links if their href contains any irrelevant path segment
                # if any(segment in href.lower() for segment in IRRELEVANT_PATH_SEGMENTS):
                #     continue
                # --- END NEW FILTERING STEPS --nTIL THIS LINE

                # Resolve relative URLs to absolute URLs
                full_url = urljoin(base_url, href)
                parsed_full_url = urlparse(full_url)

                # Check if the parsed URL's domain matches the base URL's domain
                # This ensures only internal links are collected.
                if parsed_full_url.netloc == domain:
                    # Construct a clean URL without query parameters or fragments
                    # Now using the normalize_url helper function
                    clean_url = normalize_url(full_url)
                    links.add(clean_url)
            return links # If successful, break retry loop and return links

        # Handle specific HTTP errors during the request (Selenium errors are different from requests)
        except TimeoutException:
            print(f"[!] Page load timed out for {base_url}. Retrying ({retries - attempt - 1} attempts left).")
            attempt += 1
            time.sleep(2) # Short delay before retrying
        except WebDriverException as e:
            print(f"[!] A WebDriver error occurred while crawling {base_url}: {e}. Retrying ({retries - attempt - 1} attempts left).")
            attempt += 1
            time.sleep(2) # Short delay before retrying
        except Exception as e:
            print(f"[!] An unexpected error occurred while crawling {base_url} with Selenium: {e}. Retrying ({retries - attempt - 1} attempts left).")
            attempt += 1
            time.sleep(2) # Short delay before retrying
    print(f"[!] Failed to retrieve {base_url} after {retries} attempts.")
    return links

def should_archive(url, global_archive_action):
    """Determines if a URL should be archived based on a global action or a custom check.

    Contributors: Consider adding more sophisticated checks for archiving, e.g., checking content changes.
    """
    user_agent = "ArchiveRequestBot/1.0" # Define a user agent for Wayback Machine requests
    wayback = waybackpy.Url(url, user_agent) # Initialize WaybackPy URL object

    # If the global action is 'a' (Archive All) or 's' (Skip All), we just return the boolean
    # and let the calling function handle consolidated printing.
    if global_archive_action == 'a':
        return True, wayback
    elif global_archive_action == 's':
        return False, wayback

    # If global_archive_action is 'n' (Normal), proceed with the 48-hour check logic.
    # Implement retry logic for should_archive as well
    retries = SETTINGS.get('archiving_retries', 3) # Use the archiving retries setting
    attempt = 0
    while attempt < retries:
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
            attempt += 1
            if attempt < retries:
                print(f"[!] An error occurred while checking archive for {url}: {e}. Retrying ({retries - attempt} attempts left).")
                time.sleep(5) # Wait before retrying the archive check
            else:
                print(f"[!] Failed to check archive for {url} after {retries} attempts: {e}. Skipping.")
                return False, wayback # Skip this URL if all retries fail
    return False, wayback # Should not be reached if retries are handled correctly or success occurs

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
        retries = SETTINGS['archiving_retries'] # Number of retries for archiving a single link
        while retries > 0:
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

                retries -= 1
                if rate_limit_keyword in error_message:
                    # If rate limit hit, automatically pause for 5 minutes and retry
                    print(f"[!] Wayback Machine rate limit hit for {link}. Pausing for 5 minutes before retrying ({retries} attempts left)....")
                    time.sleep(300) # Pause for 5 minutes (300 seconds)
                elif retries > 0:
                    print(f"[!] Could not save {link}: {e}. Retrying ({retries} attempts left)...")
                    time.sleep(2) # Short cooldown before next retry for other errors
                else:
                    # If no retries left, report failure
                    return f"[!] Failed to archive {link} after multiple attempts: {e}"
        return f"[!] Failed to archive {link} after multiple attempts." # Return after retry loop finishes
    else:
        return f"Skipped: {link}"

# Wrapper function to manage thread-local driver instances
def wrapper_get_internal_links(url_to_crawl):
    # Check if a WebDriver instance already exists for the current thread
    if not hasattr(_thread_local, 'driver'):
        # If no driver exists, create a new one and store it in _thread_local
        _thread_local.driver = get_driver()

    # Use the thread-local driver for scraping
    links = get_internal_links(url_to_crawl, _thread_local.driver)
    return links

def crawl_website(base_url):
    """
    Performs a breadth-first search (BFS) to discover all internal links within a given base URL.
    Uses parallel processing for efficient scraping.
    """
    # Initialize a deque (double-ended queue) for BFS, starting with the base_url
    queue = deque([base_url])
    # Keep track of visited URLs to avoid redundant processing and infinite loops
    visited_urls = {base_url}
    # Stores all unique internal links discovered during the crawl
    all_unique_internal_links = {base_url}

    try:
        # Determine max_workers based on SETTINGS
        max_workers = SETTINGS['max_crawler_workers']
        if max_workers == 0:
            max_workers = None # Set to None for unlimited workers (ThreadPoolExecutor default)

        # Use ThreadPoolExecutor for concurrent processing of `wrapper_get_internal_links` calls
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            while queue:
                # Define a batch size for processing URLs in parallel
                batch_size = SETTINGS['max_crawler_workers'] if SETTINGS['max_crawler_workers'] > 0 else 65 # Use max_crawler_workers as batch size, or a reasonable default if unlimited
                current_batch_urls = [] # Stores just URLs, no longer (url, driver) tuples

                # Populate the batch with URLs from the queue, up to `batch_size`
                while queue and len(current_batch_urls) < batch_size:
                    url_to_crawl = queue.popleft() # Get the next URL from the front of the queue
                    current_batch_urls.append(url_to_crawl) # Append just the URL

                # If the current batch is empty, there are no more URLs to process
                if not current_batch_urls:
                    break

                print(f"Processing batch of {len(current_batch_urls)} URLs for crawling.")

                # Submit `wrapper_get_internal_links` for each URL in the batch to the executor.
                for new_links_from_url in executor.map(wrapper_get_internal_links, current_batch_urls):
                    # Ensure new_links_from_url is an iterable (e.g., set), even if an error occurred in wrapper_get_internal_links
                    if new_links_from_url is None: # This should not happen if wrapper_get_internal_links always returns a set
                        continue # Skip if wrapper_get_internal_links somehow returns None

                    for link in new_links_from_url:
                        all_unique_internal_links.add(link) # Add discovered link to the overall set
                        # Print discovered URL if it's new
                        if link not in visited_urls:
                            print(f"[DISCOVERED] {link}")
                            visited_urls.add(link)
                            queue.append(link)
    except Exception as e:
        print(f"An error occurred during website crawling: {e}")
        return set() # Explicitly return an empty set on error
    finally:
        # Note: WebDriver instances are no longer explicitly quit after each URL.
        # They will persist for the lifetime of their respective worker threads within the ThreadPoolExecutor.
        # Proper cleanup (driver.quit()) should ideally be handled when the ThreadPoolExecutor itself shuts down,
        # which might require more advanced patterns for explicit resource management with concurrent.futures.
        pass

    return all_unique_internal_links

def main():
    """
    Main function to orchestrate the website crawling and archiving process.

    Contributors: Consider adding command-line argument parsing for URLs, or integrating a configuration file.
    """
    clear_output(wait=True) # Clear output at the very beginning for a cleaner console

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

    # Clear previous output before asking for archiving action to keep the console clean
    clear_output(wait=True)

    # Set global archiving action based on SETTINGS, with validation and fallback
    global_choice = SETTINGS.get('default_archiving_action', 'n').lower() # Default to 'n' if not set or invalid
    valid_choices = ['a', 'n', 's']
    if global_choice not in valid_choices:
        print(f"Invalid default_archiving_action '{global_choice}' found in SETTINGS. Falling back to 'Normal' archiving.")
        global_choice = 'n'

    # Print consolidated message for 'Archive All' or 'Skip All' actions
    if global_choice == 'a':
        print(f"Archiving action from settings: Archive All. Archiving all {len(all_discovered_links)} discovered links.")
    elif global_choice == 's':
        print(f"Archiving action from settings: Skip All. Skipping all {len(all_discovered_links)} discovered links.")
    elif global_choice == 'n':
        print(f"Archiving action from settings: Normal. Archiving normally (respecting {SETTINGS['archiving_cooldown']*24}h rule) for {len(all_discovered_links)} discovered links.")

    # Clear output again before the final summary for cleanliness
    clear_output(wait=True)

    results = [] # List to store the results of archiving attempts
    # Iterate through all discovered unique links (sorted for consistent output)
    for link in sorted(list(all_discovered_links)):
        # Process each link for archiving based on the global choice
        results.append(process_link_for_archiving(link, global_choice))

    # Clear output again before the final summary for cleanliness
    clear_output(wait=True)

    print("\n--- Archiving Summary ---")
    for result in results:
        print(result)

if __name__ == "__main__":
    main()
