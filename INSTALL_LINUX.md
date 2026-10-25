# WronGL - Linux Installation & Troubleshooting Guide

This guide provides detailed instructions for installing and running WronGL on Linux distributions (primarily tested on Ubuntu)

## 📋 Prerequisites

WronGL requires **Python 3.10+**. However, because it uses GUI frameworks (`Tkinter`, `CustomTkinter`) and system-level input hooks (`pynput`), you must install several system dependencies first.

Open your terminal and run:

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv python3-tk xclip libayatana-appindicator3-1
```

**Why these packages?**

`python3-tk`: Required for the graphical interface `Tkinter`

`xclip`: Required by `pyperclip` to interact with the Linux clipboard.

libayatana-appindicator3-1: Required for the System Tray icon to appear correctly in GNOME/Ubuntu.
_Note: On older Ubuntu versions, you might need `libappindicator3-1` instead of `libayatana-appindicator3-1`_

## 🚀 Installation Methods

**Method 1: From Pre-built Executable (Recommended for Users)**

Go to the Releases page.
Download the latest `WronGL-Linux.zip` file.
Extract the archive.
Open a terminal in the extracted folder and make the binary executable
```bash
chmod +x WronGL
```
Run the application
```bash
./WronGL
```


**Method 2: From Source (Recommended for Developers)**

If you want to run the latest code or contribute to the project:

```bash
* Clone the repository
git clone https://github.com/bluefork/WronGL.git
cd WronGL

* Create a virtual environment
python3 -m venv .venv

* Activate the virtual environment
source .venv/bin/activate

* Install the package and dependencies
pip install -e ".[dev]"

* Run the application
python -m wrongl
```

## 🛠️ Diagnostics & Troubleshooting

- Issue 1:
Global Hotkey `Ctrl+Shift+L` is not working
Cause: Modern Linux distributions (like Ubuntu 22.04+) use Wayland by default. For security reasons, Wayland prevents background applications from listening to global keyboard events.
Solution: You must switch to the X11 (Xorg) display server.

1. Log out of your current session.

2. On the login screen, click on your username.

3. A gear icon (⚙️) will appear at the bottom right of the screen. Click it.

4. Select _"Ubuntu on Xorg"_

5. Log in with your password. The hotkey will now work perfectly.

- Issue 2:
Persian text is rendering backwards or disconnected
Cause: The default fonts on Linux might not support Arabic/Persian character shaping by default within Tkinter.
Solution: WronGL v1.0.0+ includes `arabic-reshaper` and `python-bidi` to fix this mathematically. Ensure you have the latest dependencies installed `pip install -e ".[dev]"`. If the issue persists, install a standard Persian font:

```bash
sudo apt install fonts-farsiweb fonts-noto-core
```

- Issue 3:
System Tray Icon does not appear
Cause: GNOME requires an extension to show legacy system tray icons.
Solution: Install the "AppIndicator and KStatusNotifierItem Support" extension from the GNOME Extensions website, or install the `gnome-shell-extension-appindicator` package:

```bash
sudo apt install gnome-shell-extension-appindicator
```
_(After installation, restart your session)_

- Issue 4:
Clipboard monitoring is not working
Cause: Missing `xclip`
Solution: Ensure xclip is installed `sudo apt install xclip`. If you are using Wayland, clipboard monitoring might require `wl-clipboard` `sudo apt install wl-clipboard`

## 🗑️ Uninstallation

If you installed from source, simply delete the project folder and deactivate the virtual environment. If you installed system dependencies specifically for this app and no longer need them, you can remove them via `sudo apt remove <package_name>`
