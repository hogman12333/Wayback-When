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
    'max_crawler_workers': 1, # Max concurrent workers for website crawling (0 for unlimited)
    'retries': 5, # Max retries for archiving a single link
    'default_archiving_action': 'N', # Default archiving action: 'n' (Normal), 'a' (Archive All), 's' (Skip All)
    'debug_mode': False, # Set to True to enable debug messages, False to disable
    'max_archiver_workers': 0,
    'enable_visual_tree_generation': False, #setting for visual tree generation-incredibly ram intensive
    'min_link_search_delay': 3, # New setting: Minimum delay between link searches (seconds)
    'max_link_search_delay': 7, # New setting: Maximum delay between link search delays (seconds)
    'sequential_crawling_mode': True, # If True, max_crawler_workers will be set to 1 for sequential crawling
    'proxies': [], # List of proxies, e.g., ['http://user:pass@ip:port', 'socks5://user:pass@ip:port']. Leave empty to disable proxies.
    'max_archiving_queue_size': 100,
    'global_cooldown_on_error_duration': 120 # Global cooldown in seconds when a WebDriverException (e.g., connection error) occurs
}

# Define a threading.local() object at the module level for WebDriver instances and requests sessions
_thread_local = threading.local()

# Lock to ensure only one CAPTCHA prompt is active at a time
captcha_prompt_lock = threading.Lock()

# Global state for network error cooldown
_global_network_error_cooldown_until = 0.0 # Timestamp until which global cooldown is active
_global_network_error_lock = threading.Lock() # Lock to protect _global_network_error_cooldown_until

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

    # Add proxy if available
    if SETTINGS['proxies']:
        proxy = random.choice(SETTINGS['proxies'][0]) # Select from the inner list
        options.add_argument(f'--proxy-server={proxy}')
        log_message('DEBUG', f"Using proxy for Selenium: {proxy}", debug_only=True)

    # Configure Chrome to not download files automatically
    prefs = {
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
        "download.default_directory": "/dev/null"
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
    driver.implicitly_wait(10) # seconds. This is an example, adjust as needed.

    return driver


def get_requests_session():
    """Returns a requests.Session object configured with retries and a random proxy if available."""
    session = requests.Session()
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    if SETTINGS['proxies']:
        proxy = random.choice(SETTINGS['proxies'][0]) # Select from the inner list
        session.proxies = {
            'http': proxy,
            'https': proxy,
        }
        log_message('DEBUG', f"Using proxy for requests session: {proxy}", debug_only=True)
    return session

# Configure a retry strategy once, to be used for each new session
retry_strategy = Retry(
    total=5,
    backoff_factor=1,
    status_forcelist=[403, 404, 429, 500, 502, 503, 504],
    allowed_methods=False # Apply retry to all HTTP methods
)
adapter = HTTPAdapter(max_retries=retry_strategy)

# Define irrelevant extensions and path segments globally
IRRELEVANT_EXTENSIONS = ('.3g2', '.3gp', '.7z', '.aac', '.accdb', '.ace', '.aif', '.aiff', '.ai', '.apk', '.arj', '.arw', '.asm', '.azw3', '.bak', '.bash', '.bin', '.blend', '.bmp', '.bz2', '.cab', '.cache', '.c', '.cso', '.conf', '.cpp', '.cr2', '.crt', '.cs', '.csv', '.dat', '.dae', '.deb', '.dmg', '.doc', '.docx', '.drv', '.dxf', '.dwg', '.eml', '.eps', '.epub', '.exe', '.fbx', '.fish', '.flac', '.flv', '.fon', '.gb', '.gba', '.gif', '.go', '.gz', '.h', '.har', '.hpp', '.ics', '.ico', '.igs', '.img', '.ini', '.iso', '.java', '.jpeg', '.jpg', '.js', '.json', '.key', '.kt', '.kts', '.lock', '.log', '.lua', '.lz', '.lzma', '.m', '.map', '.max', '.mdb', '.mid', '.midi', '.mkv', '.mobi', '.mov', '.mp3', '.mp4', '.mpg', '.mpeg', '.msg', '.msi', '.msm', '.msp', '.nef', '.nes', '.obj', '.odp', '.ods', '.odt', '.ogg', '.old', '.opus', '.orf', '.otf', '.pak', '.pcap', '.pcapng', '.pem', '.pdf', '.php', '.pl', '.ply', '.png', '.ppt', '.pptx', '.prn', '.ps', '.py', '.qbb', '.qbw', '.qfx', '.rar', '.rb', '.rm', '.rmvb', '.rom', '.rpm', '.rs', '.rtf', '.r', '.rfa', '.rvt', '.s', '.sav', '.sh', '.sit', '.sitx', '.skp', '.so', '.sqlite', '.sqlite3', '.stl', '.step', '.stp', '.sub', '.swift', '.sys', '.tar', '.temp', '.tif', '.tiff', '.tmp', '.toml', '.tsv', '.ttf', '.uue', '.vhd', '.vhdx', '.vmdk', '.vtt', '.wav', '.wbmp', '.webm', '.webp', '.wma', '.woff', '.woff2', '.wps', '.wmv', '.xcf', '.xls', '.xlsx', '.ppt', '.pptx', '.xml', '.xz', '.yaml', '.yml', '.z', '.zip', '.zsh')
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

def _get_links_from_page_content(base_url, driver):
    """Scrapes a given URL to find all internal links and returns them as a set, along with relationships.

    Contributors: Consider enhancing error handling for different HTTP status codes or improving URL normalization.
    """
    links = set()
    relationships_on_page = [] # New list to store (source_url, discovered_link) tuples

    # Extract the domain from the base_url and its root domain
    parsed_base_url = urlparse(base_url)
    base_netloc = parsed_base_url.netloc
    base_root_domain = get_root_domain(base_netloc)
    normalized_base_url_for_comparison = normalize_url(base_url) # Normalize base_url for comparison

    log_message('DEBUG', f"Starting _get_links_from_page_content for base_url: {base_url} with base_netloc: {base_netloc} and root_domain: {base_root_domain}", debug_only=True)

    retries = SETTINGS['retries'] # Use the 'retries' setting
    attempt = 0
    while attempt < retries:
        try:
            # Select a random user agent for the current request
            random_user_agent = generate_random_user_agent()
            # Set the user agent for the current request using CDP command
            driver.execute_cdp_cmd('Network.setUserAgentOverride', {'userAgent': random_user_agent})

            # Navigate to the base_url using Selenium
            driver.get(base_url)

            # Add a small delay to ensure page elements are loaded, improving stealth
            time.sleep(random.uniform(SETTINGS['min_link_search_delay'], SETTINGS['max_link_search_delay']))

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
                with captcha_prompt_lock:
                    log_message('WARNING', f"CAPTCHA DETECTED for {base_url}. Waiting 5-10 seconds before attempting to continue...", debug_only=True)
                    time.sleep(random.uniform(5, 10))
                    log_message('INFO', "Attempting to continue after automated wait...", debug_only=True)

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
                        # Only add relationship if visual tree generation is enabled
                        if SETTINGS['enable_visual_tree_generation']:
                            relationships_on_page.append((base_url, clean_url))
                    else:
                        log_message('DEBUG', f"Skipping external or parent link: {full_url} (Link root domain: {link_root_domain} != Base root domain: {base_root_domain} OR not sub-path of base_url)", debug_only=True)
            if not found_any_href:
                log_message('DEBUG', f"No href attributes found on {base_url} by Selenium.", debug_only=True)

            log_message('DEBUG', f"Finished processing {base_url}. Discovered {len(links)} links.", debug_only=True)
            return links, relationships_on_page # Return both discovered links and relationships

        except TimeoutException:
            log_message('WARNING', f"Page load timed out for {base_url}. Retrying ({retries - attempt - 1} attempts left).", debug_only=True)
            attempt += 1
            time.sleep(random.uniform(5, 15)) # Longer, randomized delay
        except WebDriverException as e:
            # This can catch ConnectionRefusedError, DNS errors, etc., as reported by Selenium
            error_message_lower = str(e).lower()
            # Specifically check for 'connection refused' error code (111) or message
            if 'net::err_connection_refused' in error_message_lower or 'connection refused' in error_message_lower or '(connection aborted.)' in error_message_lower:
                log_message('ERROR', f"A WebDriver error occurred (Connection Refused) while crawling {base_url}: {e}. Triggering global cooldown and retrying ({retries - attempt - 1} attempts left).")
                with _global_network_error_lock:
                    # Update the global cooldown timestamp, ensuring it only extends the cooldown
                    _global_network_error_cooldown_until = max(
                        _global_network_error_cooldown_until,
                        time.time() + SETTINGS['global_cooldown_on_error_duration']
                    )
            else:
                log_message('WARNING', f"A non-connection-refused WebDriver error occurred while crawling {base_url}: {e}. Not triggering global cooldown but retrying ({retries - attempt - 1} attempts left).", debug_only=True)
            attempt += 1
            time.sleep(random.uniform(5, 15)) # Longer, randomized delay
        except Exception as e:
            log_message('ERROR', f"An unexpected error occurred while crawling {base_url}: {e}. Retrying ({retries - attempt - 1} attempts left).", debug_only=True)
            attempt += 1
            time.sleep(random.uniform(5, 15)) # Longer, randomized delay
    log_message('ERROR', f"Failed to retrieve {base_url} after {retries} attempts.", debug_only=True)
    return set(), [] # Return empty set and list on failure

def _crawl_single_page(url_to_crawl):
    """Wrapper function to manage WebDriver instance for a single page crawl."""
    driver = get_driver() # Get a new driver for each call
    try:
        links_on_page, relationships_on_page = _get_links_from_page_content(url_to_crawl, driver)
    finally:
        driver.quit() # Ensure the driver is closed
    return links_on_page, relationships_on_page # Return both discovered links and relationships

def should_archive(url, global_archive_action):
    """Determines if a URL should be archived based on a global action or a custom check.

    Contributors: Consider adding more sophisticated checks for archiving, e.g., checking content changes.
    """
    user_agent = generate_random_user_agent() # Use the new generator
    requests_session = get_requests_session() # Get a new session with a random proxy for each archive check
    wayback = waybackpy.Url(url, user_agent) # Initialize WaybackPy URL object without session

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
                log_message('INFO', f"Needs Archive: {url} (Last archived {time_diff.total_seconds() // 3600:.1f} hours ago, > {SETTINGS['archiving_cooldown']*24} hours)", debug_only=True)
                return True, wayback

        # Handle cases where no existing archive record is found for the URL
        except waybackpy.exceptions.NoCDXRecordFound:
            log_message('INFO', f"No existing archive found for {url}. Archiving.", debug_only=True)
            return True, wayback
        # Handle other unexpected errors during the archive check
        except Exception as e:
            attempt += 1
            if attempt < retries:
                log_message('WARNING', f"An error occurred while checking archive for {url}: {e}. Retrying ({retries - attempt} attempts left).", debug_only=True)
                time.sleep(5) # Wait before retrying the archive check
            else:
                log_message('ERROR', f"Failed to check archive for {url} after {retries} attempts: {e}. Defaulting to archive.", debug_only=True)
                return True, wayback # Default to archive if all retries fail
    return False, wayback # Should not be reached if retries are handled correctly or success occurs

# A lock to ensure only one thread modifies `last_archive_time` at a time
archive_lock = threading.Lock()
# Timestamp of the last archive request, initialized to 0.0
last_archive_time = 0.0
# Minimum delay required between archive requests to respect rate limits
MIN_ARCHIVE_DELAY_SECONDS = 60 / SETTINGS['urls_per_minute_limit']

def process_link_for_archiving(link, global_archive_action):
    """Checks if a link needs archiving and attempts to save it to Wayback Machine with rate limiting and retries.Z

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
                    log_message('RATE LIMIT', f"Sleeping for {sleep_duration:.2f} seconds before archiving {link}", debug_only=True)
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
                    log_message('WARNING', f"Wayback Machine rate limit hit for {link}. Pausing for 1 minute before retrying ({retries} attempts left).", debug_only=True)
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

def main():
    """
    Main function to orchestrate the website crawling and archiving process.
    """
    clear_output(wait=True)

    # Prompt the user to enter one or more URLs
    target_urls_input = input("Enter URLs (comma-separated, e.g., https://notawebsite.org/, https://example.com/): ").strip()
    # Split the input string by commas and clean up whitespace, filtering out empty strings
    initial_urls_raw = [url.strip() for url in target_urls_input.split(',') if url.strip()]

    # If no valid URLs were entered, exit the function
    if not initial_urls_raw:
        log_message('INFO', "No valid URLs entered.", debug_only=True)
        return

    # --- Initialize Queues and Sets for concurrent management ---
    crawling_queue = deque() # URLs waiting to be crawled
    queue_for_archiving = deque() # URLs waiting to be archived
    visited_urls = set() # All unique URLs encountered (crawled or added to a queue)
    crawling_futures_set = set() # Set of active Future objects for crawling tasks
    archiving_futures_set = set() # Set of active Future objects for archiving tasks
    all_link_relationships = [] # List to store all (source, target) link relationships for visual tree
    final_archive_results = [] # List to store results from archiving attempts

    # Set global archiving action
    global_choice = SETTINGS.get('default_archiving_action', 'n').lower()
    valid_choices = ['a', 'n', 's']
    if global_choice not in valid_choices:
        log_message('WARNING', f"Invalid default_archiving_action '{global_choice}' found in SETTINGS. Falling back to 'Normal' archiving.", debug_only=True)
        global_choice = 'n'

    # Determine max_crawler_workers and max_archiver_workers based on SETTINGS
    max_crawler_workers_setting = SETTINGS['max_crawler_workers']
    if SETTINGS.get('sequential_crawling_mode', False):
        max_crawler_workers_resolved = 1 # Force to 1 worker for sequential mode
        log_message('INFO', "Sequential crawling mode is enabled. Crawling with 1 worker.", debug_only=True)
    elif max_crawler_workers_setting == 0:
        max_crawler_workers_resolved = None # Set to None for unlimited workers
    else:
        max_crawler_workers_resolved = max_crawler_workers_setting

    max_archiver_workers_setting = SETTINGS['max_archiver_workers']
    if max_archiver_workers_setting == 0:
        max_archiver_workers_resolved = None # Set to None for unlimited workers
    else:
        max_archiver_workers_resolved = max_archiver_workers_setting

    # Process initial URLs: normalize, add to visited, crawling queue, and archiving queue
    for url in initial_urls_raw:
        if not url.startswith("http"): # Basic validation
            log_message('WARNING', f"Invalid URL format for {url}. Skipping.", debug_only=True)
            continue
        normalized_url = normalize_url(url)

        if normalized_url not in visited_urls:
            log_message('INFO', f"Adding initial URL to queues: {normalized_url}", debug_only=True)
            visited_urls.add(normalized_url)
            crawling_queue.append(normalized_url)
            queue_for_archiving.append(normalized_url)

    log_message('INFO', f"Starting main processing loop with {len(crawling_queue)} initial URLs.", debug_only=True)

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_crawler_workers_resolved) as crawler_executor, \
         concurrent.futures.ThreadPoolExecutor(max_workers=max_archiver_workers_resolved) as archiver_executor:

        while True:
            # --- Section A: Crawling Task Submission ---
            # Submit new crawling tasks if:
            # 1. There are URLs in the crawling queue.
            # 2. The number of active crawling tasks is below the max_crawler_workers limit.
            # 3. The archiving system (queue + active futures) is not excessively backed up.
            #    The 'max_archiving_queue_size * 2' is an arbitrary buffer to prevent crawler from overwhelming archiver.
            current_crawler_capacity = (max_crawler_workers_resolved if max_crawler_workers_resolved is not None else 65) - len(crawling_futures_set)
            archiving_load = len(archiving_futures_set) + len(queue_for_archiving)

            if archiving_load >= SETTINGS['max_archiving_queue_size'] * 2:
                log_message('INFO', f"CRAWLER PAUSED: Archiving load ({archiving_load}) exceeds buffer ({SETTINGS['max_archiving_queue_size'] * 2}). Halting new crawling tasks.", debug_only=True)
            elif crawling_queue and current_crawler_capacity > 0:
                url_to_crawl = crawling_queue.popleft()
                log_message('DEBUG', f"Submitting crawling task for: {url_to_crawl}", debug_only=True)
                future = crawler_executor.submit(_crawl_single_page, url_to_crawl)
                crawling_futures_set.add(future)

            # --- Section B: Completed Crawling Tasks Processing ---
            # Process results from completed crawling tasks
            completed_crawling_futures = {f for f in crawling_futures_set if f.done()}
            for future in completed_crawling_futures:
                crawling_futures_set.remove(future)
                try:
                    discovered_links_on_page, relationships_on_page = future.result()

                    if SETTINGS['enable_visual_tree_generation']:
                        all_link_relationships.extend(relationships_on_page)

                    for new_link in discovered_links_on_page:
                        if new_link not in visited_urls:
                            visited_urls.add(new_link)
                            # Only add to crawling_queue if not an irrelevant link
                            if not is_irrelevant_link(new_link):
                                crawling_queue.append(new_link)
                                log_message('DISCOVERED', new_link, debug_only=False) # Always show DISCOVERED
                            # Always add to archiving queue, regardless of irrelevancy for crawling
                            queue_for_archiving.append(new_link)
                except Exception as e:
                    log_message('ERROR', f"Error during crawling task: {e}", debug_only=True)

            # --- Section C: Archiving Task Submission ---
            # Submit new archiving tasks if:
            # 1. There are URLs in the archiving queue.
            # 2. The number of active archiving tasks is below the configured max_archiving_queue_size.
            if queue_for_archiving and len(archiving_futures_set) < SETTINGS['max_archiving_queue_size']:
                link_to_archive = queue_for_archiving.popleft()
                log_message('DEBUG', f"Submitting archiving task for: {link_to_archive}", debug_only=True)
                future = archiver_executor.submit(process_link_for_archiving, link_to_archive, global_choice)
                archiving_futures_set.add(future)

            # --- Section D: Completed Archiving Tasks Processing ---
            # Process results from completed archiving tasks
            completed_archiving_futures = {f for f in archiving_futures_set if f.done()}
            for future in completed_archiving_futures:
                archiving_futures_set.remove(future)
                try:
                    result = future.result()
                    final_archive_results.append(result)
                    log_message('DEBUG', f"Archiving result: {result}", debug_only=True)
                except Exception as e:
                    final_archive_results.append(f"[FAILED] Archiving task failed with error: {e}")
                    log_message('ERROR', f"Error during archiving task: {e}", debug_only=True)

            # --- Section E: Termination Condition ---
            # Break loop if all queues and active tasks are empty
            if not crawling_queue and not crawling_futures_set and \
               not queue_for_archiving and not archiving_futures_set:
                log_message('INFO', "All crawling and archiving tasks completed. Exiting main loop.", debug_only=True)
                break

            # --- Section F: Sleep to prevent busy-waiting ---
            # Only sleep if there's no immediate work to be done to avoid busy-waiting.
            # This means if all queues are empty AND all futures sets are empty, we already broke.
            # If there's work in queues or futures, we might want to keep checking more frequently.
            # A small sleep is good practice to yield control and prevent 100% CPU usage.
            if not crawling_queue and not queue_for_archiving and \
               not crawling_futures_set and not archiving_futures_set: # Already handled by break above, but defensive
                pass # No need to sleep if about to break
            else:
                time.sleep(0.1)

    log_message('INFO', f"Found {len(visited_urls)} unique URLs processed (includes those not queued for crawling due to irrelevancy or already visited).", debug_only=True)

    # Clear output again before the final summary for cleanliness
    clear_output(wait=True)

    # Print consolidated message for 'Archive All' or 'Skip All' actions
    if global_choice == 'a':
        log_message('INFO', f"Archiving action from settings: Archive All.", debug_only=True)
    elif global_choice == 's':
        log_message('INFO', f"Archiving action from settings: Skip All.", debug_only=True)
    elif global_choice == 'n':
        log_message('INFO', f"Archiving action from settings: Normal (respecting {SETTINGS['archiving_cooldown']*24}h rule).", debug_only=True)

    log_message('INFO', f"Processed {len(final_archive_results)} archiving tasks.", debug_only=True)
    log_message('INFO', "--- Archiving Summary ---", debug_only=True)
    
    # The final archive results are iterated through and printed directly, 
    # so they are always visible without needing a debug_only flag here.
    for result in final_archive_results:
        print(result)

    # If visual tree generation is enabled, proceed with graph generation
    if SETTINGS['enable_visual_tree_generation']:
        log_message('INFO', "--- Generating Visual Link Tree ---", debug_only=True)
        G = nx.DiGraph() # Create a directed graph

        # Add nodes and edges from the collected relationships
        for source, target in all_link_relationships:
            G.add_edge(source, target)

        # If no nodes were added (e.g., no links found or only one URL crawled), log and exit
        if not G.nodes():
            log_message('WARNING', "No graph nodes to display. Skipping visual tree generation.", debug_only=True)
            return

        # Set the 'mother' URL (first initial URL) to be at the center
        mother_url = initial_urls_raw[0] # Use the first raw input URL as mother for display context
        fixed_pos = {normalize_url(mother_url): (0, 0)} # Fix the normalized mother URL at the center

        # Increase figure size for better readability
        plt.figure(figsize=(16, 12))

        # Use a layout that works well for trees/hierarchical structures
        # Pass the fixed_pos to spring_layout
        pos = nx.spring_layout(G, k=0.15, iterations=50, seed=42, pos=fixed_pos, fixed=[normalize_url(mother_url)])

        # Draw nodes with a smaller size and light color
        # Differentiate the mother_url node
        node_colors = ['lightblue' if node != normalize_url(mother_url) else 'red' for node in G.nodes()]
        node_sizes = [100 if node != normalize_url(mother_url) else 300 for node in G.nodes()]
        nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color=node_colors, alpha=0.8)

        # Draw edges with arrows, light gray color, and lower alpha
        nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color='gray', arrows=True, arrowsize=10, alpha=0.6)

        # Draw labels for nodes, but only for a subset or if the graph is small, to prevent clutter
        node_labels = {}
        for node in G.nodes():
            parsed_node = urlparse(node)
            label_candidate = parsed_node.netloc
            if parsed_node.path and parsed_node.path != '/':
                label_candidate += parsed_node.path

            # Define a maximum length for the label to prevent excessive width
            max_label_length = 25 # This can be tuned for desired verbosity

            if len(label_candidate) > max_label_length:
                domain_part = parsed_node.netloc
                path_part = parsed_node.path if parsed_node.path and parsed_node.path != '/' else ''

                if len(domain_part) + len(path_part) > max_label_length:
                    allowed_path_len = max_label_length - len(domain_part) - 3 # -3 for "..."
                    if allowed_path_len > 0 and path_part:
                        label = domain_part + path_part[:allowed_path_len] + "..."
                    elif len(domain_part) > max_label_length - 3: # If domain itself is too long
                        label = domain_part[:max_label_length - 3] + "..."
                    else:
                        label = domain_part
                else:
                    label = label_candidate
            else:
                label = label_candidate

            node_labels[node] = label

        # Adjust font size based on the number of nodes to avoid overlap
        font_size = max(2, min(6, 400 // (len(G.nodes()) + len(initial_urls_raw)))) if len(G.nodes()) > 0 else 8

        nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=font_size, font_color='black', bbox=dict(facecolor='white', edgecolor='none', boxstyle='round,pad=0.2'))

        plt.title('Website Internal Link Tree', size=20)
        plt.axis('off') # Hide axes
        plt.savefig('website_link_tree.png') # Save the plot
        plt.show()
        plt.close() # Close the plot to free up resources
        log_message('INFO', "Visual link tree saved as 'website_link_tree.png'", debug_only=True)


if __name__ == "__main__":
    main()
