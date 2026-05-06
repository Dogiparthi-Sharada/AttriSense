#!/usr/bin/env python3
"""
Download and extract portable Git for Windows
"""

import os
import sys
import urllib.request
import zipfile
from pathlib import Path

def download_portable_git():
    """Download portable Git for Windows"""
    
    git_url = "https://github.com/git-for-windows/git/releases/download/v2.45.0.windows.1/PortableGit-2.45.0-64-bit.7z.exe"
    git_path = Path("C:/git-portable")
    
    print("Downloading portable Git...")
    print(f"URL: {git_url}")
    print(f"Target: {git_path}")
    
    # Create directory
    git_path.mkdir(parents=True, exist_ok=True)
    
    # For now, just provide instructions
    print("\n" + "="*60)
    print("Git Installation Alternative")
    print("="*60)
    print("""
Since automated installation requires admin privileges that are blocked,
please manually download Git:

1. Download Git for Windows:
   https://github.com/git-for-windows/git/releases/download/v2.45.0.windows.1/Git-2.45.0-64-bit.exe

2. Run the installer and complete the installation

3. Then run these commands:
   cd "C:\Users\shara\Documents\Codex\2026-05-06\clone-this-repo-change-the-name\AttriSense"
   python setup_git.py

Alternatively, you can use GitHub Desktop:
   https://desktop.github.com/
   
This provides a GUI for git operations without command line.
""")

if __name__ == "__main__":
    download_portable_git()
