from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).parent / "data"


def cbam_cost(tonnes, emissions_per_tonne, phase_in_share, eu_price):
    """Estimate CBAM certificate cost in EUR (simplified).

    tonnes: tonnes of product exported
    emissions_per_tonne: tCO2 emitted per tonne of product
    phase_in_share: share of emissions CBAM charges (0.025 in 2026, 1.0 in 2034)
    eu_price: EU carbon price in EUR per tCO2
    """
    return tonnes * emissions_per_tonne * phase_in_share * eu_price


def load_phase_in():
    """Read the year -> CBAM factor schedule from data/phase_in.csv."""
    df = pd.read_csv(DATA_DIR / "phase_in.csv")
    return dict(zip(df["year"], df["cbam_factor"]))


def phase_in_share(year):
    schedule = load_phase_in()
    if year not in schedule:
        raise ValueError(
            f"No phase-in value for {year}. Available: {min(schedule)}-{max(schedule)}"
        )
    return schedule[year]


def cbam_cost_for_year(tonnes, emissions_per_tonne, year, eu_price):
    """Same as cbam_cost, but looks up the phase-in share for the given year."""
    return cbam_cost(tonnes, emissions_per_tonne, phase_in_share(year), eu_price)
