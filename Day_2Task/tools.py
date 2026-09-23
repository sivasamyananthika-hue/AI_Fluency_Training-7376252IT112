# tools.py

def get_route_fare(route_code):
    """
    Mock external tool for retrieving the current fare
    for a travel route.
    """

    fares = {
        "CHN-BLR": 850,
        "BLR-MYS": 500,
        "CHN-MYS": 1200
    }

    if route_code in fares:
        return fares[route_code]

    return "Route not found"


if __name__ == "__main__":
    print(get_route_fare("CHN-BLR"))