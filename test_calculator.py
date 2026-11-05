import pytest

from calculator import (
    cost_per_tonne,
    default_benchmark,
    default_see,
    free_allocation_share,
    get_route,
    get_routes,
    load_products,
    load_schedule,
    shipment_cost,
)


def test_steel_default_see_includes_markup():
    assert default_see("steel_7210", 2026) == pytest.approx(9.075)
    assert default_see("steel_7210", 2027) == pytest.approx(9.9)
    assert default_see("steel_7210", 2028) == pytest.approx(10.725)
    assert default_see("steel_7210", 2034) == pytest.approx(10.725)


def test_aluminium_default_see_includes_markup():
    assert default_see("aluminium_7601", 2026) == pytest.approx(1.87)
    assert default_see("aluminium_7601", 2027) == pytest.approx(2.04)
    assert default_see("aluminium_7601", 2028) == pytest.approx(2.21)


def test_reproduces_iisd_default_example():
    # IISD 2026, section 4.3: about EUR 86,890 per 1,000 t (Vietnam, CN 7210)
    assert cost_per_tonne(2.607, 1.491, 0.975, 75.36) == pytest.approx(86.89, rel=0.001)


def test_reproduces_iisd_scrap_eaf_example():
    # IISD 2026, Table 2: about EUR 39 per tonne
    assert cost_per_tonne(0.62, 0.1118, 0.975, 75.36) == pytest.approx(38.5, rel=0.01)


def test_indonesia_steel_default_2026_matches_iisd():
    # IISD reports about EUR 574 per tonne at the Q2 2026 price of EUR 75.28
    cost = cost_per_tonne(
        default_see("steel_7210", 2026),
        default_benchmark("steel_7210"),
        free_allocation_share(2026),
        75.28,
    )
    assert cost == pytest.approx(574, rel=0.005)


def test_no_free_allocation_in_2034():
    cost = shipment_cost(
        1000, default_see("steel_7210", 2034), default_benchmark("steel_7210"), 2034, 100
    )
    assert cost == pytest.approx(1_072_500)


def test_aluminium_default_cost_2026():
    # (1.87 - 1.423 x 0.975) x 82 = about EUR 39.57 per tonne
    cost = cost_per_tonne(
        default_see("aluminium_7601", 2026),
        default_benchmark("aluminium_7601"),
        free_allocation_share(2026),
        82,
    )
    assert cost == pytest.approx(39.57, rel=0.001)


def test_primary_aluminium_saving_2034():
    route = get_route("aluminium_7601", "Primary smelter")
    share = free_allocation_share(2034)
    d = cost_per_tonne(
        default_see("aluminium_7601", 2034), default_benchmark("aluminium_7601"), share, 82
    )
    v = cost_per_tonne(route["example_see"], route["benchmark"], share, 82)
    assert d - v == pytest.approx(45.92, rel=0.01)


def test_every_product_has_routes():
    for product_id in load_products().index:
        assert len(get_routes(product_id)) >= 1


def test_cost_never_negative():
    assert cost_per_tonne(0.05, 1.0, 0.975, 80) == 0


def test_free_allocation_never_increases():
    values = list(load_schedule().sort_index()["free_allocation_share"])
    assert values == sorted(values, reverse=True)


def test_year_outside_schedule_raises():
    with pytest.raises(ValueError):
        free_allocation_share(2025)


def test_unknown_product_raises():
    with pytest.raises(ValueError):
        default_see("not_a_product", 2026)
