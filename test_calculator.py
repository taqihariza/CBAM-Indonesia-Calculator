import pytest

from calculator import (
    cost_per_tonne,
    default_see,
    free_allocation_share,
    load_parameters,
    load_schedule,
    shipment_cost,
)


def test_default_see_includes_markup():
    assert default_see(2026) == pytest.approx(9.075)
    assert default_see(2027) == pytest.approx(9.9)
    assert default_see(2028) == pytest.approx(10.725)
    assert default_see(2034) == pytest.approx(10.725)


def test_reproduces_iisd_default_example():
    # IISD 2026, section 4.3: about EUR 86,890 per 1,000 t (Vietnam, CN 7210)
    assert cost_per_tonne(2.607, 1.491, 0.975, 75.36) == pytest.approx(86.89, rel=0.001)


def test_reproduces_iisd_scrap_eaf_example():
    # IISD 2026, Table 2: about EUR 39 per tonne
    assert cost_per_tonne(0.62, 0.1118, 0.975, 75.36) == pytest.approx(38.5, rel=0.01)


def test_indonesia_default_2026_matches_iisd():
    # IISD reports about EUR 574 per tonne at the Q2 2026 price of EUR 75.28
    p = load_parameters()
    cost = cost_per_tonne(
        default_see(2026), p["benchmark_bf_bof"], free_allocation_share(2026), 75.28
    )
    assert cost == pytest.approx(574, rel=0.005)


def test_no_free_allocation_in_2034():
    p = load_parameters()
    cost = shipment_cost(1000, default_see(2034), p["benchmark_bf_bof"], 2034, 100)
    assert cost == pytest.approx(1_072_500)


def test_cost_never_negative():
    assert cost_per_tonne(0.05, 1.0, 0.975, 80) == 0


def test_free_allocation_never_increases():
    values = list(load_schedule().sort_index()["free_allocation_share"])
    assert values == sorted(values, reverse=True)


def test_year_outside_schedule_raises():
    with pytest.raises(ValueError):
        free_allocation_share(2025)
