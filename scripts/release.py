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

def get_current_branch():
    try:
        result = subprocess.run("git rev-parse --abbrev-ref HEAD", shell=True, text=True, capture_output=True)
        return result.stdout.strip()
    except:
        return "master" # Fallback

def run_command(command, shell=True, ignore_error=False):
    print(f"Running: {command}")
    result = subprocess.run(command, shell=shell, text=True, capture_output=True)
    if result.returncode != 0 and not ignore_error:
        print(f"Error: {result.stderr}")
        # Don't exit immediately on some git errors (like 'nothing to commit')
        if "nothing to commit" in result.stdout or "nothing to commit" in result.stderr:
            return result.stdout
        sys.exit(1)
    return result.stdout

def main():
    print("--- Sanctum Release Automation ---")
    
    # 0. Check Environment
    branch = get_current_branch()
    print(f"Detected Branch: {branch}")
    
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
    # Ignore error if nothing to commit (e.g. only version bump or re-run)
    run_command(f'git commit -m "{commit_msg}"', ignore_error=True)
    
    # Handle tag exists
    run_command(f"git tag -d v{new_ver}", ignore_error=True) # Delete local if exists
    run_command(f"git push origin :refs/tags/v{new_ver}", ignore_error=True) # Delete remote if exists
    
    run_command(f'git tag v{new_ver}')
    
    # Push to correct branch
    run_command(f"git push origin {branch} --tags")

    # 6. GitHub Release
    print("\nCreating GitHub Release...")
    # We use ignore_error=True because if the release already exists, this will fail.
    # We want to then try uploading the asset instead.
    cmd_create = f'gh release create v{new_ver} "{exe_path}" --title "v{new_ver}" --notes "{commit_msg}"'
    output = run_command(cmd_create, ignore_error=True)

    # If creation failed (potentially), try uploading asset directly just in case the release exists
    # If the previous command succeeded, this might be redundant but harmless (or fail harmlessly with clobber)
    if "Release.TagAlreadyExists" in output or "already exists" in output:
        print("Release/Tag already exists. Attempting to upload/overwrite asset...")
        cmd_upload = f'gh release upload v{new_ver} "{exe_path}" --clobber'
        run_command(cmd_upload, ignore_error=True)

    print("\n--- Release Complete! ---")
    print(f"Check your release at: https://github.com/{get_repo_name()}/releases/tag/v{new_ver}")

def get_repo_name():
    try:
        # git remote get-url origin -> https://github.com/User/Repo.git
        res = subprocess.run("git remote get-url origin", shell=True, text=True, capture_output=True)
        url = res.stdout.strip()
        # Parse User/Repo from URL
        if "github.com" in url:
            return url.split("github.com/")[-1].replace(".git", "")
        return "Sanctum-App"
    except:
        return "Sanctum-App"

if __name__ == "__main__":
    main()
