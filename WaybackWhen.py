import os
import sys
import requests
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning
from urllib.parse import (
    urljoin,
    urlparse,
    parse_qs,
    urlencode,
    urlunparse,
)
from collections import OrderedDict, deque
import waybackpy
from datetime import datetime, timedelta, timezone
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import concurrent.futures
import threading
import queue
import warnings
import random

# Selenium imports - these are used for browser automation to scrape dynamic content
from selenium import webdriver
from selenium.webdriver.chrome.options import Options # Used to configure Chrome browser options
from selenium.webdriver.chrome.service import Service as ChromeService # Manages the ChromeDriver executable
from webdriver_manager.chrome import ChromeDriverManager # Automatically downloads and manages ChromeDriver
from selenium.webdriver.common.by import By # Used to locate elements on a web page (e.g., By.ID, By.XPATH)
from selenium.common.exceptions import TimeoutException, WebDriverException # Exceptions for WebDriver operations
from selenium_stealth import stealth # Helps avoid detection by websites that block automated browsers

# Visualization imports - for creating graphical representations of the crawled links
import networkx as nx # Library for creating and manipulating graphs (networks)
import matplotlib.pyplot as plt # Plotting library, used with networkx for visualization

# Jupyter/console helper - for clearing output in interactive environments
from IPython.display import clear_output

# Filter out specific warnings that might be noisy but don't prevent execution
warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)


# =========================
# Custom Exceptions
# =========================

class CaptchaDetectedError(Exception):
    """Raised when a CAPTCHA is detected on a page."""
    pass


class ConnectionRefusedForCrawlerError(Exception):
    """Raised when a connection is refused for a given URL branch."
    ""Raised specifically when a WebDriver encounters a 'Connection Refused' error,
    indicating that further crawling on that domain/branch might be futile or problematic.
    """
    pass


# =========================
# Settings
# =========================

# Global configuration settings for the web crawler and archiver
SETTINGS = {
    "archiving_cooldown": 28,          # Number of days to wait before re-archiving a URL that's already in Wayback Machine.
    "urls_per_minute_limit": 15,       # Rate limit for Wayback Machine API requests (specific to waybackpy).
    "max_crawler_workers": 10,         # Maximum number of concurrent threads/processes for crawling. 0 means unlimited (but capped by system resources).
    "retries": 5,                      # Number of times to retry a failed HTTP request or WebDriver operation.
    "default_archiving_action": "N",   # Default action for archiving: 'n' (normal - check cooldown), 'a' (archive all), 's' (skip all).
    "debug_mode": True,
    "max_archiver_workers": 0,         # Maximum number of concurrent threads/processes for archiving. 0 means unlimited.
    "enable_visual_tree_generation": False, # Whether to generate a visual graph of crawled links using NetworkX and Matplotlib.
    "min_link_search_delay": 0.0,      # Minimum random delay (seconds) between link extraction on a page to simulate human behavior.
    "max_link_search_delay": 0.0,      # Maximum random delay (seconds) between link extraction on a page.
    "safety_switch": False,            # If True, forces the crawler to run sequentially (1 worker) to avoid detection or aggressive crawling.
    "proxies": [],                     # List of proxy URLs (e.g., ['http://user:pass@ip:port']). If provided, random proxies will be used.
    "max_archiving_queue_size": 0,     # Maximum size of the queue for archiving tasks. 0 means unlimited.
    "allow_external_links": False,     # If True, the crawler will follow links to external domains.
    "archive_timeout_seconds": 300,    # Timeout in seconds for a single archiving request to the Wayback Machine.
}

# Thread-local storage (if needed later) - useful for storing data unique to each thread
_thread_local = threading.local()

# Lock to ensure only one CAPTCHA prompt is active at a time - prevents multiple threads from trying to solve a CAPTCHA simultaneously
captcha_prompt_lock = threading.Lock()

# Archive rate limiting variables
archive_lock = threading.Lock() # Ensures only one thread modifies last_archive_time or rate_limit_active_until_time at a time
last_archive_time = 0.0  # Global timestamp of the last successful archive request.
rate_limit_active_until_time = 0.0 # Global timestamp until which a reactive rate limit (e.g., from Wayback Machine) is active.

# Minimum delay between archive requests, calculated from urls_per_minute_limit
MIN_ARCHIVE_DELAY_SECONDS = 60 / SETTINGS["urls_per_minute_limit"]


# =========================
# User-Agent / Stealth Pools
# =========================

# Lists of realistic browser and OS configurations to generate diverse User-Agent strings and mimic real users.
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
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/{version}.1 Safari/605.1.15", # Safari on desktop/iPad
    "AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/{version}.0.0.0 Mobile/15E148 Safari/604.1", # Chrome on iOS
]

CHROME_VERSIONS = [str(v) for v in range(1, 126)]
FIREFOX_VERSIONS = [str(v) for v in range(1, 126)]
SAFARI_VERSIONS = [str(v) for v in range(1, 18)]

# Stealth parameters for Selenium to make the automated browser less detectable
STEALTH_PLATFORMS = [
    "Win32",
    "Linux x86_64",
    "MacIntel",
]
STEALTH_WEBGL_VENDORS = [
    "Google Inc. (Intel)",
    "Intel Inc.",
    "NVIDIA Corporation",
    "Apple Inc.",
]
STEALTH_RENDERERS = [
    "ANGLE (Intel, Intel(R) Iris(TM) Graphics 6100 (OpenGL 4.5), OpenGL 4.5.0)",
    "Intel Iris OpenGL Engine",
    "Google SwiftShader",
    "Metal",
]


# =========================
# Irrelevant Extensions / Paths
# =========================

# A tuple of file extensions that are typically not relevant for web content crawling (e.g., binaries, media files).
# Links ending with these extensions will be ignored by the crawler.
IRRELEVANT_EXTENSIONS = (
    ".3g2", ".3gp", ".7z", ".aac", ".accdb", ".ace", ".aif", ".aiff", ".ai",
    ".apk", ".arj", ".arw", ".asm", ".azw3", ".bak", ".bash", ".bin", ".blend",
    ".bmp", ".bz2", ".cab", ".cache", ".c", ".cso", ".conf", ".cpp", ".cr2",
    ".crt", ".cs", ".csv", ".dat", ".dae", ".deb", ".dmg", ".doc", ".docx",
    ".drv", ".dxf", ".dwg", ".eml", ".eps", ".epub", ".exe", ".fbx", ".fish",
    ".flac", ".flv", ".fon", ".gb", ".gba", ".gif", ".go", ".gz", ".h", ".har",
    ".hpp", ".ics", ".ico", ".igs", ".img", ".ini", ".iso", ".java", ".jpeg",
    ".jpg", ".js", ".json", ".key", ".kt", ".kts", ".lock", ".log", ".lua",
    ".lz", ".lzma", ".m", ".map", ".max", ".mdb", ".mid", ".midi", ".mkv",
    ".mobi", ".mov", ".mp3", ".mp4", ".mpg", ".mpeg", ".msg", ".msi", ".msm",
    ".msp", ".nef", ".nes", ".obj", ".odp", ".ods", ".odt", ".ogg", ".old",
    ".opus", ".orf", ".otf", ".pak", ".pcap", ".pcapng", ".pem", ".pdf", ".php",
    ".pl", ".ply", ".png", ".ppt", ".pptx", ".prn", ".ps", ".py", ".qbb", ".qbw",
    ".qfx", ".rar", ".rb", ".rm", ".rmvb", ".rom", ".rpm", ".rs", ".rtf", ".r",
    ".rfa", ".rvt", ".s", ".sav", ".sh", ".sit", ".sitx", ".skp", ".so",
    ".sqlite", ".sqlite3",
    ".stl", ".step", ".stp", ".sub", ".swift", ".sys",
    ".tar", ".temp", ".tif", ".tiff", ".tmp", ".toml", ".tsv", ".ttf", ".uue",
    ".vhd", ".vhdx", ".vmdk", ".vtt", ".wav", ".wbmp", ".webm", ".webp", ".wma",
    ".woff", ".woff2", ".wps", ".wmv", ".xcf", ".xls", ".xlsx", ".xml", ".xz",
    ".yaml", ".yml", ".z", ".zip", ".zsh",
)

# A tuple of URL path segments that indicate irrelevant content (e.g., common asset folders, CMS specific paths).
# URLs containing these segments will be ignored.
IRRELEVANT_PATH_SEGMENTS = (
    "/cdn-cgi/", # Cloudflare related paths
    "/assets/", # Common asset folder
    "/uploads/", # Common upload folder
    "/wp-content/", # WordPress content
    "/wp-includes/", # WordPress includes
    "/themes/", # WordPress themes
    "/plugins/", # WordPress plugins
    "/node_modules/", # JavaScript module dependencies
    "/static/", # Common static files folder
    "/javascript/", # Common JavaScript folder
    "/css/", # Common CSS folder
    "/img/", # Common images folder
)


# =========================
# Logging
# =========================

def log_message(level: str, message: str, debug_only: bool = False) -> None:
    """Standardized logging function."
    Prints messages to the console with a timestamp and log level.
    Can be configured to only print in debug_mode.
    """
    if debug_only and not SETTINGS["debug_mode"]:
        return
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}][{level.upper()}] {message}")


# =========================
# Utility Functions
# =========================

def generate_random_user_agent() -> str:
    """Generate a random realistic User-Agent string."
    This helps in making requests appear to come from different browsers and operating systems,
    reducing the likelihood of being blocked by anti-bot measures.
    """
    os_part = random.choice(OS_TYPES)
    browser_template = random.choice(BROWSER_TYPES)

    if "Chrome" in browser_template:
        version = random.choice(CHROME_VERSIONS)
    elif "Firefox" in browser_template:
        version = random.choice(FIREFOX_VERSIONS)
    elif "Safari" in browser_template or "CriOS" in browser_template:
        version = random.choice(SAFARI_VERSIONS)
    else:
        version = "100" # Default if no specific version range found

    browser = browser_template.format(version=version)
    return f"Mozilla/5.0 ({os_part}) {browser}"


def normalize_url(url: str) -> str:
    """Normalizes a URL to ensure consistency and avoid duplicate entries."
    Steps include:
    - Lowercasing scheme and netloc.
    - Cleaning and lowercasing the path.
    - Removing common index page names (e.g., index.html).
    - Removing URL fragments (e.g., #section).
    - Removing common tracking query parameters.
    """
    parsed = urlparse(url)

    scheme = parsed.scheme.lower()
    netloc = parsed.netloc.lower()

    # Normalize path: remove double slashes, trailing slashes, and lowercase
    path = parsed.path or "/"
    path = path.replace("//", "/")
    path = path.rstrip("/") if path not in ("/", "") else "/"
    path = path.lower()

    # Remove common index pages from the path to treat e.g. /index.html and / as the same page
    for index_page in ["index.html", "index.htm", "default.html", "default.htm"]:
        if path.endswith(index_page):
            path = path[: -len(index_page)]
            if not path:
                path = "/"

    # Remove fragments (the part after '#') as they usually refer to sections within the same page
    fragment = ""

    # Clean query parameters by removing common tracking parameters
    query_params = parse_qs(parsed.query) # Parses query string into a dictionary
    tracking_params = {
        "utm_source", "utm_medium", "utm_campaign", "utm_term",
        "utm_content", "gclid", "fbclid", "ref", "src", "cid", "referrer"
    }
    for p in tracking_params:
        query_params.pop(p, None) # Remove tracking parameters if they exist

    # Re-encode the cleaned query parameters, ensuring consistent order
    query = urlencode(sorted(query_params.items()), doseq=True)

    # Reconstruct the URL from its normalized components
    return urlunparse((scheme, netloc, path, parsed.params, query, fragment))

def get_root_domain(netloc: str) -> str:
    """Extract root domain from netloc (simple heuristic)."
    This function attempts to get the 'main' part of a domain name,
    handling common cases like 'www.' subdomains and top-level domains.
    """
    netloc = netloc.lower()
    parts = netloc.split(".")
    if len(parts) > 2 and parts[0] == "www":
        return ".".join(parts[1:]) # e.g., www.example.com -> example.com
    elif len(parts) > 2: # Heuristic for cases like blog.example.com, taking last two parts
        return ".".join(parts[-2:])
    return netloc # If only one or two parts, assume it's the root domain


def is_irrelevant_link(url: str) -> bool:
    """Check if URL should be considered irrelevant for crawling."
    This helps in filtering out links to files or administrative sections
    that are not part of the primary content to be archived or crawled.
    """
    parsed_url = urlparse(url)
    path = parsed_url.path.lower()

    # Check against irrelevant file extensions
    if path.endswith(IRRELEVANT_EXTENSIONS):
        return True

    # Check against irrelevant path segments (e.g., common asset folders)
    for segment in IRRELEVANT_PATH_SEGMENTS:
        if segment in path:
            return True
    return False


# =========================
# HTTP Session Factory
# =========================

# Configure retry strategy for requests to handle transient network errors or server issues
retry_strategy = Retry(
    total=5, # Maximum number of retries
    backoff_factor=1, # Delay factor for exponential backoff between retries
    status_forcelist=[403, 404, 429, 500, 502, 503, 504], # HTTP status codes that should trigger a retry
    allowed_methods=False, # Only retry GET requests by default
)
adapter = HTTPAdapter(max_retries=retry_strategy) # Create an HTTP adapter with the retry strategy


def get_requests_session() -> requests.Session:
    """Return a configured requests.Session with retries and optional proxy."
    Using a session allows for connection pooling and cookie persistence,
    which can improve performance and maintain state across requests.
    """
    session = requests.Session()
    session.mount("http://", adapter) # Mount the adapter for HTTP requests
    session.mount("https://", adapter) # Mount the adapter for HTTPS requests

    # If proxies are configured in SETTINGS, randomly select and apply one to the session
    if SETTINGS["proxies"]:
        proxy = random.choice(SETTINGS["proxies"])
        session.proxies = {"http": proxy, "https": proxy}
        log_message("DEBUG", f"Using proxy for requests session: {proxy}", debug_only=True)

    return session


# =========================
# WebDriver Manager
# =========================

class WebDriverManager:
    """Encapsulates Selenium WebDriver creation and teardown."
    Manages the lifecycle of Chrome WebDriver instances, including configuration,
    stealth settings, and proper shutdown.
    """

    def __init__(self) -> None:
        pass

    def create_driver(self) -> webdriver.Chrome:
        """Creates and configures a new Chrome WebDriver instance."
        The driver is set up with headless mode, various optimizations, stealth options,
        and optional proxy support.
        """
        options = Options() # Initialize ChromeOptions to customize browser behavior

        # Headless mode (new headless is more stable on modern Chrome versions)
        options.add_argument("--headless=new") # Runs Chrome without a visible UI
        options.add_argument("--no-sandbox") # Required for running Chrome in a containerized environment (like Colab)
        options.add_argument("--disable-dev-shm-usage") # Overcomes limited /dev/shm space in some environments
        options.add_argument("--disable-gpu") # Disables GPU hardware acceleration
        options.add_argument("--disable-software-rasterizer") # Disables software rasterizer
        options.add_argument("--disable-blink-features=AutomationControlled") # Attempts to hide automation indicators

        # Proxy support: if proxies are defined in SETTINGS, a random one is selected and applied
        if SETTINGS["proxies"]:
            proxy = random.choice(SETTINGS["proxies"])
            options.add_argument(f"--proxy-server={proxy}")
            log_message("DEBUG", f"Using proxy for Selenium: {proxy}", debug_only=True)

        # OS-specific binary fallback: attempts to find Chrome executable in common locations
        # This is primarily for environments where Chrome is not in the default PATH.
        if sys.platform.startswith("linux"):
            # Only set if Chrome is not discoverable via system PATH
            possible_paths = [
                "/usr/bin/google-chrome",
                "/usr/bin/google-chrome-stable",
                "/usr/bin/chromium",
                "/usr/bin/chromium-browser",
            ]
            for path in possible_paths:
                if os.path.exists(path):
                    options.binary_location = path # Set the explicit path to the Chrome binary
                    break

        elif sys.platform.startswith("win"):
            possible_paths = [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            ]
            for path in possible_paths:
                if os.path.exists(path):
                    options.binary_location = path
                    break

        # Preferences: configure browser download behavior and security settings
        prefs = {
            "download.prompt_for_download": False, # Prevent download dialogs
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True, # Enable Google Safe Browsing
        }
        options.add_experimental_option("prefs", prefs)

        # Initialize ChromeDriver using ChromeDriverManager to handle installation/updates
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        # Apply stealth settings to make the Selenium browser less detectable as automated
        stealth(
            driver,
            languages=["en-US", "en"], # Set preferred languages
            vendor="Google Inc.", # Mimic common browser vendor
            platform=random.choice(STEALTH_PLATFORMS), # Randomly select OS platform
            webgl_vendor=random.choice(STEALTH_WEBGL_VENDORS), # Randomly select WebGL vendor
            renderer=random.choice(STEALTH_RENDERERS), # Randomly select renderer
            fix_hairline=True, # Apply a fix for a hairline rendering issue that can be a stealth detection vector
        )

        driver.set_page_load_timeout(240) # Set a maximum time for page to load
        driver.implicitly_wait(10) # Set implicit wait time for element discovery

        return driver

    def destroy_driver(self, driver: webdriver.Chrome) -> None:
        """Safely quit the WebDriver."
        Ensures the browser instance is properly closed, releasing system resources.
        """
        try:
            driver.quit()
        except Exception:
            pass # Ignore errors during quit, as the driver might already be closed

# =========================
# Driver Pool
# =========================

class DriverPool:
    """Thread-safe pool of Selenium WebDrivers."
    Manages a fixed number of WebDriver instances that can be acquired and released
    by multiple threads, reducing the overhead of creating new drivers repeatedly.
    """

    def __init__(self, webdriver_manager: WebDriverManager, pool_size: int):
        self.webdriver_manager = webdriver_manager
        self.pool_size = pool_size
        self.pool = queue.Queue(maxsize=pool_size) # A thread-safe queue to hold driver instances
        self._initialize_pool()

    def _initialize_pool(self):
        """Populates the driver pool with a specified number of WebDriver instances."""
        log_message("INFO", f"Initializing Selenium driver pool with {self.pool_size} drivers")
        for _ in range(self.pool_size):
            driver = self.webdriver_manager.create_driver() # Create a new driver
            self.pool.put(driver) # Add it to the queue

    def acquire(self, timeout=None):
        """Acquires a WebDriver instance from the pool."
        Blocks if no drivers are available until one is released or timeout occurs.
        """
        return self.pool.get(timeout=timeout)

    def release(self, driver):
        """Releases a WebDriver instance back to the pool."
        The driver is then available for reuse by other threads.
        """
        self.pool.put(driver)

    def shutdown(self):
        """Shuts down all WebDriver instances in the pool."
        Called when the application is closing to clean up resources.
        """
        log_message("INFO", "Shutting down Selenium driver pool")
        while not self.pool.empty():
            driver = self.pool.get_nowait() # Get drivers without blocking
            try:
                driver.quit() # Quit each driver
            except Exception:
                pass


# =========================
# Crawler
# =========================

class Crawler:
    """Responsible for fetching web page content and extracting links."
    It attempts to use a faster requests-based approach first, falling back to Selenium
    for dynamic content or JavaScript-rendered pages. It also handles various error scenarios.
    """
    def __init__(self, webdriver_manager: WebDriverManager) -> None:
        self.webdriver_manager = webdriver_manager

    def _get_links_from_page_content(self, base_url: str, driver: webdriver.Chrome):
        """Core logic to load a page using Selenium and extract internal links."
        Handles CAPTCHA detection, retries for timeouts, and WebDriver-specific errors.
        """
        links = set() # Stores unique normalized links found on the page
        relationships_on_page = [] # Stores (source, target) tuples for graph visualization

        parsed_base_url = urlparse(base_url)
        base_netloc = parsed_base_url.netloc
        base_root_domain = get_root_domain(base_netloc)

        log_message(
            "DEBUG",
            f"Starting _get_links_from_page_content for base_url: {base_url} "
            f"with base_netloc: {base_netloc} and root_domain: {base_root_domain}",
            debug_only=True,
        )

        retries = SETTINGS["retries"]
        attempt = 0

        while attempt < retries: # Loop for retrying page load in case of transient errors
            try:
                # Set a random User-Agent for each request to further mimic human browsing
                random_user_agent = generate_random_user_agent()
                driver.execute_cdp_cmd(
                    "Network.setUserAgentOverride", {"userAgent": random_user_agent}
                )

                driver.get(base_url) # Navigate the browser to the URL

                # Introduce a random delay to simulate human reading/interaction time
                time.sleep(
                    random.uniform(
                        SETTINGS["min_link_search_delay"],
                        SETTINGS["max_link_search_delay"],
                    )
                )

                # Define indicators to detect CAPTCHAs or bot-detection challenges
                captcha_indicators = [
                    (By.ID, "g-recaptcha"), # Google reCAPTCHA by ID
                    (By.CLASS_NAME, "g-recaptcha"), # Google reCAPTCHA by class
                    (By.XPATH, "//iframe[contains(@src, 'recaptcha')]"), # reCAPTCHA iframe
                    (By.XPATH, "//*[contains(@class, 'h-captcha')]"), # hCaptcha by class
                    (By.XPATH, "//iframe[contains(@src, 'hcaptcha')]"), # hCaptcha iframe
                    (By.XPATH, "//*[contains(text(), 'verify you are human')]"), # Generic human verification text
                    (By.XPATH, "//div[contains(@class, 'cf-challenge')]"), # Cloudflare challenge
                    (By.XPATH, "//title[contains(text(), 'Attention Required')]"), # Cloudflare attention required page
                ]

                captcha_detected = False
                for by_type, value in captcha_indicators:
                    # Check if any captcha indicator elements are present on the page
                    if driver.find_elements(by_type, value): # find_elements returns a list, empty if not found
                        captcha_detected = True
                        break

                if captcha_detected:
                    with captcha_prompt_lock: # Use a lock to ensure only one thread acts on CAPTCHA at a time
                        log_message(
                            "WARNING",
                            f"CAPTCHA DETECTED for {base_url}. Waiting 5-10 seconds...",
                            debug_only=True,
                        )
                        time.sleep(random.uniform(5, 10)) # Wait before attempting to proceed
                        log_message(
                            "INFO",
                            "Attempting to continue after automated wait...",
                            debug_only=True,
                        )

                log_message(
                    "DEBUG",
                    f"Page loaded for {base_url}. Extracting links...",
                    debug_only=True,
                )
                found_any_href = False

                # Find all 'a' (anchor) elements on the page
                for anchor_element in driver.find_elements(By.TAG_NAME, "a"):
                    href = anchor_element.get_attribute("href") # Get the 'href' attribute (the link URL)
                    if not href:
                        continue # Skip if no href attribute

                    found_any_href = True
                    log_message("DEBUG", f"Found href: {href}", debug_only=True)

                    full_url = urljoin(base_url, href) # Resolve relative URLs to absolute URLs
                    parsed_full_url = urlparse(full_url)

                    link_netloc = parsed_full_url.netloc
                    link_root_domain = get_root_domain(link_netloc)

                    clean_url = normalize_url(full_url) # Normalize the URL for consistent comparison

                    # Determine if the link is relevant and internal (or external if allowed)
                    # Links are added if: (same root domain OR external links allowed) AND not an irrelevant link type.
                    if (
                        (link_root_domain == base_root_domain or SETTINGS["allow_external_links"])
                        and not is_irrelevant_link(clean_url)
                    ):
                        log_message(
                            "DEBUG",
                            f"Adding internal link: {clean_url} "
                            f"(Root domain: {link_root_domain})",
                            debug_only=True,
                        )
                        links.add(clean_url) # Add to the set of unique links
                        if SETTINGS["enable_visual_tree_generation"]:
                            relationships_on_page.append((base_url, clean_url)) # Record for graph visualization
                    else:
                        log_message(
                            "DEBUG",
                            f"Skipping external/irrelevant link: {full_url} "
                            f"(Link root domain: {link_root_domain} != Base root domain: {base_root_domain} "
                            f"OR irrelevant link)", # Adjusted log message to be more explicit
                            debug_only=True,
                        )

                if not found_any_href:
                    log_message(
                        "DEBUG",
                        f"No href attributes found on {base_url} by Selenium.",
                        debug_only=True,
                    )

                log_message(
                    "DEBUG",
                    f"Finished processing {base_url}. Discovered {len(links)} links.",
                    debug_only=True,
                )
                return links, relationships_on_page # Return discovered links and graph relationships

            except TimeoutException:
                log_message(
                    "WARNING",
                    f"Page load timed out for {base_url}. Retrying ({retries - attempt - 1} attempts left).",
                    debug_only=True,
                )
                attempt += 1
                time.sleep(random.uniform(5, 15)) # Wait before retrying
            except WebDriverException as e:
                error_message_lower = str(e).lower()
                # Specific handling for connection refused errors, which might indicate a dead end for a domain
                if (
                    "net::err_connection_refused" in error_message_lower
                    or "connection refused" in error_message_lower
                    or "(connection aborted.)" in error_message_lower
                ):
                    log_message(
                        "ERROR",
                        f"WebDriver error (Connection Refused) while crawling {base_url}: {e}. "
                        f"Skipping further crawling for this branch.",
                    )
                    raise ConnectionRefusedForCrawlerError(base_url) # Raise custom exception to halt further crawling on this branch
                else:
                    log_message(
                        "WARNING",
                        f"Non-connection-refused WebDriver error while crawling {base_url}: {e}. "
                        f"Retrying ({retries - attempt - 1} attempts left).",
                        debug_only=True,
                    )
                attempt += 1
                time.sleep(random.uniform(5, 15))
            except Exception as e:
                log_message(
                    "ERROR",
                    f"Unexpected error while crawling {base_url}: {e}. "
                    f"Retrying ({retries - attempt - 1} attempts left).",
                    debug_only=True,
                )
                attempt += 1
                time.sleep(random.uniform(5, 15))

        log_message(
            "ERROR",
            f"Failed to retrieve {base_url} after {retries} attempts.",
            debug_only=True,
        )
        return set(), [] # Return empty sets if all retries fail

    def _try_requests_first(self, url):
        """Attempt to fetch page with requests before using Selenium."
        This method is faster and lighter than Selenium, suitable for static HTML content.
        It attempts to parse links directly from the HTML response.
        """
        try:
            session = get_requests_session()
            headers = {"User-Agent": generate_random_user_agent()} # Use a random User-Agent
            resp = session.get(url, headers=headers, timeout=15) # Fetch the page content

            if resp.status_code >= 400:
                return None # Return None if there's an HTTP error (client or server side)

            soup = BeautifulSoup(resp.text, "html.parser") # Parse HTML content with Beautiful Soup
            anchors = soup.find_all("a") # Find all anchor tags

            links = set()
            relationships = []

            parsed_base = urlparse(url)
            base_root = get_root_domain(parsed_base.netloc)

            for a in anchors:
                href = a.get("href")
                if not href:
                    continue

                full = urljoin(url, href)
                clean = normalize_url(full)
                parsed = urlparse(clean)
                root = get_root_domain(parsed.netloc)

                # Apply the same link filtering logic as with Selenium
                if (root == base_root or SETTINGS["allow_external_links"]) and not is_irrelevant_link(clean):
                    links.add(clean)
                    if SETTINGS["enable_visual_tree_generation"]:
                        relationships.append((url, clean))

            return links, relationships

        except Exception:
            return None # Return None if any error occurs (e.g., network issues, parsing errors)

    def crawl_single_page(self, url_to_crawl: str):
        """Try fast requests-based crawl first, then fall back to Selenium."
        This is the main entry point for crawling a single URL.
        """
        fast_result = self._try_requests_first(url_to_crawl) # Attempt fast crawl
        if fast_result:
            return fast_result # If successful, return the result immediately

        # If fast crawl fails or is not suitable, use Selenium WebDriver
        driver = self.webdriver_manager.create_driver() # Acquire a WebDriver instance
        try:
            return self._get_links_from_page_content(url_to_crawl, driver) # Perform Selenium-based crawl
        except ConnectionRefusedForCrawlerError as e:
            log_message("INFO", f"Skipping branch due to connection refused: {e.args[0]}")
            return set(), [] # Return empty sets if connection is refused for the branch
        finally:
            self.webdriver_manager.destroy_driver(driver) # Ensure the WebDriver is quit (or returned to pool)


# =========================
# Archiver
# =========================

class Archiver:
    """Handles Wayback Machine archiving with cooldown and rate limiting."
    Interacts with the Wayback Machine API to check archiving status and save URLs.
    """

    def __init__(self) -> None:
        # Initialize global archive action based on settings, defaulting to 'n'
        self.global_archive_action = SETTINGS.get(
            "default_archiving_action", "n"
        ).lower()
        if self.global_archive_action not in ["a", "n", "s"]:
            log_message(
                "WARNING",
                f"Invalid default_archiving_action '{self.global_archive_action}' in SETTINGS. "
                f"Falling back to 'n'.",
                debug_only=True
            )
            self.global_archive_action = "n"

    def should_archive(self, url: str):
        """Determine if URL should be archived based on cooldown and global action."
        Checks if the URL has been recently archived and respects the configured cooldown period.
        """
        user_agent = generate_random_user_agent()
        _ = get_requests_session()  # kept for parity; session not passed to waybackpy, but might be needed for internal checks.
        wayback = waybackpy.Url(url, user_agent) # Create a waybackpy Url object for the given URL

        # Respect global archiving action settings
        if self.global_archive_action == "a":
            return True, wayback # Archive all
        elif self.global_archive_action == "s":
            return False, wayback # Skip all

        retries = SETTINGS.get("retries", 3)
        attempt = 0

        while attempt < retries:
            try:
                newest = wayback.newest() # Get information about the newest archive of the URL
                last_archived_dt = newest.timestamp.replace(tzinfo=timezone.utc) # Get the timestamp of the last archive
                current_utc_dt = datetime.now(timezone.utc)
                time_diff = current_utc_dt - last_archived_dt # Calculate time difference since last archive

                # If last archive is within the cooldown period, skip archiving
                if time_diff < timedelta(days=SETTINGS["archiving_cooldown"]):
                    log_message(
                        "SKIPPED",
                        f"{url} (Last archived {time_diff.total_seconds() // 3600:.1f} hours ago)",
                    )
                    return False, wayback
                else:
                    # If outside cooldown, mark for archiving
                    log_message(
                        "INFO",
                        f"Needs Archive: {url} "
                        f"(Last archived {time_diff.total_seconds() // 3600:.1f} hours ago, "
                        f"> {SETTINGS['archiving_cooldown'] * 24} hours)",
                        debug_only=True
                    )
                    return True, wayback

            except waybackpy.exceptions.NoCDXRecordFound:
                # If no record is found, the URL has never been archived, so it needs archiving
                log_message(
                    "INFO",
                    f"No existing archive found for {url}. Archiving.",
                    debug_only=True
                )
                return True, wayback
            except Exception as e:
                attempt += 1
                if attempt < retries:
                    log_message(
                        "WARNING",
                        f"Error checking archive for {url}: {e}. "
                        f"Retrying ({retries - attempt} attempts left).",
                        debug_only=True
                    )
                    time.sleep(5) # Wait before retrying archive check
                else:
                    # If all retries fail, default to archiving to be safe
                    log_message(
                        "ERROR",
                        f"Failed to check archive for {url} after {retries} attempts: {e}. "
                        f"Defaulting to archive.",
                        debug_only=True
                    )
                    return True, wayback

        return False, wayback # Should not be reached if retries are handled, but as a fallback

    def process_link_for_archiving(self, link: str) -> str:
        """Check if link needs archiving and attempt to save it to Wayback."
        This method incorporates thread-safe rate limiting to respect Wayback Machine's API policies.
        It also handles archiving timeouts and retries for failed archiving attempts.
        """
        global last_archive_time, rate_limit_active_until_time # Access global rate limiting variables

        needs_save, wb_obj = self.should_archive(link,) # Determine if archiving is necessary

        if not needs_save:
            return f"[SKIPPED] {link}" # Return if link doesn't need archiving

        retries = SETTINGS["retries"]
        while retries > 0:
            with archive_lock: # Critical section: ensures thread-safe access to global rate limit variables
                now = time.time()

                # Reactive Global Rate Limit: If a previous archiving attempt hit a global rate limit,
                # current thread waits until that cooldown period is over.
                if now < rate_limit_active_until_time:
                    sleep_duration = rate_limit_active_until_time - now
                    log_message(
                        "RATE LIMIT",
                        f"Global rate limit active. Sleeping for {sleep_duration:.2f} seconds before archiving {link}",
                        debug_only=True,
                    )
                    time.sleep(sleep_duration)

                now = time.time() # Re-evaluate current time after potential global sleep

                # Proactive Individual Archive Delay: Ensures minimum delay between consecutive archive requests
                # from this thread to comply with Wayback Machine's rate limits.
                elapsed = now - last_archive_time
                if elapsed < MIN_ARCHIVE_DELAY_SECONDS:
                    sleep_duration = MIN_ARCHIVE_DELAY_SECONDS - elapsed
                    log_message(
                        "RATE LIMIT",
                        f"Sleeping for {sleep_duration:.2f} seconds before archiving {link}",
                        debug_only=True,
                    )
                    time.sleep(sleep_duration)

                last_archive_time = time.time() # Update the global timestamp of the last archive request

            # --- Start of timeout logic for wb_obj.save() ---
            archive_result = [] # A list to hold the result (success or exception) from the archiving thread

            def _save_target():
                """Target function for the archiving thread. Attempts to save the URL."""
                try:
                    wb_obj.save() # Call waybackpy's save method
                    archive_result.append(True) # Indicate success
                except Exception as e:
                    archive_result.append(e) # Store any exception that occurred

            archive_thread = threading.Thread(target=_save_target) # Create a new thread for archiving
            archive_thread.start()
            # Wait for the archiving thread to complete, with a configured timeout
            archive_thread.join(timeout=SETTINGS['archive_timeout_seconds'])

            if archive_thread.is_alive():
                # If the thread is still alive after join, it means the archiving timed out
                log_message(
                    "WARNING",
                    f"Archiving {link} timed out after {SETTINGS['archive_timeout_seconds']} seconds. Skipping this attempt.",
                    debug_only=True
                )
                retries -= 1 # Decrement retry count
                if retries > 0:
                    log_message(
                        "INFO",
                        f"Retrying archiving for {link} after timeout ({retries} attempts left)...",
                        debug_only=True
                    )
                    time.sleep(2) # Short delay before next retry
                else:
                    return f"[FAILED - TIMEOUT] Failed to archive {link} after {SETTINGS['retries']} attempts due to timeout." # All retries failed due to timeout
            else:
                # The thread completed, now check its result
                if archive_result and archive_result[0] is True:
                    return f"[ARCHIVED] {link}" # Successfully archived
                elif archive_result and isinstance(archive_result[0], Exception):
                    e = archive_result[0] # Retrieve the exception
                    error_message = str(e)
                    rate_limit_keyword = (
                        "Save request refused by the server. Save Page Now limits saving 15 URLs per minutes."
                    )
                    retries -= 1
                    # Check if the failure was due to Wayback Machine's specific rate limit message
                    if rate_limit_keyword in error_message and retries > 0:
                        with archive_lock: # Protect modification of global rate_limit_active_until_time
                            log_message(
                                "WARNING",
                                f"Wayback Machine rate limit hit for {link}. "
                                f"Pausing for 1 minute and activating global cooldown ({retries} attempts left).",
                                debug_only=True,
                            )
                            rate_limit_active_until_time = time.time() + 60 # Set global cooldown for 60 seconds
                        time.sleep(60) # Current thread waits for the rate limit period
                    elif retries > 0:
                        log_message(
                            "WARNING",
                            f"Could not save {link}: {e}. Retrying ({retries} attempts left)...",
                        )
                        time.sleep(2) # Short delay before next retry
                    else:
                        return f"[FAILED] Failed to archive {link} after multiple attempts: {e}" # All retries failed for other reasons
                else:
                    # Fallback for unexpected thread completion without a clear result
                    retries -= 1
                    log_message(
                        "ERROR",
                        f"Archiving thread for {link} finished unexpectedly without result. Retrying ({retries} attempts left)...",
                        debug_only=True
                    )
                    time.sleep(2) # Short delay before next retry

        return f"[FAILED] Failed to archive {link} after multiple attempts." # Should only be reached if all retries are exhausted


# =========================
# Visual Graph Builder
# =========================

class VisualGraphBuilder:
    """Builds and optionally displays a link graph using networkx."
    Visualizes the relationships (links) discovered during the crawling process.
    """

    def __init__(self) -> None:
        self.edges = [] # List to store (source, target) tuples representing links

    def add_relationships(self, relationships):
        """Add (source, target) relationships to the graph builder."
        Each tuple represents a link from a source URL to a target URL.
        """
        self.edges.extend(relationships)

    def build_and_show(self):
        """Build and display the graph if visualization is enabled."
        Uses NetworkX to create a directed graph and Matplotlib to draw it.
        """
        if not SETTINGS["enable_visual_tree_generation"]:
            return # Do nothing if visualization is disabled
        if not self.edges:
            log_message("INFO", "No relationships to visualize.", debug_only=True)
            return

        graph = nx.DiGraph() # Create a directed graph
        graph.add_edges_from(self.edges) # Add all recorded links as edges

        plt.figure(figsize=(12, 8)) # Set figure size for the plot
        pos = nx.spring_layout(graph, k=0.3) # Calculate node positions using a spring layout algorithm
        nx.draw(
            graph,
            pos,
            with_labels=False, # Do not display node labels (can be too cluttered for large graphs)
            node_size=50, # Size of each node in the graph
            arrows=True, # Draw arrows to indicate link direction
            arrowstyle="-|>", # Style of the arrows
            arrowsize=10,
        )
        plt.title("Crawl Link Graph") # Set plot title
        plt.tight_layout() # Adjust layout to prevent labels/elements from overlapping
        plt.show() # Display the plot


# =========================
# Crawl Coordinator
# =========================

class CrawlCoordinator:
    """Coordinates crawling and archiving with concurrency and queues."
    This is the main orchestrator, managing multiple crawler and archiver threads,
    queues, and visited URL tracking.
    """

    def __init__(self) -> None:
        self.webdriver_manager = WebDriverManager() # Manages Selenium WebDriver instances
        self.crawler = Crawler(self.webdriver_manager) # Handles page fetching and link extraction
        self.driver_pool = DriverPool(self.webdriver_manager, pool_size=10) # Pool of WebDrivers for efficiency
        self.archiver = Archiver() # Handles Wayback Machine archiving
        self.graph_builder = VisualGraphBuilder() # Builds link graph for visualization
        self.crawling_queue = deque() # Queue for URLs to be crawled (stores (url, root_domain) tuples)
        self.queue_for_archiving = deque() # Queue for URLs to be archived
        self.visited_urls = set() # Set to keep track of URLs that have been visited/enqueued to avoid cycles and duplicates
        self.crawling_futures_set = set() # (Not currently used, but could be for explicit tracking of Futures)
        self.archiving_futures_set = set() # (Not currently used, but could be for explicit tracking of Futures)
        self.skipped_root_domains = set() # Stores root domains that had a connection refused error, to avoid re-crawling

        self._resolve_worker_counts() # Determine actual worker counts based on settings

    def _resolve_worker_counts(self) -> None:
        """Resolve max workers for crawler and archiver based on SETTINGS."
        Applies 'safety_switch' if enabled, limiting crawling to a single worker.
        """
        max_crawler_workers_setting = SETTINGS["max_crawler_workers"]
        if SETTINGS.get("safety_switch", False): # Check if safety switch is active
            self.max_crawler_workers = 1 # Force 1 crawler worker for sequential mode
            log_message(
                "INFO",
                "Sequential crawling mode is enabled. Crawling with 1 worker.",
                debug_only=True,
            )
        elif max_crawler_workers_setting == 0:
            self.max_crawler_workers = None # None means ThreadPoolExecutor will use default (usually # of CPU cores * 5)
        else:
            self.max_crawler_workers = max_crawler_workers_setting

        max_archiver_workers_setting = SETTINGS["max_archiver_workers"]
        if max_archiver_workers_setting == 0:
            self.max_archiver_workers = None # None means unlimited archiver workers (within system limits)
        else:
            self.max_archiver_workers = max_archiver_workers_setting

    def add_initial_urls(self, urls):
        """Normalize and enqueue initial URLs for crawling and archiving."
        Filters out invalid URLs and ensures unique entries.
        """
        for url in urls:
            if not url.startswith("http"): # Basic validation for URL format
                log_message(
                    "WARNING",
                    f"Invalid URL format for {url}. Skipping.",
                    debug_only=True,
                )
                continue
            normalized_url = normalize_url(url) # Normalize the URL for consistency
            root_domain = get_root_domain(urlparse(normalized_url).netloc)

            if normalized_url not in self.visited_urls: # Add only if not already processed/enqueued
                log_message(
                    "INFO",
                    f"Adding initial URL to queues: {normalized_url}",
                    debug_only=True,
                )
                self.visited_urls.add(normalized_url) # Mark as visited
                self.crawling_queue.append((normalized_url, root_domain)) # Add to crawling queue
                self.queue_for_archiving.append(normalized_url) # Add to archiving queue

    def _submit_crawl_tasks(self, executor):
        """Submits crawl tasks to the thread pool executor."
        Pops URLs from the crawling queue and creates futures for their processing.
        Skips URLs whose root domains have previously caused connection refused errors.
        """
        futures = {} # Dictionary to map Future objects back to their original URL and root domain
        while self.crawling_queue: # While there are URLs to crawl
            url, root_domain = self.crawling_queue.popleft() # Get the next URL from the left of the deque
            if root_domain in self.skipped_root_domains: # Check if this root domain is to be skipped
                log_message(
                    "INFO",
                    f"Skipping URL {url} because its root domain {root_domain} "
                    f"was previously marked as connection refused.",
                    debug_only=True,
                )
                continue
            future = executor.submit(self.crawler.crawl_single_page, url) # Submit crawl task to executor
            futures[future] = (url, root_domain) # Store future with associated URL and root domain
        return futures

    def _submit_archive_tasks(self, executor):
        """Submits archiving tasks to the thread pool executor."
        Pops URLs from the archiving queue and creates futures for their processing.
        """
        futures = {} # Dictionary to map Future objects back to their original URL
        while self.queue_for_archiving: # While there are URLs to archive
            url = self.queue_for_archiving.popleft() # Get the next URL
            future = executor.submit(self.archiver.process_link_for_archiving, url) # Submit archive task
            futures[future] = url # Store future with associated URL
        return futures

    def run(self):
        """Main coordination loop: crawl + archive until queues are empty."
        This method uses two separate ThreadPoolExecutors for crawling and archiving,
        allowing them to run concurrently. It continuously monitors queues and processes results.
        """
        log_message(
            "INFO",
            f"Starting main processing loop with {len(self.crawling_queue)} initial URLs.",
            debug_only=True,
        )

        # Initialize two thread pool executors: one for crawling, one for archiving
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=self.max_crawler_workers # Configure with resolved crawler worker count
        ) as crawler_executor, concurrent.futures.ThreadPoolExecutor(
            max_workers=self.max_archiver_workers # Configure with resolved archiver worker count
        ) as archiver_executor:

            # Main loop continues as long as there are URLs to crawl or archive
            while self.crawling_queue or self.queue_for_archiving:
                # Submit all available crawl tasks from the queue
                crawl_futures = self._submit_crawl_tasks(crawler_executor)

                # Process completed crawl results
                for future in concurrent.futures.as_completed(crawl_futures): # Blocks until at least one crawl task completes
                    url = crawl_futures[future][0] # Retrieve the original URL associated with the completed future
                    root_domain = crawl_futures[future][1] # Retrieve the root domain
                    try:
                        links_on_page, relationships_on_page = future.result() # Get the result of the crawl task
                    except ConnectionRefusedForCrawlerError: # Handle specific connection refused error from crawler
                        log_message(
                            "INFO",
                            f"Marking root domain {root_domain} as skipped due to connection refused.",
                            debug_only=True,
                        )
                        self.skipped_root_domains.add(root_domain) # Add domain to skipped list
                        continue # Skip to the next completed future
                    except Exception as e:
                        log_message(
                            "ERROR",
                            f"Error while crawling {url}: {e}",
                            debug_only=True,
                        )
                        continue # Skip to the next completed future if an unexpected error occurs

                    # Add relationships to graph builder if visualization is enabled
                    if SETTINGS["enable_visual_tree_generation"]:
                        self.graph_builder.add_relationships(relationships_on_page)

                    # Enqueue newly discovered links for further crawling and archiving
                    for link in links_on_page:
                        if link not in self.visited_urls: # Ensure link is not already known
                            self.visited_urls.add(link) # Mark as visited/enqueued
                            link_root_domain = get_root_domain(
                                urlparse(link).netloc
                            )
                            self.crawling_queue.append((link, link_root_domain)) # Add to crawling queue
                            self.queue_for_archiving.append(link) # Add to archiving queue

                # Submit all available archive tasks from the queue
                archive_futures = self._submit_archive_tasks(archiver_executor)

                # Process completed archive results
                for future in concurrent.futures.as_completed(archive_futures): # Blocks until at least one archive task completes
                    url = archive_futures[future] # Retrieve the original URL for the completed archive task
                    try:
                        result = future.result() # Get the result (status message) of the archiving task
                        log_message("INFO", result) # Log the archiving result
                    except Exception as e:
                        log_message(
                            "ERROR",
                            f"Error while archiving {url}: {e}",
                            debug_only=True,
                        )

        # After all crawling and archiving queues are empty, build and show the visual graph
        self.graph_builder.build_and_show()
        self.driver_pool.shutdown() # Ensure all WebDriver instances are properly closed

# =========================
# Main Entry Point
# =========================

def main():
    """Main function to orchestrate crawling and archiving."
    Prompts the user for initial URLs and starts the CrawlCoordinator.
    """
    clear_output(wait=True) # Clears previous output in Colab/Jupyter for a cleaner console

    target_urls_input = input(
        "Enter URLs (comma-separated, e.g., https://notawebsite.org/, https://example.com/): "
    ).strip()
    # Parse input string into a list of URLs
    initial_urls_raw = [
        url.strip() for url in target_urls_input.split(",") if url.strip()
    ]

    if not initial_urls_raw:
        log_message("INFO", "No valid URLs entered.", debug_only=False)
        return # Exit if no URLs provided

    coordinator = CrawlCoordinator() # Instantiate the main coordinator
    coordinator.add_initial_urls(initial_urls_raw) # Add user-provided URLs to start the process
    coordinator.run() # Start the crawling and archiving process


if __name__ == "__main__":
    main() # Execute the main function when the script is run
