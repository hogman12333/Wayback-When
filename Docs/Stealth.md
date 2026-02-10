# Stealth Features

The crawler includes several stealth mechanisms designed to make its behavior look more like real user traffic and less like bot traffic.

## User Agent Randomization
Every request uses a randomly generated User Agent string. The generator mixes:
- Different operating systems (Windows, macOS, Linux, Android, iOS)
- Spoofing different browsers (Chrome, Firefox, Safari)

## Browser Stealth (Selenium)
When Selenium is used, the driver is wrapped with `selenium_stealth`, which adjusts browser properties to resemble a normal user environment. It modifies:
- `navigator.webdriver`
- WebGL vendor and renderer
- Platform and language values

These changes help avoid simple automation checks.

## Proxy Rotation
If proxies are configured, the crawler randomly selects one for both HTTP requests and Selenium sessions. This spreads traffic across multiple IPs and reduces the chance of rate‑limiting.

## Timing Jitter
The crawler introduces random delays when loading pages or retrying failed requests. This avoids the timing patterns that automated systems often produce.

## Requests‑First Approach
Before launching Selenium, the crawler attempts to extract links using a standard HTTP request. This reduces exposure to JavaScript‑based bot detection.

## CAPTCHA Detection
The crawler checks for CAPTCHA's. When detected, it pauses briefly and retries with a new User‑Agent. This prevents repeated hits on challenge pages and reduces escalation.
