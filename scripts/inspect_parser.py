from pathlib import Path
from src.parser import parse_cordeau_mdvrp


# Find the project root directory
BASE_DIR = Path(__file__).resolve().parents[1]

# Path to the Cordeau benchmark instance
file_path = BASE_DIR / "data" / "raw" / "cordeau" / "p01.txt"

# Run the parser
data = parse_cordeau_mdvrp(file_path)


print("\n" + "=" * 60)
print("PARSER OUTPUT INSPECTION")
print("=" * 60)

print("\nType returned by parser:")
print(type(data))

print("\nFull structure:")
print(data)

print("\n" + "=" * 60)
