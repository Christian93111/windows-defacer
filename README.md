# Windows Defacer

Windows Defacer is a Python-based system demonstration tool designed to simulate a "Defacement" scenario on Windows. It displays a fullscreen overlay with a countdown and triggers a Blue Screen of Death (BSOD) using native Windows APIs upon completion.

Source: https://github.com/0x7f9/blue-screen

> [!CAUTION]
> **Educational & Testing Purpose Only**: This tool is designed for security research and educational purposes. Executing this script will cause your system to crash (BSOD). Use only in controlled environments like Virtual Machines.

## Features

- **Fullscreen Overlay**: A black, non-closable fullscreen window that stays on top of all applications.
- **Visual Branding**: Supports custom branding with a logo (as seen in `logo.png`).
- **Real-time Countdown**: Informs the user of the impending system crash.
- **Native BSOD Trigger**: Uses `ntdll.dll` (`NtRaiseHardError`) to forcefully crash the Windows kernel.
- **Admin Privilege Support**: Designed to run with administrative rights to access sensitive system calls.

## Build Instructions

To package this tool into a single standalone executable, use the following command with PyInstaller:

```bash
pyinstaller --onefile --noconsole --manifest admin.manifest --add-data "logo.png;." deface.py
```

### Command Breakdown:

- `--onefile`: Bundles everything into a single `.exe`.
- `--noconsole`: Hides the command prompt window during execution.
- `--manifest admin.manifest`: Ensures the executable requests Administrator privileges upon startup.
- `--add-data "logo.png;."`: Embeds the logo into the internal temporary directory of the executable.

## Prerequisites

- **OS**: Windows (Required for `ctypes.windll` and `ntdll` calls).
- **Python**: 3.x
- **Libraries**: `tkinter` (Standard library), `PyInstaller` (For building).

Install the build requirements using:

```bash
pip install -r requirements.txt
```

## Disclaimer

The creator of this tool is not responsible for any damage, data loss, or illegal use. This software is provided "as is" without warranty of any kind. Use it responsibly and at your own risk.
