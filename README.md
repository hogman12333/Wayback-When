# Wayback When

Wayback When is a tool that crawls a website and saves its pages to the Internet Archive’s Wayback Machine. It uses a headless browser to load pages the same way a real visitor would, so it can find links that only appear after scripts run.
As it crawls, it keeps track of every internal link it discovers. Before archiving anything, it checks when the page was last saved. If the page was archived recently, it skips it. If it hasn’t been saved in a while, it sends it to the Wayback Machine.
The goal is to make website preservation easier, faster, and less repetitive. Instead of manually checking pages or wasting time on duplicates, Wayback When handles the crawling, the decision‑making, and the archiving for you.

## Scraper
Wayback When uses a Selenium‑based scraper to explore a website and collect every link it can find. Instead of looking only at the raw HTML, it loads each page in a full browser environment, just like a real visitor. This allows it to find every link while remaining invisible to anti-scraping protections.

## Archiver
The archiver decides which pages actually need to be saved. For every link the scraper finds, it checks the Wayback Machine to see when the page was last archived. If the snapshot is recent, it skips it. If it’s old or missing, it sends a new save request. It also handles rate limits and retries so the process can run for long periods without manual supervision.

# V1.1 Release

# New Additions and Enhancements in V1.1

* **New Imports and Reorganization**
  * Reworked import grouping into clear sections: Selenium, visualization, Jupyter helpers.
  * Consolidated `collections` imports to include `deque` alongside `OrderedDict`.

* **Refactored Architecture**
  * Introduced classes: **WebDriverManager**, **Crawler**, and **Archiver** to encapsulate driver lifecycle, crawling, and archiving responsibilities.
  * Replaced many procedural globals and helper wrappers with class methods for improved lifecycle management and testability.

* **New Exceptions**
  * **ConnectionRefusedForCrawlerError**: Raised to abort crawling a branch when the browser reports a connection-refused error.
  * **CaptchaDetectedError** retained and clarified as a dedicated CAPTCHA signal.

* **Updated SETTINGS Dictionary**
  * **Changed defaults** and added new keys:
    * `archiving_cooldown` increased to **90** days.
    * `max_crawler_workers` default set to **10** (0 still supported as unlimited).
    * `retries` default set to **3**.
    * New keys: `min_link_search_delay`, `max_link_search_delay`, `safety_switch`, `proxies`, `max_archiving_queue_size`, `allow_external_links`, `archive_timeout_seconds`.
  * `max_archiver_workers` retained and clarified (0 = unlimited).

* **Requests-first Fast Path**
  * Added `_try_requests_first()` to attempt a lightweight `requests` + `BeautifulSoup` crawl before falling back to Selenium, improving speed and reducing resource usage for simple pages.

* **Improved WebDriver Management**
  * `WebDriverManager.create_driver()` centralizes driver creation, adds proxy support, experimental prefs, `implicitly_wait(10)`, and consistent stealth application.
  * `WebDriverManager.destroy_driver()` ensures safe `driver.quit()` cleanup.

* **Enhanced Crawling Logic**
  * `_get_links_from_page_content()` replaces the older `get_internal_links()` with:
    * Better CAPTCHA detection (more indicators).
    * Connection-refused detection that raises `ConnectionRefusedForCrawlerError`.
    * Respect for `SETTINGS["allow_external_links"]` and `is_irrelevant_link()` filtering.
    * Optional visual relationship collection when `enable_visual_tree_generation` is enabled.
  * `crawl_single_page()` now tries the fast requests path first, then Selenium if needed.

* **New Utility is_irrelevant_link**
  * Centralized logic to filter out assets and irrelevant paths using an expanded `IRRELEVANT_EXTENSIONS` and `IRRELEVANT_PATH_SEGMENTS` list.

* **HTTP Session Factory**
  * `get_requests_session()` returns a configured `requests.Session` with retry strategy and optional proxy selection.

* **Archiving Improvements**
  * `Archiver.should_archive()` and `Archiver.process_link_for_archiving()` replace the old procedural archiving functions.
  * Archiving now runs `wb_obj.save()` inside a dedicated thread and enforces `archive_timeout_seconds` to avoid indefinite blocking.
  * Reactive global cooldown: `rate_limit_active_until_time` is set when Wayback rate limits are detected to coordinate pauses across threads.
  * Improved rate-limit handling and clearer failure messages (`[FAILED - TIMEOUT]`, reactive sleeps).

* **Concurrency and Rate-limiting**
  * Cleaner use of `ThreadPoolExecutor` with explicit worker limits.
  * Implemented DFS instead of BFS
  * Global `archive_lock`, `last_archive_time`, and `rate_limit_active_until_time` coordinate per-thread and global rate limiting.

* **Logging and Typing**
  * `log_message(level, message, debug_only=False)` retained and used consistently across modules.
  * Several functions now include type hints for clarity and maintainability.

* **Visualization Integration**
  * `networkx` and `matplotlib.pyplot` remain available for visual tree generation; relationships are now collected in a structured way by the crawler class for later plotting.

# Notable Changes and Fixes

* **URL Normalization and Filtering**
  * `normalize_url()` rewritten to normalize paths, remove duplicate slashes, strip index pages, lowercase paths, and produce a sorted query string.
  * `is_irrelevant_link()` now aggressively filters many asset types and common CMS/static path segments to reduce noise.

* **Behavioral Changes**
  * Default behavior is more conservative (longer archiving cooldown, debug enabled, limited crawler workers). Update `SETTINGS` to restore previous aggressive defaults if desired.
  * The crawler no longer requires discovered links to be strict sub-paths of the base URL; `allow_external_links` controls whether external domains are permitted.

* **Robustness Fixes**
  * Fixed potential indefinite blocking on `wb_obj.save()` by adding a timeout and threaded execution.
  * Improved handling of WebDriver connection errors to avoid endless retries on unreachable branches.
  * Added proxy support for both `requests` sessions and Selenium driver options.

* **Cleaner Output**
  * Cleaner Terminal Output
# Removed and Deprecated

* **Removed or Replaced**
  * Procedural orchestration functions such as `crawl_website` and `wrapper_get_internal_links` were replaced by class-based equivalents and `crawl_single_page`.
  * The previous global pattern of long-lived thread-local drivers is reduced in favor of explicit create/destroy per crawl where appropriate.

* **Deprecated**
  * Relying on `0` to mean "unlimited" is still supported but discouraged; explicit numeric limits are recommended for production runs.


## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.
