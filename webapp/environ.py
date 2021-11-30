from pathlib import Path
import os

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent/'.env')

data_path: Path = Path(os.getenv('DATA_PATH', '.'))
