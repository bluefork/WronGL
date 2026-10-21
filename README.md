<div align="center">

# ⌨️ WronGL

**A Smart, Bidirectional Keyboard Layout Converter for Persian (Farsi) & English**

[![Build](https://github.com/BlueFork/WronGL/actions/workflows/build.yml/badge.svg)](https://github.com/BlueFork/WronGL/actions/workflows/build.yml)
[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-lightgrey.svg)]()
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

</div>

---

## 📖 Overview

**WronGL** is an advanced, lightweight desktop utility designed to solve a universal typing problem: accidentally typing an entire sentence with the wrong keyboard layout. 

Instead of just mapping characters blindly, WronGL employs **lexical scoring and frequency analysis (`wordfreq`)** to intelligently detect the user's intended language. Whether you typed `sghl` instead of `سلام`, or `اثممخ` instead of `hello`, WronGL fixes it instantly.

## ✨ Key Features

- **🧠 Smart Lexical Detection:** Uses statistical language models to guess the intended language based on word frequencies, rather than simple character ratios.
- **⚡ Global Hotkey:** Select mistyped text in *any* application (browser, IDE, Word) and press `Ctrl + Shift + L` to convert and replace it instantly.
- **🎨 Modern & Responsive UI:** Built with `CustomTkinter`, featuring a sleek dark/light mode interface.
- **📌 System Tray Support:** Runs quietly in the background. Closing the window minimizes it to the system tray.
- **💻 Command-Line Interface (CLI):** A fully-featured CLI (`wrongl-cli`) for pipeline integration and terminal usage.
- **🔤 Arabic Normalization:** Automatically normalizes Arabic lookalike characters (e.g., `ي` to `ی`, `ك` to `ک`) to Persian standards.
- **🔢 Digit Conversion:** Optional conversion between English digits (`0123`) and Persian digits (`۰۱۲۳`).
- **🧪 Robust Testing:** Includes a comprehensive test suite with `pytest` for the core conversion and detection engines.

## 🏗️ Architecture & Tech Stack

- **Language:** Python 3.10+
- **GUI Framework:** [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- **NLP & Detection:** [Wordfreq](https://github.com/rspeer/wordfreq)
- **Global Hotkey Management:** [pynput](https://github.com/moses-palmer/pynput)
- **Clipboard Operations:** [pyperclip](https://github.com/asweigart/pyperclip)
- **CI/CD:** GitHub Actions (Automated cross-platform builds via PyInstaller)

## 🚀 Getting Started

### Prerequisites
- Python 3.10 or higher installed on your system.
- Git (for cloning the repository).

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/BlueFork/WronGL.git
   cd WronGL

Create and activate a virtual environment:
```bash
# Windows (PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1

# Linux/macOS
python -m venv .venv
source .venv/bin/activate

Install the package in editable mode (with dev dependencies):
```bash
pip install -e ".[dev]"

💻 Usage

1. Desktop Application (GUI)

Launch the modern graphical interface:
bash

```python
python -m wrongl

    Type or paste your text into the input box.

    Use the Auto button for smart detection, or manually force the direction.

    Press the Copy button to grab the result.

2. Global Hotkey (The Magic Shortcut)

    Ensure the WronGL app is running (it will sit in your system tray).

    Highlight any mistyped text in any application.

    Press Ctrl + Shift + L (Default).

    The text will be converted, and the correct string will automatically replace your selection.

3. Command-Line Interface (CLI)

    For quick terminal-based conversions:
    ```bash
    # Auto-detect and convert
wrongl-cli "sghl o,f"

# Force a specific direction
wrongl-cli "sghl" -d en2fa

# Read from stdin
echo "اثممخ" | wrongl-cli -d fa2en

⚙️ Configuration

WronGL saves your preferences (theme, digit conversion, window size) automatically.

    Windows: %APPDATA%\WronGL\config.json

    Linux: ~/.config/WronGL/config.json

Logs are stored in the logs/ directory within the application data folder for troubleshooting.

🧪 Testing

We use pytest with pytest-cov to ensure the reliability of the conversion engine.
To run the test suite:
bash

```python
pytest

The GitHub Actions CI will automatically run these tests on Windows and Linux for every pull request.

🤝 Contributing

Contributions make the open-source community an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

    Fork the Project.

    Create your Feature Branch (git checkout -b feature/AmazingFeature).

    Commit your Changes (git commit -m 'Add some AmazingFeature').

    Push to the Branch (git push origin feature/AmazingFeature).

    Open a Pull Request.

## 📄 License

This project is licensed under the **GNU General Public License v3.0 (GPLv3)**. 
See the `LICENSE` file for the full license text.

By using or contributing to this project, you agree to the terms of the GPLv3. Any derivative work or modification must also be open-source and distributed under the same license.