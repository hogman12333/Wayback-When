import asyncio
import aiohttp
import requests
import concurrent
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
import threading
import warnings
import random
import os
import logging
import sys
import json
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium_stealth import stealth

try:
    from IPython.display import clear_output
except ImportError:
    def clear_output(wait=False):
        pass  # No-op when not in Jupyter

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

SETTINGS_FILE = "settings.txt"

def load_settings():
    """Load settings from file if it exists."""
    try:
        if Path(SETTINGS_FILE).exists():
            with open(SETTINGS_FILE, 'r') as f:
                loaded = json.load(f)
                SETTINGS.update(loaded)
    except Exception:
        pass

# Default settings
SETTINGS = {
    "allow_external_links": False,     # Allow crawling external links
    "archive_timeout_seconds": 1200,   # Seconds for archiving a single link
    "archiving_cooldown": 90,          # Days between archiving the same URL
    "debug_mode": False,
    "default_archiving_action": "N",   # 'n' normal, 'a' archive all, 's' skip all
    "max_archiver_workers": 1,         # 0 = unlimited
    "max_crawler_workers": 10,         # 0 = Unlimited
    "min_link_search_delay": 0.0,
    "max_link_search_delay": 5.0,
    "max_crawl_runtime": 0,            # Maximum total crawling time in Seconds (0 = Unlimited)
    "max_archive_runtime": 0,          # Maximum total archiving time in Seconds (0 = Unlimited)
    "proxies": [],                     # e.g. ['http://user:pass@ip:port']
    "retries": 5,                      # Retries for crawling/archiving
    "safety_switch": False,            # Forces the script to slowdown to avoid detection
    "urls_per_minute_limit": 15,       # Wayback rate limit
    "restrict_sideways_crawling": False, # True to restrict crawling to sub-paths of the initial URL
    "restrict_backwards_crawling": True, # True to restrict crawling from going 'up' the path structure
}

load_settings()

# Thread-local storage
_thread_local = threading.local()

# Lock to ensure only one CAPTCHA prompt is active at a time
captcha_prompt_lock = threading.Lock()

# Archive rate limiting
archive_lock = threading.Lock()
last_archive_time = 0.0  
rate_limit_active_until_time = 0.0

MIN_ARCHIVE_DELAY_SECONDS = 60 / SETTINGS["urls_per_minute_limit"]

class CaptchaDetectedError(Exception):
    """Raised when a CAPTCHA is detected on a page."""
    pass

class ConnectionRefusedForCrawlerError(Exception):
    """Raised when a connection is refused for a given URL branch."""
    pass

'''
=========================
User-Agent / Stealth Pools
=========================
'''
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

'''
=========================
Irrelevant Extensions / Paths
=========================
'''
IRRELEVANT_EXTENSIONS = (
    ".3g2", ".3gp", ".7z", ".aac", ".accdb", ".ace", ".aif",
    ".aiff", ".ai", ".apk", ".arj", ".arw", ".asm", ".azw3",
    ".bak", ".bash", ".bin", ".blend", ".bmp", ".bz2", ".cab",
    ".cache", ".c", ".cso", ".conf", ".cpp", ".cr2", ".crt",
    ".cs", ".csv", ".dat", ".dae", ".deb", ".dmg", ".doc",
    ".docx", ".drv", ".dxf", ".dwg", ".eml", ".eps", ".epub",
    ".exe", ".fbx", ".fish", ".flac", ".flv", ".fon", ".gb",
    ".gba", ".gif", ".go", ".gz", ".h", ".har", ".hpp",
    ".ics", ".ico", ".igs", ".img", ".ini", ".iso", ".java",
    ".jpeg", ".jpg", ".js", ".json", ".key", ".kt", ".kts",
    ".lock", ".log", ".lua", ".lz", ".lzma", ".m", ".map",
    ".max", ".mdb", ".mid", ".midi", ".mkv", ".mobi", ".mov",
    ".mp3", ".mp4", ".mpg", ".mpeg", ".msg", ".msi", ".msm",
    ".msp", ".nef", ".nes", ".obj", ".odp", ".ods", ".odt",
    ".ogg", ".old", ".opus", ".orf", ".otf", ".pak", ".pcap",
    ".pcapng", ".pem", ".pdf", ".php", ".pl", ".ply", ".png",
    ".ppt", ".pptx", ".prn", ".ps", ".py", ".qbb", ".qbw",
    ".qfx", ".rar", ".rb", ".rm", ".rmvb", ".rom", ".rpm",
    ".rs", ".rtf", ".r", ".rfa", ".rvt", ".s", ".sav",
    ".sh", ".sit", ".sitx", ".skp", ".so", ".sqlite",
    ".sqlite3", ".stl", ".step", ".stp", ".sub", ".swift",
    ".sys", ".tar", ".temp", ".tif", ".tiff", ".tmp",
    ".toml", ".tsv", ".ttf", ".uue", ".vhd", ".vhdx",
    ".vmdk", ".vtt", ".wav", ".wbmp", ".webm", ".webp",
    ".wma", ".woff", ".woff2", ".wps", ".wmv", ".xcf",
    ".xls", ".xlsx", ".xml", ".xz", ".yaml", ".yml",
    ".z", ".zip", ".zsh",
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

def log_message(level: str, message: str, debug_only: bool = False) -> None:
    """Standardized logging function."""
    if debug_only and not SETTINGS["debug_mode"]:
        return
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}][{level.upper()}] {message}")

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
    """Normalize URL by removing tracking parameters, standardizing path, etc."""
    parsed = urlparse(url)

    scheme = parsed.scheme.lower()
    netloc = parsed.netloc.lower()

    path = parsed.path or "/"
    path = path.replace("//", "/")
    path = path.rstrip("/") if path not in ("/", "") else "/"
    path = path.lower()

    for index_page in ["index.html", "index.htm", "default.html", "default.htm"]:
        if path.endswith(index_page):
            path = path[: -len(index_page)]
            if not path:
                path = "/"

    fragment = ""

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
        netloc = parsed.hostname
        if parsed.port:
            netloc = f"{netloc}:{parsed.port}"
        return urlunparse((parsed.scheme, netloc, "", "", "", ""))
    return proxy

'''
=========================
HTTP Session
=========================
'''
def get_requests_session() -> requests.Session:
    """Return a configured requests.Session with retries and optional proxy."""
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
    
    retry_strategy = Retry(
        total=3,
        backoff_factor=0.5,
        status_forcelist=[403, 404, 429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS"],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    
    session = requests.Session()
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    if SETTINGS["proxies"]:
        proxy = random.choice(SETTINGS["proxies"])
        session.proxies = {"http": proxy, "https": proxy}
        log_message("DEBUG", f"Using proxy for requests session: {redact_proxy(proxy)}", debug_only=True)

    return session

'''
=========================
WebDriver Manager
=========================
'''
class WebDriverManager:
    """Encapsulates Selenium WebDriver creation and teardown."""

    def __init__(self) -> None:
        self._driver_cache = {}

    def create_driver(self) -> webdriver.Chrome:
        """Create and configure a headless Chrome WebDriver with stealth."""
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-plugins")
        options.add_argument("--disable-images")
        options.add_argument("--disable-javascript") if not SETTINGS.get("enable_js_for_crawling", False) else None
        browser_paths = [
            '/usr/bin/chromium',
            '/usr/bin/chromium-browser',
            '/snap/bin/chromium',
            '/usr/bin/google-chrome',
            '/usr/bin/google-chrome-stable',
            '/snap/bin/google-chrome'
        ]
        for path in browser_paths:
            if os.path.exists(path):
                options.binary_location = path
                break
        else:
            try:
                import subprocess
                result = subprocess.run(['which', 'chromium-browser'], 
                                    stdout=subprocess.PIPE, 
                                    stderr=subprocess.DEVNULL,
                                    text=True)
                if result.returncode == 0 and result.stdout.strip():
                    options.binary_location = result.stdout.strip()
                else:
                    result = subprocess.run(['which', 'google-chrome'],
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.DEVNULL,
                                        text=True)
                    if result.returncode == 0 and result.stdout.strip():
                        options.binary_location = result.stdout.strip()
            except Exception:
                pass

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
        options.add_experimental_option("useAutomationExtension", False)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])

        try:
            driver = webdriver.Chrome(options=options)
        except Exception as e:
            log_message("DEBUG", f"System ChromeDriver failed, trying ChromeDriverManager: {str(e)}", debug_only=True)
            try:
                service = ChromeService(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=options)
            except Exception as e2:
                log_message("ERROR", f"Failed to create WebDriver: {str(e2)}", debug_only=False)
                try:
                    driver = webdriver.Chrome(service=None, options=options)
                except Exception as e3:
                    log_message("CRITICAL", f"All WebDriver creation attempts failed: {str(e3)}", debug_only=False)
                    raise

        stealth(
            driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform=random.choice(STEALTH_PLATFORMS),
            webgl_vendor=random.choice(STEALTH_WEBGL_VENDORS),
            renderer=random.choice(STEALTH_RENDERERS),
            fix_hairline=True,
        )

        driver.set_page_load_timeout(60)
        driver.implicitly_wait(5)
        return driver

    def destroy_driver(self, driver: webdriver.Chrome) -> None:
        """Safely quit the WebDriver."""
        try:
            driver.quit()
        except Exception:
            pass

'''
=========================
Crawler
=========================
'''
class Crawler:
    """Responsible for crawling pages using Selenium and extracting internal links."""

    def __init__(self, webdriver_manager: WebDriverManager) -> None:
        self.webdriver_manager = webdriver_manager

    async def _get_links_from_page_content(self, base_url: str, driver: webdriver.Chrome, initial_url_path: str):
        """Core logic to load a page and extract internal links."""
        links = set()

        parsed_base_url = urlparse(base_url)
        base_netloc = parsed_base_url.netloc
        base_root_domain = get_root_domain(base_netloc)

        retries = SETTINGS["retries"]
        attempt = 0

        while attempt < retries:
            try:
                random_user_agent = generate_random_user_agent()
                driver.execute_cdp_cmd(
                    "Network.setUserAgentOverride", {"userAgent": random_user_agent}
                )

                driver.get(base_url)

                await asyncio.sleep(
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
                        await asyncio.sleep(random.uniform(5, 10))
                        log_message(
                            "INFO",
                            "Attempting to continue after automated wait...",
                            debug_only=True,
                        )

                anchor_elements = driver.find_elements(By.TAG_NAME, "a")

                for anchor_element in anchor_elements:
                    href = anchor_element.get_attribute("href")
                    if not href:
                        continue

                    full_url = urljoin(base_url, href)
                    parsed_full_url = urlparse(full_url)

                    link_netloc = parsed_full_url.netloc
                    link_root_domain = get_root_domain(link_netloc)

                    clean_url = normalize_url(full_url)
                    clean_url_path = urlparse(clean_url).path

                    is_valid_domain = (link_root_domain == base_root_domain or SETTINGS["allow_external_links"])
                    is_not_irrelevant_extension = not is_irrelevant_link(clean_url)

                    passes_sideways_restriction = True
                    if SETTINGS["restrict_sideways_crawling"]:
                        effective_initial_path = initial_url_path if initial_url_path.endswith('/') else initial_url_path + '/'
                        passes_sideways_restriction = clean_url_path.startswith(effective_initial_path)

                    passes_backwards_restriction = True
                    if SETTINGS["restrict_backwards_crawling"]:
                        if initial_url_path != '/':
                            if clean_url_path == '/' or initial_url_path.startswith(clean_url_path + '/'):
                                if clean_url_path == '/' and initial_url_path != '/':
                                    passes_backwards_restriction = False
                                elif initial_url_path.startswith(clean_url_path + '/'):
                                    passes_backwards_restriction = False

                    if is_valid_domain and is_not_irrelevant_extension and passes_sideways_restriction and passes_backwards_restriction:
                        links.add(clean_url)

                return links

            except TimeoutException:
                attempt += 1
                await asyncio.sleep(random.uniform(2, 5))
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
                    attempt += 1
                    await asyncio.sleep(random.uniform(2, 5))
            except Exception as e:
                attempt += 1
                await asyncio.sleep(random.uniform(1, 3))

        return set()

    async def _try_requests_first(self, url, initial_url_path: str):
        """Attempt to fetch page with requests before using Selenium."""
        try:
            session = get_requests_session()
            headers = {"User-Agent": generate_random_user_agent()}
            resp = session.get(url, headers=headers, timeout=10)

            if resp.status_code >= 400:
                return None

            soup = BeautifulSoup(resp.text, "html.parser")
            anchors = soup.find_all("a")

            links = set()

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
                clean_url_path = parsed.path

                is_valid_domain = (root == base_root or SETTINGS["allow_external_links"])
                is_not_irrelevant_extension = not is_irrelevant_link(clean)

                passes_sideways_restriction = True
                if SETTINGS["restrict_sideways_crawling"]:
                    effective_initial_path = initial_url_path if initial_url_path.endswith('/') else initial_url_path + '/'
                    passes_sideways_restriction = clean_url_path.startswith(effective_initial_path)

                passes_backwards_restriction = True
                if SETTINGS["restrict_backwards_crawling"]:
                    if initial_url_path != '/':
                        if clean_url_path == '/' or initial_url_path.startswith(clean_url_path + '/'):
                             if clean_url_path == '/' and initial_url_path != '/':
                                passes_backwards_restriction = False
                             elif initial_url_path.startswith(clean_url_path + '/'):
                                passes_backwards_restriction = False

                if is_valid_domain and is_not_irrelevant_extension and passes_sideways_restriction and passes_backwards_restriction:
                    links.add(clean)

            return links

        except Exception:
            return None

    async def crawl_single_page(self, url_to_crawl: str, initial_url_path: str):
        """Try fast requests-based crawl first, then fall back to Selenium."""
        fast_result = await self._try_requests_first(url_to_crawl, initial_url_path)
        if fast_result:
            return fast_result

        driver = self.webdriver_manager.create_driver()
        try:
            return await self._get_links_from_page_content(url_to_crawl, driver, initial_url_path)
        except ConnectionRefusedForCrawlerError as e:
            raise e
        finally:
            self.webdriver_manager.destroy_driver(driver)

'''
=========================
Archiver
=========================
'''
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

    async def should_archive(self, url: str):
        """Determine if URL should be archived based on cooldown and global action."""
        user_agent = generate_random_user_agent()
        _ = get_requests_session()  
        wayback = waybackpy.Url(url, user_agent)

        if self.global_archive_action == "a":
            return True, wayback
        elif self.global_archive_action == "s":
            return False, wayback

        retries = 2
        attempt = 0

        while attempt < retries:
            try:
                newest = wayback.newest()
                last_archived_dt = newest.timestamp.replace(tzinfo=timezone.utc)
                current_utc_dt = datetime.now(timezone.utc)
                time_diff = current_utc_dt - last_archived_dt

                if time_diff < timedelta(days=SETTINGS["archiving_cooldown"]):
                    return False, wayback
                else:
                    return True, wayback

            except waybackpy.exceptions.NoCDXRecordFound:
                return True, wayback
            except Exception as e:
                attempt += 1
                if attempt < retries:
                    await asyncio.sleep(2)
                else:
                    return True, wayback

        return False, wayback

    async def process_link_for_archiving(self, link: str) -> tuple[str, str]:
        """Check if link needs archiving and attempt to save it to Wayback."""
        global last_archive_time, rate_limit_active_until_time

        needs_save, wb_obj = await self.should_archive(link)

        if not needs_save:
            return "SKIPPED", link

        retries = 2
        while retries > 0:
            with archive_lock:
                now = time.time()

                if now < rate_limit_active_until_time:
                    sleep_duration = rate_limit_active_until_time - now
                    time.sleep(sleep_duration)

                now = time.time() 

                elapsed = now - last_archive_time
                if elapsed < MIN_ARCHIVE_DELAY_SECONDS:
                    sleep_duration = MIN_ARCHIVE_DELAY_SECONDS - elapsed
                    time.sleep(sleep_duration)

                last_archive_time = time.time() 

            archive_result = [] 

            def _save_target():
                try:
                    wb_obj.save()
                    archive_result.append(True) 
                except Exception as e:
                    archive_result.append(e) 

            archive_thread = threading.Thread(target=_save_target)
            archive_thread.daemon = True 
            archive_thread.start()
            archive_thread.join(timeout=min(SETTINGS['archive_timeout_seconds'], 300))

            if archive_thread.is_alive():
                retries -= 1
                if retries == 0:
                    return "FAILED", link
                else:
                    await asyncio.sleep(random.uniform(2, 5)) 
                    continue 
            else:
                if archive_result and archive_result[0] is True:
                    return "ARCHIVED", link 
                elif archive_result and isinstance(archive_result[0], Exception):
                    e = archive_result[0]
                    error_message = str(e)
                    rate_limit_keyword = (
                        "Save request refused by the server. Save Page Now limits saving 15 URLs per minutes."
                    )
                    retries -= 1 
                    if rate_limit_keyword in error_message and retries > 0:
                        with archive_lock:
                            rate_limit_active_until_time = time.time() + 60
                        await asyncio.sleep(60)
                    elif retries > 0:
                        await asyncio.sleep(random.uniform(1, 3))
                    else:
                        return "FAILED", link 
                else:
                    retries -= 1
                    await asyncio.sleep(random.uniform(1, 3)) 

        return "FAILED", link 

'''
=========================
   Crawl Coordinator
=========================
'''
class CrawlCoordinator:
    """Coordinates crawling and archiving with concurrency and queues."""

    def __init__(self) -> None:
        self.webdriver_manager = WebDriverManager()
        self.crawler = Crawler(self.webdriver_manager)
        self.archiver = Archiver()

        self.crawling_queue = deque()
        self.queue_for_archiving = deque()
        self.visited_urls = set()
        self.crawling_tasks = set()
        self.archiving_tasks = set() 
        self.skipped_root_domains = set()
        self.initial_url_path = None 
        self.archived_count = 0
        self.skipped_count = 0
        self.failed_count = 0
        self.total_links_to_archive = 0
        self.is_paused = False
        self.should_stop = False
        self.pause_lock = threading.Lock()

        self._resolve_worker_counts()

    def _resolve_worker_counts(self) -> None:
        """Resolve max workers for crawler and archiver based on SETTINGS."""
        max_crawler_workers_setting = SETTINGS["max_crawler_workers"]
        if max_crawler_workers_setting == 0:
            self.max_crawler_workers = 4  
        else:
            self.max_crawler_workers = min(max_crawler_workers_setting, 4)

        max_archiver_workers_setting = SETTINGS["max_archiver_workers"]
        if max_archiver_workers_setting == 0:
            self.max_archiver_workers = 2 
        else:
            self.max_archiver_workers = min(max_archiver_workers_setting, 2)

        if SETTINGS.get("safety_switch", False):
            self.max_crawler_workers = 1
            SETTINGS["min_link_search_delay"] = 12.0
            SETTINGS["max_link_search_delay"] = 15.0

    def add_initial_urls(self, urls):
        """Normalize and enqueue initial URLs for crawling and archiving."""
        for url in urls:
            parsed_url = urlparse(url)
            if not parsed_url.scheme:
                url = "http://" + url

            parsed_url_with_scheme = urlparse(url)
            if not parsed_url_with_scheme.scheme or not parsed_url_with_scheme.netloc:
                continue

            normalized_url = normalize_url(url)
            root_domain = get_root_domain(urlparse(normalized_url).netloc)

            if self.initial_url_path is None:
                self.initial_url_path = urlparse(normalized_url).path
                if self.initial_url_path != '/' and not self.initial_url_path.endswith('/'):
                    self.initial_url_path += '/'

            if normalized_url not in self.visited_urls:
                self.visited_urls.add(normalized_url)
                self.crawling_queue.append((normalized_url, root_domain, self.initial_url_path))
                self.queue_for_archiving.append(normalized_url)
        self.total_links_to_archive = len(self.queue_for_archiving)

    def add_url_live(self, url: str):
        """Add a new URL while the crawler is running."""
        parsed_url = urlparse(url)
        if not parsed_url.scheme:
            url = "http://" + url

        parsed_url_with_scheme = urlparse(url)
        if not parsed_url_with_scheme.scheme or not parsed_url_with_scheme.netloc:
            return

        normalized_url = normalize_url(url)
        root_domain = get_root_domain(parsed_url_with_scheme.netloc)

        if self.initial_url_path is None:
            self.initial_url_path = parsed_url_with_scheme.path
            if self.initial_url_path != '/' and not self.initial_url_path.endswith('/'):
                self.initial_url_path += '/'

        if normalized_url not in self.visited_urls:
            self.visited_urls.add(normalized_url)
            self.crawling_queue.append((normalized_url, root_domain, self.initial_url_path))
            self.queue_for_archiving.append(normalized_url)
            self.total_links_to_archive += 1

    def pause(self):
        """Pause crawling and archiving operations."""
        with self.pause_lock:
            self.is_paused = True

    def resume(self):
        """Resume crawling and archiving operations."""
        with self.pause_lock:
            self.is_paused = False

    def stop(self):
        """Stop all crawling and archiving operations."""
        self.should_stop = True

    def reset_state(self):
        """Reset the coordinator's state while keeping settings and initial URLs"""
        self.crawling_queue = deque()
        self.queue_for_archiving = deque()
        self.visited_urls = set()
        self.crawling_tasks = set()
        self.archiving_tasks = set()
        self.skipped_root_domains = set()
        self.archived_count = 0
        self.skipped_count = 0
        self.failed_count = 0
        self.total_links_to_archive = 0
        self.is_paused = False
        self.should_stop = False

    def is_completed(self):
        """Check if the coordinator has finished processing"""
        return (not self.crawling_queue and 
                not self.queue_for_archiving and 
                not self.crawling_tasks and 
                not self.archiving_tasks and
                not self.is_paused and
                not self.should_stop)

    async def _submit_crawl_tasks(self):
        """Submit crawl tasks while respecting queue and skipped domains and worker limits."""
        while (
            self.crawling_queue
            and len(self.crawling_tasks) < self.max_crawler_workers
            and not self.is_paused
            and not self.should_stop
        ):
            url, root_domain, initial_url_path = self.crawling_queue.popleft()
            if root_domain in self.skipped_root_domains:
                continue
            task = asyncio.create_task(self.crawler.crawl_single_page(url, initial_url_path))
            task.url = url
            task.root_domain = root_domain
            task.initial_url_path = initial_url_path
            self.crawling_tasks.add(task)

    async def _submit_archive_tasks(self):
        """Submit archiving tasks for URLs in the archiving queue, respecting worker limits."""
        while (
            self.queue_for_archiving
            and len(self.archiving_tasks) < self.max_archiver_workers
            and not self.is_paused
            and not self.should_stop
        ):
            url = self.queue_for_archiving.popleft()
            task = asyncio.create_task(self.archiver.process_link_for_archiving(url))
            task.url = url
            self.archiving_tasks.add(task)

    async def run(self):
        """Main coordination loop: crawl + archive until queues are empty or stopped."""
        overall_start_time = time.time()
        crawl_process_start_time = time.time()
        archive_process_start_time = time.time()
        crawling_enabled = True
        archiving_enabled = True

        try:
            while not self.should_stop:
                while self.is_paused and not self.should_stop:
                    await asyncio.sleep(0.2)
                    continue
                current_time = time.time()
                if crawling_enabled and SETTINGS["max_crawl_runtime"] > 0 and (current_time - crawl_process_start_time) > SETTINGS["max_crawl_runtime"]:
                    crawling_enabled = False
                    self.crawling_queue.clear()

                if archiving_enabled and SETTINGS["max_archive_runtime"] > 0 and (current_time - archive_process_start_time) > SETTINGS["max_archive_runtime"]:
                    archiving_enabled = False
                    self.queue_for_archiving.clear()

                if crawling_enabled:
                    await self._submit_crawl_tasks()
                if archiving_enabled:
                    await self._submit_archive_tasks()

                all_crawling_done = (not crawling_enabled) or (not self.crawling_queue and not self.crawling_tasks)
                all_archiving_done = (not archiving_enabled) or (not self.queue_for_archiving and not self.archiving_tasks)

                if all_crawling_done and all_archiving_done:
                    break

                all_active_tasks = self.crawling_tasks | self.archiving_tasks

                if not all_active_tasks:
                    await asyncio.sleep(0.1)
                    continue
                    
                done_tasks, _ = await asyncio.wait(
                    all_active_tasks,
                    timeout=0.5,
                    return_when=asyncio.FIRST_COMPLETED
                )
                
                for task in done_tasks:
                    if task in self.crawling_tasks:
                        self.crawling_tasks.discard(task)
                        if task.cancelled():
                            continue

                        try:
                            links_on_page = await task

                            if crawling_enabled and not self.is_paused:
                                for link in links_on_page:
                                    if link not in self.visited_urls:
                                        self.visited_urls.add(link)
                                        link_root_domain = get_root_domain(urlparse(link).netloc)
                                        self.crawling_queue.append((link, link_root_domain, task.initial_url_path))
                                        self.queue_for_archiving.append(link)
                                        self.total_links_to_archive += 1
                        except ConnectionRefusedForCrawlerError:
                            self.skipped_root_domains.add(task.root_domain)
                        except asyncio.CancelledError:
                            pass
                        except Exception:
                            pass
                            
                    elif task in self.archiving_tasks:
                        self.archiving_tasks.discard(task)
                        if task.cancelled():
                            continue

                        try:
                            status, result_url = await task
                            if status == "ARCHIVED":
                                self.archived_count += 1
                            elif status == "SKIPPED":
                                self.skipped_count += 1
                            elif status == "FAILED":
                                self.failed_count += 1

                        except asyncio.CancelledError:
                            pass
                        except Exception:
                            self.failed_count += 1

        except KeyboardInterrupt:
            self.should_stop = True
        finally:
            for task in self.crawling_tasks | self.archiving_tasks:
                task.cancel()

        end_time = time.time()
        duration = end_time - overall_start_time

        days = int(duration // (24 * 3600))
        remaining_seconds = duration % (24 * 3600)
        hours = int(remaining_seconds // 3600)
        remaining_seconds %= 3600
        minutes = int(remaining_seconds // 60)
        final_seconds = remaining_seconds % 60

        duration_str_list = []
        if days > 0:
            duration_str_list.append(f"{days}d")
        if hours > 0:
            duration_str_list.append(f"{hours}h")
        if minutes > 0:
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

async def async_main():
    clear_output(wait=True)

    if not SETTINGS["debug_mode"]:
        logging.getLogger('urllib3').setLevel(logging.CRITICAL)
        logging.getLogger('urllib3.connectionpool').setLevel(logging.CRITICAL)
    if '--gui' in sys.argv:
        from gui import main as gui_main
        gui_main()
        return

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
    await coordinator.run()

def main():
    asyncio.run(async_main())

if __name__ == "__main__":
    main()