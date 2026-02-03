# These are WIP, Please Execute with caution

# Windows Setup Guide

## 1. Install Python
- Download Python 3.9 from: https://www.python.org/downloads/windows/
- Run the installer and enable **“Add Python to PATH”**.
- Verify installation:
  ```cmd
  python --version
  pip --version
  ```

## 2. Install Google Chrome
- Download from: https://www.google.com/chrome/

## 3. ChromeDriver (Automatic)
- No manual setup required.
- The script uses **webdriver‑manager**, which automatically downloads the correct ChromeDriver version.

## 4. Install Required Python Packages
Navigate to your project directory and run:
```cmd
pip install requests beautifulsoup4 waybackpy selenium webdriver-manager selenium-stealth networkx matplotlib ipython
```
## 5. Run the Script
```cmd
python WaybackWhen.py
```
Debian/Ubuntu
---
```cmd 
sudo apt update && sudo apt install -y python3 python3-pip wget unzip gnupg ca-certificates fonts-liberation libnss3 libxss1 libasound2 libatk1.0-0 libatk-bridge2.0-0 libgtk-3-0 libx11-xcb1 libxcomposite1 libxrandr2 libgbm1 && wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add - && sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list' && sudo apt update && sudo apt install -y google-chrome-stable && sudo pip3 install --upgrade pip && sudo pip3 install selenium webdriver-manager waybackpy beautifulsoup4 requests networkx matplotlib selenium-stealth 
```
```cmd
source venv/bin/activate
```
```cmd
Python3 WaybackWhen.py
```
Arch
---
``` cmd
sudo pacman -Syu --noconfirm && sudo pacman -S --noconfirm --needed python python-pip chromium chromedriver wget unzip ca-certificates libnss libxss alsa-lib atk atk-bridge gtk3 libx11 libxcomposite libxrandr libgbm liberation-fonts && sudo pip3 install --upgrade pip && sudo pip3 install selenium webdriver-manager waybackpy beautifulsoup4 requests networkx matplotlib selenium-stealth
```
