# Wayback When


Wayback When Finds every page: Uses a "headless" browser to crawl a website and discover all its internal links.

Archives smartly: Checks if a page was saved recently to avoid wasting time on redundant backups based on user settings.

# V1 Release

# New Additions and Enhancements in V1

*   **New Imports:**
    *   `random`: For generating random user-agents and sleep times.
    *   `selenium-stealth`: To evade bot detection while using Selenium.
    *   `networkx` and `matplotlib.pyplot`: For generating and visualizing the link tree.

*   **Updated `SETTINGS` Dictionary:**
    *   Renamed `'archiving_retries'` to a more general `'retries'`.
    *   Added `'debug_mode'`: To toggle detailed logging.
    *   Added `'max_archiver_workers'`: To control concurrency for archiving tasks.
    *   Added `'enable_visual_tree_generation'`: To enable/disable the visual link tree output.

*   **New Helper Functions:**
    *   `log_message(level, message, debug_only=False)`: Standardized logging function.
    *   `get_root_domain(netloc)`: To extract the root domain from a URL's network location.
    *   `generate_random_user_agent()`: To create varied user-agents for requests.

*   **Enhanced `get_driver()` Function:**
    *   Now applies `selenium-stealth` with randomized platforms, webgl vendors, and renderers for better bot evasion.

*   **Improved `get_internal_links()` Function:**
    *   Uses `generate_random_user_agent()` for each request.
    *   Includes a crucial check `clean_url.startswith(normalized_base_url_for_comparison)` to ensure discovered links are sub-paths of the base URL, preventing navigation to parent directories.
    *   Utilizes the `get_root_domain()` function for more accurate domain comparison.
    *   Incorporates `log_message()` for structured logging.
    *   **Removed older explicit filtering** for `IRRELEVANT_EXTENSIONS` and `IRRELEVANT_PATH_SEGMENTS` as the sub-path check makes it less necessary.
    *   CAPTCHA detection is more robust with `captcha_prompt_lock` and a custom `CaptchaDetectedError` (though currently handled by automated wait and retry).
    *   Retry delays are now randomized (`time.sleep(random.uniform(5, 15))`).

*   **Modified `should_archive()` Function:**
    *   Uses `generate_random_user_agent()` for Wayback Machine requests.
    *   Uses `log_message()` for clear output.
    *   Refers to the general `'retries'` setting.

*   **Modified `process_link_for_archiving()` Function:**
    *   Uses `log_message()` for consistent output.
    *   Refers to the general `'retries'` setting.
    *   Rate limit warnings use `log_message()`.

*   **Refactored `crawl_website()` Function:**
    *   Now accepts `archiver_executor`, `archiving_futures`, `global_archive_action`, and `link_relationships` to support parallel archiving and visual graph data collection.
    *   Uses `wrapper_get_internal_links()` to manage thread-local WebDriver instances.
    *   Submits links for archiving immediately upon discovery if an `archiver_executor` is provided.
    *   Utilizes `log_message()` for all output.

*   **Major Overhaul of `main()` Function:**
    *   Introduced `all_link_relationships`, `archiving_futures`, and `crawling_futures` to manage concurrent operations and graph data.
    *   Implemented `concurrent.futures.ThreadPoolExecutor` for both crawling and archiving, allowing parallel execution.
    *   Revised archiving action logic to print consolidated messages based on the global choice.
    *   **New Visual Tree Generation Logic:**
        *   Generates a directed graph (`nx.DiGraph()`) using `networkx`.
        *   Adds nodes and edges based on `all_link_relationships`.
        *   Positions the `mother_url` (first initial URL) at the center and makes it visually distinct (larger node, red color).
        *   **Dynamic and Truncated Node Labels:** Labels are now derived from the domain and path, and are smartly truncated to a `max_label_length` (e.g., 25 characters) to prevent overlap, prioritizing the domain and a portion of the path.
        *   The font size of labels is dynamically adjusted (`font_size = max(2, min(6, 400 // (len(G.nodes()) + len(initial_urls))))`) to scale based on the number of nodes and initial URLs, minimizing overlap.
        *   Increases the figure size (`figsize=(16, 12)`) for better readability of the graph.
        *   Saves the plot as 'website_link_tree.png'.


## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.
