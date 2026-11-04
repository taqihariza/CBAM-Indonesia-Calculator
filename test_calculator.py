import pytest
from calculator import cbam_cost


def test_full_phase_in_default_emissions():
    # 1,000 t steel x 10.7 tCO2/t x 100% x EUR 82 = EUR 877,400
    assert cbam_cost(1000, 10.7, 1.0, 82) == pytest.approx(877_400)


def test_2026_phase_in():
    # Same shipment in 2026, when only 2.5% is charged
    assert cbam_cost(1000, 10.7, 0.025, 82) == pytest.approx(21_935)
