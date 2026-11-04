def cbam_cost(tonnes, emissions_per_tonne, phase_in_share, eu_price):
    """Estimate CBAM certificate cost in EUR (simplified).

    tonnes: tonnes of product exported
    emissions_per_tonne: tCO2 emitted per tonne of product
    phase_in_share: share of emissions CBAM charges (0.025 in 2026, 1.0 in 2034)
    eu_price: EU carbon price in EUR per tCO2
    """
    return tonnes * emissions_per_tonne * phase_in_share * eu_price
