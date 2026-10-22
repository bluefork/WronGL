# Security Policy

## Reporting a Vulnerability

We take the security of WronGL seriously. If you find any security vulnerabilities, please **do not** report them via public GitHub issues. Instead, please report them using the private vulnerability reporting feature on GitHub or by contacting the maintainers directly.

We will acknowledge your report within 48 hours and provide an estimated timeline for a fix. We kindly ask you to keep the vulnerability confidential until we have had a chance to address it.

## Security Considerations & False Positives

### 1. Antivirus False Positives (Windows)
The standalone Windows executable (`WronGL.exe`) is built using `PyInstaller`. PyInstaller bundles the Python interpreter and required libraries into a single file. Due to the self-extracting nature of these executables, Windows Defender and some third-party antivirus software may flag the executable as a false positive (e.g., `Trojan:Script/Wacatac.B!ml`). 
**This is a known issue with PyInstaller.** The source code is fully open and available in this repository for auditing. If you encounter this, you can safely ignore the warning or whitelist the file.

### 2. Clipboard Monitoring
WronGL includes a "Smart Clipboard" feature that monitors the system clipboard to auto-paste copied text for conversion. 
- This data is processed **locally in your RAM**.
- No text, keystrokes, or clipboard data is ever sent to any external server or API.
- If you wish to disable this feature for privacy reasons, you can turn it off in the application settings.

### 3. Global Hotkeys and Keylogging
WronGL uses `pynput` to listen for the configured global hotkey (e.g., `Ctrl+Shift+L`). The application only listens for the specific key combination and does not record or log your general typing activity.
- **Linux (Wayland):** For security reasons, Wayland restricts global hotkey listeners. To use this feature, WronGL must be run under the X11 (Xorg) display server.

### 4. Dependencies
We regularly monitor our dependencies (`pyperclip`, `pynput`, `wordfreq`, `customtkinter`) for known vulnerabilities. We use Dependabot to automatically alert us of any security advisories related to our supply chain.