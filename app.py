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
    shipment_cost_with_deduction,
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

st.sidebar.header("What-if: carbon price paid in Indonesia")
paid = st.sidebar.slider(
    "Effective carbon price paid in Indonesia (EUR per tCO2)",
    0, 100, 0,
    help="Net of free allocation and rebates. Today Indonesia's ETS and carbon tax do not cover steel or aluminium, so the realistic setting is 0.",
)
apply_default = st.sidebar.checkbox(
    "Also give default-emissions exporters the deduction",
    value=False,
    help="Default-emissions exporters can only claim a deduction through a Commission 'default carbon price'. None exists yet for Indonesia, so this assumes one is published.",
)

default_bm = default_benchmark(product_id)
route_bm = float(route["benchmark"])

rows = []
for y in years:
    d = shipment_cost_with_deduction(
        tonnes, default_see(product_id, y), default_bm, y, eu_price, paid if apply_default else 0.0
    )
    v = shipment_cost_with_deduction(tonnes, verified_see, route_bm, y, eu_price, paid)
    domestic = tonnes * verified_see * paid
    rows.append(
        {
            "Year": y,
            "Default: EU bill (EUR)": d,
            "Verified: EU bill (EUR)": v,
            "Paid in Indonesia (EUR)": domestic,
            "Saving (EUR)": d - v,
        }
    )
df = pd.DataFrame(rows)

first, last = df.iloc[0], df.iloc[-1]
c1, c2 = st.columns(2)
c1.metric(f"Saving in {int(first['Year'])}", f"EUR {first['Saving (EUR)']:,.0f}")
c2.metric(f"Saving in {int(last['Year'])}", f"EUR {last['Saving (EUR)']:,.0f}")
c3, c4 = st.columns(2)
c3.metric(f"Verified route: paid to the EU in {int(last['Year'])}", f"EUR {last['Verified: EU bill (EUR)']:,.0f}")
c4.metric(f"Verified route: paid in Indonesia in {int(last['Year'])}", f"EUR {last['Paid in Indonesia (EUR)']:,.0f}")
st.caption(
    f"EU default emissions for Indonesia, {product['label']}: "
    f"{default_see(product_id, 2026):.3f} tCO2/t in 2026, {default_see(product_id, 2027):.3f} in 2027, "
    f"{default_see(product_id, 2028):.3f} from 2028 (mark-up included)."
)
if paid > 0:
    st.info(
        "Each euro paid in Indonesia comes off the EU bill, so the exporter's total stays the same "
        "until the EU bill reaches zero. The money simply goes to Indonesia instead of the EU. "
        "The EU rules for this deduction are still in draft."
    )

fig, ax = plt.subplots(figsize=(8, 4.5))
ax.plot(df["Year"], df["Default: EU bill (EUR)"] / 1000, marker="o", label="Default: EU bill")
ax.plot(df["Year"], df["Verified: EU bill (EUR)"] / 1000, marker="o", label="Verified: EU bill")
if paid > 0:
    total = (df["Verified: EU bill (EUR)"] + df["Paid in Indonesia (EUR)"]) / 1000
    ax.plot(df["Year"], total, linestyle="--", marker="o", label="Verified: EU bill + paid in Indonesia")
ax.set_xlabel("Year")
ax.set_ylabel("Cost (EUR thousands)")
ax.set_ylim(bottom=0)
ax.grid(alpha=0.3)
ax.legend()
st.pyplot(fig)

st.subheader("Year by year")
money = {c: "{:,.0f}" for c in df.columns if c != "Year"}
st.dataframe(df.style.format(money), hide_index=True)

st.subheader("Sources for these inputs")
st.caption(f"Product: {product['source']}")
st.caption(f"Route: {route['source']}")
