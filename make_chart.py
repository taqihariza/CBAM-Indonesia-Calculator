import matplotlib.pyplot as plt

from calculator import (
    default_benchmark,
    default_see,
    get_routes,
    load_products,
    load_schedule,
    shipment_cost,
)

TONNES = 1000
EU_PRICE = 82  # EUR per tCO2, assumed

products = load_products()
years = [int(y) for y in load_schedule().index]

for product_id, product in products.iterrows():
    plt.figure(figsize=(9, 5))
    default_costs = [
        shipment_cost(TONNES, default_see(product_id, y), default_benchmark(product_id), y, EU_PRICE) / 1000
        for y in years
    ]
    plt.plot(years, default_costs, marker="o", label="EU default emissions (with mark-up)")
    for _, route in get_routes(product_id).iterrows():
        costs = [
            shipment_cost(TONNES, route["example_see"], route["benchmark"], y, EU_PRICE) / 1000
            for y in years
        ]
        plt.plot(years, costs, marker="o", label=f"Verified: {route['route']} (illustrative)")
    plt.title(f"Illustrative CBAM cost of 1,000 t of {product['label']} from Indonesia")
    plt.xlabel("Year")
    plt.ylabel("Cost (EUR thousands)")
    plt.ylim(bottom=0)
    plt.legend()
    plt.grid(alpha=0.3)
    plt.figtext(
        0.01, 0.01,
        "Defaults: EU IR 2025/2621 (see README). Verified values are illustrative, not from Indonesian mills. EU price fixed at EUR 82/tCO2.",
        fontsize=7,
    )
    plt.tight_layout()
    path = f"charts/cost_by_year_{product_id}.png"
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"Saved {path}")
