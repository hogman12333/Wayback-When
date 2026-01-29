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
import warnings
import random
import os
import logging
import re # Import regex for parsing duration

# Selenium imports
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium_stealth import stealth

# Visualization imports
import networkx as nx
import matplotlib.pyplot as plt

# Jupyter/console helper (optional)
try:
    from IPython.display import clear_output
except ImportError:
    def clear_output(wait=False):
        pass  # No-op when not in Jupyter

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)


# =========================
# Custom Exceptions
# =========================

class CaptchaDetectedError(Exception):
    """Raised when a CAPTCHA is detected on a page."""
    pass


class ConnectionRefusedForCrawlerError(Exception):
    """Raised when a connection is refused for a given URL branch."""
    pass


# =========================
# Settings
# =========================

SETTINGS = {
    "allow_external_links": False,     # New setting: True to allow crawling external links
    "archive_timeout_seconds": 1200,   # seconds for archiving a single link
    "archiving_cooldown": 90,          # days
    "debug_mode": False,
    "default_archiving_action": "N",   # 'n' normal, 'a' archive all, 's' skip all
    "enable_visual_tree_generation": False,
    "max_archiver_workers": 1,         # 0 = unlimited
    "max_crawler_workers": 10,         # 0 = Unlimited
    "min_link_search_delay": 0.0,
    "max_link_search_delay": 5.0,
    "max_runtime": 0,                  # Maximum runtime in Seconds (0 = Unlimited)
    "proxies": [],                     # e.g. ['http://user:pass@ip:port']
    "retries": 3,                      # retries for crawling/archiving
    "safety_switch": False,            # Forces the script to slowdown to avoid detection
    "urls_per_minute_limit": 15,       # Wayback rate limit
}

# Thread-local storage (if needed later)
_thread_local = threading.local()

# Lock to ensure only one CAPTCHA prompt is active at a time
captcha_prompt_lock = threading.Lock()

# Archive rate limiting
archive_lock = threading.Lock()
last_archive_time = 0.0  # global timestamp of last archive request
rate_limit_active_until_time = 0.0 # New global timestamp for reactive rate limiting

# Minimum delay between archive requests
MIN_ARCHIVE_DELAY_SECONDS = 60 / SETTINGS["urls_per_minute_limit"]


# =========================
# User-Agent / Stealth Pools
# =========================

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
    "AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/{version}.0.0.0 Mobile/15E148 Safari/604.1",
]

CHROME_VERSIONS = [str(v) for v in range(1, 126)]
FIREFOX_VERSIONS = [str(v) for v in range(1, 126)]
SAFARI_VERSIONS = [str(v) for v in range(1, 18)]

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

IRRELEVANT_PATH_SEGMENTS = (
    "/cdn-cgi/",
    "/assets/",
    "/uploads/",
    "/wp-content/",
    "/wp-includes/",
    "/themes/",
    "/plugins/",
    "/node_modules/",
    "/static/",
    "/javascript/",
    "/css/",
    "/img/",
)


# =========================
# Logging
# =========================

def log_message(level: str, message: str, debug_only: bool = False) -> None:
    """Standardized logging function."""
    if debug_only and not SETTINGS["debug_mode"]:
        return
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}][{level.upper()}] {message}")


# =========================
# Utility Functions
# =========================

def generate_random_user_agent() -> str:
    """Generate a random realistic User-Agent string."""
    os_part = random.choice(OS_TYPES)
    browser_template = random.choice(BROWSER_TYPES)

    if "Chrome" in browser_template:
        version = random.choice(CHROME_VERSIONS)
    elif "Firefox" in browser_template:
        version = random.choice(FIREFOX_VERSIONS)
    elif "Safari" in browser_template or "CriOS" in browser_template:
        version = random.choice(SAFARI_VERSIONS)
    else:
        version = "100"

    browser = browser_template.format(version=version)
    return f"Mozilla/5.0 ({os_part}) {browser}"


def normalize_url(url: str) -> str:
    parsed = urlparse(url)

    scheme = parsed.scheme.lower()
    netloc = parsed.netloc.lower()

    # Normalize path
    path = parsed.path or "/"
    path = path.replace("//", "/")
    path = path.rstrip("/") if path not in ("/", "") else "/"
    path = path.lower()

    # Remove index pages
    for index_page in ["index.html", "index.htm", "default.html", "default.htm"]:
        if path.endswith(index_page):
            path = path[: -len(index_page)]
            if not path:
                path = "/"

    # Remove fragments
    fragment = ""

    # Clean query params
    query_params = parse_qs(parsed.query)
    tracking_params = (
        "utm_source", "utm_medium", "utm_campaign", "utm_term",
        "utm_content", "gclid", "fbclid", "ref", "src", "cid", "referrer"
    )
    for p in tracking_params:
        query_params.pop(p, None)

    query = urlencode(sorted(query_params.items()), doseq=True)

    return urlunparse((scheme, netloc, path, parsed.params, query, fragment))

def get_root_domain(netloc: str) -> str:
    """Extract root domain from netloc (simple heuristic)."""
    netloc = netloc.lower()
    parts = netloc.split(".")
    if len(parts) > 2 and parts[0] == "www":
        return ".".join(parts[1:])
    elif len(parts) > 2:
        return ".".join(parts[-2:])
    return netloc


def is_irrelevant_link(url: str) -> bool:
    """Check if URL should be considered irrelevant for crawling."""
    parsed_url = urlparse(url)
    path = parsed_url.path.lower()

    if path.endswith(IRRELEVANT_EXTENSIONS):
        return True

    for segment in IRRELEVANT_PATH_SEGMENTS:
        if segment in path:
            return True
    return False

def redact_proxy(proxy: str) -> str:
    """Strips username/password from a proxy string for logging."""
    parsed = urlparse(proxy)
    if parsed.username or parsed.password:
        # Reconstruct the URL without username and password
        netloc = parsed.hostname
        if parsed.port:
            netloc = f"{netloc}:{parsed.port}"
        return urlunparse((parsed.scheme, netloc, "", "", "", ""))
    return proxy


# =========================
# HTTP Session Factory
# =========================

retry_strategy = Retry(
    total=5,
    backoff_factor=1,
    status_forcelist=[403, 404, 429, 500, 502, 503, 504],
    allowed_methods=False,
)
adapter = HTTPAdapter(max_retries=retry_strategy)


def get_requests_session() -> requests.Session:
    """Return a configured requests.Session with retries and optional proxy."""
    session = requests.Session()
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    if SETTINGS["proxies"]:
        proxy = random.choice(SETTINGS["proxies"])
        session.proxies = {"http": proxy, "https": proxy}
        log_message("DEBUG", f"Using proxy for requests session: {redact_proxy(proxy)}", debug_only=True)

    return session


# =========================
# WebDriver Manager
# =========================

class WebDriverManager:
    """Encapsulates Selenium WebDriver creation and teardown."""

    def __init__(self) -> None:
        pass

    def create_driver(self) -> webdriver.Chrome:
        """Create and configure a headless Chrome WebDriver with stealth."""
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")

        # Conditionally set binary location for Colab environment
        if os.name == 'posix' and os.path.exists('/usr/bin/google-chrome'):
            options.binary_location = '/usr/bin/google-chrome'

        if SETTINGS["proxies"]:
            proxy = random.choice(SETTINGS["proxies"])
            options.add_argument(f"--proxy-server={proxy}")
            log_message("DEBUG", f"Using proxy for Selenium: {redact_proxy(proxy)}", debug_only=True)

        prefs = {
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
            "download.default_directory": "/dev/null",
        }
        options.add_experimental_option("prefs", prefs)

        service = ChromeService(executable_path=ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        stealth(
            driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform=random.choice(STEALTH_PLATFORMS),
            webgl_vendor=random.choice(STEALTH_WEBGL_VENDORS),
            renderer=random.choice(STEALTH_RENDERERS),
            fix_hairline=True,
        )

        driver.set_page_load_timeout(240)
        driver.implicitly_wait(10)
        return driver

    def destroy_driver(self, driver: webdriver.Chrome) -> None:
        """Safely quit the WebDriver."""
        try:
            driver.quit()
        except Exception:
            pass


# =========================
# Crawler
# =========================

class Crawler:
    """Responsible for crawling pages using Selenium and extracting internal links."""

    def __init__(self, webdriver_manager: WebDriverManager) -> None:
        self.webdriver_manager = webdriver_manager

    def _get_links_from_page_content(self, base_url: str, driver: webdriver.Chrome):
        """Core logic to load a page and extract internal links."""
        links = set()
        relationships_on_page = []

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

        while attempt < retries:
            try:
                random_user_agent = generate_random_user_agent()
                driver.execute_cdp_cmd(
                    "Network.setUserAgentOverride", {"userAgent": random_user_agent}
                )

                driver.get(base_url)

                time.sleep(
                    random.uniform(
                        SETTINGS["min_link_search_delay"],
                        SETTINGS["max_link_search_delay"],
                    )
                )

                captcha_indicators = [
                    (By.ID, "g-recaptcha"),
                    (By.CLASS_NAME, "g-recaptcha"),
                    (By.XPATH, "//iframe[contains(@src, 'recaptcha')]"),
                    (By.XPATH, "//*[contains(@class, 'h-captcha')]"),
                    (By.XPATH, "//iframe[contains(@src, 'hcaptcha')]"),
                    (By.XPATH, "//*[contains(text(), 'verify you are human')]"),
                    (By.XPATH, "//div[contains(@class, 'cf-challenge')]"),
                    (By.XPATH, "//title[contains(text(), 'Attention Required')]"),
                ]

                captcha_detected = False
                for by_type, value in captcha_indicators:
                    if driver.find_elements(by_type, value):
                        captcha_detected = True
                        break

                if captcha_detected:
                    with captcha_prompt_lock:
                        log_message(
                            "WARNING",
                            f"CAPTCHA DETECTED for {base_url}. Waiting 5-10 seconds...",
                            debug_only=True,
                        )
                        time.sleep(random.uniform(5, 10))
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
                anchor_elements = driver.find_elements(By.TAG_NAME, "a")
                log_message("DEBUG", f"Found {len(anchor_elements)} <a> tags on {base_url}", debug_only=True)

                for anchor_element in anchor_elements:
                    href = anchor_element.get_attribute("href")
                    if not href:
                        log_message("DEBUG", f"Skipping <a> tag with no href attribute on {base_url}.", debug_only=True)
                        continue

                    found_any_href = True
                    log_message("DEBUG", f"Found raw href: {href} on {base_url}", debug_only=True)

                    full_url = urljoin(base_url, href)
                    parsed_full_url = urlparse(full_url)

                    link_netloc = parsed_full_url.netloc
                    link_root_domain = get_root_domain(link_netloc)

                    clean_url = normalize_url(full_url)

                    if (
                        (link_root_domain == base_root_domain or SETTINGS["allow_external_links"])
                        and not is_irrelevant_link(clean_url)
                    ):
                        log_message(
                            "INFO",
                            f"Discovered internal link: {clean_url} "
                            f"(Root domain: {link_root_domain})",
                            debug_only=True
                        )
                        links.add(clean_url)
                        if SETTINGS["enable_visual_tree_generation"]:
                            relationships_on_page.append((base_url, clean_url))
                    else:
                        skip_reason = []
                        if link_root_domain != base_root_domain and not SETTINGS["allow_external_links"]:
                            skip_reason.append(f"External Domain ({link_root_domain} != {base_root_domain})")
                        if is_irrelevant_link(clean_url):
                            skip_reason.append("Irrelevant Link")

                        log_message(
                            "DEBUG",
                            f"Skipping link: {full_url} - Reason: {'; '.join(skip_reason)}",
                            debug_only=True,
                        )

                if not found_any_href:
                    log_message(
                        "DEBUG",
                        f"No href attributes found on {base_url} that were processed as valid links by Selenium.",
                        debug_only=True,
                    )

                log_message(
                    "INFO",
                    f"Finished processing {base_url}. Discovered {len(links)} links.",
                    debug_only=False,
                )
                return links, relationships_on_page

            except TimeoutException:
                log_message(
                    "WARNING",
                    f"Page load timed out for {base_url}. Retrying ({retries - attempt - 1} attempts left).",
                    debug_only=False,
                )
                attempt += 1
                time.sleep(random.uniform(5, 15))
            except WebDriverException as e:
                error_message_lower = str(e).lower()
                if (
                    "net::err_connection_refused" in error_message_lower
                    or "connection refused" in error_message_lower
                    or "(connection aborted.)" in error_message_lower
                ):
                    log_message(
                        "ERROR",
                        f"WebDriver error (Connection Refused) while crawling {base_url}: {e}. "
                        f"Skipping further crawling for this branch.",
                        debug_only=True
                    )
                    raise ConnectionRefusedForCrawlerError(base_url)
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
                    debug_only=False,
                )
                attempt += 1
                time.sleep(random.uniform(2, 10))

        log_message(
            "ERROR",
            f"Failed to retrieve {base_url} after {retries} attempts.",
            debug_only=False,
        )
        return set(), []

    def _try_requests_first(self, url):
        """Attempt to fetch page with requests before using Selenium."""
        try:
            session = get_requests_session()
            headers = {"User-Agent": generate_random_user_agent()}
            resp = session.get(url, headers=headers, timeout=15)

            if resp.status_code >= 400:
                return None

            soup = BeautifulSoup(resp.text, "html.parser")
            anchors = soup.find_all("a")

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

                if (root == base_root or SETTINGS["allow_external_links"]) and not is_irrelevant_link(clean):
                    links.add(clean)
                    if SETTINGS["enable_visual_tree_generation"]:
                        relationships.append((url, clean))

            return links, relationships

        except Exception:
            return None

    def crawl_single_page(self, url_to_crawl: str):
        """Try fast requests-based crawl first, then fall back to Selenium."""
        fast_result = self._try_requests_first(url_to_crawl)
        if fast_result:
            return fast_result

        driver = self.webdriver_manager.create_driver()
        try:
            return self._get_links_from_page_content(url_to_crawl, driver)
        except ConnectionRefusedForCrawlerError as e:
            # Re-raise the exception to be caught by the coordinator
            raise e
        finally:
            self.webdriver_manager.destroy_driver(driver)


# =========================
# Archiver
# =========================

class Archiver:
    """Handles Wayback Machine archiving with cooldown and rate limiting."""

    def __init__(self) -> None:
        self.global_archive_action = SETTINGS.get(
            "default_archiving_action", "n"
        ).lower()
        if self.global_archive_action not in ["a", "n", "s"]:
            log_message(
                "WARNING",
                f"Invalid default_archiving_action '{self.global_archive_action}' in SETTINGS. "
                f"Falling back to 'n'.",
                debug_only=False
            )
            self.global_archive_action = "n"

    def should_archive(self, url: str):
        """Determine if URL should be archived based on cooldown and global action."""
        user_agent = generate_random_user_agent()
        _ = get_requests_session()  # kept for parity; session not passed to waybackpy
        wayback = waybackpy.Url(url, user_agent)

        if self.global_archive_action == "a":
            return True, wayback
        elif self.global_archive_action == "s":
            return False, wayback

        retries = SETTINGS.get("retries", 3)
        attempt = 0

        while attempt < retries:
            try:
                newest = wayback.newest()
                last_archived_dt = newest.timestamp.replace(tzinfo=timezone.utc)
                current_utc_dt = datetime.now(timezone.utc)
                time_diff = current_utc_dt - last_archived_dt

                if time_diff < timedelta(days=SETTINGS["archiving_cooldown"]):
                    log_message(
                        "SKIPPED",
                        f"{url} (Last archived {time_diff.total_seconds() // 3600:.1f} hours ago)",
                        debug_only=True
                    )
                    return False, wayback
                else:
                    log_message(
                        "INFO",
                        f"Needs Archive: {url} "
                        f"(Last archived {time_diff.total_seconds() // 3600:.1f} hours ago, "
                        f"> {SETTINGS['archiving_cooldown'] * 24} hours)",
                        debug_only=True
                    )
                    return True, wayback

            except waybackpy.exceptions.NoCDXRecordFound:
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
                    time.sleep(5)
                else:
                    log_message(
                        "ERROR",
                        f"Failed to check archive for {url} after {retries} attempts: {e}. "
                        f"Defaulting to archive.",
                        debug_only=True
                    )
                    return True, wayback

        return False, wayback

    def process_link_for_archiving(self, link: str) -> tuple[str, str]:
        """Check if link needs archiving and attempt to save it to Wayback."""
        global last_archive_time, rate_limit_active_until_time

        needs_save, wb_obj = self.should_archive(link,)

        if not needs_save:
            return "SKIPPED", link

        retries = SETTINGS["retries"]
        while retries > 0:
            with archive_lock:
                now = time.time()

                # Check for global rate limit imposed by another thread
                if now < rate_limit_active_until_time:
                    sleep_duration = rate_limit_active_until_time - now
                    log_message(
                        "RATE LIMIT",
                        f"Global rate limit active. Sleeping for {sleep_duration:.2f} seconds before archiving {link}",
                        debug_only=True,
                    )
                    time.sleep(sleep_duration)

                now = time.time() # Re-evaluate now after potential global sleep

                # Check for proactive individual archive delay
                elapsed = now - last_archive_time
                if elapsed < MIN_ARCHIVE_DELAY_SECONDS:
                    sleep_duration = MIN_ARCHIVE_DELAY_SECONDS - elapsed
                    log_message(
                        "RATE LIMIT",
                        f"Sleeping for {sleep_duration:.2f} seconds before archiving {link}",
                        debug_only=True,
                    )
                    time.sleep(sleep_duration)

                last_archive_time = time.time() # Update last_archive_time right before attempt

            # --- Start of timeout logic for wb_obj.save() ---
            archive_result = [] # A list to hold the result or exception from the archiving thread

            def _save_target():
                try:
                    wb_obj.save()
                    archive_result.append(True) # Indicate success
                except Exception as e:
                    archive_result.append(e) # Store exception

            archive_thread = threading.Thread(target=_save_target)
            archive_thread.daemon = True # Set as daemon to prevent blocking shutdown
            archive_thread.start()
            archive_thread.join(timeout=SETTINGS['archive_timeout_seconds'])

            if archive_thread.is_alive():
                log_message(
                    "INFO",
                    f"Archiving {link} timed out after {SETTINGS['archive_timeout_seconds']} seconds. Skipping this attempt.",
                    debug_only=False
                )
                return "FAILED", link # Immediately return FAILED on timeout
            else:
                # The thread completed, check its result
                if archive_result and archive_result[0] is True:
                    return "ARCHIVED", link # Return status and URL
                elif archive_result and isinstance(archive_result[0], Exception):
                    e = archive_result[0] # Get the exception
                    error_message = str(e)
                    rate_limit_keyword = (
                        "Save request refused by the server. Save Page Now limits saving 15 URLs per minutes."
                    )
                    retries -= 1
                    if rate_limit_keyword in error_message and retries > 0:
                        with archive_lock: # Protect update to global rate_limit_active_until_time
                            log_message(
                                "WARNING",
                                f"Wayback Machine rate limit hit for {link}. "
                                f"Pausing for 1 minute and activating global cooldown ({retries} attempts left).",
                                debug_only=True,
                            )
                            # Set global cooldown for 60 seconds
                            rate_limit_active_until_time = time.time() + 60
                        # This sleep is for the *current* thread that hit the rate limit
                        time.sleep(60)
                    elif retries > 0:
                        log_message(
                            "WARNING",
                            f"Could not save {link}: {e}. Retrying ({retries} attempts left)...",
                            debug_only=True
                        )
                        time.sleep(2)
                    else:
                        return "FAILED", link # Return status and URL
                else:
                    retries -= 1
                    log_message(
                        "ERROR",
                        f"Archiving thread for {link} finished unexpectedly without result. Retrying ({retries} attempts left)...",
                        debug_only=True
                    )
                    time.sleep(2)

        return "FAILED", link # Return status and URL


# =========================
# Visual Graph Builder
# =========================

class VisualGraphBuilder:
    """Builds and optionally displays a link graph using networkx."""

    def __init__(self) -> None:
        self.edges = []

    def add_relationships(self, relationships):
        """Add (source, target) relationships."""
        self.edges.extend(relationships)

    def build_and_show(self):
        """Build and display the graph if enabled."""
        if not SETTINGS["enable_visual_tree_generation"]:
            return
        if not self.edges:
            log_message("INFO", "No relationships to visualize.", debug_only=True)
            return

        graph = nx.DiGraph()
        graph.add_edges_from(self.edges)

        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(graph, k=0.3)
        nx.draw(
            graph,
            pos,
            with_labels=False,
            node_size=50,
            arrows=True,
            arrowstyle="-|>",
            arrowsize=10,
        )
        plt.title("Crawl Link Graph")
        plt.tight_layout()
        plt.show()


# =========================
# Crawl Coordinator
# =========================

class CrawlCoordinator:
    """Coordinates crawling and archiving with concurrency and queues."""

    def __init__(self) -> None:
        self.webdriver_manager = WebDriverManager()
        self.crawler = Crawler(self.webdriver_manager)
        self.archiver = Archiver()
        self.graph_builder = VisualGraphBuilder()

        self.crawling_queue = deque()
        self.queue_for_archiving = deque()
        self.visited_urls = set()
        self.crawling_futures_set = set() # Store (Future, url, root_domain) tuples
        self.archiving_futures_set = set() # Store (Future, url) tuples
        self.skipped_root_domains = set()

        # Archiving stats
        self.archived_count = 0
        self.skipped_count = 0
        self.failed_count = 0
        self.total_links_to_archive = 0 # Initialize for progress bar

        self._resolve_worker_counts()

    def _resolve_worker_counts(self) -> None:
        """Resolve max workers for crawler and archiver based on SETTINGS."""
        max_crawler_workers_setting = SETTINGS["max_crawler_workers"]
        if max_crawler_workers_setting == 0:
            self.max_crawler_workers = None # None implies unlimited
        else:
            self.max_crawler_workers = max_crawler_workers_setting

        max_archiver_workers_setting = SETTINGS["max_archiver_workers"]
        if max_archiver_workers_setting == 0:
            self.max_archiver_workers = None # None implies unlimited
        else:
            self.max_archiver_workers = max_archiver_workers_setting

        if SETTINGS.get("safety_switch", False):
            self.max_crawler_workers = 1
            SETTINGS["min_link_search_delay"] = 12.0
            SETTINGS["max_link_search_delay"] = 15.0
            log_message(
                "INFO",
                "Safety is enabled. Crawling with 1 worker and increasing cooldown.",
                debug_only=False,
            )

    def add_initial_urls(self, urls):
        """Normalize and enqueue initial URLs for crawling and archiving."""
        for url in urls:
            parsed_url = urlparse(url)
            # If scheme is empty, prepend http://
            if not parsed_url.scheme:
                url = "http://" + url
                log_message("INFO", f"Prepending 'http://' to URL: {url}", debug_only=True)

            # After ensuring a scheme exists, check for validity
            parsed_url_with_scheme = urlparse(url)
            if not parsed_url_with_scheme.scheme or not parsed_url_with_scheme.netloc:
                log_message("WARNING", f"Invalid URL format for {url}. Skipping.", debug_only=False)
                continue

            normalized_url = normalize_url(url)
            root_domain = get_root_domain(urlparse(normalized_url).netloc)

            if normalized_url not in self.visited_urls:
                log_message("INFO", f"Starting with URLs: {normalized_url}", debug_only=False)
                self.visited_urls.add(normalized_url)
                self.crawling_queue.append((normalized_url, root_domain))
                self.queue_for_archiving.append(normalized_url)
        self.total_links_to_archive = len(self.queue_for_archiving) # Set initial total

    def _submit_crawl_tasks(self, executor):
        """Submit crawl tasks while respecting queue and skipped domains and worker limits."""
        while (
            self.crawling_queue
            and (self.max_crawler_workers is None or len(self.crawling_futures_set) < self.max_crawler_workers)
        ):
            url, root_domain = self.crawling_queue.popleft()
            if root_domain in self.skipped_root_domains:
                log_message(
                    "INFO",
                    f"Skipping URL {url} because its root domain {root_domain} was marked as refused.",
                    debug_only=True,
                )
                continue
            future = executor.submit(self.crawler.crawl_single_page, url)
            self.crawling_futures_set.add((future, url, root_domain))
            log_message("INFO", f"Submitted crawl task for: {url}", debug_only=True)

    def _submit_archive_tasks(self, executor):
        """Submit archiving tasks for URLs in the archiving queue, respecting worker limits."""
        while (
            self.queue_for_archiving
            and (self.max_archiver_workers is None or len(self.archiving_futures_set) < self.max_archiver_workers)
        ):
            url = self.queue_for_archiving.popleft()
            future = executor.submit(self.archiver.process_link_for_archiving, url)
            self.archiving_futures_set.add((future, url))
            log_message("DEBUG", f"Submitted archive task for: {url}", debug_only=True)

    def run(self):
        """Main coordination loop: crawl + archive until queues are empty."""
        log_message(
            "INFO",
            f"Starting main processing loop with {len(self.crawling_queue)} initial URLs.",
            debug_only=True,
        )

        start_time = time.time()

        crawler_executor = None # Initialize to None
        archiver_executor = None # Initialize to None

        try:
            crawler_executor = concurrent.futures.ThreadPoolExecutor(max_workers=self.max_crawler_workers)
            archiver_executor = concurrent.futures.ThreadPoolExecutor(max_workers=self.max_archiver_workers)

            while True:
                # Check for max runtime
                if SETTINGS["max_runtime"] > 0 and (time.time() - start_time) > SETTINGS["max_runtime"]:
                    log_message("INFO", f"Max runtime of {SETTINGS['max_runtime']} seconds reached. Stopping.", debug_only=False)
                    # Immediately shut down executors and cancel pending futures
                    crawler_executor.shutdown(wait=False, cancel_futures=True)
                    archiver_executor.shutdown(wait=False, cancel_futures=True)
                    break

                # Submit new tasks from queues if workers are available
                self._submit_crawl_tasks(crawler_executor)
                self._submit_archive_tasks(archiver_executor)

                # Check if all queues are empty and all active futures are done
                if not self.crawling_queue and not self.queue_for_archiving and \
                   not self.crawling_futures_set and not self.archiving_futures_set:
                    log_message("INFO", "All crawling and archiving tasks completed.", debug_only=False)
                    break # All work is done

                # Collect all active futures to wait on
                all_active_futures = {f_info[0] for f_info in self.crawling_futures_set} | \
                                     {f_info[0] for f_info in self.archiving_futures_set}

                if not all_active_futures:
                    # This can happen if all workers are busy but more tasks are in queue,
                    # or if there's a momentary lull before new tasks are submitted.
                    # Sleep briefly to avoid busy-waiting.
                    time.sleep(0.1)
                    continue

                # Wait for any of the active futures to complete
                done_futures, _ = concurrent.futures.wait(
                    all_active_futures,
                    timeout=1, # Periodically check queues for new tasks
                    return_when=concurrent.futures.FIRST_COMPLETED
                )

                # Process completed futures
                for future in done_futures:
                    # Check if it's a crawling future
                    found_and_processed = False
                    for cf_info in list(self.crawling_futures_set): # Iterate over a copy to allow modification
                        if cf_info[0] == future:
                            self.crawling_futures_set.remove(cf_info)
                            url, current_branch_root = cf_info[1], cf_info[2]
                            try:
                                links_on_page, relationships_on_page = future.result()
                                log_message("DEBUG", f"Crawl task for {url} completed.", debug_only=True)
                                if SETTINGS["enable_visual_tree_generation"]:
                                    self.graph_builder.add_relationships(relationships_on_page)

                                # Enqueue discovered links: Treat every link as a potential new branch
                                for link in links_on_page:
                                    if link not in self.visited_urls:
                                        self.visited_urls.add(link)

                                        # Determine the root domain for this specific link
                                        link_root_domain = get_root_domain(urlparse(link).netloc)

                                        # Add to crawling queue with its own root domain context
                                        self.crawling_queue.append((link, link_root_domain))
                                        self.queue_for_archiving.append(link)
                                        self.total_links_to_archive += 1 # Increment total for newly discovered links
                                        log_message("DEBUG", f"Branching to: {link_root_domain} via {link}", debug_only=True)
                            except ConnectionRefusedForCrawlerError:
                                log_message("INFO", f"Marking branch {current_branch_root} as skipped due to connection refused.", debug_only=False)
                                self.skipped_root_domains.add(current_branch_root)
                            except Exception as e:
                                log_message("ERROR", f"Error while crawling {url}: {e}", debug_only=False)
                            found_and_processed = True
                            break # Found and processed this crawling future

                    if found_and_processed:
                        continue

                    # If not a crawling future, check if it's an archiving future
                    for af_info in list(self.archiving_futures_set):
                        if af_info[0] == future:
                            self.archiving_futures_set.remove(af_info)
                            url = af_info[1]

                            status = "FAILED" # Default status in case of exception
                            result_url = url # Default result_url

                            try:
                                status, result_url = future.result()
                                if status == "ARCHIVED":
                                    self.archived_count += 1
                                elif status == "SKIPPED":
                                    self.skipped_count += 1
                                elif status == "FAILED":
                                    self.failed_count += 1

                                processed = self.archived_count + self.skipped_count + self.failed_count
                                progress_suffix = ""
                                if self.total_links_to_archive > 0:
                                    progress_percent = (processed / self.total_links_to_archive) * 100
                                    progress_suffix = f" ({processed}/{self.total_links_to_archive} {progress_percent:.2f}%)"
                                else:
                                    progress_suffix = f" ({processed} links processed)"

                                log_message("INFO", f"[{status}] {result_url}{progress_suffix}", debug_only=False)

                            except Exception as e:
                                self.failed_count += 1
                                processed = self.archived_count + self.skipped_count + self.failed_count
                                progress_suffix = ""
                                if self.total_links_to_archive > 0:
                                    progress_percent = (processed / self.total_links_to_archive) * 100
                                    progress_suffix = f" ({processed}/{self.total_links_to_archive} {progress_percent:.2f}%)"
                                else:
                                    progress_suffix = f" ({processed} links processed)"

                                log_message("ERROR", f"Error while archiving {url}: {e}{progress_suffix}", debug_only=False)
                            break

        finally:
            # Ensure executors are shut down cleanly even if loop breaks unexpectedly
            if crawler_executor is not None:
                crawler_executor.shutdown(wait=True)
            if archiver_executor is not None:
                archiver_executor.shutdown(wait=True)
            log_message("INFO", "Executors shut down.", debug_only=True)

        # Finalize
        self.graph_builder.build_and_show()

        end_time = time.time()
        duration = end_time - start_time

        # Format duration into days, hours, minutes, and seconds
        days = int(duration // (24 * 3600))
        remaining_seconds = duration % (24 * 3600)
        hours = int(remaining_seconds // 3600)
        remaining_seconds %= 3600
        minutes = int(remaining_seconds // 60)
        final_seconds = remaining_seconds % 60

        duration_str_list = []
        duration_str_list.append(f"{days}d")
        duration_str_list.append(f"{hours}h")
        duration_str_list.append(f"{minutes}m")
        duration_str_list.append(f"{final_seconds:.2f}s")

        duration_str = ' '.join(duration_str_list)

        print("\n========== Archiving Summary ==========")
        total = self.archived_count + self.skipped_count + self.failed_count
        print(f"Total URLs processed: {total}")
        print(f"URLs Archived: {self.archived_count}")
        print(f"URLs Skipped: {self.skipped_count}")
        print(f"URLs Failed: {self.failed_count}")
        print(f"Total Run Time: {duration_str}")
        print("=======================================")

# =========================
# Main Entry Point
# =========================

def main():
    """Main function to orchestrate crawling and archiving."""
    clear_output(wait=True)

    if not SETTINGS["debug_mode"]:
        logging.getLogger('urllib3').setLevel(logging.CRITICAL)
        logging.getLogger('urllib3.connectionpool').setLevel(logging.CRITICAL)

    target_urls_input = input(
        "Enter URLs (comma separated, e.g., https://notawebsite.org/, example.com): "

    ).strip()
    initial_urls_raw = [
        url.strip() for url in target_urls_input.split(",") if url.strip()
    ]

    if not initial_urls_raw:
        log_message("INFO", "No valid URLs entered.", debug_only=False)
        return

    coordinator = CrawlCoordinator()
    coordinator.add_initial_urls(initial_urls_raw)
    coordinator.run()


if __name__ == "__main__":
    main()
