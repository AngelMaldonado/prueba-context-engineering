#!/usr/bin/env python3
"""
CoachX Launcher
================
One-command setup and launch script for CoachX.

Usage:
    Linux/macOS: python3 main.py
    Windows:     python main.py  (or py main.py)

This script will:
1. Check Docker availability
2. Configure your Gemini API key
3. Build and launch CoachX using Docker
4. Show live logs from both services
"""

import os
import sys
import subprocess
import platform
import shutil
import signal
from pathlib import Path
from typing import Optional


# Platform detection
IS_WINDOWS = platform.system() == "Windows"
SUPPORTS_COLOR = (
    sys.stdout.isatty() and
    (os.getenv("TERM") != "dumb") and
    (not IS_WINDOWS or os.getenv("ANSICON") or "TERM" in os.environ)
)


class Colors:
    """Terminal colors for better UX."""
    if SUPPORTS_COLOR:
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKCYAN = '\033[96m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
    else:
        HEADER = OKBLUE = OKCYAN = OKGREEN = WARNING = FAIL = ENDC = BOLD = ''


def print_header(message: str) -> None:
    """Print a styled header message."""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 70}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{message.center(70)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 70}{Colors.ENDC}\n")


def print_success(message: str) -> None:
    """Print a success message."""
    print(f"{Colors.OKGREEN}✓ {message}{Colors.ENDC}")


def print_error(message: str) -> None:
    """Print an error message."""
    print(f"{Colors.FAIL}✗ {message}{Colors.ENDC}")


def print_info(message: str) -> None:
    """Print an info message."""
    print(f"{Colors.OKCYAN}ℹ {message}{Colors.ENDC}")


def print_warning(message: str) -> None:
    """Print a warning message."""
    print(f"{Colors.WARNING}⚠ {message}{Colors.ENDC}")


def check_command(command: str) -> bool:
    """Check if a command is available in the system."""
    return shutil.which(command) is not None


def run_command(command: list[str], check: bool = True, capture: bool = False) -> Optional[subprocess.CompletedProcess]:
    """Run a shell command."""
    try:
        if capture:
            return subprocess.run(command, capture_output=True, text=True, check=check)
        else:
            return subprocess.run(command, check=check)
    except subprocess.CalledProcessError as e:
        if check:
            print_error(f"Command failed: {' '.join(command)}")
            sys.exit(1)
        return None


def check_docker() -> tuple[bool, str]:
    """Check if Docker and Docker Compose are available."""
    if not check_command("docker"):
        return False, "Docker not found"

    # Check if Docker daemon is running
    result = run_command(["docker", "info"], check=False, capture=True)
    if result and result.returncode != 0:
        return False, "Docker daemon not running"

    # Check Docker Compose (v2 style: docker compose)
    result = run_command(["docker", "compose", "version"], check=False, capture=True)
    if result and result.returncode == 0:
        return True, "docker compose"

    # Check old docker-compose
    if check_command("docker-compose"):
        return True, "docker-compose"

    return False, "Docker Compose not found"


def setup_env_file() -> None:
    """Setup or verify .env file with API key."""
    env_file = Path(".env")
    env_example = Path(".env.example")

    # If .env doesn't exist, copy from example
    if not env_file.exists():
        if env_example.exists():
            shutil.copy(env_example, env_file)
            print_info(".env file created from template")
        else:
            print_error(".env.example not found")
            sys.exit(1)

    # Read current .env
    env_content = env_file.read_text()

    # Check if API key is set
    if "GEMINI_API_KEY=your_api_key_here" in env_content or "GEMINI_API_KEY=" not in env_content:
        print_warning("Gemini API key not configured!")
        print_info("Get your free API key at: https://aistudio.google.com/app/apikey")

        api_key = input(f"\n{Colors.BOLD}Enter your Gemini API key: {Colors.ENDC}").strip()

        if not api_key:
            print_error("API key is required")
            sys.exit(1)

        # Update .env file
        env_content = env_content.replace(
            "GEMINI_API_KEY=your_api_key_here",
            f"GEMINI_API_KEY={api_key}"
        )
        env_file.write_text(env_content)
        print_success("API key configured successfully")
    else:
        print_success("API key already configured")


def cleanup_handler(signum, frame):
    """Handle Ctrl+C gracefully."""
    print(f"\n\n{Colors.WARNING}Shutting down CoachX...{Colors.ENDC}")
    run_command(["docker", "compose", "down"], check=False)
    print_success("CoachX stopped successfully")
    sys.exit(0)


def main():
    """Main launcher function."""
    print_header("CoachX - AI Personal Training Assistant")

    # Step 1: Check Docker
    print_info("Checking Docker installation...")
    docker_ok, docker_msg = check_docker()

    if not docker_ok:
        print_error(f"{docker_msg}")
        print("\nDocker is required to run CoachX.")
        print("Install Docker from: https://docs.docker.com/get-docker/")
        print("\nAfter installing Docker:")
        if IS_WINDOWS or platform.system() == "Darwin":
            print("  1. Open Docker Desktop")
            print("  2. Wait for it to start (whale icon in system tray)")
            print("  3. Run this script again")
        else:
            print("  1. Start Docker: sudo systemctl start docker")
            print("  2. Run this script again")
        sys.exit(1)

    print_success(f"Docker available ({docker_msg})")

    # Step 2: Setup environment
    print_info("Configuring environment...")
    setup_env_file()

    # Step 3: Check if images need building
    print_info("Checking Docker images...")
    result = run_command(
        ["docker", "images", "-q", "prueba-context-engineering-backend"],
        capture=True,
        check=False
    )

    needs_build = not result or not result.stdout.strip()

    if needs_build:
        print_warning("Docker images not found. Building now (this takes ~5 minutes)...")
        print_info("Downloading base images and installing dependencies...")
        run_command(["docker", "compose", "build"])
        print_success("Docker images built successfully")
    else:
        print_success("Docker images already built")

    # Step 4: Start services
    print_header("Starting CoachX Services")
    print_info("Starting containers...")

    # Start in detached mode first
    run_command(["docker", "compose", "up", "-d"])

    print_success("Containers started successfully")
    print()
    print(f"{Colors.BOLD}{Colors.OKGREEN}CoachX is running!{Colors.ENDC}")
    print()
    print(f"  {Colors.BOLD}Frontend:{Colors.ENDC} http://localhost:5173")
    print(f"  {Colors.BOLD}Backend API:{Colors.ENDC} http://localhost:8000")
    print(f"  {Colors.BOLD}API Docs:{Colors.ENDC} http://localhost:8000/docs")
    print()
    print(f"{Colors.WARNING}Press Ctrl+C to stop CoachX{Colors.ENDC}")
    print(f"\n{Colors.HEADER}{'=' * 70}{Colors.ENDC}")
    print(f"{Colors.BOLD}Live Logs:{Colors.ENDC}\n")

    # Setup signal handler for Ctrl+C
    signal.signal(signal.SIGINT, cleanup_handler)

    # Follow logs
    try:
        subprocess.run(["docker", "compose", "logs", "-f"])
    except KeyboardInterrupt:
        cleanup_handler(None, None)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        cleanup_handler(None, None)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        sys.exit(1)
