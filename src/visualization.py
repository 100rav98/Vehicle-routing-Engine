import matplotlib.pyplot as plt

def plot_solution(data, solution, title="Vehicle Routing Solution"):
    """
    Draws a map of the depots, customers, and the routes taken by the vehicles.
    """
    if not solution or "routes" not in solution:
        print("No valid solution to plot!")
        return

    # 1. Set up the canvas
    plt.figure(figsize=(10, 8))
    plt.title(f"{title}\nTotal Distance: {solution['total_distance']:.2f}", fontsize=14, fontweight="bold")
    
    # 2. Extract coordinates from the parsed data DataFrames
    customers_df = data["customers"]
    depots_df = data["depots"]
    
    # 3. Plot Customers (Small blue dots)
    plt.scatter(
        customers_df["x"], 
        customers_df["y"], 
        c='blue', 
        label='Customers', 
        s=30, 
        alpha=0.6,
        zorder=2
    )
    
    # 4. Plot Depots (Large red squares)
    plt.scatter(
        depots_df["x"], 
        depots_df["y"], 
        c='red', 
        marker='s', 
        label='Depots', 
        s=100,
        edgecolors='black',
        zorder=3
    )

    # 5. Draw the routes (colored lines)
    # FIX: Using the updated modern Matplotlib command for colors
    cmap = plt.get_cmap("tab20", len(solution["routes"]))
    
    # Create fast-lookup dictionaries for coordinates
    cust_coords = customers_df.set_index("customer_id")[["x", "y"]].to_dict("index")
    depot_coords = depots_df.set_index("depot_id")[["x", "y"]].to_dict("index")
    
    for i, route_info in enumerate(solution["routes"]):
        route = route_info["route"]
        route_x = []
        route_y = []
        
        for node_id in route:
            # Check if it's a depot or a customer to get the right coordinates
            if node_id in depot_coords:
                route_x.append(depot_coords[node_id]["x"])
                route_y.append(depot_coords[node_id]["y"])
            else:
                route_x.append(cust_coords[node_id]["x"])
                route_y.append(cust_coords[node_id]["y"])
                
        # Draw the line for this specific truck
        plt.plot(route_x, route_y, color=cmap(i), linewidth=2, alpha=0.7, zorder=1)

    # 6. Final visual touches
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    
    # Show the map on the screen!
    return plt.gcf()