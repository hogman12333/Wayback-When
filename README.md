# Wayback When

Wayback When is a tool that crawls a website and saves its pages to the Internet Archive’s Wayback Machine. It uses a headless browser to load pages the same way a real visitor would, so it can find links that only appear after scripts run.
As it crawls, it keeps track of every internal link it discovers. Before archiving anything, it checks when the page was last saved. If the page was archived recently, it skips it. If it hasn’t been saved in a while, it sends it to the Wayback Machine.
The goal is to make website preservation easier, faster, and less repetitive. Instead of manually checking pages or wasting time on duplicates, Wayback When handles the crawling, the decision‑making, and the archiving for you.

## Scraper
Wayback When uses a Selenium‑based scraper to explore a website and collect every link it can find. Instead of looking only at the raw HTML, it loads each page in a full browser environment, just like a real visitor. This allows it to find every link while remaining invisible to anti-scraping protections.

## Archiver
The archiver decides which pages actually need to be saved. For every link the scraper finds, it checks the Wayback Machine to see when the page was last archived. If the snapshot is recent, it skips it. If it’s old or missing, it sends a new save request. It also handles rate limits and retries so the process can run for long periods without manual supervision.

# V1.2 Release

# New Additions and Enhancements in V1.2

 ### Settings
 * Added a ``max_crawl_runtime`` setting
 * Added a ``max_archive_runtime`` setting
 * ``SETTINGS`` have been sorted alphabetically

 ### Added Features
 * Added Runtime to Archiving Summary
 * Added Progress Counter to the Archival Messages

 ### Error Handling
 * Hid ``urllib3`` Error Messages behind ``DEBUG_MODE``.
 * Hid ``WebDriver`` Error Messages behind ``DEBUG_MODE``.
 * Hid "Attempting to continue after automated wait..." behind ``DEBUG_MODE``.
 * Hid "Failed to retrieve ``{base_url}`` after ``{retries}`` attempts." behind ``DEBUG_MODE``.
 * Hid "CAPTCHA DETECTED for ``{base_url}``. Waiting 5-10 seconds..." behind ``DEBUG_MODE``.
 * Archving errors now fall under the retry variable

 ### Bug Fixes
 * Fixed issue where "Finished processing ``{base_url}``. Discovered ``{len(links)}`` links." would be shown as ``DEBUG`` instead of ``INFO``.
 * Fixed issue where URL Normalisation would add ``HTTP://`` to FTP and RSYNC URLs, causing scraping issues.

 ### Miscellaneous
 * Changed message from ``Adding initial URL to queues:`` to ``Starting with URLs:``
 * Depreciated ``max_archiving_queue_size``

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.
