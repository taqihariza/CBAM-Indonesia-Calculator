import pytest

from calculator import (
    cost_per_tonne,
    cost_per_tonne_with_deduction,
    shipment_cost_with_deduction,
)


def test_zero_price_changes_nothing():
    base = cost_per_tonne(0.62, 0.1118, 0.975, 82)
    assert cost_per_tonne_with_deduction(0.62, 0.1118, 0.975, 82, 0) == pytest.approx(base)


def test_deduction_reduces_cost():
    # 0.62 tCO2/t x EUR 10 = EUR 6.2 per tonne off the EU bill
    base = cost_per_tonne(0.62, 0.1118, 0.975, 82)
    assert cost_per_tonne_with_deduction(0.62, 0.1118, 0.975, 82, 10) == pytest.approx(base - 6.2)


def test_deduction_cannot_make_cost_negative():
    assert cost_per_tonne_with_deduction(0.62, 0.1118, 0.975, 82, 500) == 0


def test_exporter_total_unchanged_until_bill_is_zero():
    base = cost_per_tonne(0.62, 0.1118, 0.975, 82)
    paid_at_home = 10 * 0.62
    eu_bill = cost_per_tonne_with_deduction(0.62, 0.1118, 0.975, 82, 10)
    assert paid_at_home + eu_bill == pytest.approx(base)


def test_shipment_version_matches_per_tonne():
    shipment = shipment_cost_with_deduction(1000, 0.62, 0.1118, 2026, 82, 10)
    per_tonne = cost_per_tonne_with_deduction(0.62, 0.1118, 0.975, 82, 10)
    assert shipment == pytest.approx(1000 * per_tonne)
