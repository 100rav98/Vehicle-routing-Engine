def validate_data(data):
    """
    Validate the basic structure of parsed MDVRP data.
    """

    customers = data["customers"]
    depots = data["depots"]
    vehicles = data["vehicles"]

    # Check 1: customer count
    assert len(customers) == data["customer_count"], (
        "Customer count does not match the customer table."
    )

    # Check 2: depot count
    assert len(depots) == data["depot_count"], (
        "Depot count does not match the depot table."
    )

    # Check 3: vehicle count
    expected_vehicles = (
        data["depot_count"] * data["vehicles_per_depot"]
    )

    assert len(vehicles) == expected_vehicles, (
        "Vehicle count does not match depots × vehicles per depot."
    )

    # Check 4: customer IDs must be unique
    assert customers["customer_id"].is_unique, (
        "Customer IDs are not unique."
    )

    # Check 5: depot IDs must be unique
    assert depots["depot_id"].is_unique, (
        "Depot IDs are not unique."
    )

    # Check 6: vehicle IDs must be unique
    assert vehicles["vehicle_id"].is_unique, (
        "Vehicle IDs are not unique."
    )

    # Check 7: every vehicle must belong to a valid depot
    valid_depot_ids = set(depots["depot_id"])

    assert set(vehicles["depot_id"]).issubset(valid_depot_ids), (
        "At least one vehicle belongs to an invalid depot."
    )

    return True