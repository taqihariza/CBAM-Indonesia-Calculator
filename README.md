# CBAM-Indonesia-Calculator
## Preview

![Illustrative CBAM cost by year](charts/cost_by_year_steel_7210.png)

Run the app locally with `streamlit run app.py`.

## Method and sources

Cost per tonne = (embedded emissions - benchmark x free allocation share left) x certificate price.

- Free allocation share: 97.5% in 2026 falling to 0% in 2034 (Directive 2003/87/EC Art. 10a(1a)).
- Default emissions: Indonesia CN 7210 base value of 8.25 tCO2/t plus a 10% mark-up in 2026, 20% in 2027, 30% from 2028 (IR (EU) 2025/2621).
- Benchmarks: IR (EU) 2025/2620 Annex, as used in IISD (2026).
- Only direct emissions are priced for steel.
- Validation: the calculator reproduces IISD's figure of about EUR 574/t for an Indonesian default in 2026 (see tests).

Limitations: two products (steel CN 7210 and aluminium CN 7601), cross-sectoral correction factor assumed 1.0, the verified-emissions figure is illustrative, and the carbon-price deduction for Indonesia's ETS is not modelled yet.

Source: IISD (2026), Navigating the EU Carbon Border Adjustment Mechanism: An exporter's technical guide.

## Products covered

- Steel: coated flat steel (CN 7210). Indonesia default 8.25 tCO2/t before mark-up. Benchmark 1.491 (blast furnace route assigned by default). Source: IISD (2026).
- Aluminium: unwrought aluminium (CN 7601). Indonesia default 1.70 tCO2/t before mark-up (single secondary source - to verify against IR (EU) 2025/2621 Annex I). Primary aluminium benchmark 1.423 and scrap-based benchmark 0.091 (Argus and Reuters reports of the EU benchmarks).

All inputs live in data/products.csv and data/routes.csv with a source for each row. The "verified" emissions values are illustrative examples and are not from Indonesian installations.

Finding: for primary aluminium the default is close to what a real smelter emits, because only direct emissions are priced, so verified data saves far less than for steel. Scrap-based producers gain the most.

![Illustrative CBAM cost, aluminium](charts/cost_by_year_aluminium_7601.png)

## Important caveats

- Coated steel (CN 7210) is a "complex good": verified figures also need verified data from the mills that supplied the steel it is made from, otherwise defaults apply for those inputs (IISD 2026). The verified lines are therefore a best case.
- The Indonesia default for steel (8.25 tCO2/t) is the highest among the countries IISD compares, which makes the default-versus-verified gap especially large.
- The EU price is held fixed in the charts. Forecasts for 2034 are EUR 150-200/tCO2 (IISD 2026), which would scale every line up.

## Carbon price deduction scenario

The app has a what-if slider for a carbon price paid in Indonesia. Deduction per tonne = price paid x embedded emissions, and the EU bill cannot go below zero (simplified from IISD 2026, Equation 1). The EU rules are still in draft, and Indonesia's ETS and carbon tax do not currently cover steel or aluminium, so the realistic setting today is zero. Exporters on default emissions can only claim a deduction through a Commission default carbon price, which does not exist yet for Indonesia.
