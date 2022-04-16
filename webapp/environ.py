from pathlib import Path
import os


data_path: Path = Path(os.getenv('DATA_PATH', '.'))
