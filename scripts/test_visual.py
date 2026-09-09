from pathlib import Path
from src.parser import parse_cordeau_mdvrp
from src.distance import create_distance_matrix
from src.model import solve_with_ortools
from src.visualization import plot_solution

# 1. Locate the data file
BASE_DIR = Path(__file__).resolve().parents[1]
file_path = BASE_DIR / "data" / "raw" / "cordeau" / "p01.txt"

# 2. Parse the data and build the math matrix
print("Loading data and calculating distances...")
data = parse_cordeau_mdvrp(file_path)
locations, dist_matrix = create_distance_matrix(data)

# 3. Ask the AI to find the best routes (giving it 10 seconds)
print("Running AI optimizer...")
solution = solve_with_ortools(data, dist_matrix, time_limit_seconds=10)

# 4. Draw the map!
if solution:
    print("Drawing the map...")
    plot_solution(data, solution, title="Google OR-Tools: Optimized MDVRP Routes")
else:
    print("Could not find a solution to plot.")