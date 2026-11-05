import pytest

from calculator import cbam_cost, cbam_cost_for_year, load_phase_in, phase_in_share


def test_full_phase_in_default_emissions():
    # 1,000 t x 10.7 tCO2/t x 100% x EUR 82 = EUR 877,400
    assert cbam_cost(1000, 10.7, 1.0, 82) == pytest.approx(877_400)


def test_2026_phase_in():
    assert cbam_cost(1000, 10.7, 0.025, 82) == pytest.approx(21_935)


def test_schedule_endpoints():
    assert phase_in_share(2026) == pytest.approx(0.025)
    assert phase_in_share(2030) == pytest.approx(0.485)
    assert phase_in_share(2034) == pytest.approx(1.0)


def test_schedule_never_decreases():
    values = [v for _, v in sorted(load_phase_in().items())]
    assert values == sorted(values)


def test_cost_for_year_2030():
    # 1,000 x 10.7 x 0.485 x 82 = 425,539
    assert cbam_cost_for_year(1000, 10.7, 2030, 82) == pytest.approx(425_539)


def test_year_outside_schedule_raises():
    with pytest.raises(ValueError):
        phase_in_share(2025)
