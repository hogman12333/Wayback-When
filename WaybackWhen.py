# Install required Python packages
!pip install --upgrade requests beautifulsoup4 waybackpy selenium webdriver-manager selenium-stealth

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
import random # Import random for selecting user-agents and sleep times

# Import selenium components
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService # Import ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By # Import By for CAPTCHA detection
from selenium.common.exceptions import TimeoutException, WebDriverException # Import TimeoutException and WebDriverException
from selenium_stealth import stealth

import networkx as nx # Import networkx
import matplotlib.pyplot as plt # Import matplotlib for plotting

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

# Custom exception for CAPTCHA detection
class CaptchaDetectedError(Exception):
    """Custom exception to indicate that a CAPTCHA was detected."""
    pass

# Define Settings Dictionary
SETTINGS = {
    'archiving_cooldown': 7, # Default cooldown in days
    'urls_per_minute_limit': 15, # Max URLs to archive per minute
    'max_crawler_workers': 0, # Max concurrent workers for website crawling (0 for unlimited) - affects RAM usage massively
    'retries': 5, # Max retries for archiving a single link
    'default_archiving_action': 'N', # Default archiving action: 'n' (Normal), 'a' (Archive All), 's' (Skip All)
    'debug_mode': False, # Set to True to enable debug messages, False to disable
    'max_archiver_workers': 0,
    'enable_visual_tree_generation': False #setting for visual tree generation-incredibly ram intensive
}

# Define a threading.local() object at the module level for WebDriver instances
_thread_local = threading.local()

# Lock to ensure only one CAPTCHA prompt is active at a time
captcha_prompt_lock = threading.Lock()

# Define User-Agent components for dynamic generation
OS_TYPES = [
    "Windows NT 10.0; Win64; x64",
    "Windows NT 6.3; Win64; x64",
    "Windows NT 6.2; Win64; x64",
    "Windows NT 6.1; Win64; x64",
    "Macintosh; Intel Mac OS X 10_15_7",
    "Macintosh; Intel Mac OS X 10_14_6",
    "Macintosh; Intel Mac OS X 10_13_6",
    "X11; Linux x86_64",
    "X11; Ubuntu; Linux x86_64",
    "X11; CrOS x86_64 15329.74.0",
    "Linux; Android 13; SM-G998B",
    "Linux; Android 12; Pixel 6",
    "Linux; Android 10; SM-A505FN",
    "iPhone; CPU iPhone OS 17_0 like Mac OS X",
    "iPhone; CPU iPhone OS 16_0 like Mac OS X",
    "iPad; CPU OS 17_0 like Mac OS X",
    "iPad; CPU OS 16_0 like Mac OS X",
]

BROWSER_TYPES = [
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version}.0.0.0 Safari/537.36",
    "AppleWebKit/537.36 (KHTML, like Gecko) Firefox/{version}.0",
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/{version}.1 Safari/605.1.15",
    "AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/{version}.0.0.0 Mobile/15E148 Safari/604.1"
]

CHROME_VERSIONS = [str(v) for v in range(1, 126)]
FIREFOX_VERSIONS = [str(v) for v in range(1, 126)]
SAFARI_VERSIONS = [str(v) for v in range(1, 18)]

def generate_random_user_agent():
    os = random.choice(OS_TYPES)
    browser_template = random.choice(BROWSER_TYPES)

    if "Chrome" in browser_template:
        version = random.choice(CHROME_VERSIONS)
    elif "Firefox" in browser_template:
        version = random.choice(FIREFOX_VERSIONS)
    elif "Safari" in browser_template or "CriOS" in browser_template:
        version = random.choice(SAFARI_VERSIONS)
    else:
        version = "100" # Default or fallback version

    browser = browser_template.format(version=version)
    return f"Mozilla/5.0 ({os}) {browser}"

# Possible platforms, webgl_vendors, and renderers for randomization
STEALTH_PLATFORMS = [
    "Win32",
    "Linux x86_64",
    "MacIntel"
]
STEALTH_WEBGL_VENDORS = [
    "Google Inc. (Intel)", "Intel Inc.", "NVIDIA Corporation", "Apple Inc."
]
STEALTH_RENDERERS = [
    "ANGLE (Intel, Intel(R) Iris(TM) Graphics 6100 (OpenGL 4.5), OpenGL 4.5.0)",
    "Intel Iris OpenGL Engine",
    "Google SwiftShader",
    "Metal"
]

# Function to set up and return a headless Chrome WebDriver
def get_driver():
    options = Options()
    options.add_argument("--headless") # Run Chrome in headless mode
    options.add_argument("--no-sandbox") # Bypass OS security model, required for Colab
    options.add_argument("--disable-dev-shm-usage") # Overcome limited resource problems
    options.add_argument("--disable-gpu") # Added for headless stability
    # Explicitly set the binary location for google-chrome-stable
    options.binary_location = '/usr/bin/google-chrome'

    # Configure Chrome to not download files automatically
    prefs = {
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
        "download.default_directory": "/dev/null" # Set a dummy directory, downloads will be suppressed
    }
    options.add_experimental_option("prefs", prefs)

    # Initialize ChromeDriver using webdriver_manager to handle downloads and setup
    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # Apply selenium-stealth with randomized parameters
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform=random.choice(STEALTH_PLATFORMS),
            webgl_vendor=random.choice(STEALTH_WEBGL_VENDORS),
            renderer=random.choice(STEALTH_RENDERERS),
            fix_hairline=True,
            )

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

# Define irrelevant extensions and path segments globally
IRRELEVANT_EXTENSIONS = ('.3g2', '.3gp', '.7z', '.aac', '.accdb', '.ace', '.aif', '.aiff', '.ai', '.apk', '.arj', '.arw', '.asm', '.azw3', '.bak', '.bash', '.bin', '.blend', '.bmp', '.bz2', '.cab', '.cache', '.c', '.cso', '.conf', '.cpp', '.cr2', '.crt', '.cs', '.csv', '.dat', '.dae', '.deb', '.dmg', '.doc', '.docx', '.drv', '.dxf', '.dwg', '.eml', '.eps', '.epub', '.exe', '.fbx', '.fish', '.flac', '.flv', '.fon', '.gb', '.gba', '.gif', '.go', '.gz', '.h', '.har', '.hpp', '.ics', '.ico', '.igs', '.img', '.ini', '.iso', '.java', '.jpeg', '.jpg', '.js', '.json', '.key', '.kt', '.kts', '.lock', '.log', '.lua', '.lz', '.lzma', '.m', '.map', '.max', '.mdb', '.mid', '.midi', '.mkv', '.mobi', '.mov', '.mp3', '.mp4', '.mpg', '.mpeg', '.msg', '.msi', '.msm', '.msp', '.nef', '.nes', '.obj', '.odp', '.ods', '.odt', '.ogg', '.old', '.opus', '.orf', '.otf', '.pak', '.pcap', '.pcapng', '.pem', '.pdf', '.php', '.pl', '.ply', '.png', '.ppt', '.pptx', '.prn', '.ps', '.py', '.qbb', '.qbw', '.qfx', '.rar', '.rb', '.rm', '.rmvb', '.rom', '.rpm', '.rs', '.rtf', '.r', '.rfa', '.rvt', '.s', '.sav', '.sh', '.sit', '.sitx', '.skp', '.so', '.sqlite', '.sqlite3', '.stl', '.step', '.stp', '.sub', '.swift', '.sys', '.tar', '.temp', '.tif', '.tiff', '.tmp', '.toml', '.tsv', '.ttf', '.uue', '.vhd', '.vhdx', '.vmdk', '.vtt', '.wav', '.wbmp', '.webm', '.webp', '.wma', '.woff', '.woff2', '.wps', '.wmv', '.xcf', '.xls', '.xlsx', '.xml', '.xz', '.yaml', '.yml', '.z', '.zip', '.zsh')
IRRELEVANT_PATH_SEGMENTS = ('/cdn-cgi/', '/assets/', '/uploads/', '/wp-content/', '/wp-includes/', '/themes/', '/plugins/', '/node_modules/', '/static/', '/javascript/', '/css/', '/img/')

def log_message(level, message, debug_only=False):
    """Standardized logging function."""
    if debug_only and not SETTINGS['debug_mode']:
        return
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}][{level.upper()}] {message}")

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

def get_root_domain(netloc):
    """Extracts the root domain from a netloc (e.g., 'example.com' from 'www.example.com' or 'sub.example.com')."""
    # Lowercase for consistent comparison
    netloc = netloc.lower()
    parts = netloc.split('.')
    if len(parts) > 2 and parts[0] == 'www':
        return ".".join(parts[1:])
    elif len(parts) > 2: # For sub.example.com, take the last two parts assuming a TLD like .com, .org
        return ".".join(parts[-2:])
    return netloc # For example.com

def is_irrelevant_link(url):
    """Checks if a URL should be considered irrelevant for crawling based on extensions or path segments."""
    parsed_url = urlparse(url)
    path = parsed_url.path.lower()

    # Check for irrelevant file extensions
    if path.endswith(IRRELEVANT_EXTENSIONS):
        return True

    # Check for irrelevant path segments
    for segment in IRRELEVANT_PATH_SEGMENTS:
        if segment in path:
            return True
    return False

def get_internal_links(base_url, driver): # Modified to accept a driver object
    """Scrapes a given URL to find all internal links and returns them as a set.

    This function uses a browser-like User-Agent and retry logic for robustness.
    Contributors: Consider enhancing error handling for different HTTP status codes or improving URL normalization.
    """
    links = set()

    # Extract the domain from the base_url and its root domain
    parsed_base_url = urlparse(base_url)
    base_netloc = parsed_base_url.netloc
    base_root_domain = get_root_domain(base_netloc)
    normalized_base_url_for_comparison = normalize_url(base_url) # Normalize base_url for comparison

    log_message('DEBUG', f"Starting get_internal_links for base_url: {base_url} with base_netloc: {base_netloc} and root_domain: {base_root_domain}", debug_only=True)

    retries = SETTINGS['retries'] # Use the 'retries' setting
    attempt = 0
    while attempt < retries:
        try:
            # Select a random user agent for the current request
            random_user_agent = generate_random_user_agent() # Use the new generator
            # Set the user agent for the current request using CDP command
            driver.execute_cdp_cmd('Network.setUserAgentOverride', {'userAgent': random_user_agent})

            # Navigate to the base_url using Selenium
            driver.get(base_url)

            # Add a small delay to ensure page elements are loaded ---
            # Randomize sleep duration between 2 and 5 seconds
            time.sleep(random.uniform(2, 5))

            # CAPTCHA Detection (keep this as it is)
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
                with captcha_prompt_lock:
                    log_message('WARNING', f"CAPTCHA DETECTED for {base_url}. Waiting 5-10 seconds before attempting to continue...")
                    time.sleep(random.uniform(5, 10)) # Wait for a random time between 5 and 10 seconds
                    log_message('INFO', "Attempting to continue after automated wait...")
                    # After waiting, the code will proceed to re-attempt scraping implicitly

            # Find all anchor tags (<a>) that have an 'href' attribute using Selenium
            log_message('DEBUG', f"Page loaded for {base_url}. Extracting links...", debug_only=True)
            found_any_href = False
            for anchor_element in driver.find_elements(By.TAG_NAME, 'a'):
                href = anchor_element.get_attribute('href')
                if href:
                    found_any_href = True
                    log_message('DEBUG', f"Found href: {href}", debug_only=True)
                    # Resolve relative URLs to absolute URLs
                    full_url = urljoin(base_url, href)
                    parsed_full_url = urlparse(full_url)

                    # Check if the parsed URL's root domain matches the base URL's root domain
                    link_netloc = parsed_full_url.netloc
                    link_root_domain = get_root_domain(link_netloc)

                    clean_url = normalize_url(full_url)

                    # New check: Ensure the discovered link is the same as or a sub-path of the base_url
                    if link_root_domain == base_root_domain and clean_url.startswith(normalized_base_url_for_comparison):
                        log_message('DEBUG', f"Adding internal link: {clean_url} (Root domain: {link_root_domain}, is sub-path of base_url)", debug_only=True)
                        links.add(clean_url)
                    else:
                        log_message('DEBUG', f"Skipping external or parent link: {full_url} (Link root domain: {link_root_domain} != Base root domain: {base_root_domain} OR not sub-path of base_url)", debug_only=True)
            if not found_any_href:
                log_message('DEBUG', f"No href attributes found on {base_url} by Selenium.", debug_only=True)

            log_message('DEBUG', f"Finished processing {base_url}. Discovered {len(links)} links.", debug_only=True)
            return links # If successful, break retry loop and return links

        # Handle specific HTTP errors during the request (Selenium errors are different from requests)
        except TimeoutException:
            log_message('WARNING', f"Page load timed out for {base_url}. Retrying ({retries - attempt - 1} attempts left).")
            attempt += 1
            time.sleep(random.uniform(5, 15)) # Longer, randomized delay
        except WebDriverException as e:
            log_message('ERROR', f"A WebDriver error occurred while crawling {base_url}: {e}. Retrying ({retries - attempt - 1} attempts left).")
            attempt += 1
            time.sleep(random.uniform(5, 15)) # Longer, randomized delay
        except Exception as e:
            log_message('ERROR', f"An unexpected error occurred while crawling {base_url} with Selenium: {e}. Retrying ({retries - attempt - 1} attempts left).")
            attempt += 1
            time.sleep(random.uniform(5, 15)) # Longer, randomized delay
    log_message('ERROR', f"Failed to retrieve {base_url} after {retries} attempts.")
    return links

def should_archive(url, global_archive_action):
    """Determines if a URL should be archived based on a global action or a custom check.

    Contributors: Consider adding more sophisticated checks for archiving, e.g., checking content changes.
    """
    user_agent = generate_random_user_agent() # Use the new generator
    wayback = waybackpy.Url(url, user_agent) # Initialize WaybackPy URL object

    # If the global action is 'a' (Archive All) or 's' (Skip All), we just return the boolean
    # and let the calling function handle consolidated printing.
    if global_archive_action == 'a':
        return True, wayback
    elif global_archive_action == 's':
        return False, wayback

    # If global_archive_action is 'n' (Normal), proceed with the cooldwon check logic.
    # Implement retry logic for should_archive as well
    retries = SETTINGS.get('retries', 3) # Use the archiving retries setting
    attempt = 0
    while attempt < retries:
        try:
            # Get the most recent archive record for the URL from Wayback Machine
            newest = wayback.newest()
            # Extract the timestamp of the last archive and make it timezone-aware (UTC)
            # WaybackPy's timestamp is naive but represents UTC, so we made it explicit.
            last_archived_dt = newest.timestamp.replace(tzinfo=timezone.utc)

            # Get the current UTC time for comparison
            current_utc_dt = datetime.now(timezone.utc)
            # Calculate the time difference since the last archive
            time_diff = current_utc_dt - last_archived_dt

            # If the last archive was less than `archiving_cooldown` days ago, skip archiving
            if time_diff < timedelta(days=SETTINGS['archiving_cooldown']):
                log_message('SKIPPED', f"{url} (Last archived {time_diff.total_seconds() // 3600:.1f} hours ago)")
                return False, wayback
            # Otherwise, the URL needs archiving
            else:
                log_message('INFO', f"Needs Archive: {url} (Last archived {time_diff.total_seconds() // 3600:.1f} hours ago, > {SETTINGS['archiving_cooldown']*24} hours)")
                return True, wayback

        # Handle cases where no existing archive record is found for the URL
        except waybackpy.exceptions.NoCDXRecordFound:
            log_message('INFO', f"No existing archive found for {url}. Archiving.")
            return True, wayback
        # Handle other unexpected errors during the archive check
        except Exception as e:
            attempt += 1
            if attempt < retries:
                log_message('WARNING', f"An error occurred while checking archive for {url}: {e}. Retrying ({retries - attempt} attempts left).")
                time.sleep(5) # Wait before retrying the archive check
            else:
                log_message('ERROR', f"Failed to check archive for {url} after {retries} attempts: {e}. Defaulting to archive.")
                return True, wayback # Default to archive if all retries fail
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
        retries = SETTINGS['retries'] # Number of retries for archiving a single link
        while retries > 0:
            # Acquire a lock to safely manage the global rate limit timer
            with archive_lock:
                now = time.time() # Current time
                elapsed = now - last_archive_time # Time since the last archive request
                # If the elapsed time is less than the minimum required delay, pause.
                if elapsed < MIN_ARCHIVE_DELAY_SECONDS:
                    sleep_duration = MIN_ARCHIVE_DELAY_SECONDS - elapsed
                    log_message('RATE LIMIT', f"Sleeping for {sleep_duration:.2f} seconds before archiving {link}")
                    time.sleep(sleep_duration)

                # Update the last archive time after potentially sleeping
                last_archive_time = time.time()

            try:
                log_message('INFO', f"Archiving: {link}...")
                wb_obj.save() # Attempt to save the URL to Wayback Machine
                return f"[ARCHIVED] {link}"
            except Exception as e:
                error_message = str(e)
                # Check for a specific rate limit error message from Wayback Machine
                rate_limit_keyword = 'Save request refused by the server. Save Page Now limits saving 15 URLs per minutes.'

                retries -= 1
                if rate_limit_keyword in error_message:
                    log_message('WARNING', f"Wayback Machine rate limit hit for {link}. Pausing for 1 minute before retrying ({retries} attempts left).")
                    time.sleep(60) # Pause for 1 minutes (60 seconds)
                elif retries > 0:
                    log_message('WARNING', f"Could not save {link}: {e}. Retrying ({retries} attempts left)...")
                    time.sleep(2) # Short cooldown before next retry for other errors
                else:
                    # If no retries left, report failure
                    return f"[FAILED] Failed to archive {link} after multiple attempts: {e}"
        return f"[FAILED] Failed to archive {link} after multiple attempts."
    else:
        return f"[SKIPPED] {link}"

# Wrapper function to manage thread-local driver instances
def wrapper_get_internal_links(url_to_crawl):
    # Check if a WebDriver instance already exists for the current thread
    if not hasattr(_thread_local, 'driver'):
        # If no driver exists, create a new one and store it in _thread_local
        _thread_local.driver = get_driver()

    # Use the thread-local driver for scraping
    links = get_internal_links(url_to_crawl, _thread_local.driver)
    return links

def crawl_website(base_url, archiver_executor, archiving_futures, global_archive_action, link_relationships): # Added link_relationships
    """
    Performs a breadth-first search (BFS) to discover all internal links within a given base URL.
    Uses parallel processing for efficient scraping.
    """
    # Initialize a deque (double-ended queue) for BFS, starting with the base_url
    queue = deque()
    # Keep track of visited URLs to avoid redundant processing and infinite loops
    visited_urls = set()
    # Stores all unique internal links discovered during the crawl
    all_unique_internal_links = set()

    # Check if the base_url itself is an irrelevant link (e.g., a direct download file)
    if is_irrelevant_link(base_url):
        log_message('SKIPPED CRAWL', f"Initial URL {base_url} is an irrelevant link. Not crawling, but will attempt to archive.")
        all_unique_internal_links.add(base_url)
        visited_urls.add(base_url)
        if archiver_executor:
            log_message('DEBUG', f"Submitting initial irrelevant URL for archiving: {base_url}", debug_only=True)
            archiving_futures.append(archiver_executor.submit(process_link_for_archiving, base_url, global_archive_action))
        return all_unique_internal_links, link_relationships
    else:
        # If not an irrelevant link, proceed with normal crawling process
        queue.append(base_url)
        visited_urls.add(base_url)
        all_unique_internal_links.add(base_url)
        # Submit the base_url for archiving if an archiver_executor is provided
        if archiver_executor:
            log_message('DEBUG', f"Submitting base URL for archiving: {base_url}", debug_only=True)
            archiving_futures.append(archiver_executor.submit(process_link_for_archiving, base_url, global_archive_action))

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
                current_batch_urls = [] # Stores just URLs, no longer (url, driver)

                # Populate the batch with URLs from the queue, up to `batch_size`
                while queue and len(current_batch_urls) < batch_size:
                    url_to_crawl = queue.popleft() # Get the next URL from the front of the queue
                    current_batch_urls.append(url_to_crawl) # Append just the URL

                # If the current batch is empty, there are no more URLs to process
                if not current_batch_urls:
                    break

                log_message('INFO', f"Processing batch of {len(current_batch_urls)} URLs for crawling.")

                futures = {executor.submit(wrapper_get_internal_links, url_to_crawl): url_to_crawl for url_to_crawl in current_batch_urls}

                for future in concurrent.futures.as_completed(futures):
                    url_to_crawl = futures[future]
                    try:
                        new_links_from_url = future.result()
                        # Ensure new_links_from_url is an iterable (e.g., set), even if an error occurred in wrapper_get_internal_links
                        if new_links_from_url is None: # This should not happen if wrapper_get_internal_links somehow returns None
                            continue # Skip if wrapper_get_internal_links somehow returns None

                        for link in new_links_from_url:
                            # Only add and potentially archive if the link is truly new and hasn't been visited
                            if link not in visited_urls:
                                all_unique_internal_links.add(link) # Add discovered link to the overall set
                                visited_urls.add(link)

                                if not is_irrelevant_link(link):
                                    queue.append(link) # Only queue for crawling if it's not an irrelevant link
                                    log_message('DISCOVERED', link) # Log if it's actually going to be crawled
                                else:
                                    log_message('SKIPPED CRAWL', f"Skipping crawl for {link} due to irrelevant extension/path.")

                                # Conditionally capture parent-child relationship
                                if SETTINGS['enable_visual_tree_generation']:
                                    link_relationships.append((url_to_crawl, link))

                                # Submit new link for archiving if archiver_executor is provided
                                if archiver_executor:
                                    log_message('DEBUG', f"Submitting link for archiving: {link}", debug_only=True)
                                    archiving_futures.append(archiver_executor.submit(process_link_for_archiving, link, global_archive_action))
                    except CaptchaDetectedError as e:
                        # This exception will only be caught if the user explicitly chose 'skip' in the CAPTCHA prompt
                        # or if an unexpected CAPTCHA-related error occurred that wasn't handled by the prompt loop.
                        log_message('WARNING', f"CAPTCHA detection handled for {url_to_crawl}. Continuing with other URLs.")
                        # No need to shutdown executor here, as the user opted to skip or continue.
                    except Exception as e:
                        log_message('ERROR', f"An error occurred while processing {url_to_crawl}: {e}")
                        # Continue with other URLs, but log the error.
    except Exception as e:
        log_message('ERROR', f"An unexpected error occurred during website crawling: {e}")
        return set(), [] # Explicitly return an empty set and empty list on error
    finally:
        # Note: WebDriver instances are no longer explicitly quit after each URL.
        # They will persist for the lifetime of their respective worker threads within the ThreadPoolExecutor.
        # Proper cleanup (driver.quit()) should ideally be handled when the ThreadPoolExecutor itself shuts down,
        # which might require more advanced patterns for explicit resource management with concurrent.futures.
        pass

    return all_unique_internal_links, link_relationships # Return both discovered links and relationships

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
        log_message('INFO', "No valid URLs entered.")
        return

    all_discovered_links = set() # Set to store all unique internal links found across all initial URLs
    all_link_relationships = [] # List to store all (source, target) link relationships
    archiving_futures = [] # List to hold futures for archiving tasks
    crawling_futures = [] # New list to hold futures for crawling tasks

    # Set global archiving action based on SETTINGS, with validation and fallback
    global_choice = SETTINGS.get('default_archiving_action', 'n').lower() # Default to 'n' if not set or invalid
    valid_choices = ['a', 'n', 's']
    if global_choice not in valid_choices:
        log_message('WARNING', f"Invalid default_archiving_action '{global_choice}' found in SETTINGS. Falling back to 'Normal' archiving.")
        global_choice = 'n'

    # Determine max_crawler_workers and max_archiver_workers based on SETTINGS
    max_crawler_workers = SETTINGS['max_crawler_workers']
    if max_crawler_workers == 0:
        max_crawler_workers = None # Set to None for unlimited workers

    max_archiver_workers = SETTINGS['max_archiver_workers']
    if max_archiver_workers == 0:
        max_archiver_workers = None # Set to None for unlimited workers

    # Initialize both crawler and archiver executors
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_crawler_workers) as crawler_executor, \
         concurrent.futures.ThreadPoolExecutor(max_workers=max_archiver_workers) as archiver_executor:

        for url in initial_urls:
            # Basic validation to ensure the URL starts with 'http' or 'https'
            if not url.startswith("http"):
                log_message('WARNING', f"Invalid URL format for {url}. Skipping.")
                continue
            log_message('INFO', f"Starting crawl for initial URL: {url}")
            # Submit crawling tasks to the crawler_executor
            # Pass the all_link_relationships list to the crawl_website function
            crawling_futures.append(
                crawler_executor.submit(crawl_website, url, archiver_executor, archiving_futures, global_choice, all_link_relationships)
            )

        # Process crawling results as they complete
        log_message('INFO', "Waiting for crawling tasks to complete...")
        for future in concurrent.futures.as_completed(crawling_futures):
            try:
                discovered_links_for_url, _ = future.result() # Unpack both returned values, but only use the first
                all_discovered_links.update(discovered_links_for_url)
            except Exception as e:
                log_message('ERROR', f"Error during crawling task: {e}")

        log_message('INFO', f"Found {len(all_discovered_links)} unique internal links across all initial URLs.")

        # Clear previous output before providing archiving information
        clear_output(wait=True)

        # Print consolidated message for 'Archive All' or 'Skip All' actions
        if global_choice == 'a':
            log_message('INFO', f"Archiving action from settings: Archive All.")
        elif global_choice == 's':
            log_message('INFO', f"Archiving action from settings: Skip All.")
        elif global_choice == 'n':
            log_message('INFO', f"Archiving action from settings: Normal (respecting {SETTINGS['archiving_cooldown']*24}h rule).") # Updated message to reflect 'Normal' action.

        log_message('INFO', f"Submitted {len(archiving_futures)} archiving tasks.")
        log_message('INFO', "Waiting for all archiving tasks to complete...")

        results = [] # List to store the results of archiving attempts
        for future in concurrent.futures.as_completed(archiving_futures):
            try:
                results.append(future.result())
            except Exception as e:
                results.append(f"[FAILED] Archiving task failed with error: {e}")

    # Clear output again before the final summary for cleanliness
    clear_output(wait=True)

    log_message('INFO', "--- Archiving Summary ---")
    for result in results:
        print(result)

    # If visual tree generation is enabled, proceed with graph generation
    if SETTINGS['enable_visual_tree_generation']:
        log_message('INFO', "--- Generating Visual Link Tree ---")
        G = nx.DiGraph() # Create a directed graph

        # Add nodes and edges from the collected relationships
        for source, target in all_link_relationships:
            G.add_edge(source, target)

        # If no nodes were added (e.g., no links found or only one URL crawled), log and exit
        if not G.nodes():
            log_message('WARNING', "No graph nodes to display. Skipping visual tree generation.")
            return

        # Set the 'mother' URL (first initial URL) to be at the center
        mother_url = initial_urls[0] # Assuming the first URL is the 'mother' URL
        fixed_pos = {mother_url: (0, 0)} # Fix the mother URL at the center

        # Increase figure size for better readability
        plt.figure(figsize=(16, 12)) # New line for larger figure size

        # Use a layout that works well for trees/hierarchical structures
        # Pass the fixed_pos to spring_layout
        pos = nx.spring_layout(G, k=0.15, iterations=50, seed=42, pos=fixed_pos, fixed=[mother_url]) # Increased iterations for better convergence

        # Draw nodes with a smaller size and light color
        # Differentiate the mother_url node
        node_colors = ['lightblue' if node != mother_url else 'red' for node in G.nodes()]
        node_sizes = [100 if node != mother_url else 300 for node in G.nodes()]
        nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color=node_colors, alpha=0.8)

        # Draw edges with arrows, light gray color, and lower alpha
        nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color='gray', arrows=True, arrowsize=10, alpha=0.6)

        # Draw labels for nodes, but only for a subset or if the graph is small, to prevent clutter
        # For very large graphs, this might need to be optimized (e.g., only label root/important nodes)
        node_labels = {}
        for node in G.nodes():
            parsed_node = urlparse(node)
            label_candidate = parsed_node.netloc
            if parsed_node.path and parsed_node.path != '/':
                # If the path is long, prioritize keeping some part of it visible.
                # Combine domain and path for a more descriptive label.
                label_candidate += parsed_node.path

            # Define a maximum length for the label to prevent excessive width
            max_label_length = 25 # This can be tuned for desired verbosity

            if len(label_candidate) > max_label_length:
                # If the full combined label is too long, truncate it smartly.
                # Try to keep the domain and a truncated part of the path.
                domain_part = parsed_node.netloc
                path_part = parsed_node.path if parsed_node.path and parsed_node.path != '/' else ''

                if len(domain_part) + len(path_part) > max_label_length:
                    # Calculate how much of the path can fit after the domain (minus '...')
                    allowed_path_len = max_label_length - len(domain_part) - 3 # -3 for "..."
                    if allowed_path_len > 0 and path_part:
                        label = domain_part + path_part[:allowed_path_len] + "..."
                    elif len(domain_part) > max_label_length - 3: # If domain itself is too long
                        label = domain_part[:max_label_length - 3] + "..."
                    else: # Fallback if domain is too long and no path, or path is too short
                        label = domain_part # Just show domain if nothing else fits well
                else:
                    label = label_candidate # Should not be reached if initial check was correct
            else:
                label = label_candidate # Label fits within max_label_length

            node_labels[node] = label

        # Adjust font size based on the number of nodes to avoid overlap
        # Adjusted font_size calculation for better scaling and smaller text
        font_size = max(2, min(6, 400 // (len(G.nodes()) + len(initial_urls)))) if len(G.nodes()) > 0 else 8 # Modified this line

        nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=font_size, font_color='black', bbox=dict(facecolor='white', edgecolor='none', boxstyle='round,pad=0.2'))

        plt.title('Website Internal Link Tree', size=20)
        plt.axis('off') # Hide axes
        plt.savefig('website_link_tree.png') # Save the plot
        plt.show()
        plt.close() # Close the plot to free up resources
        log_message('INFO', "Visual link tree saved as 'website_link_tree.png'")


if __name__ == "__main__":
    main()
