# XBRL/ESEF Validation Report

**File:** `clients/TotalEnergies/xbrl/TotalEnergies_2024_ixbrl.html`
**Status:** ✅ PASS
**Validated:** 2026-06-08T20:48:00.552823

## Checks (14)

✅ **XML well-formedness**
✅ **Root element** — html (XHTML)
✅ **Namespaces** — All 6 required namespaces declared with correct URIs
✅ **ix:hidden section**
✅ **XHTML body**
✅ **XBRL facts** — 11 hidden + 0 inline facts
✅ **Unit definitions** — 6 units: u_esrs_tCo2e=esrs:tCo2e, u_esrs_tCo2ePerEur=esrs:tCo2ePerEur, u_esrs_t=esrs:t, u_esrs_m3=esrs:m3, u_xbrli_pure=xbrli:pure, u_iso4217_EUR=iso4217:EUR
✅ **Context definitions** — 2 contexts: FY2024: lei:totalenergies-csrd-2024 [2023-01-01/2024-12-31]; FY2024_Instant: lei:totalenergies-csrd-2024 [2024-12-31 (instant)]
✅ **Entity identifier scheme** — Present on all contexts
✅ **Fact extraction** — Extracted 11 facts
✅ **EFRAG taxonomy mapping** — 11/11 concepts mapped to official taxonomy
✅ **Unit validation** — All facts have expected unit types
✅ **ESRS standard coverage** — Facts per standard: E1=5, E3=1, E5=1, G1=1, S1=3
✅ **Audit trail** — 11 entries generated

## Facts

| # | Concept | Value | Unit | EF Taxonomy | Standard |
|---|---------|-------|------|-------------|----------|
| 1 | esrs:GHGScope1Emissions | 36000000 | u_esrs_tCo2e | ✅ esrs-e1:Scope1GreenhouseGasEmissions | E1 |
| 2 | esrs:GHGScope2LocationBasedEmissions | 2000000 | u_esrs_tCo2e | ✅ esrs-e1:Scope2LocationBasedGreenhouseGasEmissions | E1 |
| 3 | esrs:GHGScope3Emissions | 370000000 | u_esrs_tCo2e | ✅ esrs-e1:Scope3GreenhouseGasEmissions | E1 |
| 4 | esrs:GHGTotalEmissions | 408000000 | u_esrs_tCo2e | ✅ esrs-e1:TotalGreenhouseGasEmissions | E1 |
| 5 | esrs:GHGIntensity | 0.19 | u_esrs_tCo2ePerEur | ✅ esrs-e1:GreenhouseGasEmissionsIntensity | E1 |
| 6 | esrs:WaterWithdrawalTotal | 200000000 | u_esrs_m3 | ✅ esrs-e3:WaterWithdrawalTotal | E3 |
| 7 | esrs:WasteGeneratedTotal | 900000 | u_esrs_t | ✅ esrs-e5:WasteGeneratedTotal | E5 |
| 8 | esrs:RevenueTotal | 201196000000 | u_iso4217_EUR | ✅ esrs-g1:TotalRevenue | G1 |
| 9 | esrs:TotalEmployees | 101513 | u_xbrli_pure | ✅ esrs-s1:TotalNumberOfEmployees | S1 |
| 10 | esrs:GenderDiversityManagement | 0.28 | u_xbrli_pure | ✅ esrs-s1:GenderDiversityAtManagementLevel | S1 |
| 11 | esrs:FatalitiesWorkRelated | 3 | u_xbrli_pure | ✅ esrs-s1:NumberOfFatalitiesWorkRelated | S1 |

## Audit Trail

| Concept | Value | Standard | Confidence |
|---------|-------|----------|------------|
| esrs-e1:Scope1GreenhouseGasEmissions | 36000000 | E1 | 🟢 high |
| esrs-e1:Scope2LocationBasedGreenhouseGasEmissions | 2000000 | E1 | 🟢 high |
| esrs-e1:Scope3GreenhouseGasEmissions | 370000000 | E1 | 🟢 high |
| esrs-e1:TotalGreenhouseGasEmissions | 408000000 | E1 | 🟢 high |
| esrs-e1:GreenhouseGasEmissionsIntensity | 0.19 | E1 | 🟢 high |
| esrs-e3:WaterWithdrawalTotal | 200000000 | E3 | 🟢 high |
| esrs-e5:WasteGeneratedTotal | 900000 | E5 | 🟢 high |
| esrs-g1:TotalRevenue | 201196000000 | G1 | 🟢 high |
| esrs-s1:TotalNumberOfEmployees | 101513 | S1 | 🟢 high |
| esrs-s1:GenderDiversityAtManagementLevel | 0.28 | S1 | 🟢 high |
| esrs-s1:NumberOfFatalitiesWorkRelated | 3 | S1 | 🟢 high |