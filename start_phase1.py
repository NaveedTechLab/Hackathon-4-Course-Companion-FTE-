#!/usr/bin/env python3
import subprocess
import sys
import os

def check_and_install_dependencies():
    """Check if required packages are installed, install if not"""
    required_packages = [
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "psycopg2-binary",
        "python-multipart",
        "pydantic",
        "pydantic-settings",
        "python-jose[cryptography]",
        "passlib[bcrypt]",
        "boto3",
        "anthropic",
        "python-slugify",
        "httpx",
        "pytest",
        "pytest-asyncio"
    ]

    print("Checking and installing required packages...")

    # Try to install packages one by one to avoid conflicts
    for package in required_packages:
        try:
            __import__(package.split('[')[0])  # Import package to check if it exists
            print(f"✓ {package} is already installed")
        except ImportError:
            print(f"Installing {package}...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"✓ {package} installed successfully")
            except subprocess.CalledProcessError:
                print(f"✗ Failed to install {package}")

def run_server():
    """Run the Phase 1 server"""
    print("Starting Phase 1 server on port 8000...")

    # Change to phase-1 directory
    os.chdir("phase-1")

    # Run the uvicorn server
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn",
            "main:app",
            "--reload",
            "--port", "8000"
        ])
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Error running server: {e}")

if __name__ == "__main__":
    print("Setting up Course Companion FTE - Phase 1")
    check_and_install_dependencies()
    run_server()