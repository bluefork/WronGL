import customtkinter as ctk
import pyperclip
import arabic_reshaper
from bidi.algorithm import get_display

class HistoryWindow(ctk.CTkToplevel):
    def __init__(self, parent, history: list):
        super().__init__(parent)
        self.history = history
        
        self.title("WronGL - History")
        self.geometry("500x500")
        
        self.transient(parent)
        self.grab_set()
        self.lift()
        self.focus_force()
        self.attributes('-topmost', True)
        self.after(200, lambda: self.attributes('-topmost', False))

        self._build_ui()

    def _build_ui(self):
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)

        ctk.CTkLabel(main_frame, text="Recent Conversions", font=("Arial", 16, "bold")).pack(anchor="w", pady=(0, 10))

        scrollable_frame = ctk.CTkScrollableFrame(main_frame)
        scrollable_frame.pack(fill="both", expand=True)

        if not self.history:
            ctk.CTkLabel(scrollable_frame, text="No history yet.", text_color="gray", font=("Arial", 12)).pack(pady=20)
            return

        for item in reversed(self.history):
            frame = ctk.CTkFrame(scrollable_frame)
            frame.pack(fill="x", pady=5, padx=5)
            
            inp = item.get("input", "").replace("\n", " ")[:25]
            raw_out = item.get("output", "")
            out = raw_out.replace("\n", " ")[:25]
            dir = item.get("direction", "")
            
            try:
                res_out = get_display(arabic_reshaper.reshape(out))
            except Exception:
                res_out = out

            lbl_text = f"[{dir}] {inp} -> {res_out}"
            
            lbl = ctk.CTkLabel(frame, text=lbl_text, anchor="w", font=("Arial", 12))
            lbl.pack(side="left", padx=10, pady=10, fill="x", expand=True)
            
            btn = ctk.CTkButton(frame, text="Copy", width=60, command=lambda t=raw_out: pyperclip.copy(t))
            btn.pack(side="right", padx=10)