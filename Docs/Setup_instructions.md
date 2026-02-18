# Installation Instructions

WaybackWhen requires Python, pip libraries, and a Chromium‑based browser. Some commands may need `sudo` permissions.

---

## Debian/Ubuntu‑Based
```
sudo apt update
sudo apt install python3 python3-pip python3-venv curl unzip
sudo apt install chromium-browser
```

---

## Arch‑Based
```
sudo pacman -Syu
sudo pacman -S python python-pip chromium
```

---

## RHEL‑Based
```
sudo dnf update
sudo dnf install python3 python3-pip python3-virtualenv curl unzip
sudo dnf install chromium
```

---

## Gentoo‑Based
```
sudo emerge --sync
sudo emerge --ask dev-lang/python dev-python/pip www-client/chromium
```

---

## Nix / NixOS
Temporary shell:
```
nix-shell -p python3 python3Packages.pip chromium
```

Or alternatively, add to configuration.nix:
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

After the dependencies have been installed, it is a good idea to create a Python virtual envoriment:

```
python -m venv venv
```

Once the venv is made install the dependencies as needed:

```
./venv/bin/pip install -r requirements.txt
```

With the necessary dependenices installed, you can now run either wayback-when's CLI interface:

```
./venv/bin/python ./WaybackWhen.py
```

Or run the GUI frontend:

```
./venv/bin/python ./gui.py
```

---
