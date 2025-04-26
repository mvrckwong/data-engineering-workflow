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
DEFAULT_DOTENV_FILENAME = ".env" # Default name of the .env file
# Name of the environment variable users can set to specify a custom .env file path
DOTENV_PATH_ENV_VAR = "AIRFLOW_BACKUP_DOTENV_PATH" # Reuse same var as backup script

# --- Helper Functions ---

def get_restore_file_path_interactive() -> Optional[str]:
    """
    Shows an interactive 'Open' dialog to select the backup file.
    Provides a command-line fallback if Tkinter is unavailable.
    Returns the selected file path as a string, or None if cancelled/failed.
    """
    if TKINTER_AVAILABLE:
        logger.info("Opening interactive file dialog to choose backup file...")
        root = tk.Tk()
        root.withdraw() # Hide the main tkinter window

        file_path_selected = None
        try:
            # Suggest starting directory as current working directory
            initial_dir = str(Path.cwd())
            file_path_selected = filedialog.askopenfilename(
                title="Select Airflow Backup File to Restore",
                initialdir=initial_dir,
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
                pass # Window might already be closed

        if file_path_selected:
            logger.info(f"Backup file selected: {file_path_selected}")
            return file_path_selected
        else:
            logger.warning("File selection cancelled or no file chosen via dialog.")
            return None
    else:
        logger.warning("Tkinter not available. Cannot show interactive file dialog.")
        logger.info("Please enter the full path to the backup (.dump) file:")
        try:
            file_path_input = input("> ")
            if file_path_input and Path(file_path_input).is_file():
                 logger.info(f"Using backup file path from input: {file_path_input}")
                 return file_path_input
            elif file_path_input:
                 logger.error(f"File not found at provided path: {file_path_input}")
                 return None
            else:
                 logger.warning("No file path entered.")
                 return None
        except Exception as e:
            logger.error(f"Error reading input: {e}")
            return None


def run_pg_restore(
    db_host: str,
    db_user: str,
    db_name: str,
    input_file: Path,
    db_port: Optional[str] = None,
    db_password: Optional[str] = None,
) -> bool:
    """
    Executes the pg_restore command to restore the specified PostgreSQL database.
    Assumes the input file is in the custom format (-Fc from pg_dump).
    """
    if not input_file.is_file():
        logger.error(f"Input backup file not found: {input_file}")
        return False

    # Check if target database exists (basic check - tool will fail if not)
    logger.warning(f"Ensure the target database '{db_name}' exists on host '{db_host}' before proceeding.")
    logger.warning(f"The restore process will attempt to drop and recreate objects within '{db_name}'.")

    command = [
        "pg_restore",
        "-h", db_host,
        "-U", db_user,
        "-d", db_name,      # Target database *to restore into*
        "-v",               # Verbose mode
        "--clean",          # Drop database objects before recreating them
        "--if-exists",      # Add '--if-exists' to clean commands (prevents errors if object missing)
        "-1",               # Run commands in a single transaction
        str(input_file),    # The backup file to restore from
    ]

    if db_port:
        command.extend(["-p", db_port])

    # Use PGPASSWORD environment variable for security
    env = os.environ.copy()
    if db_password:
        env["PGPASSWORD"] = db_password
        logger.info(f"Attempting pg_restore into database '{db_name}' on host '{db_host}'...")
        # Avoid logging password in debug command
        debug_command = [part if i > 0 and command[i-1] != "-U" else part for i, part in enumerate(command)]
        logger.debug(f"Executing command (password set via env): {' '.join(debug_command)}")
    else:
        logger.info(f"Attempting pg_restore into database '{db_name}' on host '{db_host}' (no password provided)...")
        logger.debug(f"Executing command: {' '.join(command)}")


    try:
        # Run the command
        result = subprocess.run(
            command,
            check=True,           # Raise CalledProcessError on non-zero exit code
            capture_output=True,  # Capture stdout and stderr
            text=True,            # Decode stdout/stderr as text
            env=env,              # Pass the environment with PGPASSWORD
            encoding='utf-8'      # Specify encoding
        )
        # pg_restore outputs progress/info to stderr
        if result.stderr:
            logger.info("pg_restore output (stderr):\n" + result.stderr.strip())
        if result.stdout: # Should generally be empty unless errors redirected
             logger.info("pg_restore output (stdout):\n" + result.stdout.strip())

        logger.success(f"Database restore successful from: '{input_file}'")
        return True
    except FileNotFoundError:
        logger.error("Error: 'pg_restore' command not found.")
        logger.error("Please ensure the PostgreSQL client tools are installed and 'pg_restore' is in your system's PATH.")
        return False
    except subprocess.CalledProcessError as e:
        logger.error(f"Error during pg_restore execution (Return Code: {e.returncode}):")
        # Log stderr first, as it usually contains the error message from pg_restore
        if e.stderr:
             logger.error("STDERR:\n" + e.stderr.strip())
        else:
             logger.error("STDERR: (empty)")
        if e.stdout:
            logger.error("STDOUT:\n" + e.stdout.strip())
        logger.error(f"Common causes: Target database ('{db_name}') does not exist, incorrect password, insufficient user permissions, or corrupted backup file.")
        return False
    except Exception as e:
        # Catch any other unexpected exceptions
        logger.error(f"An unexpected error occurred during pg_restore: {e}")
        return False

def main():
    """Orchestrates the restore process."""

    script_directory = Path(__file__).resolve().parent
    script_parent_directory = script_directory.parent # Directory above the script

    # --- Determine Input File ---
    input_path_str = get_restore_file_path_interactive()
    if not input_path_str:
        logger.error("No input backup file selected or provided. Exiting.")
        sys.exit(1)

    input_path = Path(input_path_str).resolve()
    if not input_path.is_file():
         logger.error(f"Selected input file does not exist: {input_path}")
         sys.exit(1)

    # --- Determine and Load .env File ---
    # (Same logic as the backup script)
    custom_env_path_str = os.getenv(DOTENV_PATH_ENV_VAR)
    if custom_env_path_str:
        env_file_path = Path(custom_env_path_str).resolve()
        logger.info(f"Using .env path specified by environment variable '{DOTENV_PATH_ENV_VAR}': {env_file_path}")
    else:
        env_file_path = script_parent_directory / DEFAULT_DOTENV_FILENAME
        logger.info(f"Environment variable '{DOTENV_PATH_ENV_VAR}' not set.")
        logger.info(f"Looking for default .env file in parent directory: {env_file_path}")

    if env_file_path.is_file():
        logger.info(f"Loading environment variables from: {env_file_path}")
        load_dotenv(dotenv_path=env_file_path, verbose=True, override=True)
    else:
        logger.warning(f"Environment file not found at '{env_file_path}'.")
        logger.warning("Relying solely on system environment variables for DB connection.")

    # --- Get Database Configuration ---
    db_host = os.getenv("POSTGRES_HOST")
    db_port = os.getenv("POSTGRES_PORT")
    db_user = os.getenv("POSTGRES_USER")
    db_password = os.getenv("POSTGRES_PASSWORD")
    db_name = os.getenv("POSTGRES_DB") # This is the TARGET database

    # --- Basic Validation ---
    required_vars = {
        "POSTGRES_HOST": db_host,
        "POSTGRES_USER": db_user,
        "POSTGRES_DB": db_name # Target DB name is required
    }
    missing_vars = [k for k, v in required_vars.items() if not v]

    if missing_vars:
        logger.error(f"Missing required environment variables for target database: {', '.join(missing_vars)}")
        logger.error(f"Please set them in the system environment or in '{env_file_path}'.")
        sys.exit(1)

    if not db_password:
        logger.warning("POSTGRES_PASSWORD environment variable not set.")
        logger.warning("Database connection may fail if a password is required.")
    if not db_port:
        logger.info("POSTGRES_PORT environment variable not set. pg_restore will use the default port (usually 5432).")


    # --- Run Restore ---
    logger.info(f"Starting restore for database '{db_name}' on host '{db_host}'...")
    logger.info(f"Input file: '{input_path}'")

    # Optional: Add a confirmation step
    # confirm = input(f"This will restore '{input_path}' into database '{db_name}' on '{db_host}', potentially overwriting existing data. Proceed? (y/N): ")
    # if confirm.lower() != 'y':
    #     logger.info("Restore cancelled by user.")
    #     sys.exit(0)

    success = run_pg_restore(
        db_host=db_host,
        db_user=db_user,
        db_name=db_name,
        input_file=input_path,
        db_port=db_port,
        db_password=db_password
    )

    # --- Exit ---
    if success:
        logger.info("Restore process completed successfully.")
        sys.exit(0) # Exit with success code
    else:
        logger.error("Restore process failed.")
        sys.exit(1) # Exit with error code

if __name__ == "__main__":
    main()