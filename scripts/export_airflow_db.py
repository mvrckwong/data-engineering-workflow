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
TIMESTAMP_FORMAT = "%Y%m%d"
DEFAULT_FILENAME_PATTERN = f"airflow_backup_{{timestamp}}.dump"
DEFAULT_DOTENV_FILENAME = ".env" # Default name of the .env file

# Name of the environment variable users can set to specify a custom .env file path
DOTENV_PATH_ENV_VAR = "AIRFLOW_BACKUP_DOTENV_PATH"

# --- Helper Functions ---

def get_save_path_interactive(default_filename: str) -> str:
    """
    Shows an interactive 'Save As' dialog or returns the default path.
    """
    if not TKINTER_AVAILABLE:
        logger.warning("Tkinter not available. Cannot show interactive file dialog.")
        logger.warning(f"Using default filename: {default_filename}")
        return default_filename

    logger.info("Opening interactive file dialog to choose save location...")
    root = tk.Tk()
    root.withdraw() # Hide the main tkinter window

    file_path_selected = None
    try:
        suggested_name = Path(default_filename).name
        suggested_dir = Path(default_filename).parent if Path(default_filename).is_absolute() else Path.cwd()
        file_path_selected = filedialog.asksaveasfilename(
            title="Save Airflow Backup As",
            initialfile=suggested_name,
            initialdir=str(suggested_dir),
            defaultextension=".dump",
            filetypes=[("Dump files", "*.dump"), ("All files", "*.*")]
        )
    except Exception as e:
        logger.error(f"Error opening tkinter file dialog: {e}")
        file_path_selected = None
    finally:
        # Ensure the tkinter root window is destroyed
        try:
            root.destroy()
        except tk.TclError:
            # Can happen if the window was already closed/destroyed
            pass

    if file_path_selected:
        logger.info(f"File path selected: {file_path_selected}")
        return file_path_selected
    else:
        logger.warning("File selection cancelled or failed.")
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
    """
    command = [
        "pg_dump",
        "-h", db_host,
        "-U", db_user,
        "-d", db_name,
        "-F", "c",    # Format: custom (compressed, suitable for pg_restore)
        "-b",         # Include large objects
        "-v",         # Verbose mode
        "-f", str(output_file), # Output file path
    ]

    if db_port:
        command.extend(["-p", db_port])

    # Use PGPASSWORD environment variable for security instead of command-line arg
    env = os.environ.copy()
    if db_password:
        env["PGPASSWORD"] = db_password
        logger.info(f"Attempting pg_dump for database '{db_name}' on host '{db_host}'...")
        # Avoid logging password in debug command
        debug_command = [part if i > 0 and command[i-1] != "-U" else part for i, part in enumerate(command)]
        logger.debug(f"Executing command (password set via env): {' '.join(debug_command)}")
    else:
        logger.info(f"Attempting pg_dump for database '{db_name}' on host '{db_host}' (no password provided)...")
        logger.debug(f"Executing command: {' '.join(command)}")


    try:
        # Run the command
        result = subprocess.run(
            command,
            check=True,         # Raise CalledProcessError on non-zero exit code
            capture_output=True,# Capture stdout and stderr
            text=True,          # Decode stdout/stderr as text
            env=env,            # Pass the environment with PGPASSWORD
            encoding='utf-8'    # Specify encoding
        )
        # pg_dump often outputs progress/info to stderr even on success
        if result.stderr:
            logger.info("pg_dump output (stderr):\n" + result.stderr.strip())
        if result.stdout: # Should generally be empty unless errors redirected
             logger.info("pg_dump output (stdout):\n" + result.stdout.strip())

        logger.success(f"Database dump successful: '{output_file}'")
        return True
    except FileNotFoundError:
        logger.error("Error: 'pg_dump' command not found.")
        logger.error("Please ensure the PostgreSQL client tools are installed and 'pg_dump' is in your system's PATH.")
        return False
    except subprocess.CalledProcessError as e:
        logger.error(f"Error during pg_dump execution (Return Code: {e.returncode}):")
        # Log stderr first, as it usually contains the error message from pg_dump
        if e.stderr:
             logger.error("STDERR:\n" + e.stderr.strip())
        else:
             logger.error("STDERR: (empty)")
        if e.stdout:
            logger.error("STDOUT:\n" + e.stdout.strip())
        return False
    except Exception as e:
        # Catch any other unexpected exceptions
        logger.error(f"An unexpected error occurred during pg_dump: {e}")
        return False

def main():
    """Orchestrates the backup process."""

    script_directory = Path(__file__).resolve().parent
    script_parent_directory = script_directory.parent # Directory above the script
    default_output_directory = Path.cwd() # Default save *to* is current working dir

    # --- Determine Output Path ---
    current_timestamp = datetime.datetime.now().strftime(TIMESTAMP_FORMAT)
    default_filename_only = DEFAULT_FILENAME_PATTERN.format(timestamp=current_timestamp)
    default_full_path = str(default_output_directory / default_filename_only)

    # Ask user for save location (or use default if cancelled/Tkinter unavailable)
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
    custom_env_path_str = os.getenv(DOTENV_PATH_ENV_VAR) # Use the string name
    if custom_env_path_str:
        env_file_path = Path(custom_env_path_str).resolve()
        logger.info(f"Using .env path specified by environment variable '{DOTENV_PATH_ENV_VAR}': {env_file_path}")
    else:
        # Default to looking for '.env' in the script's PARENT directory
        env_file_path = script_parent_directory / DEFAULT_DOTENV_FILENAME
        logger.info(f"Environment variable '{DOTENV_PATH_ENV_VAR}' not set.")
        logger.info(f"Looking for default .env file in parent directory: {env_file_path}")

    if env_file_path.is_file():
        logger.info(f"Loading environment variables from: {env_file_path}")
        # load_dotenv loads variables into os.environ
        # verbose=True logs which variables are loaded
        # override=True ensures variables in .env overwrite existing ones
        load_dotenv(dotenv_path=env_file_path, verbose=True, override=True)
    else:
        logger.warning(f"Environment file not found at '{env_file_path}'.")
        logger.warning("Relying solely on system environment variables for DB connection.")
        # Proceeding, as required vars might be set globally or via other means

    # --- Get Database Configuration ---
    # Read from os.environ, which includes variables loaded by load_dotenv
    # Using distinct variables for host and port
    db_host = os.getenv("POSTGRES_HOST")
    db_port = os.getenv("POSTGRES_PORT") # Port is optional, pg_dump uses default 5432 if not set
    db_user = os.getenv("POSTGRES_USER")
    db_password = os.getenv("POSTGRES_PASSWORD") # Password is optional but recommended
    db_name = os.getenv("POSTGRES_DB")

    # --- Basic Validation ---
    # Host, User, and DB Name are strictly required
    required_vars = {
        "POSTGRES_HOST": db_host,
        "POSTGRES_USER": db_user,
        "POSTGRES_DB": db_name
    }
    missing_vars = [k for k, v in required_vars.items() if not v] # Check for None or empty string

    if missing_vars:
        logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        logger.error(f"Please set them in the system environment or in '{env_file_path}'.")
        sys.exit(1)

    if not db_password:
        # Warn if password is not set, as connection might fail
        logger.warning("POSTGRES_PASSWORD environment variable not set.")
        logger.warning("Database connection may fail if a password is required.")
    if not db_port:
        logger.info("POSTGRES_PORT environment variable not set. pg_dump will use the default port (usually 5432).")


    # --- Run Backup ---
    logger.info(f"Starting backup for database '{db_name}' on host '{db_host}'...")
    logger.info(f"Output file: '{output_path}'")
    success = run_pg_dump(
        db_host=db_host,
        db_user=db_user,
        db_name=db_name,
        output_file=output_path,
        db_port=db_port,          # Pass port (can be None)
        db_password=db_password   # Pass password (can be None)
    )

    # --- Exit ---
    if success:
        logger.info("Backup process completed successfully.")
        sys.exit(0) # Exit with success code
    else:
        logger.error("Backup process failed.")
        # Optional: Delete potentially incomplete/empty output file on failure
        # try:
        #     if output_path.exists() and output_path.stat().st_size == 0:
        #          logger.warning(f"Deleting empty output file due to failure: {output_path}")
        #          output_path.unlink()
        #     elif output_path.exists():
        #          logger.warning(f"Backup failed, leaving potentially incomplete file: {output_path}")
        # except OSError as e:
        #     logger.error(f"Failed to delete empty/incomplete output file: {e}")
        sys.exit(1) # Exit with error code

if __name__ == "__main__":
    main()