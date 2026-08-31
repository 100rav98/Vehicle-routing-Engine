from pathlib import Path
import pandas as pd


def parse_cordeau_mdvrp(file_path):
    """
    Read a Cordeau Multi-Depot Vehicle Routing Problem (MDVRP)
    benchmark instance and convert it into structured data.
    """

    # ---------------------------------------------------------
    # 1. Read the raw file
    # ---------------------------------------------------------

    file_path = Path(file_path)

    with open(file_path, "r") as file:
        lines = [line.strip() for line in file if line.strip()]

    # ---------------------------------------------------------
    # 2. Read the problem header
    # ---------------------------------------------------------

    header = lines[0].split()

    problem_type = int(header[0])
    vehicles_per_depot = int(header[1])
    customer_count = int(header[2])
    depot_count = int(header[3])

    # ---------------------------------------------------------
    # 3. Read depot-level vehicle information
    # ---------------------------------------------------------

    depot_parameters = []

    for i in range(depot_count):
        values = lines[1 + i].split()

        max_route_duration = float(values[0])
        vehicle_capacity = float(values[1])

        depot_parameters.append(
            {
                "max_route_duration": max_route_duration,
                "vehicle_capacity": vehicle_capacity,
            }
        )

    # ---------------------------------------------------------
    # 4. Read customer records
    # ---------------------------------------------------------

    customers = []

    customer_start = 1 + depot_count
    customer_end = customer_start + customer_count

    for line in lines[customer_start:customer_end]:

        values = line.split()

        customer_id = int(values[0])
        x = float(values[1])
        y = float(values[2])
        service_duration = float(values[3])
        demand = float(values[4])
        frequency = int(values[5])
        combination_count = int(values[6])

        visit_combinations = [
            int(value)
            for value in values[7:]
        ]

        customers.append(
            {
                "customer_id": customer_id,
                "x": x,
                "y": y,
                "service_duration": service_duration,
                "demand": demand,
                "frequency": frequency,
                "combination_count": combination_count,
                "visit_combinations": visit_combinations,
            }
        )

    # ---------------------------------------------------------
    # 5. Read depot records
    # ---------------------------------------------------------

    depots = []

    depot_start = customer_end

    for i, line in enumerate(lines[depot_start:]):

        values = line.split()

        depot_id = int(values[0])
        x = float(values[1])
        y = float(values[2])

        depots.append(
            {
                "depot_id": depot_id,
                "x": x,
                "y": y,
                "max_route_duration": depot_parameters[i][
                    "max_route_duration"
                ],
                "vehicle_capacity": depot_parameters[i][
                    "vehicle_capacity"
                ],
                "vehicle_count": vehicles_per_depot,
            }
        )

    # ---------------------------------------------------------
    # 6. Convert everything into Pandas DataFrames
    # ---------------------------------------------------------

    customers_df = pd.DataFrame(customers)
    depots_df = pd.DataFrame(depots)

    # ---------------------------------------------------------
    # 7. Create vehicle records
    # ---------------------------------------------------------

    vehicles = []

    for depot in depots:

        for vehicle_number in range(1, vehicles_per_depot + 1):

            vehicles.append(
                {
                    "vehicle_id": (
                        f"D{depot['depot_id']}_V{vehicle_number}"
                    ),
                    "depot_id": depot["depot_id"],
                    "capacity": depot["vehicle_capacity"],
                    "max_route_duration": depot[
                        "max_route_duration"
                    ],
                }
            )

    vehicles_df = pd.DataFrame(vehicles)

    # ---------------------------------------------------------
    # 8. Return all parsed information
    # ---------------------------------------------------------

    return {
        "problem_type": problem_type,
        "vehicles_per_depot": vehicles_per_depot,
        "customer_count": customer_count,
        "depot_count": depot_count,
        "customers": customers_df,
        "depots": depots_df,
        "vehicles": vehicles_df,
    }

# The entire program is basically doing the following steps:
# 1. Open file
#        ↓
# 2. Read header
#        ↓
# 3. Read depot parameters
#        ↓
# 4. Read customers
#        ↓
# 5. Read depots
#        ↓
# 6. Create tables
#        ↓
# 7. Create vehicles
#        ↓
# 8. Return everything