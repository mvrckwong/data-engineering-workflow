import os
import subprocess
import sys
from pathlib import Path
from typing import Optional, Union
import datetime

# Attempt to import tkinter for optional GUI file dialog
try:
    import tkinter as tk
    from tkinter import filedialog
    TKINTER_AVAILABLE = True
except ImportError:
    TKINTER_AVAILABLE = False

# Use python-dotenv to load environment variables from a .env file
# It needs to be installed: pip install python-dotenv
try:
    from dotenv import load_dotenv
except ImportError:
    print("Error: python-dotenv is not installed. Please install it: pip install python-dotenv")
    sys.exit(1)

from loguru import logger

# --- Logger Configuration ---
logger.remove()
logger.add(sys.stderr, level="INFO")

# --- Constants ---
TIMESTAMP_FORMAT = "%Y%m%d_%H%M%S"
DEFAULT_FILENAME_PATTERN = f"airflow_backup_{{timestamp}}.dump"
DEFAULT_DOTENV_FILENAME = ".env" # Default name if path not specified
# Environment variable to specify the path to the .env file
ENV_FILE_PATH_VAR = "BACKUP_ENV_FILE_PATH"

# --- Helper Functions ---

def get_save_path_interactive(default_filename: str) -> str:
    """
    Shows an interactive 'Save As' dialog or returns the default path.
    (Function implementation remains the same)
    """
    if not TKINTER_AVAILABLE:
        logger.warning("Tkinter not available. Cannot show interactive file dialog.")
        logger.warning(f"Using default filename: {default_filename}")
        return default_filename

    logger.info("Opening interactive file dialog to choose save location...")
    root = tk.Tk()
    root.withdraw()

    file_path_selected = None
    try:
        suggested_name = Path(default_filename).name
        suggested_dir = Path(default_filename).parent if Path(default_filename).is_absolute() else None
        file_path_selected = filedialog.asksaveasfilename(
            title="Save Airflow Backup As",
            initialfile=suggested_name,
            initialdir=str(suggested_dir) if suggested_dir else None,
            defaultextension=".dump",
            filetypes=[("Dump files", "*.dump"), ("All files", "*.*")]
        )
    except Exception as e:
        logger.error(f"Error opening tkinter file dialog: {e}")
        file_path_selected = None
    finally:
        try:
            root.destroy()
        except tk.TclError:
            pass

    if file_path_selected:
        logger.info(f"File path selected: {file_path_selected}")
        return file_path_selected
    else:
        logger.warning("File selection cancelled or failed. Using default path.")
        logger.warning(f"Using default filename: {default_filename}")
        return default_filename

def run_pg_dump(
    db_host: str,
    db_user: str,
    db_name: str,
    output_file: Path,
    db_port: Optional[str] = None,
    db_password: Optional[str] = None,
) -> bool:
    """
    Executes the pg_dump command to back up the specified PostgreSQL database.
    (Function implementation remains the same)
    """
    command = [
        "pg_dump",
        "-h", db_host,
        "-U", db_user,
        "-d", db_name,
        "-F", "c",
        "-b",
        "-v",
        "-f", str(output_file),
    ]

    if db_port:
        command.extend(["-p", db_port])

    env = os.environ.copy()
    if db_password:
        env["PGPASSWORD"] = db_password
        logger.info(f"Attempting pg_dump for database '{db_name}' on host '{db_host}'...")
        logger.debug(f"Executing command (password omitted): {' '.join(command)}")
    else:
        logger.info(f"Attempting pg_dump for database '{db_name}' on host '{db_host}' (no password provided)...")
        logger.debug(f"Executing command: {' '.join(command)}")

    try:
        result = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
            env=env,
            encoding='utf-8'
        )
        if result.stderr:
            logger.info("pg_dump output:\n" + result.stderr.strip())
        logger.success(f"Database dump successful: '{output_file}'")
        return True
    except FileNotFoundError:
        logger.error("Error: 'pg_dump' command not found. Is PostgreSQL client installed and in PATH?")
        return False
    except subprocess.CalledProcessError as e:
        logger.error(f"Error during pg_dump execution (Return Code: {e.returncode}):")
        logger.error("STDERR:\n" + e.stderr.strip())
        if e.stdout:
            logger.error("STDOUT:\n" + e.stdout.strip())
        return False
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return False

def main():
    """Orchestrates the backup process."""

    script_directory = Path(__file__).resolve().parent
    default_output_directory = Path.cwd()

    # --- Determine Output Path ---
    current_timestamp = datetime.datetime.now().strftime(TIMESTAMP_FORMAT)
    default_filename_only = DEFAULT_FILENAME_PATTERN.format(timestamp=current_timestamp)
    default_full_path = str(default_output_directory / default_filename_only)
    output_path_str = get_save_path_interactive(default_full_path)
    output_path = Path(output_path_str).resolve()

    # --- Ensure Output Directory Exists ---
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        logger.info(f"Ensured output directory exists: {output_path.parent}")
    except OSError as e:
        logger.error(f"Failed to create output directory {output_path.parent}: {e}")
        sys.exit(1)

    # --- Determine and Load .env File ---
    # Check if a specific path is provided via environment variable
    custom_env_path_str = os.getenv(ENV_FILE_PATH_VAR)
    if custom_env_path_str:
        env_file_path = Path(custom_env_path_str).resolve()
        logger.info(f"Using .env path specified by environment variable {ENV_FILE_PATH_VAR}: {env_file_path}")
    else:
        # Default to looking for '.env' in the script's directory
        env_file_path = script_directory / DEFAULT_DOTENV_FILENAME
        logger.info(f"Environment variable {ENV_FILE_PATH_VAR} not set.")
        logger.info(f"Looking for default .env file at: {env_file_path}")

    if env_file_path.is_file():
        logger.info(f"Loading environment variables from: {env_file_path}")
        # The load_dotenv function loads variables into os.environ
        load_dotenv(dotenv_path=env_file_path, verbose=True, override=True)
    else:
        logger.warning(f"Environment file not found at '{env_file_path}'. Relying only on system environment variables.")
        # Proceeding, as required vars might be set globally

    # --- Get Database Configuration ---
    # Now read from os.environ, which includes variables loaded by load_dotenv
    db_host = os.getenv("POSTGRES_HOST")
    db_user = os.getenv("POSTGRES_USER")
    db_password = os.getenv("POSTGRES_PASSWORD")
    db_name = os.getenv("POSTGRES_DB")
    db_port = os.getenv("PORT_POSTGRES")

    # --- Basic Validation ---
    required_vars = {"POSTGRES_HOST": db_host, "POSTGRES_USER": db_user, "POSTGRES_DB": db_name}
    missing_vars = [k for k, v in required_vars.items() if v is None]

    if missing_vars:
        logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        logger.error(f"Please set them (e.g., in '{env_file_path}') or the system environment.")
        sys.exit(1)

    if not db_password:
        logger.warning("POSTGRES_PASSWORD environment variable not set. Connection may fail if password is required.")

    # --- Run Backup ---
    logger.info(f"Starting backup for database '{db_name}' to file '{output_path}'...")
    success = run_pg_dump(
        db_host=db_host,
        db_user=db_user,
        db_name=db_name,
        output_file=output_path,
        db_port=db_port,
        db_password=db_password
    )

    # --- Exit ---
    if success:
        logger.info("Backup process completed successfully.")
        sys.exit(0)
    else:
        logger.error("Backup process failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()