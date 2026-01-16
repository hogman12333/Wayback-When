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
pip install requests beautifulsoup4 waybackpy selenium webdriver-manager selenium-stealth networkx matplotlib
```

## 5. Run the Script
```cmd
python your_script_name.py
```

---

# Linux Setup Guide

## 1. Install Python
Check if Python is installed:
```bash
python3 --version
pip3 --version
```

If missing:

**Debian/Ubuntu:**
```bash
sudo apt install python3 python3-pip
```

**Fedora/RHEL:**
```bash
sudo dnf install python3 python3-pip
```

## 2. Install Google Chrome

### Debian/Ubuntu
```bash
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install ./google-chrome-stable_current_amd64.deb -y
rm google-chrome-stable_current_amd64.deb
google-chrome --version
```

### Fedora/RHEL
```bash
sudo dnf install fedora-workstation-repositories -y   # Fedora only
sudo dnf config-manager --set-enabled google-chrome   # Fedora only
# RHEL/CentOS users must ensure google-chrome.repo exists in /etc/yum.repos.d/
sudo dnf install google-chrome-stable -y
google-chrome --version
```

## 3. ChromeDriver (Automatic)
- No manual ChromeDriver installation needed.
- webdriver‑manager handles driver downloads automatically.

## 4. Install Required Python Packages
```bash
pip3 install requests beautifulsoup4 waybackpy selenium webdriver-manager selenium-stealth networkx matplotlib
```

Optional verification:
```bash
python3 -c "import requests, bs4, waybackpy, selenium, webdriver_manager, selenium_stealth, networkx, matplotlib"
```

## 5. Run the Script
```bash
python3 WaybackWhen.py
```
