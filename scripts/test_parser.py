from src.parser import parse_cordeau_mdvrp


# Path to our benchmark instance
file_path = "data/raw/cordeau/p01.txt"


# Parse the benchmark
data = parse_cordeau_mdvrp(file_path)


# Print basic information
print("Problem type:", data["problem_type"])
print("Vehicles per depot:", data["vehicles_per_depot"])
print("Customer count:", data["customer_count"])
print("Depot count:", data["depot_count"])


print("\nCustomers:")
print(data["customers"].head())


print("\nDepots:")
print(data["depots"])


print("\nVehicles:")
print(data["vehicles"])
