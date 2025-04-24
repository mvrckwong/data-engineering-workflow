# generate_airflow_key.py

import argparse
import sys
from typing import List

from cryptography.fernet import Fernet
from loguru import logger

# Configure logging to output to stderr
logger.remove()
logger.add(sys.stderr, level="INFO")

def generate_fernet_key() -> str:
    """
    Generates a cryptographically secure Fernet key.

    Returns:
        str: The generated Fernet key, base64-encoded as a string.
    """
    key_bytes = Fernet.generate_key()
    # Decode bytes to string for easier handling/display and use in config files
    return key_bytes.decode('utf-8')

def main():
    """Handles command-line arguments for generating Fernet keys."""
    parser = argparse.ArgumentParser(
        description="Generate one or more secure Fernet keys suitable for Airflow.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "-n", "--number",
        type=int,
        default=1,
        help="Number of Fernet keys to generate."
    )

    args = parser.parse_args()

    if args.number < 1:
        logger.error("Number of keys must be at least 1.")
        # Use parser.error to exit cleanly with usage message
        parser.error("Number of keys must be at least 1.")
        # return is redundant after parser.error() but kept for clarity if error handling changes
        return

    logger.info(f"Generating {args.number} Fernet Key(s)...")
    generated_keys: List[str] = []
    for i in range(args.number):
        try:
            fernet_key = generate_fernet_key()
            generated_keys.append(fernet_key)
            # Log each key successfully generated
            logger.success(f"Key {i+1}: {fernet_key}")
        except Exception as e:
            # Catching generic Exception as Fernet generation is usually robust
            logger.error(f"Error generating key {i+1}: {e}")
            # Stop generation if an error occurs to avoid partial results without notice
            break

    # Give a final status update
    if len(generated_keys) == args.number:
        logger.info("Generation complete.")
    else:
        logger.warning("Generation finished, but encountered errors.")


if __name__ == "__main__":
    main()