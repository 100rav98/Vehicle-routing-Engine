import time
from pathlib import Path
from src.parser import parse_cordeau_mdvrp
from src.distance import create_distance_matrix
from src.baseline import solve_nearest_neighbor
from src.model import solve_with_ortools

# 1. Load Data
BASE_DIR = Path(__file__).resolve().parents[1]
file_path = BASE_DIR / "data" / "raw" / "cordeau" / "p01.txt"

print("\nLoading data and calculating matrix...")
data = parse_cordeau_mdvrp(file_path)
_, dist_matrix = create_distance_matrix(data)

# 2. Run Baseline
print("\nRunning Baseline (Nearest Neighbor)...")
start_time = time.time()
baseline_sol = solve_nearest_neighbor(data, dist_matrix)
baseline_time = time.time() - start_time

# 3. Run OR-Tools
print("\nRunning OR-Tools AI...")
start_time = time.time()
ortools_sol = solve_with_ortools(data, dist_matrix, time_limit_seconds=10)
ortools_time = time.time() - start_time

# 4. Calculate Savings
base_dist = baseline_sol["total_distance"]
or_dist = ortools_sol["total_distance"]
savings = base_dist - or_dist
improvement_pct = (savings / base_dist) * 100

# 5. Print the Executive Summary
print("\n" + "="*55)
print("🏆 FINAL BENCHMARK RESULTS 🏆")
print("="*55)
print(f"{'Metric':<18} | {'Baseline':<12} | {'OR-Tools':<12}")
print("-" * 49)
print(f"{'Distance':<18} | {base_dist:<12.2f} | {or_dist:<12.2f}")
print(f"{'Vehicles Used':<18} | {len(baseline_sol['routes']):<12} | {ortools_sol['vehicles_used']:<12}")
print(f"{'Solve Time (sec)':<18} | {baseline_time:<12.4f} | {ortools_time:<12.4f}")
print("-" * 49)
print(f"Total Distance Saved: {savings:.2f} units")
print(f"Overall Improvement:  {improvement_pct:.1f}%")
print("="*55)