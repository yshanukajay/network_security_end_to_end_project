import logging
import os
from datetime import datetime

# 1. Create a timestamp for the filename
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# 2. Define the path for the 'logs' FOLDER only
logs_dir = os.path.join(os.getcwd(), "logs")

# 3. Create the 'logs' folder if it doesn't exist
os.makedirs(logs_dir, exist_ok=True)

# 4. Join the folder path with the filename to get the full file path
LOG_FILE_PATH = os.path.join(logs_dir, LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)