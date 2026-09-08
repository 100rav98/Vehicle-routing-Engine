import pandas as pd

def solve_nearest_neighbor(data, distance_matrix):
    """
    A basic greedy heuristic (Nearest Neighbor) for the MDVRP.
    Adapted for Pandas DataFrame structures.
    """
    print("\n" + "="*50)
    print("INITIALIZING NEAREST NEIGHBOR BASELINE SOLVER")
    print("="*50)
    
    # 1. Extract rules directly from the top level
    num_vehicles = data["vehicles_per_depot"]
    
    # 2. Convert DataFrames to Dictionaries for fast routing lookups
    customers_df = data["customers"]
    customers_dict = customers_df.set_index("customer_id").to_dict(orient="index")
    
    depots_df = data["depots"]
    depots_dict = depots_df.set_index("depot_id").to_dict(orient="index")
    
    # Get capacity and duration limits from the first depot
    vehicle_capacity = depots_df["vehicle_capacity"].iloc[0]
    max_duration = depots_df["max_route_duration"].iloc[0]
    
    unvisited_customers = set(customers_dict.keys())
    routes = []
    total_distance = 0.0
    
    print(f"Total customers to route: {len(unvisited_customers)}")
    print(f"Vehicles per depot: {num_vehicles}")
    print(f"Vehicle capacity: {vehicle_capacity}")
    print(f"Max route duration: {max_duration}")
    
    # 3. Iterate through each depot
    for depot_id in depots_dict.keys():
        if not unvisited_customers:
            break
            
        # 4. Dispatch vehicles from the current depot
        for vehicle_id in range(num_vehicles):
            if not unvisited_customers:
                break
                
            current_route = [depot_id]
            current_load = 0
            current_duration = 0.0
            current_node = depot_id
            
            # 5. Build the route by finding the nearest valid customer
            while unvisited_customers:
                nearest_customer = None
                shortest_dist = float('inf')
                
                for customer_id in unvisited_customers:
                    # Note: using .loc because distance_matrix is a pandas DataFrame
                    dist_to_customer = distance_matrix.loc[current_node, customer_id]
                    demand = customers_dict[customer_id]["demand"]
                    service_time = customers_dict[customer_id]["service_duration"]
                    dist_back_to_depot = distance_matrix.loc[customer_id, depot_id]
                    
                    # Constraint Check A: Capacity
                    if current_load + demand > vehicle_capacity:
                        continue
                        
                    # Constraint Check B: Max Duration
                    if max_duration > 0:
                        proposed_duration = (current_duration + dist_to_customer + 
                                             service_time + dist_back_to_depot)
                        if proposed_duration > max_duration:
                            continue
                            
                    # If feasible and closest so far, save it
                    if dist_to_customer < shortest_dist:
                        shortest_dist = dist_to_customer
                        nearest_customer = customer_id
                        
                # If we couldn't find a valid customer, return to depot
                if nearest_customer is None:
                    break
                    
                # Make the move to the nearest customer
                current_route.append(nearest_customer)
                unvisited_customers.remove(nearest_customer)
                
                # Update trackers
                current_load += customers_dict[nearest_customer]["demand"]
                current_duration += shortest_dist + customers_dict[nearest_customer]["service_duration"]
                total_distance += shortest_dist
                current_node = nearest_customer
                
            # Vehicle is done. Drive back to the depot.
            dist_back = distance_matrix.loc[current_node, depot_id]
            total_distance += dist_back
            current_duration += dist_back
            current_route.append(depot_id)
            
            # Save route if it actually served someone
            if len(current_route) > 2:
                routes.append({
                    "depot": depot_id,
                    "vehicle": vehicle_id + 1,
                    "route": current_route,
                    "load": current_load,
                    "duration": current_duration
                })

    print(f"\nRouting Complete!")
    print(f"Total Routes used: {len(routes)}")
    print(f"Total Distance: {total_distance:.2f}")
    print(f"Unvisited Customers: {len(unvisited_customers)}")
    
    return {
        "total_distance": total_distance,
        "routes": routes,
        "unvisited_count": len(unvisited_customers)
    }