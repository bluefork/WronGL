import threading
import pystray
from PIL import Image, ImageDraw

def create_image():
    # ساخت یک آیکون ساده آبی در حافظه بدون نیاز به فایل عکس
    image = Image.new('RGB', (64, 64), color=(31, 83, 141))
    d = ImageDraw.Draw(image)
    d.text((10, 20), "W", fill=(255, 255, 255))
    return image

class TrayIcon:
    def __init__(self, on_show, on_quit):
        self.on_show = on_show
        self.on_quit = on_quit
        self.icon = pystray.Icon("WronGL", create_image(), "WronGL Layout Converter", menu=self._menu())
        self.thread = threading.Thread(target=self.icon.run, daemon=True)

    def _menu(self):
        return pystray.Menu(
            pystray.MenuItem("Open WronGL", self.on_show, default=True),
            pystray.MenuItem("Quit", self.on_quit)
        )

    def start(self):
        self.thread.start()

    def stop(self):
        self.icon.stop()