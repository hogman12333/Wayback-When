The crawler has two main runtime limits that help keep it safe and under control. These limits stop the system from running too long or using too many resources.

## Crawl Time Limit
The setting `max_crawl_runtime` controls how long the crawler is allowed to search for new links.  
- If the value is **0**, there is no limit.  
- If you set a number, the crawler will stop adding new pages once that time is reached.

This keeps the crawler from running forever on very large sites.

## Archive Time Limit
The setting `max_archive_runtime` controls how long the archiver is allowed to save pages.  
- If the value is **0**, there is no limit.  
- If you set a number, the archiver stops taking new jobs once the time is up.

This prevents long waits when many links need archiving.

## What Happens When Time Runs Out
When a limit is reached:
- No new tasks are added.
- Current tasks finish if they can.
- The code shuts down cleanly.

## Why Are These Limits Implimented
Runtime limits help avoid:
- Endless loops  
- Wasted CPU time  
- Huge queues using up RAM
