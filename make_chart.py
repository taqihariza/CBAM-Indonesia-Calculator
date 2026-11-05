import matplotlib.pyplot as plt

from calculator import cbam_cost_for_year, load_phase_in

# Illustrative inputs, to be replaced with sourced values later
TONNES = 1000
EU_PRICE = 82              # EUR per tCO2
DEFAULT_EMISSIONS = 10.7   # tCO2 per tonne of steel (EU default, illustrative)
VERIFIED_EMISSIONS = 0.5   # tCO2 per tonne of steel (verified, illustrative)

years = sorted(load_phase_in())
default_costs = [cbam_cost_for_year(TONNES, DEFAULT_EMISSIONS, y, EU_PRICE) / 1000 for y in years]
verified_costs = [cbam_cost_for_year(TONNES, VERIFIED_EMISSIONS, y, EU_PRICE) / 1000 for y in years]

plt.figure(figsize=(9, 5))
plt.plot(years, default_costs, marker="o", label="Default emissions (10.7 tCO2/t)")
plt.plot(years, verified_costs, marker="o", label="Verified emissions (0.5 tCO2/t)")
plt.title("Illustrative CBAM cost of 1,000 t of steel exported to the EU")
plt.xlabel("Year")
plt.ylabel("Cost (EUR thousands)")
plt.legend()
plt.grid(alpha=0.3)
plt.figtext(0.01, 0.01, "Illustrative inputs. EU price fixed at EUR 82/tCO2. Simplified formula.", fontsize=8)
plt.tight_layout()
plt.savefig("charts/cost_by_year.png", dpi=150)
print("Saved charts/cost_by_year.png")
