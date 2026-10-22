import customtkinter as ctk
from tkinter import messagebox
from wrongl.config import Config, ConfigManager

class SettingsWindow(ctk.CTkToplevel):
    def __init__(self, parent, cfg: Config, cfg_mgr: ConfigManager, on_save_callback):
        super().__init__(parent)
        self.cfg = cfg
        self.cfg_mgr = cfg_mgr
        self.on_save = on_save_callback

        self.title("WronGL - Settings")
        self.geometry("400x250")
        self.resizable(False, False)
        
        self.transient(parent)
        self.grab_set()

        self._build_ui()

    def _build_ui(self):
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(main_frame, text="Global Hotkey (pynput format):", font=("Tahoma", 14)).pack(anchor="w", pady=(0, 5))
        
        self.hotkey_var = ctk.StringVar(value=self.cfg.hotkey)
        hotkey_entry = ctk.CTkEntry(main_frame, textvariable=self.hotkey_var, font=("Consolas", 14))
        hotkey_entry.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(
            main_frame, 
            text="Example: <ctrl>+<shift>+l or <ctrl>+<alt>+w", 
            text_color="gray", font=("Tahoma", 11)
        ).pack(anchor="w", pady=(0, 15))

        self.smart_clip_var = ctk.BooleanVar(value=getattr(self.cfg, 'smart_clipboard', True))
        ctk.CTkCheckBox(
            main_frame, 
            text="Enable Smart Clipboard", 
            variable=self.smart_clip_var
        ).pack(anchor="w", pady=(0, 20))

        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(fill="x", side="bottom")
        
        ctk.CTkButton(btn_frame, text="Cancel", fg_color="gray", command=self.destroy).pack(side="right", padx=5)
        ctk.CTkButton(btn_frame, text="Save", command=self._save).pack(side="right")

    def _save(self):
        new_hotkey = self.hotkey_var.get().strip()
        if not new_hotkey:
            messagebox.showerror("Error", "Hotkey cannot be empty.")
            return

        self.cfg.hotkey = new_hotkey
        self.cfg.smart_clipboard = self.smart_clip_var.get()
        self.cfg_mgr.save()
        
        self.on_save()
        self.destroy()