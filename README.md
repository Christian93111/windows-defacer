# Windows Defacer

Windows Defacer is a Python-based system demonstration tool designed to simulate a "Defacement" scenario on Windows. It displays a fullscreen overlay with a countdown and triggers a Blue Screen of Death (BSOD) using native Windows APIs upon completion.

Source Inspiration: [0x7f9/blue-screen](https://github.com/0x7f9/blue-screen)

> [!CAUTION]
> **Educational & Testing Purpose Only**: This tool is designed for security research and educational purposes. Executing this script will cause your system to crash (BSOD). Use only in controlled environments like Virtual Machines.

## Features:

- **Fullscreen Overlay**: A black, non-closable fullscreen window that stays on top of all applications.
- **Visual Branding**: Supports custom branding with a logo (as seen in `logo.png`).
- **Real-time Countdown**: Informs the user of the impending system crash.
- **Native BSOD Trigger**: Uses `ntdll.dll` (`NtRaiseHardError`) to forcefully crash the Windows kernel.
- **Persistence Support**: Includes a built-in feature to add the executable to the Windows Startup folder.
- **Admin Privilege Support**: Designed to run with administrative rights to access sensitive system calls.

## Build Instructions:

To package this tool into a single standalone executable, use the following command with PyInstaller:

```bash
pyinstaller --onefile --noconsole --add-data "logo.png;." --icon ping_pong.ico deface.py
```

### Command Breakdown:

- `--onefile`: Bundles everything into a single `.exe`.
- `--noconsole`: Hides the command prompt window during execution.
- `--add-data "logo.png;."`: Embeds the logo into the internal temporary directory of the executable.
- `--icon ping_pong.ico`: Adds a custom icon to the executable.
- `deface.py`: The main script to be packaged.

## Persistence (Optional)

The script includes an `add_to_startup()` function that provides persistence by copying the binary to the Windows Startup folder.

### How to Enable:

1. Open `deface.py`.
2. Locate the `if __name__ == "__main__":` block at the end of the file.
3. Uncomment the call to `add_to_startup()`.

### Details:

- **Location**: Copies itself to `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup`.
- **Filename**: By default, it saves as `Ping Pong.exe.mal`.
- **Auto-Trigger**: To make it trigger automatically on every reboot, rename the destination file in `deface.py` by removing the `.mal` extension (e.g., `Ping Pong.exe`).

## Prerequisites:

- **OS**: Windows (Required for `ctypes.windll` and `ntdll` calls).
- **Python**: 3.x
- **Libraries**: `tkinter` (Standard library), `PyInstaller` (For building).

Install the build requirements using:

```bash
pip install -r requirements.txt
```

## Disclaimer

The creator of this tool is not responsible for any damage, data loss, or illegal use. This software is provided "as is" without warranty of any kind. Use it responsibly and at your own risk.
