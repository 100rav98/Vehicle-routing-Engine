from pathlib import Path

from src.parser import parse_cordeau_mdvrp
from src.distance import create_distance_matrix


# Find project root
BASE_DIR = Path(__file__).resolve().parents[1]

# Path to benchmark instance
file_path = (
    BASE_DIR
    / "data"
    / "raw"
    / "cordeau"
    / "p01.txt"
)

# Parse benchmark
data = parse_cordeau_mdvrp(file_path)

# Create locations and distance matrix
locations, distance_matrix = create_distance_matrix(data)


print("\n" + "=" * 60)
print("DISTANCE MATRIX TEST")
print("=" * 60)

print("\nNumber of locations:")
print(len(locations))

print("\nLocation table:")
print(locations.head())

print("\nDistance matrix shape:")
print(distance_matrix.shape)

print("\nFirst 5 x 5 section of distance matrix:")
print(distance_matrix.iloc[:5, :5])

print("\nDistance from first location to itself:")
print(distance_matrix.iloc[0, 0])

print("\n" + "=" * 60)