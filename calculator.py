from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).parent / "data"


def load_schedule():
    """Free allocation share and default mark-up for each year."""
    return pd.read_csv(DATA_DIR / "schedule.csv").set_index("year")


def load_parameters():
    """Sourced inputs (default emissions, benchmarks) from data/parameters.csv."""
    df = pd.read_csv(DATA_DIR / "parameters.csv")
    return {k: float(v) for k, v in zip(df["parameter"], df["value"])}


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


def default_see(year):
    """EU default emissions for Indonesian CN 7210 steel, including the mark-up."""
    base = load_parameters()["indonesia_default_base"]
    return base * (1 + float(_row(year)["default_markup"]))


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
