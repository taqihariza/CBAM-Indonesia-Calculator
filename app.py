import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from calculator import cbam_cost_for_year, load_phase_in

st.set_page_config(page_title="CBAM Indonesia Calculator")
st.title("CBAM cost calculator for Indonesian exports")
st.caption(
    "Illustrative estimates using a simplified formula and placeholder inputs. "
    "Not legal or financial advice."
)

st.sidebar.header("Inputs")
tonnes = st.sidebar.number_input("Tonnes exported", min_value=1, value=1000, step=100)
default_emissions = st.sidebar.number_input(
    "Default emissions (tCO2 per tonne)", min_value=0.0, value=10.7, step=0.1
)
verified_emissions = st.sidebar.number_input(
    "Verified emissions (tCO2 per tonne)", min_value=0.0, value=0.5, step=0.1
)
eu_price = st.sidebar.slider("EU carbon price (EUR per tCO2)", 30, 200, 82)

years = sorted(load_phase_in())
rows = []
for y in years:
    d = cbam_cost_for_year(tonnes, default_emissions, y, eu_price)
    v = cbam_cost_for_year(tonnes, verified_emissions, y, eu_price)
    rows.append({"Year": y, "Default (EUR)": d, "Verified (EUR)": v, "Saving (EUR)": d - v})
df = pd.DataFrame(rows)

last = df.iloc[-1]
st.metric(
    f"Saving from verified emissions in {int(last['Year'])}",
    f"EUR {last['Saving (EUR)']:,.0f}",
)

fig, ax = plt.subplots(figsize=(8, 4.5))
ax.plot(df["Year"], df["Default (EUR)"] / 1000, marker="o", label="Default emissions")
ax.plot(df["Year"], df["Verified (EUR)"] / 1000, marker="o", label="Verified emissions")
ax.set_xlabel("Year")
ax.set_ylabel("Cost (EUR thousands)")
ax.grid(alpha=0.3)
ax.legend()
st.pyplot(fig)

st.subheader("Year by year")
st.dataframe(
    df.style.format({"Default (EUR)": "{:,.0f}", "Verified (EUR)": "{:,.0f}", "Saving (EUR)": "{:,.0f}"}),
    hide_index=True,
)
