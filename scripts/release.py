import os
import subprocess
import sys
import shutil

VERSION_FILE = "src/core/version.py"
DIST_DIR = "dist"
BUILD_DIR = "build"
EXE_NAME = "Sanctum.exe"

def get_current_version():
    if os.path.exists(VERSION_FILE):
        with open(VERSION_FILE, "r") as f:
            for line in f:
                if line.startswith('VERSION ='):
                    return line.split('=')[1].strip().strip('"')
    return "0.0.0"

def update_version(new_version):
    with open(VERSION_FILE, "w") as f:
        f.write(f'VERSION = "{new_version}"\n')
    print(f"Updated version to {new_version}")

def run_command(command, shell=True):
    print(f"Running: {command}")
    result = subprocess.run(command, shell=shell, text=True, capture_output=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        sys.exit(1)
    print(result.stdout)

def main():
    print("--- Sanctum Release Automation ---")
    
    # 1. Get Version
    current_ver = get_current_version()
    print(f"Current Version: {current_ver}")
    new_ver = input(f"Enter New Version (default {current_ver}): ").strip()
    if not new_ver: new_ver = current_ver
    
    commit_msg = input("Enter Commit Message: ").strip()
    if not commit_msg: commit_msg = f"Release v{new_ver}"

    # 2. Update Version File
    if not os.path.exists("src/core"): os.makedirs("src/core")
    update_version(new_ver)

    # 3. Build .exe
    print("\nBuilding Executable...")
    # --noconsole hides terminal, --onefile bundles everything
    # --add-data assets;assets includes the assets folder
    cmd = f'pyinstaller --noconsole --onefile --name Sanctum --add-data "assets;assets" main.py'
    run_command(cmd)

    # 4. Check Build
    exe_path = os.path.join(DIST_DIR, EXE_NAME)
    if not os.path.exists(exe_path):
        print("Build failed: .exe not found.")
        sys.exit(1)
    
    print(f"\nBuild Successful: {exe_path}")

    # 5. Git Operations
    print("\nPushing to GitHub...")
    run_command("git add .")
    run_command(f'git commit -m "{commit_msg}"')
    run_command(f'git tag v{new_ver}')
    run_command("git push origin main --tags")

    # 6. GitHub Release
    print("\nCreating GitHub Release...")
    # gh release create v1.0.0 dist/Sanctum.exe --title "v1.0.0" --notes "Release notes"
    run_command(f'gh release create v{new_ver} "{exe_path}" --title "v{new_ver}" --notes "{commit_msg}"')

    print("\n--- Release Complete! ---")

if __name__ == "__main__":
    main()
