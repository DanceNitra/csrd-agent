# XBRL/ESEF Validation Report

**File:** `clients/ACS_Energy/xbrl/ACS_Energy_2024_ixbrl.html`
**Status:** ✅ PASS
**Validated:** 2026-06-08T19:50:36.056987

## Checks (14)

✅ **XML well-formedness**
✅ **Root element** — html (XHTML)
✅ **Namespaces** — All 6 required namespaces declared with correct URIs
✅ **ix:hidden section**
✅ **XHTML body**
✅ **XBRL facts** — 27 hidden + 0 inline facts
✅ **Unit definitions** — 6 units: u_esrs:tCo2e=esrs:tCo2e, u_xbrli:pure=xbrli:pure, u_iso4217:EUR=iso4217:EUR, u_esrs:MWh=esrs:MWh, u_esrs:t=esrs:t, u_esrs:m3=esrs:m3
✅ **Context definitions** — 2 contexts: FY2024: lei:acs-energy-csrd-2024 [2023-01-01/2024-12-31]; FY2024_Instant: lei:acs-energy-csrd-2024 [2024-12-31 (instant)]
✅ **Entity identifier scheme** — Present on all contexts
✅ **Fact extraction** — Extracted 27 facts
✅ **EFRAG taxonomy mapping** — 27/27 concepts mapped to official taxonomy
✅ **Unit validation** — All facts have expected unit types
✅ **ESRS standard coverage** — Facts per standard: E1=7, E2=4, E3=3, E5=2, G1=4, S1=7
✅ **Audit trail** — 27 entries generated

## Facts

| # | Concept | Value | Unit | EF Taxonomy | Standard |
|---|---------|-------|------|-------------|----------|
| 1 | esrs:GHGScope1Emissions | 2450000 | u_esrs:tCo2e | ✅ esrs-e1:Scope1GreenhouseGasEmissions | E1 |
| 2 | esrs:GHGScope2LocationBasedEmissions | 85000 | u_esrs:tCo2e | ✅ esrs-e1:Scope2LocationBasedGreenhouseGasEmissions | E1 |
| 3 | esrs:GHGScope2MarketBasedEmissions | 32000 | u_esrs:tCo2e | ✅ esrs-e1:Scope2MarketBasedGreenhouseGasEmissions | E1 |
| 4 | esrs:GHGScope3Emissions | 890000 | u_esrs:tCo2e | ✅ esrs-e1:Scope3GreenhouseGasEmissions | E1 |
| 5 | esrs:GHGReductionTarget2030 | 0.55 | u_xbrli:pure | ✅ esrs-e1:GHGReductionTarget | E1 |
| 6 | esrs:InternalCarbonPrice | 85 | u_iso4217:EUR | ✅ esrs-e1:InternalCarbonPrice | E1 |
| 7 | esrs:EnergyConsumptionTotal | 8200000 | u_esrs:MWh | ✅ esrs-e1:TotalEnergyConsumption | E1 |
| 8 | esrs:NOxEmissions | 4200 | u_esrs:t | ✅ esrs-e2:NitrogenOxidesEmissions | E2 |
| 9 | esrs:SOxEmissions | 1800 | u_esrs:t | ✅ esrs-e2:SulphurDioxideEmissions | E2 |
| 10 | esrs:ParticulateMatterEmissionsTotal | 415 | u_esrs:t | ✅ esrs-e2:ParticulateMatterEmissions | E2 |
| 11 | esrs:HazardousWasteGenerated | 4200 | u_esrs:t | ✅ esrs-e2:HazardousWasteGenerated | E2 |
| 12 | esrs:WaterWithdrawalTotal | 42500000 | u_esrs:m3 | ✅ esrs-e3:WaterWithdrawalTotal | E3 |
| 13 | esrs:WaterConsumptionTotal | 8750000 | u_esrs:m3 | ✅ esrs-e3:WaterConsumptionTotal | E3 |
| 14 | esrs:WaterDischargeTotal | 33750000 | u_esrs:m3 | ✅ esrs-e3:WaterDischargeTotal | E3 |
| 15 | esrs:WasteGeneratedTotal | 28500 | u_esrs:t | ✅ esrs-e5:WasteGeneratedTotal | E5 |
| 16 | esrs:WasteDiversionRate | 0.54 | u_xbrli:pure | ✅ esrs-e5:WasteDiversionRate | E5 |
| 17 | esrs:CorruptionConvictions | 0 | u_xbrli:pure | ✅ esrs-g1:NumberOfConvictionsForCorruptionAndBribery | G1 |
| 18 | esrs:LobbyingExpenditure | 45000 | u_iso4217:EUR | ✅ esrs-g1:LobbyingExpenditure | G1 |
| 19 | esrs:AveragePaymentDays | 28 | u_xbrli:pure | ✅ esrs-g1:AveragePaymentDays | G1 |
| 20 | esrs:RevenueTotal | 1200000000 | u_iso4217:EUR | ✅ esrs-g1:TotalRevenue | G1 |
| 21 | esrs:TotalEmployees | 5000 | u_xbrli:pure | ✅ esrs-s1:TotalNumberOfEmployees | S1 |
| 22 | esrs:TotalEmployees | 5000 | u_xbrli:pure | ✅ esrs-s1:TotalNumberOfEmployees | S1 |
| 23 | esrs:InjuryRateRecordable | 1.8 | u_xbrli:pure | ✅ esrs-s1:RateOfRecordableWorkRelatedInjuries | S1 |
| 24 | esrs:FatalitiesWorkRelated | 0 | u_xbrli:pure | ✅ esrs-s1:NumberOfFatalitiesWorkRelated | S1 |
| 25 | esrs:EmployeeTurnoverRate | 0.085 | u_xbrli:pure | ✅ esrs-s1:EmployeeTurnoverRate | S1 |
| 26 | esrs:GenderDiversityManagement | 0.18 | u_xbrli:pure | ✅ esrs-s1:GenderDiversityAtManagementLevel | S1 |
| 27 | esrs:GenderPayGapMean | 0.125 | u_xbrli:pure | ✅ esrs-s1:MeanGenderPayGap | S1 |

## Audit Trail

| Concept | Value | Standard | Confidence |
|---------|-------|----------|------------|
| esrs-e1:Scope1GreenhouseGasEmissions | 2450000 | E1 | 🟢 high |
| esrs-e1:Scope2LocationBasedGreenhouseGasEmissions | 85000 | E1 | 🟢 high |
| esrs-e1:Scope2MarketBasedGreenhouseGasEmissions | 32000 | E1 | 🟢 high |
| esrs-e1:Scope3GreenhouseGasEmissions | 890000 | E1 | 🟢 high |
| esrs-e1:GHGReductionTarget | 0.55 | E1 | 🟢 high |
| esrs-e1:InternalCarbonPrice | 85 | E1 | 🟢 high |
| esrs-e1:TotalEnergyConsumption | 8200000 | E1 | 🟢 high |
| esrs-e2:NitrogenOxidesEmissions | 4200 | E2 | 🟢 high |
| esrs-e2:SulphurDioxideEmissions | 1800 | E2 | 🟢 high |
| esrs-e2:ParticulateMatterEmissions | 415 | E2 | 🟢 high |
| esrs-e2:HazardousWasteGenerated | 4200 | E2 | 🟢 high |
| esrs-e3:WaterWithdrawalTotal | 42500000 | E3 | 🟢 high |
| esrs-e3:WaterConsumptionTotal | 8750000 | E3 | 🟢 high |
| esrs-e3:WaterDischargeTotal | 33750000 | E3 | 🟢 high |
| esrs-e5:WasteGeneratedTotal | 28500 | E5 | 🟢 high |
| esrs-e5:WasteDiversionRate | 0.54 | E5 | 🟢 high |
| esrs-g1:NumberOfConvictionsForCorruptionAndBribery | 0 | G1 | 🟢 high |
| esrs-g1:LobbyingExpenditure | 45000 | G1 | 🟢 high |
| esrs-g1:AveragePaymentDays | 28 | G1 | 🟢 high |
| esrs-g1:TotalRevenue | 1200000000 | G1 | 🟢 high |
| esrs-s1:TotalNumberOfEmployees | 5000 | S1 | 🟢 high |
| esrs-s1:TotalNumberOfEmployees | 5000 | S1 | 🟢 high |
| esrs-s1:RateOfRecordableWorkRelatedInjuries | 1.8 | S1 | 🟢 high |
| esrs-s1:NumberOfFatalitiesWorkRelated | 0 | S1 | 🟢 high |
| esrs-s1:EmployeeTurnoverRate | 0.085 | S1 | 🟢 high |
| esrs-s1:GenderDiversityAtManagementLevel | 0.18 | S1 | 🟢 high |
| esrs-s1:MeanGenderPayGap | 0.125 | S1 | 🟢 high |