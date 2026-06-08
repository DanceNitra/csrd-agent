# XBRL/ESEF Validation Report

**File:** `clients/Iberdrola/xbrl/Iberdrola_2024_ixbrl.html`
**Status:** ✅ PASS
**Validated:** 2026-06-08T20:48:00.550217

## Checks (14)

✅ **XML well-formedness**
✅ **Root element** — html (XHTML)
✅ **Namespaces** — All 6 required namespaces declared with correct URIs
✅ **ix:hidden section**
✅ **XHTML body**
✅ **XBRL facts** — 12 hidden + 0 inline facts
✅ **Unit definitions** — 7 units: u_esrs_tCo2e=esrs:tCo2e, u_esrs_MWh=esrs:MWh, u_esrs_tCo2ePerEur=esrs:tCo2ePerEur, u_esrs_t=esrs:t, u_esrs_m3=esrs:m3, u_xbrli_pure=xbrli:pure, u_iso4217_EUR=iso4217:EUR
✅ **Context definitions** — 2 contexts: FY2024: lei:iberdrola-csrd-2024 [2023-01-01/2024-12-31]; FY2024_Instant: lei:iberdrola-csrd-2024 [2024-12-31 (instant)]
✅ **Entity identifier scheme** — Present on all contexts
✅ **Fact extraction** — Extracted 12 facts
✅ **EFRAG taxonomy mapping** — 12/12 concepts mapped to official taxonomy
✅ **Unit validation** — All facts have expected unit types
✅ **ESRS standard coverage** — Facts per standard: E1=6, E3=1, E5=1, G1=1, S1=3
✅ **Audit trail** — 12 entries generated

## Facts

| # | Concept | Value | Unit | EF Taxonomy | Standard |
|---|---------|-------|------|-------------|----------|
| 1 | esrs:GHGScope1Emissions | 22000000 | u_esrs_tCo2e | ✅ esrs-e1:Scope1GreenhouseGasEmissions | E1 |
| 2 | esrs:GHGScope2LocationBasedEmissions | 3000000 | u_esrs_tCo2e | ✅ esrs-e1:Scope2LocationBasedGreenhouseGasEmissions | E1 |
| 3 | esrs:GHGScope3Emissions | 15000000 | u_esrs_tCo2e | ✅ esrs-e1:Scope3GreenhouseGasEmissions | E1 |
| 4 | esrs:GHGTotalEmissions | 40000000 | u_esrs_tCo2e | ✅ esrs-e1:TotalGreenhouseGasEmissions | E1 |
| 5 | esrs:EnergyConsumptionTotal | 150000000 | u_esrs_MWh | ✅ esrs-e1:TotalEnergyConsumption | E1 |
| 6 | esrs:GHGIntensity | 0.46 | u_esrs_tCo2ePerEur | ✅ esrs-e1:GreenhouseGasEmissionsIntensity | E1 |
| 7 | esrs:WaterWithdrawalTotal | 300000000 | u_esrs_m3 | ✅ esrs-e3:WaterWithdrawalTotal | E3 |
| 8 | esrs:WasteGeneratedTotal | 80000 | u_esrs_t | ✅ esrs-e5:WasteGeneratedTotal | E5 |
| 9 | esrs:RevenueTotal | 53949000000 | u_iso4217_EUR | ✅ esrs-g1:TotalRevenue | G1 |
| 10 | esrs:TotalEmployees | 40721 | u_xbrli_pure | ✅ esrs-s1:TotalNumberOfEmployees | S1 |
| 11 | esrs:GenderDiversityManagement | 0.25 | u_xbrli_pure | ✅ esrs-s1:GenderDiversityAtManagementLevel | S1 |
| 12 | esrs:InjuryRateRecordable | 0.9 | u_xbrli_pure | ✅ esrs-s1:RateOfRecordableWorkRelatedInjuries | S1 |

## Audit Trail

| Concept | Value | Standard | Confidence |
|---------|-------|----------|------------|
| esrs-e1:Scope1GreenhouseGasEmissions | 22000000 | E1 | 🟢 high |
| esrs-e1:Scope2LocationBasedGreenhouseGasEmissions | 3000000 | E1 | 🟢 high |
| esrs-e1:Scope3GreenhouseGasEmissions | 15000000 | E1 | 🟢 high |
| esrs-e1:TotalGreenhouseGasEmissions | 40000000 | E1 | 🟢 high |
| esrs-e1:TotalEnergyConsumption | 150000000 | E1 | 🟢 high |
| esrs-e1:GreenhouseGasEmissionsIntensity | 0.46 | E1 | 🟢 high |
| esrs-e3:WaterWithdrawalTotal | 300000000 | E3 | 🟢 high |
| esrs-e5:WasteGeneratedTotal | 80000 | E5 | 🟢 high |
| esrs-g1:TotalRevenue | 53949000000 | G1 | 🟢 high |
| esrs-s1:TotalNumberOfEmployees | 40721 | S1 | 🟢 high |
| esrs-s1:GenderDiversityAtManagementLevel | 0.25 | S1 | 🟢 high |
| esrs-s1:RateOfRecordableWorkRelatedInjuries | 0.9 | S1 | 🟢 high |