import os
from kaggle.api.kaggle_api_extended import KaggleApi
import zipfile
import pandas as pd

from dotenv import load_dotenv

load_dotenv()

# ------------------------------------------------------
# 1. Set Up Authentication (without CLI)
# ------------------------------------------------------
# Set environment variables for authentication
# os.environ['KAGGLE_USERNAME'] = 
# os.environ['KAGGLE_KEY'] = '52a6b8ae540e6ae86df3326b02a68a74'        # Replace with your API key (from kaggle.json)

# ------------------------------------------------------
# 2. Initialize Kaggle API Client
# ------------------------------------------------------
api = KaggleApi()
api.authenticate()  # Uses the environment variables above

# ------------------------------------------------------
# 3. Download Dataset (Entire Dataset)
# ------------------------------------------------------
dataset_owner = "zynicide"
dataset_name = "wine-reviews"
api.dataset_download_files(
    f"{dataset_owner}/{dataset_name}",  # Dataset identifier
    path="data",                           # Download to current directory
    unzip=True,                         # Auto-unzip the file
    quiet=False                         # Show progress
)

# ------------------------------------------------------
# 4. Load Data into Pandas
# ------------------------------------------------------
# Check the unzipped filename (might vary by dataset)
# df = pd.read_csv("winemag-data_first150k.csv")
# print(df.head())