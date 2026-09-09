from pathlib import Path
from src.parser import parse_cordeau_mdvrp
from src.distance import create_distance_matrix
from src.model import solve_with_ortools

BASE_DIR = Path(__file__).resolve().parents[1]
file_path = BASE_DIR / "data" / "raw" / "cordeau" / "p01.txt"

data = parse_cordeau_mdvrp(file_path)
locations, dist_matrix = create_distance_matrix(data)

# Give OR-Tools 10 seconds to find the best routes
solution = solve_with_ortools(data, dist_matrix, time_limit_seconds=10)

print("\n" + "="*50)
print("OR-TOOLS OPTIMIZATION RESULTS")
print("="*50)
print(f"Total Routes used: {solution['vehicles_used']}")
print(f"Total Distance: {solution['total_distance']:.2f}")

print("\nSample Route (First Vehicle):")
print(solution["routes"][0])