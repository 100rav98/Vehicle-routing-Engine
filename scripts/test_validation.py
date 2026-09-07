from pathlib import Path

from src.parser import parse_cordeau_mdvrp
from src.validation import validate_data


BASE_DIR = Path(__file__).resolve().parents[1]

file_path = BASE_DIR / "data" / "raw" / "cordeau" / "p01.txt"

data = parse_cordeau_mdvrp(file_path)

validate_data(data)

print("Validation passed successfully!")