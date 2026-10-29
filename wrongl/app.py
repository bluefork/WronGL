from __future__ import annotations
import logging
import sys
from wrongl.config import ConfigManager
from wrongl.logging_setup import setup_logging

log = logging.getLogger(__name__)

def main() -> int:
    setup_logging()
    log.info("Starting WronGL")
    try:
        cfg_mgr = ConfigManager()
        cfg = cfg_mgr.load()
        
        from wrongl.ui.main_window import MainWindow
        
        app = MainWindow(cfg, cfg_mgr)
        
        from wrongl.ui.tray import TrayIcon
        
        def show_window():
            app.after(0, app.deiconify)
            
        def quit_app():
            app.after(0, app._on_close)
            
        tray = TrayIcon(on_show=show_window, on_quit=quit_app)
        tray.start()

        app.mainloop()
        tray.stop()
        return 0
        
    except Exception:
        log.exception("Fatal error")
        return 1

if __name__ == "__main__":
    sys.exit(main())