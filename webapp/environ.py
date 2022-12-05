import os
from pathlib import Path

data_path: Path = Path(os.getenv('DATA_PATH', '.'))
 