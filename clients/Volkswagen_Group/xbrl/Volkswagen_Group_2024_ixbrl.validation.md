# XBRL/ESEF Validation Report

**File:** `clients/Volkswagen_Group/xbrl/Volkswagen_Group_2024_ixbrl.html`
**Status:** ✅ PASS
**Validated:** 2026-06-08T20:48:00.553976

## Checks (14)

✅ **XML well-formedness**
✅ **Root element** — html (XHTML)
✅ **Namespaces** — All 6 required namespaces declared with correct URIs
✅ **ix:hidden section**
✅ **XHTML body**
✅ **XBRL facts** — 12 hidden + 0 inline facts
✅ **Unit definitions** — 7 units: u_esrs_tCo2e=esrs:tCo2e, u_esrs_MWh=esrs:MWh, u_esrs_tCo2ePerEur=esrs:tCo2ePerEur, u_esrs_t=esrs:t, u_esrs_m3=esrs:m3, u_xbrli_pure=xbrli:pure, u_iso4217_EUR=iso4217:EUR
✅ **Context definitions** — 2 contexts: FY2024: lei:volkswagen-group-csrd-2024 [2023-01-01/2024-12-31]; FY2024_Instant: lei:volkswagen-group-csrd-2024 [2024-12-31 (instant)]
✅ **Entity identifier scheme** — Present on all contexts
✅ **Fact extraction** — Extracted 12 facts
✅ **EFRAG taxonomy mapping** — 12/12 concepts mapped to official taxonomy
✅ **Unit validation** — All facts have expected unit types
✅ **ESRS standard coverage** — Facts per standard: E1=6, E3=1, E5=1, G1=1, S1=3
✅ **Audit trail** — 12 entries generated

## Facts

| # | Concept | Value | Unit | EF Taxonomy | Standard |
|---|---------|-------|------|-------------|----------|
| 1 | esrs:GHGScope1Emissions | 1500000 | u_esrs_tCo2e | ✅ esrs-e1:Scope1GreenhouseGasEmissions | E1 |
| 2 | esrs:GHGScope2LocationBasedEmissions | 1000000 | u_esrs_tCo2e | ✅ esrs-e1:Scope2LocationBasedGreenhouseGasEmissions | E1 |
| 3 | esrs:GHGScope3Emissions | 396000000 | u_esrs_tCo2e | ✅ esrs-e1:Scope3GreenhouseGasEmissions | E1 |
| 4 | esrs:GHGTotalEmissions | 398500000 | u_esrs_tCo2e | ✅ esrs-e1:TotalGreenhouseGasEmissions | E1 |
| 5 | esrs:EnergyConsumptionTotal | 26000000 | u_esrs_MWh | ✅ esrs-e1:TotalEnergyConsumption | E1 |
| 6 | esrs:GHGIntensity | 0.058 | u_esrs_tCo2ePerEur | ✅ esrs-e1:GreenhouseGasEmissionsIntensity | E1 |
| 7 | esrs:WaterWithdrawalTotal | 37000000 | u_esrs_m3 | ✅ esrs-e3:WaterWithdrawalTotal | E3 |
| 8 | esrs:WasteGeneratedTotal | 1500000 | u_esrs_t | ✅ esrs-e5:WasteGeneratedTotal | E5 |
| 9 | esrs:RevenueTotal | 321913000000 | u_iso4217_EUR | ✅ esrs-g1:TotalRevenue | G1 |
| 10 | esrs:TotalEmployees | 672800 | u_xbrli_pure | ✅ esrs-s1:TotalNumberOfEmployees | S1 |
| 11 | esrs:GenderDiversityManagement | 0.18 | u_xbrli_pure | ✅ esrs-s1:GenderDiversityAtManagementLevel | S1 |
| 12 | esrs:InjuryRateRecordable | 2.1 | u_xbrli_pure | ✅ esrs-s1:RateOfRecordableWorkRelatedInjuries | S1 |

## Audit Trail

| Concept | Value | Standard | Confidence |
|---------|-------|----------|------------|
| esrs-e1:Scope1GreenhouseGasEmissions | 1500000 | E1 | 🟢 high |
| esrs-e1:Scope2LocationBasedGreenhouseGasEmissions | 1000000 | E1 | 🟢 high |
| esrs-e1:Scope3GreenhouseGasEmissions | 396000000 | E1 | 🟢 high |
| esrs-e1:TotalGreenhouseGasEmissions | 398500000 | E1 | 🟢 high |
| esrs-e1:TotalEnergyConsumption | 26000000 | E1 | 🟢 high |
| esrs-e1:GreenhouseGasEmissionsIntensity | 0.058 | E1 | 🟢 high |
| esrs-e3:WaterWithdrawalTotal | 37000000 | E3 | 🟢 high |
| esrs-e5:WasteGeneratedTotal | 1500000 | E5 | 🟢 high |
| esrs-g1:TotalRevenue | 321913000000 | G1 | 🟢 high |
| esrs-s1:TotalNumberOfEmployees | 672800 | S1 | 🟢 high |
| esrs-s1:GenderDiversityAtManagementLevel | 0.18 | S1 | 🟢 high |
| esrs-s1:RateOfRecordableWorkRelatedInjuries | 2.1 | S1 | 🟢 high |