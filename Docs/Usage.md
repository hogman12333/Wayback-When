## What This Program Does

This program:

- Crawls a website
- Finds internal links
- Sends those links to the Wayback Machine
- Archives them


## What You Need

1. Python 3.9 or newer
2. Google Chrome installed
3. Internet connection



## How to Run the Program

1. Open terminal
2. Go to the folder where the script is saved
3. Run:

python Waybackwhen.py

4. When asked, enter website URLs like this:

https://example.com/, example.org

If you do not write "http://" or "https://", the program will add "http://" for you.


## What Happens After You Start

The program will:

1. Visit the page
2. Find links on that page
3. Check if they should be archived
4. Send them to the Wayback Machine
5. Show a summary at the end


## Settings

Inside the script there is a SETTINGS section.

You can change how the program behaves there.

see Settings_Library.md for more info on settings


## CAPTCHA Handling

If a CAPTCHA appears:

The program waits and tries again.

If a website blocks connection completely,
that branch will be skipped and a new user agent is created.

## What Gets Ignored

The program does NOT crawl:

- Images
- Videos
- PDFs
- ZIP files
- System folders
- Static files

This keeps the crawl clean and focused on page that actually contain links.


## End Summary

When finished, you will see:

Total URLs processed  
URLs Archived  
URLs Skipped  
URLs Failed  
Total Run Time  


## What This Tool Is Good For

- Saving websites
- Archiving blogs
- Preserving important websites
- Creating total backups in the Wayback Machine


## What This Tool Is NOT For

- Breaking website rules
- ddos-ing
- Not respecting limits imposed by target websites




