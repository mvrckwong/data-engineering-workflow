# from cryptography.fernet import Fernet

# # Generate a new Fernet key (returns bytes)
# fernet_key_bytes = Fernet.generate_key()

# # Decode the bytes into a string (Fernet keys are base64 encoded)
# fernet_key_string = fernet_key_bytes.decode()

# # Print the key
# print("Generated Fernet Key:")
# print(fernet_key_string)

# # --- How to use it in Airflow ---
# # You would typically set this key as an environment variable
# # or store it securely in a secrets manager.
# # Example for environment variable:
# # export AIRFLOW__CORE__FERNET_KEY='YOUR_GENERATED_KEY_HERE'

# # In your docker-compose.yml environment section or .env file:
# # AIRFLOW__CORE__FERNET_KEY='YOUR_GENERATED_KEY_HERE'