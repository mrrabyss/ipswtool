# 📱 ipswtool

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


A powerful, all-in-one command-line and interactive utility to download **Apple Firmware (IPSW)**, **OTA Updates**, and **iTunes** versions directly from Apple's servers via the [ipsw.me](https://ipsw.me) API.

---

## 📖 Table of Contents
- [Features](#-features)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Usage](#-usage)
  - [Interactive Mode (Menu)](#1-interactive-mode-menu)
  - [CLI Mode (Arguments)](#2-cli-mode)
- [Arguments Reference](#-arguments-reference)
- [Troubleshooting](#-troubleshooting)
- [License](#-license)

---

## ✨ Features
- 🍏 **IPSW Downloads**: Automatically filter by device category (iPhone, iPad, Mac, etc.).
- 📡 **OTA Updates**: Download Over-The-Air updates using device identifiers and build IDs.
- 🎵 **iTunes Archive**: Access legacy iTunes versions for Windows and macOS.
- 🛠 **Dual Mode**: Switch between a user-friendly terminal menu and a fast CLI.

---

## 📋 Prerequisites
- **Python 3.9** or higher.
- **Operating System**: Windows, macOS, or Linux.
- **Internet Connection**: Required to fetch metadata and download firmware.

---

## ⚙️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/mrrabyss/ipswtool.git
cd ipswtool
```
### 2. Create .venv
```bash
python3 -m venv .venv
source .venv/bin/activate
```
### 3. Installing required packages
```bash
pip3 install -r requirements.txt
```
### 4. All done! You can now move to the usage section!

## Usage

### 1. Interactive Mode (Menu)
Simply run the script without any arguments to enter the guided menu system. This is best for browsing available firmware versions.

```bash
python ipsw.py
```
Navigation: Use Arrow Keys to move, Enter to select, and Ctrl+C to exit.


### 2. CLI Mode
Use CLI arguments for faster execution or integration into your own automation scripts.

#### 📱 Download IPSW (Firmware)
Download the latest signed firmware for a device:

```bash
python ipsw.py -t ipsw -d iPhone14,7 --latest
```
#### Download a specific build:

```bash
python ipsw.py -t ipsw -d iPhone14,7 -b 19H218
```

#### 📡 Download OTA (Over-The-Air Update)
Note: OTA downloads require a specific Build ID.

```bash
python ipsw.py -t ota -d iPhone14,7 -b 19H218
```

#### 🎵 Download iTunes
Download the latest version for Windows:

```bash
python ipsw.py -t itunes -p Windows --latest
```

Download a specific legacy version for macOS:

```bash
python ipsw.py -t itunes -p macOS -b 12.8.2
```

#### 📚 Arguments Reference
| Argument | Flag |	Description | Required For |
| -------- | ---- | ------------|------------- |
| Type | -t, --type | ipsw, ota, or itunes	| All |
| Device | -d, --device |	Device Identifier (e.g., iPhone14,7) | IPSW, OTA |
| Platform | -p, --platform |	Windows or macOS | iTunes |
| Build	|-b, --build | Build ID (IPSW/OTA) or Version (iTunes) | Specific downloads |
| Latest | -l, --latest | Auto-selects the newest/signed version | Latest downloads |

# 💡 Important Notes
Signed Status: The tool identifies if an IPSW is still being signed by Apple in the interactive menu. In CLI mode, --latest automatically targets the newest signed version for IPSW.
Identifiers: If you don't know your device identifier (e.g., iPhone13,2), use the Interactive Mode to find it.

# Troubleshooting
If you see anything in the console related to these specific keywords(ERR, traceback, error, exception), you may have to:

- Check your internet connection
- Check your Python envirionment
- Re-launch the script
- Try again later(may be due to the problems on the Apple or ipsw.me side)
- Update the script, see [installation](#️-installation)


# 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

Built with ❤️ by [mrrabyss](https://github.com/mrrabyss)
