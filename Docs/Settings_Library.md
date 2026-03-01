## Settings

| Name | Type | Default | Description |
|-----|------|---------|-------------|
| `allow_external_links` | bool | `False` | Allows the crawler to follow links outside the root domain. |
| `archive_timeout_seconds` | int | `300` | Maximum time (seconds) allowed for a single Wayback Machine save attempt. |
| `archiving_cooldown` | int | `90` | Minimum number of days between Wayback Machine archives for the same URL. |
| `debug_mode` | bool | `False` | Enables verbose debug logging. |
| `default_archiving_action` | str | `"N"` | `'n'` = normal behaviour, `'a'` = archive all, `'s'` = skip all archiving. |
| `enable_visual_tree_generation` | bool | `False` | Enables NetworkX graph generation of link relationships. |
| `max_archiver_workers` | int | `1` | Maximum number of concurrent archiver threads. |
| `max_crawler_workers` | int | `10` | Maximum number of concurrent crawler threads. |
| `min_link_search_delay` | float | `0.0` | Minimum random delay before extracting links from a page. |
| `max_link_search_delay` | float | `5.0` | Maximum random delay before extracting links from a page. |
| `max_crawl_runtime` | int | `0` | Maximum total crawl time in seconds (`0` = unlimited). |
| `max_archive_runtime` | int | `0` | Maximum total archiving time in seconds (`0` = unlimited). |
| `proxies` | list | `[]` | Optional list of proxies used for both Requests and Selenium. |
| `retries` | int | `5` | Number of retry attempts for crawling and archiving operations. |
| `safety_switch` | bool | `False` | Enables slower, safer crawling to reduce detection risk. |
| `urls_per_minute_limit` | int | `15` | Wayback Machine rate‑limit used to compute minimum delay between archive requests. |
