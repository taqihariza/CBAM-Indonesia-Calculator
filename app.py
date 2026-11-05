import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from calculator import (
    default_benchmark,
    default_see,
    get_product,
    get_route,
    get_routes,
    load_products,
    load_schedule,
    shipment_cost,
)

st.set_page_config(page_title="CBAM Indonesia Calculator")
st.title("CBAM cost calculator for Indonesian exports")
st.caption(
    "Illustrative estimates for research and learning. Not legal or financial advice. "
    "Method and sources are in the README."
)

products = load_products()
years = [int(y) for y in load_schedule().index]

st.sidebar.header("Inputs")
product_id = st.sidebar.selectbox(
    "Product", list(products.index), format_func=lambda pid: products.loc[pid, "label"]
)
product = get_product(product_id)
routes = get_routes(product_id)
route_name = st.sidebar.selectbox("Production route behind the verified data", list(routes["route"]))
route = get_route(product_id, route_name)

tonnes = st.sidebar.number_input("Tonnes exported", min_value=1, value=1000, step=100)
verified_see = st.sidebar.number_input(
    "Verified emissions (tCO2 per tonne)",
    min_value=0.0,
    value=float(route["example_see"]),
    step=0.05,
    key=f"see_{product_id}_{route_name}",
    help="The default is an illustrative example, not an Indonesian installation. Enter your own verified value.",
)
eu_price = st.sidebar.slider("EU carbon price (EUR per tCO2)", 30, 200, 82)

rows = []
for y in years:
    d = shipment_cost(tonnes, default_see(product_id, y), default_benchmark(product_id), y, eu_price)
    v = shipment_cost(tonnes, verified_see, float(route["benchmark"]), y, eu_price)
    rows.append({"Year": y, "Default (EUR)": d, "Verified (EUR)": v, "Saving (EUR)": d - v})
df = pd.DataFrame(rows)

first, last = df.iloc[0], df.iloc[-1]
c1, c2 = st.columns(2)
c1.metric(f"Saving in {int(first['Year'])}", f"EUR {first['Saving (EUR)']:,.0f}")
c2.metric(f"Saving in {int(last['Year'])}", f"EUR {last['Saving (EUR)']:,.0f}")
st.caption(
    f"EU default emissions for Indonesia, {product['label']}: "
    f"{default_see(product_id, 2026):.3f} tCO2/t in 2026, {default_see(product_id, 2027):.3f} in 2027, "
    f"{default_see(product_id, 2028):.3f} from 2028 (mark-up included)."
)

fig, ax = plt.subplots(figsize=(8, 4.5))
ax.plot(df["Year"], df["Default (EUR)"] / 1000, marker="o", label="EU default emissions")
ax.plot(df["Year"], df["Verified (EUR)"] / 1000, marker="o", label="Verified emissions")
ax.set_xlabel("Year")
ax.set_ylabel("Cost (EUR thousands)")
ax.set_ylim(bottom=0)
ax.grid(alpha=0.3)
ax.legend()
st.pyplot(fig)

st.subheader("Year by year")
st.dataframe(
    df.style.format(
        {"Default (EUR)": "{:,.0f}", "Verified (EUR)": "{:,.0f}", "Saving (EUR)": "{:,.0f}"}
    ),
    hide_index=True,
)

st.subheader("Sources for these inputs")
st.caption(f"Product: {product['source']}")
st.caption(f"Route: {route['source']}")
