# Windows Setup Instructions

## 1. Python Installation
* Download Python 3.9 from the official website (python.org/downloads/windows/).
* Run the installer. Make sure to check 'Add Python to PATH' during installation.
* Verify installation by opening Command Prompt and typing `python --version` and `pip --version`.

## 2. Google Chrome Installation
* Download and install Google Chrome from the official website (google.com/chrome/).

## 3. ChromeDriver Setup (Automatic with `webdriver-manager`)
* For the provided Python script, you *do not* need to manually download or configure ChromeDriver.
* The script uses the `webdriver-manager` library, which automatically downloads and sets up the correct ChromeDriver version compatible with your installed Google Chrome browser when the script is run.
* Ensure Google Chrome is installed as per step 2.

## 4. Python Package Installation
* Open Command Prompt.
* Navigate to your project directory (where your Python script is located).
* Install required packages: `pip install requests beautifulsoup4 waybackpy selenium webdriver-manager selenium-stealth networkx matplotlib`

## 5. Running the Script
* Navigate to your project directory in Command Prompt.
* Run the script: `python your_script_name.py`


# Linux Setup Instructions

## 1. Python Installation
* Python 3 is usually pre-installed. Verify with `python3 --version` and `pip3 --version`.
* If not installed, use your package manager (e.g., `sudo apt install python3 python3-pip` for Debian/Ubuntu, or `sudo dnf install python3 python3-pip` for Fedora/RHEL).

## 2. Google Chrome Installation
* **For Ubuntu/Debian-based Systems:**
  ```bash
  wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
  sudo apt install ./google-chrome-stable_current_amd64.deb -y
  rm google-chrome-stable_current_amd64.deb
  google-chrome --version
  ```
* **For Fedora/RHEL-based Systems:**
  ```bash
  sudo dnf install fedora-workstation-repositories -y # For Fedora
  sudo dnf config-manager --set-enabled google-chrome # For Fedora
  # For RHEL/CentOS, ensure google-chrome.repo exists in /etc/yum.repos.d/ pointing to stable repo
  sudo dnf install google-chrome-stable -y
  google-chrome --version
  ```

## 3. ChromeDriver Setup (Automatic with `webdriver-manager`)
* For the provided Python script, you *do not* need to manually download or configure ChromeDriver.
* The script uses the `webdriver-manager` library, which automatically downloads and sets up the correct ChromeDriver version compatible with your installed Google Chrome browser when the script is run.
* Ensure Google Chrome is installed as per step 2.

## 4. Python Package Installation (Applicable to All Linux Distributions)
* Open Terminal.
* Navigate to your project directory.
* Install required packages: `pip3 install requests beautifulsoup4 waybackpy selenium webdriver-manager selenium-stealth networkx matplotlib`
* Verify installation: `python3 -c "import requests; import bs4; import waybackpy; import selenium; import webdriver_manager; import selenium_stealth; import networkx; import matplotlib"`

## 5. Running the Script
* Navigate to your project directory in Terminal.
* Run the script: `python3 your_script_name.py`
