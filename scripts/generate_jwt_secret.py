# generate_jwt_secret.py

import argparse
import secrets
import sys
from typing import List

from loguru import logger

# Configure logging to output to stderr
logger.remove()
logger.add(sys.stderr, level="INFO")

def generate_jwt_secret(num_bytes: int = 32) -> str:
    """
    Generates a cryptographically secure, URL-safe random string suitable for a JWT secret.

    Args:
        num_bytes (int): The number of random bytes to generate.
                         Defaults to 32 bytes (256 bits), a common recommendation for HS256.
                         Use 64 bytes (512 bits) for HS512 if desired.

    Returns:
        str: The generated URL-safe secret string.
    """
    # token_urlsafe generates a base64-encoded string from num_bytes random bytes.
    # The resulting string will be longer than num_bytes.
    return secrets.token_urlsafe(num_bytes)

def main():
    """Handles command-line arguments for generating JWT secrets."""
    parser = argparse.ArgumentParser(
        description="Generate one or more secure random strings suitable for JWT secrets.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "-n", "--number",
        type=int,
        default=1,
        help="Number of JWT secrets to generate."
    )
    parser.add_argument(
        "-b", "--bytes",
        type=int,
        default=32,
        help="Number of random bytes to use for generating each secret (e.g., 32 for HS256, 64 for HS512)."
    )

    args = parser.parse_args()

    if args.number < 1:
        logger.error("Number of secrets must be at least 1.")
        parser.error("Number of secrets must be at least 1.")
        return # Redundant after parser.error()

    if args.bytes < 16:
         # Warn if the number of bytes is low, but allow it.
         # 16 bytes = 128 bits. Common minimum might be 256 bits (32 bytes).
        logger.warning(f"Generating secrets with only {args.bytes} bytes. Consider using 32 or more for stronger security.")

    logger.info(f"Generating {args.number} JWT Secret(s) using {args.bytes} random bytes each...")
    generated_secrets: List[str] = []
    for i in range(args.number):
        try:
            jwt_secret = generate_jwt_secret(num_bytes=args.bytes)
            generated_secrets.append(jwt_secret)
            # Log each secret successfully generated
            logger.success(f"Secret {i+1}: {jwt_secret}")
        except Exception as e:
            # Catching generic Exception as secrets generation is usually robust
            logger.error(f"Error generating secret {i+1}: {e}")
            # Stop generation if an error occurs
            break

    # Give a final status update
    if len(generated_secrets) == args.number:
        logger.info("Generation complete.")
    else:
        logger.warning("Generation finished, but encountered errors.")


if __name__ == "__main__":
    main()