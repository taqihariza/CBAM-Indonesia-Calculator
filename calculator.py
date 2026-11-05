from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).parent / "data"


def load_schedule():
    """Free allocation share and default mark-up for each year."""
    return pd.read_csv(DATA_DIR / "schedule.csv").set_index("year")


def load_products():
    """One row per product: Indonesia default, default benchmark, source."""
    return pd.read_csv(DATA_DIR / "products.csv").set_index("product_id")


def load_routes():
    """One row per verified production route: benchmark and example emissions."""
    return pd.read_csv(DATA_DIR / "routes.csv")


def _row(year):
    schedule = load_schedule()
    if year not in schedule.index:
        raise ValueError(
            f"No schedule for {year}. Available: {schedule.index.min()}-{schedule.index.max()}"
        )
    return schedule.loc[year]


def free_allocation_share(year):
    """Share of free allocation still in place (the regulation's 'CBAM factor')."""
    return float(_row(year)["free_allocation_share"])


def get_product(product_id):
    products = load_products()
    if product_id not in products.index:
        raise ValueError(f"Unknown product {product_id}. Available: {list(products.index)}")
    return products.loc[product_id]


def default_see(product_id, year):
    """EU default emissions for Indonesia, including the mark-up for that year."""
    base = float(get_product(product_id)["default_base"])
    return base * (1 + float(_row(year)["default_markup"]))


def default_benchmark(product_id):
    return float(get_product(product_id)["default_benchmark"])


def get_routes(product_id):
    routes = load_routes()
    return routes[routes["product_id"] == product_id].reset_index(drop=True)


def get_route(product_id, route_name):
    routes = get_routes(product_id)
    match = routes[routes["route"] == route_name]
    if match.empty:
        raise ValueError(f"Unknown route {route_name} for {product_id}")
    return match.iloc[0]


def cost_per_tonne(see, benchmark, share, eu_price, cscf=1.0):
    """CBAM cost in EUR per tonne of product.

    see: embedded emissions (tCO2 per tonne of product)
    benchmark: EU benchmark for the product route (tCO2 per tonne)
    share: free allocation share left that year (0.975 in 2026, 0 in 2034)
    eu_price: CBAM certificate price (EUR per tCO2)
    cscf: cross-sectoral correction factor (1.0 = no reduction)
    """
    free_allocation = benchmark * share * cscf
    return max(see - free_allocation, 0.0) * eu_price


def shipment_cost(tonnes, see, benchmark, year, eu_price):
    """Total CBAM cost in EUR for a shipment in a given year."""
    return tonnes * cost_per_tonne(see, benchmark, free_allocation_share(year), eu_price)
