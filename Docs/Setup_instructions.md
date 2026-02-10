# Installation Instructions

These steps install Python, pip, and a Chromium‑based browser. Commands may need `sudo` permissions.

---

## Debian‑Based
```
sudo apt update
sudo apt install python3 python3-pip python3-venv curl unzip
sudo apt install chromium-browser
pip install requests beautifulsoup4 waybackpy selenium webdriver-manager selenium-stealth networkx matplotlib
```

---

## Ubuntu‑Based
```
sudo apt update
sudo apt install python3 python3-pip python3-venv curl unzip
sudo apt install chromium-browser
pip install requests beautifulsoup4 waybackpy selenium webdriver-manager selenium-stealth networkx matplotlib
```

---

## Arch‑Based
```
sudo pacman -Syu
sudo pacman -S python python-pip chromium
pip install requests beautifulsoup4 waybackpy selenium webdriver-manager selenium-stealth networkx matplotlib
```

---

## RHEL‑Based
```
sudo dnf update
sudo dnf install python3 python3-pip python3-virtualenv curl unzip
sudo dnf install chromium
pip install requests beautifulsoup4 waybackpy selenium webdriver-manager selenium-stealth networkx matplotlib
```

---

## Gentoo‑Based
```
sudo emerge --sync
sudo emerge --ask dev-lang/python dev-python/pip www-client/chromium
pip install requests beautifulsoup4 waybackpy selenium webdriver-manager selenium-stealth networkx matplotlib
```

---

## Nix / NixOS
Temporary shell:
```
nix-shell -p python3 python3Packages.pip chromium
pip install requests beautifulsoup4 waybackpy selenium webdriver-manager selenium-stealth networkx matplotlib
```

Or add to configuration.nix:
```
environment.systemPackages = [
  python3
  python3Packages.pip
  chromium
];
```

---

## Windows
1. Install Python from https://www.python.org/downloads/  
2. Install Google Chrome from https://www.google.com/chrome/  
3. Open PowerShell:
```
py -m pip install --upgrade pip
py -m pip install requests beautifulsoup4 waybackpy selenium webdriver-manager selenium-stealth networkx matplotlib
```

---
