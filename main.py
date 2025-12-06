#!/usr/bin/env python3
"""
CoachX Launcher
================
One-command setup and launch script for evaluators.

Usage:
    Linux/macOS: python3 main.py
    Windows:     python main.py  (or py main.py)

This script will:
1. Check system requirements
2. Install backend dependencies
3. Install frontend dependencies
4. Configure environment variables
5. Launch both servers
"""

import os
import sys
import subprocess
import platform
import shutil
import time
import threading
from pathlib import Path
from typing import Optional


# Detect platform-specific commands
IS_WINDOWS = platform.system() == "Windows"
IS_MACOS = platform.system() == "Darwin"
IS_LINUX = platform.system() == "Linux"
NPM_CMD = "npm.cmd" if IS_WINDOWS else "npm"

# Detect if terminal supports colors
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
        HEADER = ''
        OKBLUE = ''
        OKCYAN = ''
        OKGREEN = ''
        WARNING = ''
        FAIL = ''
        ENDC = ''
        BOLD = ''


def print_header(message: str) -> None:
    """Print a styled header message."""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{message.center(60)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 60}{Colors.ENDC}\n")


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


def run_command(
    command: list[str],
    cwd: Optional[Path] = None,
    capture_output: bool = False,
    timeout: int = 600,  # 10 minutes default timeout
    allow_failure: bool = False
) -> subprocess.CompletedProcess:
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            check=True,
            capture_output=capture_output,
            text=True,
            timeout=timeout
        )
        return result
    except subprocess.TimeoutExpired:
        print_error(f"Command timed out after {timeout}s: {' '.join(command)}")
        if not allow_failure:
            sys.exit(1)
        raise
    except subprocess.CalledProcessError as e:
        print_error(f"Command failed: {' '.join(command)}")
        if capture_output and e.stderr:
            print_error(f"Error: {e.stderr}")
        if not allow_failure:
            sys.exit(1)
        raise


def check_python_version() -> None:
    """Verify Python version is 3.11+."""
    print_info("Checking Python version...")
    version = sys.version_info

    if version.major < 3 or (version.major == 3 and version.minor < 11):
        print_error(f"Python 3.11+ required. Found: {version.major}.{version.minor}")
        sys.exit(1)

    # Warn about Python 3.13+ (dependency compatibility issues)
    if version.major == 3 and version.minor >= 13:
        print_warning(f"Python {version.major}.{version.minor} detected")
        if IS_WINDOWS:
            print_warning("Some dependencies may require compilation tools (Rust, MSVC)")
            print_info("If installation fails, install Python 3.11 or 3.12")
        else:
            print_warning("Some dependencies may not have pre-built wheels yet")
            print_info("If installation fails, consider Python 3.11 or 3.12")
        print_info("Recommended: Python 3.11 or 3.12 for maximum compatibility\n")

    print_success(f"Python {version.major}.{version.minor}.{version.micro}")


def check_node() -> None:
    """Verify Node.js is installed."""
    print_info("Checking Node.js...")
    if not check_command("node"):
        print_error("Node.js not found. Please install Node.js 18+")
        print_info("Download: https://nodejs.org/")
        sys.exit(1)
    
    result = run_command(["node", "--version"], capture_output=True)
    version = result.stdout.strip()
    print_success(f"Node.js {version}")


def check_npm() -> None:
    """Verify npm is installed."""
    print_info("Checking npm...")
    if not check_command("npm"):
        print_error("npm not found. Please install npm")
        sys.exit(1)

    result = run_command([NPM_CMD, "--version"], capture_output=True)
    version = result.stdout.strip()
    print_success(f"npm {version}")


def get_gemini_api_key() -> str:
    """Prompt user for Gemini API key."""
    print_info("Gemini API Key required for AI features")
    print_info("Get your free key at: https://aistudio.google.com/api-keys")
    
    api_key = input(f"\n{Colors.OKCYAN}Enter your Gemini API Key: {Colors.ENDC}").strip()
    
    if not api_key:
        print_error("API Key is required!")
        sys.exit(1)
    
    return api_key


def setup_backend_env(api_key: str) -> None:
    """Create backend .env file."""
    print_info("Configuring backend environment...")
    
    backend_dir = Path("backend")
    env_file = backend_dir / ".env"
    
    env_content = f"""# CoachX Backend Configuration
GEMINI_API_KEY={api_key}
DATABASE_URL=sqlite:///./coachx.db
CHROMA_PERSIST_DIRECTORY=./chroma_db
ALLOWED_ORIGINS=http://localhost:5173
"""
    
    env_file.write_text(env_content)
    print_success("Backend .env configured")


def setup_frontend_env() -> None:
    """Create frontend .env.local file."""
    print_info("Configuring frontend environment...")

    frontend_dir = Path("frontend")
    env_file = frontend_dir / ".env.local"

    env_content = """# CoachX Frontend Configuration
VITE_API_URL=http://localhost:8000
"""

    env_file.write_text(env_content)
    print_success("Frontend .env.local configured")


def setup_backend() -> Path:
    """Install backend dependencies."""
    print_header("Setting up Backend")

    # Use absolute paths from the start
    backend_dir = Path("backend").resolve()
    if not backend_dir.exists():
        print_error(f"Backend directory not found: {backend_dir}")
        sys.exit(1)

    # Check if we're already in a virtual environment
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )

    if in_venv:
        print_info("Using current virtual environment")
        pip_path = shutil.which("pip") or shutil.which("pip3")
        python_path = Path(sys.executable)
    else:
        # Create virtual environment
        venv_dir = backend_dir / "venv"

        # Determine pip path based on OS
        # IMPORTANT: Don't resolve() the final path, it will follow symlinks to system Python
        if platform.system() == "Windows":
            pip_path = venv_dir / "Scripts" / "pip.exe"
            python_path = venv_dir / "Scripts" / "python.exe"
        else:
            pip_path = venv_dir / "bin" / "pip"
            python_path = venv_dir / "bin" / "python"

        # Check if venv exists and is valid
        if venv_dir.exists():
            if not pip_path.exists():
                print_warning("Virtual environment is corrupted, recreating...")
                shutil.rmtree(venv_dir)
                print_info("Creating virtual environment...")
                run_command([sys.executable, "-m", "venv", "venv"], cwd=backend_dir)
                print_success("Virtual environment created")
            else:
                print_info("Virtual environment already exists")
        else:
            print_info("Creating virtual environment...")
            run_command([sys.executable, "-m", "venv", "venv"], cwd=backend_dir)
            print_success("Virtual environment created")

    # Verify pip exists
    if isinstance(pip_path, Path) and not pip_path.exists():
        print_error(f"pip not found at: {pip_path}")
        print_error("Virtual environment may be corrupted. Try deleting backend/venv and run again.")
        sys.exit(1)

    # Install dependencies
    print_info("Installing Python dependencies (this may take 2-3 minutes)...")

    # Paths are already absolute, just convert to string if needed
    pip_cmd = str(pip_path) if isinstance(pip_path, Path) else pip_path

    # Step 1: Upgrade pip, setuptools, and wheel for better compatibility
    print_info("Upgrading pip and build tools...")
    try:
        run_command(
            [pip_cmd, "install", "--upgrade", "pip", "setuptools", "wheel"],
            cwd=backend_dir,
            allow_failure=True
        )
        print_success("Build tools upgraded")
    except Exception as e:
        print_warning(f"Failed to upgrade pip: {e}")
        print_warning("Continuing with existing pip version...")

    # Step 2: Install dependencies with additional flags for reliability
    print_info("Installing project dependencies...")
    install_cmd = [
        pip_cmd,
        "install",
        "-r", "requirements.txt",
        "--no-cache-dir",  # Avoid cache issues across platforms
        "--only-binary", ":all:",  # Force use of pre-built wheels only (no compilation)
    ]

    try:
        run_command(install_cmd, cwd=backend_dir)
        print_success("Backend dependencies installed")
    except Exception as e:
        print_warning("Installation with --only-binary failed, retrying without it...")
        print_info("This may require compilers on your system (MSVC on Windows)")
        # Retry without --only-binary flag
        retry_cmd = [
            pip_cmd,
            "install",
            "-r", "requirements.txt",
            "--no-cache-dir",
        ]
        run_command(retry_cmd, cwd=backend_dir)
        print_success("Backend dependencies installed (with compilation)")

    return python_path


def setup_frontend() -> None:
    """Install frontend dependencies."""
    print_header("Setting up Frontend")

    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print_error(f"Frontend directory not found: {frontend_dir}")
        sys.exit(1)

    # Check if node_modules exists
    node_modules = frontend_dir / "node_modules"
    if not node_modules.exists():
        print_info("Installing Node.js dependencies...")
        run_command([NPM_CMD, "install"], cwd=frontend_dir)
        print_success("Frontend dependencies installed")
    else:
        print_info("Node modules already installed")


def stream_output(process, prefix, color):
    """Stream process output to console with color."""
    for line in iter(process.stdout.readline, ''):
        if line:
            print(f"{color}{prefix}: {line.rstrip()}{Colors.ENDC}")


def start_servers(python_path: Path) -> None:
    """Start both backend and frontend servers."""
    print_header("Starting CoachX")

    backend_dir = Path("backend")
    frontend_dir = Path("frontend")

    print_info("Starting backend server...")
    print_info("Starting frontend server...")
    print_warning("This may take 10-15 seconds for initial setup...\n")

    # Start backend
    backend_cmd = [
        str(python_path),
        "-m",
        "uvicorn",
        "app.main:app",
        "--reload",
        "--port",
        "8000"
    ]

    # Start frontend
    frontend_cmd = [NPM_CMD, "run", "dev"]

    try:
        # Start backend process
        backend_process = subprocess.Popen(
            backend_cmd,
            cwd=backend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,  # Text mode instead of binary
            bufsize=1  # Line buffering works in text mode
        )

        # Start frontend process
        frontend_process = subprocess.Popen(
            frontend_cmd,
            cwd=frontend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,  # Text mode instead of binary
            bufsize=1  # Line buffering works in text mode
        )

        # Give servers time to start
        print_info("Waiting for servers to initialize...")
        time.sleep(5)

        # Check if processes are still running
        if backend_process.poll() is not None:
            print_error("Backend failed to start!")
            # Show error output
            stdout, stderr = backend_process.communicate()
            if stderr:
                print_error(f"Backend error:\n{stderr}")
            if stdout:
                print_info(f"Backend output:\n{stdout}")
            sys.exit(1)

        if frontend_process.poll() is not None:
            print_error("Frontend failed to start!")
            # Show error output
            stdout, stderr = frontend_process.communicate()
            if stderr:
                print_error(f"Frontend error:\n{stderr}")
            if stdout:
                print_info(f"Frontend output:\n{stdout}")
            sys.exit(1)

        print_success("\n✅ Backend running on http://localhost:8000")
        print_success("✅ Frontend running on http://localhost:5173")
        print_success("✅ CoachX is ready! 🥊\n")

        print_info(f"{Colors.BOLD}🌐 Open your browser at: http://localhost:5173{Colors.ENDC}")
        print_info(f"{Colors.BOLD}📚 API docs available at: http://localhost:8000/docs{Colors.ENDC}\n")

        print_warning("Press Ctrl+C to stop both servers")
        print_info("Server logs will appear below...\n")
        print(f"{Colors.BOLD}{'─' * 60}{Colors.ENDC}\n")

        # Start output streaming threads
        backend_thread = threading.Thread(
            target=stream_output,
            args=(backend_process, "BACKEND", Colors.OKBLUE),
            daemon=True
        )
        frontend_thread = threading.Thread(
            target=stream_output,
            args=(frontend_process, "FRONTEND", Colors.OKCYAN),
            daemon=True
        )

        backend_thread.start()
        frontend_thread.start()

        # Wait for processes
        while True:
            if backend_process.poll() is not None:
                print_error("Backend process stopped unexpectedly!")
                break
            if frontend_process.poll() is not None:
                print_error("Frontend process stopped unexpectedly!")
                break
            time.sleep(1)

    except KeyboardInterrupt:
        print_info("\n\nShutting down servers...")
        backend_process.terminate()
        frontend_process.terminate()

        # Wait for graceful shutdown
        try:
            backend_process.wait(timeout=5)
            frontend_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            backend_process.kill()
            frontend_process.kill()

        print_success("Servers stopped. Goodbye! 👋")


def main() -> None:
    """Main launcher function."""
    print_header("CoachX Launcher")
    print(f"{Colors.BOLD}Welcome to CoachX! 🥊{Colors.ENDC}")
    print("This script will set up and launch the application.\n")

    # Step 1: Check requirements
    print_header("Step 1: Checking Requirements")
    check_python_version()
    check_node()
    check_npm()

    # Step 2: Get API key (skip if .env already exists)
    print_header("Step 2: API Configuration")
    backend_env = Path("backend") / ".env"
    if backend_env.exists():
        print_info(".env file already exists, skipping API key setup")
        api_key = None
    else:
        api_key = get_gemini_api_key()

    # Step 3: Setup environments
    print_header("Step 3: Environment Setup")
    if api_key:
        setup_backend_env(api_key)
    else:
        print_success("Backend .env already configured")

    frontend_env = Path("frontend") / ".env.local"
    if not frontend_env.exists():
        setup_frontend_env()
    else:
        print_success("Frontend .env.local already configured")
    
    # Step 4: Install dependencies
    python_path = setup_backend()
    setup_frontend()
    
    # Step 5: Start servers
    start_servers(python_path)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_info("\nSetup cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        sys.exit(1)