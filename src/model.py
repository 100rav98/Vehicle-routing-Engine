from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import pandas as pd

def create_ortools_data(data, distance_matrix):
    """Translates Pandas DataFrames into OR-Tools dictionary format."""
    print("\n" + "="*50)
    print("PREPARING DATA FOR GOOGLE OR-TOOLS")
    print("="*50)
    
    ortools_data = {}
    
    vehicles_per_depot = data["vehicles_per_depot"]
    depots_df = data["depots"]
    num_depots = len(depots_df)
    
    total_vehicles = vehicles_per_depot * num_depots
    vehicle_capacity = int(depots_df["vehicle_capacity"].iloc[0])
    
    ortools_data["num_vehicles"] = total_vehicles
    ortools_data["vehicle_capacities"] = [vehicle_capacity] * total_vehicles
    
    all_ids = distance_matrix.index.tolist()
    id_to_index = {loc_id: i for i, loc_id in enumerate(all_ids)}
    
    starts = []
    for depot_id in depots_df["depot_id"]:
        depot_index = id_to_index[depot_id]
        starts.extend([depot_index] * vehicles_per_depot)
        
    ortools_data["starts"] = starts
    ortools_data["ends"] = starts
    
    demands = [0] * len(all_ids)
    customers_df = data["customers"]
    for _, row in customers_df.iterrows():
        customer_id = row["customer_id"]
        idx = id_to_index[customer_id]
        demands[idx] = int(row["demand"])
        
    ortools_data["demands"] = demands
    
    matrix_int = []
    for row_id in all_ids:
        row_distances = []
        for col_id in all_ids:
            dist = distance_matrix.loc[row_id, col_id]
            row_distances.append(int(dist * 100))
        matrix_int.append(row_distances)
        
    ortools_data["distance_matrix"] = matrix_int
    ortools_data["index_to_id"] = {i: loc_id for loc_id, i in id_to_index.items()}
    
    print("Data successfully translated for OR-Tools!")
    return ortools_data


def solve_with_ortools(data, distance_matrix, time_limit_seconds=10):
    """Sets up the OR-Tools engine and searches for the optimal MDVRP solution."""
    ortools_data = create_ortools_data(data, distance_matrix)
    
    manager = pywrapcp.RoutingIndexManager(
        len(ortools_data["distance_matrix"]),
        ortools_data["num_vehicles"],
        ortools_data["starts"],
        ortools_data["ends"]
    )
    
    routing = pywrapcp.RoutingModel(manager)
    
    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return ortools_data["distance_matrix"][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
    
    def demand_callback(from_index):
        from_node = manager.IndexToNode(from_index)
        return ortools_data["demands"][from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0, 
        ortools_data["vehicle_capacities"], 
        True, 
        "Capacity"
    )
    
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
    search_parameters.time_limit.seconds = time_limit_seconds
    
    print(f"\nOptimization Engine Running... Giving it {time_limit_seconds} seconds to think.")
    solution = routing.SolveWithParameters(search_parameters)
    
    if solution:
        return extract_solution(ortools_data, manager, routing, solution)
    else:
        print("No solution found!")
        return None


def extract_solution(ortools_data, manager, routing, solution):
    """Translates the OR-Tools output back into readable Python dictionaries."""
    routes = []
    total_distance = 0
    
    for vehicle_id in range(ortools_data["num_vehicles"]):
        index = routing.Start(vehicle_id)
        route_distance = 0
        route_load = 0
        current_route = []
        
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            real_id = ortools_data["index_to_id"][node_index]
            current_route.append(real_id)
            route_load += ortools_data["demands"][node_index]
            
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(previous_index, index, vehicle_id)
            
        node_index = manager.IndexToNode(index)
        real_id = ortools_data["index_to_id"][node_index]
        current_route.append(real_id)
        
        route_distance = route_distance / 100.0
        
        if len(current_route) > 2: 
            routes.append({
                "vehicle_index": vehicle_id,
                "route": current_route,
                "load": route_load,
                "distance": route_distance
            })
            total_distance += route_distance
            
    return {
        "total_distance": total_distance,
        "routes": routes,
        "vehicles_used": len(routes)
    }