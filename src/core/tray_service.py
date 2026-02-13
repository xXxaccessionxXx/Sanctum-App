import threading
import pystray
from PIL import Image, ImageDraw
import sys
import os

class TrayService:
    def __init__(self, app_instance):
        self.app = app_instance
        self.icon = None
        self.thread = None
        self.running = False

    def start(self):
        """Starts the tray icon in a separate thread."""
        if self.running:
            return
            
        self.running = True
        self.thread = threading.Thread(target=self._run_tray, daemon=True)
        self.thread.start()

    def _create_image(self):
        # Generate a simple icon if assets/icon.ico doesn't exist or for the tray
        # For simplicity in this script, let's look for the file or generate a blue circle
        icon_path = os.path.join("assets", "icon.ico")
        if os.path.exists(icon_path):
             return Image.open(icon_path)
        
        # Generator fallback
        width = 64
        height = 64
        color1 = "#1A237E"
        color2 = "#ffffffff"
        image = Image.new('RGB', (width, height), color1)
        dc = ImageDraw.Draw(image)
        dc.ellipse((10, 10, 54, 54), fill=color2)
        return image

    def _run_tray(self):
        image = self._create_image()
        menu = pystray.Menu(
            pystray.MenuItem("Open Grace", self._on_open),
            pystray.MenuItem("Quit", self._on_quit)
        )
        
        self.icon = pystray.Icon("GraceOfGod", image, "Grace of God", menu)
        self.icon.run()

    def _on_open(self, icon, item):
        # Schedule the UI update on the main thread
        self.app.after(0, self.app.show_window)

    def _on_quit(self, icon, item):
        self.running = False
        self.icon.stop()
        # Schedule app termination
        self.app.after(0, self.app.quit_app)

    def stop(self):
        if self.icon:
            self.icon.stop()
