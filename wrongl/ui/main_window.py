from __future__ import annotations

import logging
import threading
import customtkinter as ctk
import pyperclip
from tkinter import messagebox

from wrongl.config import Config, ConfigManager
from wrongl.core.converter import Converter
from wrongl.core.detector import detect, should_auto_convert
from wrongl.core.hotkey import GlobalHotkey

log = logging.getLogger(__name__)

# Set CustomTkinter default theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class MainWindow(ctk.CTk):
    def __init__(self, cfg: Config, cfg_mgr: ConfigManager):
        super().__init__()
        self.cfg = cfg
        self.cfg_mgr = cfg_mgr
        
        self.title("WronGL — Layout Converter")
        self.geometry(self.cfg.window_geometry)
        self.minsize(600, 500)
        
        # Global Hotkey
        self.hotkey = GlobalHotkey(
            hotkey_str=self.cfg.hotkey, 
            convert_digits=self.cfg.convert_digits,
            callback=self._on_hotkey_triggered
        )
        self.hotkey.start()

        self._build_ui()
        
        # Handle window close (hide to tray instead of exiting)
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _build_ui(self):
        # Main Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(3, weight=1)

        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=(15, 5))
        
        lbl_title = ctk.CTkLabel(header, text="WronGL", font=ctk.CTkFont(size=24, weight="bold"))
        lbl_title.pack(side="left")
        
        self.switch_theme = ctk.CTkSwitch(header, text="Dark Mode", command=self._toggle_theme)
        self.switch_theme.pack(side="right")
        if self.cfg.theme == "dark":
            self.switch_theme.select()

        # Input Textbox
        self.input_box = ctk.CTkTextbox(self, font=("Tahoma", 14), wrap="word")
        self.input_box.grid(row=1, column=0, sticky="nsew", padx=20, pady=5)
        self.input_box.bind("<KeyRelease>", lambda e: self._refresh_detection())

        # Buttons Frame
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=10)
        
        ctk.CTkButton(btn_frame, text="EN → FA", width=100, command=lambda: self._run("en2fa")).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="FA → EN", width=100, command=lambda: self._run("fa2en")).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Auto", width=100, fg_color="green", hover_color="darkgreen", command=self._auto_run).pack(side="left", padx=5)
        
        ctk.CTkButton(btn_frame, text="Paste", width=80, fg_color="gray", command=self._paste).pack(side="right", padx=5)
        ctk.CTkButton(btn_frame, text="Clear", width=80, fg_color="gray", command=self._clear).pack(side="right", padx=5)

        # Output Textbox
        self.output_box = ctk.CTkTextbox(self, font=("Tahoma", 14), wrap="word", fg_color=("gray85", "gray20"))
        self.output_box.grid(row=3, column=0, sticky="nsew", padx=20, pady=5)

        # Status Bar & Options
        bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        bottom_frame.grid(row=4, column=0, sticky="ew", padx=20, pady=(5, 15))
        
        self.var_digits = ctk.BooleanVar(value=self.cfg.convert_digits)
        ctk.CTkCheckBox(bottom_frame, text="Digits", variable=self.var_digits, width=80).pack(side="left")
        
        self.status_label = ctk.CTkLabel(bottom_frame, text="Ready", text_color="gray")
        self.status_label.pack(side="left", padx=15)
        
        ctk.CTkButton(bottom_frame, text="Copy", width=80, command=self._copy).pack(side="right")
        
        # Small hint
        hint = ctk.CTkLabel(self, text=f"Global Hotkey: {self.cfg.hotkey.replace('<', '').replace('>', '').title()}", text_color="gray", font=("Tahoma", 11))
        hint.grid(row=5, column=0, pady=(0, 10))

    def _toggle_theme(self):
        mode = "dark" if self.switch_theme.get() else "light"
        ctk.set_appearance_mode(mode)
        self.cfg.theme = mode

    def _make_converter(self) -> Converter:
        return Converter(convert_digits=self.var_digits.get())

    def _refresh_detection(self):
        text = self.input_box.get("1.0", "end-1c")
        if not text.strip():
            self.status_label.configure(text="Ready", text_color="gray")
            return
        r = detect(text)
        arrow = "EN → FA" if r.direction == "en2fa" else "FA → EN"
        self.status_label.configure(text=f"Detected: {arrow} ({r.confidence:.2f})", text_color="#5cb85c")

    def _auto_run(self):
        text = self.input_box.get("1.0", "end-1c")
        if not text: return
        r = detect(text)
        if not should_auto_convert(r):
            if not messagebox.askyesno("Low confidence", f"Confidence: {r.confidence:.2f}\nProceed as {r.direction}?"):
                return
        self._run(r.direction)

    def _run(self, direction: str):
        text = self.input_box.get("1.0", "end-1c")
        if not text: return
        conv = self._make_converter()
        result = conv.en_to_fa(text) if direction == "en2fa" else conv.fa_to_en(text)
        self.output_box.delete("1.0", "end")
        self.output_box.insert("1.0", result)

    def _paste(self):
        try:
            text = pyperclip.paste()
            self.input_box.delete("1.0", "end")
            self.input_box.insert("1.0", text)
            self._refresh_detection()
        except Exception as e:
            messagebox.showerror("Error", f"Clipboard error: {e}")

    def _copy(self):
        text = self.output_box.get("1.0", "end-1c")
        if text:
            pyperclip.copy(text)
            self.status_label.configure(text="Copied to clipboard!", text_color="green")

    def _clear(self):
        self.input_box.delete("1.0", "end")
        self.output_box.delete("1.0", "end")
        self.status_label.configure(text="Ready", text_color="gray")

    def _on_hotkey_triggered(self, direction: str, result: str):
        # Run on main thread safely using after
        self.after(0, lambda: self.status_label.configure(text=f"Hotkey applied: {direction}", text_color="green"))

    def _on_close(self):
        self.cfg.window_geometry = self.geometry()
        self.cfg.convert_digits = self.var_digits.get()
        self.cfg_mgr.save()
        self.hotkey.stop()
        self.destroy()

def run_app(cfg: Config, cfg_mgr: ConfigManager) -> int:
    app = MainWindow(cfg, cfg_mgr)
    app.mainloop()
    return 0