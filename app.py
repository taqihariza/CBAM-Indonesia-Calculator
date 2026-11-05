import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from calculator import default_see, load_parameters, load_schedule, shipment_cost

params = load_parameters()
years = [int(y) for y in load_schedule().index]

st.set_page_config(page_title="CBAM Indonesia Calculator")
st.title("CBAM cost calculator: Indonesian coated steel (CN 7210)")
st.caption(
    "Illustrative estimates for research and learning. Not legal or financial advice. "
    "Method and sources are in the README."
)

st.sidebar.header("Inputs")
tonnes = st.sidebar.number_input("Tonnes exported", min_value=1, value=1000, step=100)
route = st.sidebar.selectbox(
    "Production route behind the verified data", ["Scrap-based EAF", "Blast furnace (BF-BOF)"]
)
verified_see = st.sidebar.number_input(
    "Verified emissions (tCO2 per tonne)",
    min_value=0.0,
    value=params["verified_see_scrap_eaf"],
    step=0.05,
    help="The default is an illustrative scrap-EAF figure from an IISD example, not an Indonesian mill. Enter your own verified value.",
)
eu_price = st.sidebar.slider("EU carbon price (EUR per tCO2)", 30, 200, 82)

verified_benchmark = (
    params["benchmark_scrap_eaf"] if route.startswith("Scrap") else params["benchmark_bf_bof"]
)

rows = []
for y in years:
    d = shipment_cost(tonnes, default_see(y), params["benchmark_bf_bof"], y, eu_price)
    v = shipment_cost(tonnes, verified_see, verified_benchmark, y, eu_price)
    rows.append({"Year": y, "Default (EUR)": d, "Verified (EUR)": v, "Saving (EUR)": d - v})
df = pd.DataFrame(rows)

first, last = df.iloc[0], df.iloc[-1]
c1, c2 = st.columns(2)
c1.metric(f"Saving in {int(first['Year'])}", f"EUR {first['Saving (EUR)']:,.0f}")
c2.metric(f"Saving in {int(last['Year'])}", f"EUR {last['Saving (EUR)']:,.0f}")
st.caption(
    f"EU default emissions for Indonesia: {default_see(2026):.3f} tCO2/t in 2026, "
    f"{default_see(2027):.3f} in 2027, {default_see(2028):.3f} from 2028 (mark-up included)."
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
