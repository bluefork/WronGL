from __future__ import annotations
import logging
import threading
import time
import pyperclip
from pynput import keyboard
from wrongl.core.converter import Converter
from wrongl.core.detector import detect, should_auto_convert

log = logging.getLogger(__name__)

class GlobalHotkey:
    def __init__(self, hotkey_str: str = "<cmd>+<alt>+k", convert_digits: bool = False, callback=None):
        self.hotkey_str = hotkey_str
        self.convert_digits = convert_digits
        self.callback = callback
        self.listener = None
        self.running = False
        self.kbd = keyboard.Controller()

    def _process(self):
        # Wait for user to release the modifier keys (Win, Alt, K)
        time.sleep(0.15)
        try:
            old_clip = pyperclip.paste()
            pyperclip.copy('')
            time.sleep(0.05)

            with self.kbd.pressed(keyboard.Key.ctrl):
                self.kbd.press('c')
                self.kbd.release('c')
            time.sleep(0.2)

            text = pyperclip.paste()
            if not text or not text.strip():
                pyperclip.copy(old_clip)
                return

            r = detect(text)
            direction = r.direction
            if not should_auto_convert(r, 0.4):
                direction = "en2fa" if direction == "fa2en" else "fa2en"

            conv = Converter(convert_digits=self.convert_digits)
            result = conv.en_to_fa(text) if direction == "en2fa" else conv.fa_to_en(text)

            pyperclip.copy(result)
            time.sleep(0.1)
            with self.kbd.pressed(keyboard.Key.ctrl):
                self.kbd.press('v')
                self.kbd.release('v')

            log.info(f"Hotkey converted text successfully.")
            if self.callback:
                self.callback(direction, result)
        except Exception as e:
            log.error(f"Hotkey error: {e}")

    def _on_activate(self):
        threading.Thread(target=self._process, daemon=True).start()

    def start(self):
        if self.running: return
        self.running = True
        try:
            self.listener = keyboard.GlobalHotKeys({self.hotkey_str: self._on_activate})
            self.listener.start()
            log.info(f"Hotkey {self.hotkey_str} started.")
        except Exception as e:
            log.error(f"Failed to start hotkey: {e}")

    def stop(self):
        if self.listener:
            self.listener.stop()
            self.running = False

    def restart(self, new_hotkey: str):
        self.stop()
        self.hotkey_str = new_hotkey
        self.start()