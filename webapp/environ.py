import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

data_path: Path = Path(os.getenv("DATA_PATH", "."))
