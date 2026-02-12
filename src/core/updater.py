import os
import sys
import requests
import threading
import subprocess
import time
import src.core.version

REPO_OWNER = "xXxaccessionxXx"
REPO_NAME = "Sanctum-App"
GITHUB_API_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases/latest"

class UpdaterService:
    def __init__(self, root_app):
        self.app = root_app
        self.download_url = None
        self.new_version = None

    def check_for_updates(self):
        """Runs in background to check version."""
        def _check():
            try:
                response = requests.get(GITHUB_API_URL, timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    remote_tag = data.get("tag_name", "").strip().lstrip("v")
                    
                    local_version = src.core.version.VERSION
                    if self.is_newer(remote_tag, local_version):
                        self.new_version = remote_tag
                        # Find the .exe asset
                        for asset in data.get("assets", []):
                            if asset["name"].endswith(".exe"):
                                self.download_url = asset["browser_download_url"]
                                break
                        
                        if self.download_url:
                            # Trigger UI on main thread
                            self.app.after(0, self.show_update_dialog)
            except Exception as e:
                print(f"Update Check Failed: {e}")

        threading.Thread(target=_check, daemon=True).start()

    def is_newer(self, remote, local):
        # Simple semantic version check (assumes x.y.z)
        try:
            r_parts = [int(x) for x in remote.split('.')]
            l_parts = [int(x) for x in local.split('.')]
            return r_parts > l_parts
        except:
            return False

    def show_update_dialog(self):
        from src.ui.update_dialog import UpdateDialog
        UpdateDialog(self.app, self.new_version, self.perform_update)

    def perform_update(self, dialog):
        def _download():
            try:
                # 1. Download new exe to Sanctum.new.exe
                r = requests.get(self.download_url, stream=True)
                total_size = int(r.headers.get('content-length', 0))
                downloaded = 0
                
                new_exe_name = "Sanctum.new.exe"
                with open(new_exe_name, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            self.app.after(0, lambda: dialog.update_progress(downloaded, total_size))
                
                self.app.after(0, lambda: dialog.set_status("Installing..."))
                time.sleep(1) # Let UI update

                current_exe = sys.executable
                exe_dir = os.path.dirname(current_exe)
                exe_name = os.path.basename(current_exe)
                
                # If running from python script (dev mode), don't actually swap
                if not exe_name.lower().endswith(".exe") or "python" in exe_name.lower():
                     self.app.after(0, lambda: dialog.set_status("Dev Mode: Update Downloaded (No Install)"))
                     return

                # 3. Create a robust batch script
                batch_script = f"""
@echo off
setlocal
set "retries=0"

:loop
set /a "retries+=1"
timeout /t 1 /nobreak >nul

rem Try to rename current exe to old
move /y "{exe_name}" "{exe_name}.old" >nul 2>&1
if errorlevel 1 (
    if %retries% LSS 10 (
        goto loop
    ) else (
        echo Failed to update. Please restart manually.
        pause
        exit /b 1
    )
)

rem Move new exe to current name
move /y "{new_exe_name}" "{exe_name}"
if errorlevel 1 (
    echo Failed to move new version. Restoring...
    move /y "{exe_name}.old" "{exe_name}"
    pause
    exit /b 1
)

rem Start the new version
start "" "{exe_name}"

rem Cleanup
del "{exe_name}.old"
del "%~f0" & exit
"""
                with open("update.bat", "w") as f:
                    f.write(batch_script)

                # 4. Quit App and Run Batch
                self.app.after(0, self.app.destroy)
                subprocess.Popen("update.bat", shell=True)
                sys.exit(0)

            except Exception as e:
                self.app.after(0, lambda: dialog.set_status(f"Error: {e}"))
                print(f"Update Failed: {e}")

        threading.Thread(target=_download, daemon=True).start()
