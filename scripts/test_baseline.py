from pathlib import Path
from src.parser import parse_cordeau_mdvrp
# 1. FIX: Import the exact name used in distance.py
from src.distance import create_distance_matrix 
from src.baseline import solve_nearest_neighbor

BASE_DIR = Path(__file__).resolve().parents[1]
file_path = BASE_DIR / "data" / "raw" / "cordeau" / "p01.txt"

# 1. Parse Data
data = parse_cordeau_mdvrp(file_path)

# 2. FIX: Unpack both the locations and the distance matrix
locations, dist_matrix = create_distance_matrix(data)

# 3. Solve with Baseline
solution = solve_nearest_neighbor(data, dist_matrix)

# 4. Show a sample route
if solution.get("routes"):
    print("\nSample Route (Vehicle 1):")
    print(solution["routes"][0])