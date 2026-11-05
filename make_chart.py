import matplotlib.pyplot as plt

from calculator import default_see, load_parameters, load_schedule, shipment_cost

TONNES = 1000
EU_PRICE = 82  # EUR per tCO2, assumed

p = load_parameters()
years = [int(y) for y in load_schedule().index]
default_costs = [
    shipment_cost(TONNES, default_see(y), p["benchmark_bf_bof"], y, EU_PRICE) / 1000
    for y in years
]
verified_costs = [
    shipment_cost(TONNES, p["verified_see_scrap_eaf"], p["benchmark_scrap_eaf"], y, EU_PRICE) / 1000
    for y in years
]

plt.figure(figsize=(9, 5))
plt.plot(years, default_costs, marker="o", label="EU default emissions (with mark-up)")
plt.plot(years, verified_costs, marker="o", label="Verified scrap-based EAF (illustrative)")
plt.title("Illustrative CBAM cost of 1,000 t of coated steel (CN 7210) from Indonesia")
plt.xlabel("Year")
plt.ylabel("Cost (EUR thousands)")
plt.ylim(bottom=0)
plt.legend()
plt.grid(alpha=0.3)
plt.figtext(
    0.01, 0.01,
    "Defaults: IR 2025/2621 via IISD (2026). Verified value is an IISD example, not an Indonesian mill. EU price fixed at EUR 82/tCO2.",
    fontsize=7,
)
plt.tight_layout()
plt.savefig("charts/cost_by_year.png", dpi=150)
print("Saved charts/cost_by_year.png")
