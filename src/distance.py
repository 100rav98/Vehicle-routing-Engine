import math
import pandas as pd


def euclidean_distance(x1, y1, x2, y2):
    """
    Calculate the Euclidean distance between two points.

    Parameters
    ----------
    x1, y1 : float
        Coordinates of the first point.

    x2, y2 : float
        Coordinates of the second point.

    Returns
    -------
    float
        Euclidean distance between the two points.
    """

    return math.sqrt(
        (x2 - x1) ** 2 +
        (y2 - y1) ** 2
    )


def create_locations_table(data):
    """
    Combine customer and depot coordinates into one locations table.

    Parameters
    ----------
    data : dict
        Parsed Cordeau MDVRP data returned by parse_cordeau_mdvrp().

    Returns
    -------
    pandas.DataFrame
        DataFrame containing:
        - location_id
        - location_type
        - x
        - y
    """

    customers = data["customers"]
    depots = data["depots"]

    # Create customer locations
    customer_locations = customers[
        ["customer_id", "x", "y"]
    ].copy()

    customer_locations = customer_locations.rename(
        columns={
            "customer_id": "location_id"
        }
    )

    customer_locations["location_type"] = "customer"

    # Create depot locations
    depot_locations = depots[
        ["depot_id", "x", "y"]
    ].copy()

    depot_locations = depot_locations.rename(
        columns={
            "depot_id": "location_id"
        }
    )

    depot_locations["location_type"] = "depot"

    # Combine customers and depots
    locations = pd.concat(
        [
            depot_locations,
            customer_locations
        ],
        ignore_index=True
    )

    # Arrange columns in a clean order
    locations = locations[
        [
            "location_id",
            "location_type",
            "x",
            "y"
        ]
    ]

    return locations


def build_distance_matrix(locations):
    """
    Build a complete pairwise Euclidean distance matrix.

    Parameters
    ----------
    locations : pandas.DataFrame
        Location table containing:
        - location_id
        - x
        - y

    Returns
    -------
    pandas.DataFrame
        Square distance matrix.
    """

    location_ids = locations["location_id"].tolist()

    distance_matrix = pd.DataFrame(
        0.0,
        index=location_ids,
        columns=location_ids
    )

    for i in range(len(locations)):

        location_i = locations.iloc[i]

        for j in range(len(locations)):

            location_j = locations.iloc[j]

            distance = euclidean_distance(
                location_i["x"],
                location_i["y"],
                location_j["x"],
                location_j["y"]
            )

            distance_matrix.loc[
                location_i["location_id"],
                location_j["location_id"]
            ] = distance

    return distance_matrix


def create_distance_matrix(data):
    """
    Create the complete distance matrix directly from
    parsed Cordeau MDVRP data.

    Parameters
    ----------
    data : dict
        Parsed benchmark data.

    Returns
    -------
    tuple
        locations, distance_matrix
    """

    locations = create_locations_table(data)

    distance_matrix = build_distance_matrix(locations)

    return locations, distance_matrix