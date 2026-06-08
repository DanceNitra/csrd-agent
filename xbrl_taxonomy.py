"""
ESRS XBRL Taxonomy — simplified concept definitions for iXBRL/ESEF export.

Maps ESRS datapoints to XBRL concepts based on the official EFRAG ESRS
XBRL Taxonomy (publicly available at https://xbrl.efrag.org).

This is a simplified subset covering the most common mandatory datapoints.
For production use, download the full EFRAG taxonomy package.
"""

# ── ESRS Namespaces ──
ESRS_NS = {
    "esrs": "http://xbrl.efrag.org/sites/esrs/2024-12-16/esrs-cor",
    "iso4217": "http://www.xbrl.org/2003/iso4217",
    "xbrli": "http://www.xbrl.org/2003/instance",
    "xlink": "http://www.w3.org/1999/xlink",
    "link": "http://www.xbrl.org/2003/linkbase",
    "ix": "http://www.xbrl.org/2013/inlineXBRL",
    "ixt": "http://www.xbrl.org/inlineXBRL/transformation/2020-02-12",
    "xbrldi": "http://xbrl.org/2006/xbrldi",
}

ESRS_SCHEMA_LOCATION = (
    "https://xbrl.efrag.org/sites/esrs/2024-12-16/esrs-cor/esrs-cor-2024-12-16.xsd"
)

# ── ESRS Concept Definitions ──
# Each concept: (name, type, period_type, balance, prefix, label)
# Types: xbrli:monetaryItemType, xbrli:decimalItemType, xbrli:booleanItemType,
#        xbrli:stringItemType, xbrli:dateItemType, esrs:percentItemType,
#        esrs:areaItemType, esrs:energyItemType, esrs:massItemType
# Period types: instant, duration
# Balance (for monetary): debit, credit

ESRS_CONCEPTS = {
    # ── E1 Climate ──
    "E1-1_01_TransitionPlan": {
        "name": "TransitionPlanClimateMitigation",
        "type": "xbrli:booleanItemType",
        "period_type": "instant",
        "label": "Existence of transition plan for climate change mitigation",
    },
    "E1-4_01_GHGReductionTarget": {
        "name": "GHGReductionTarget2030",
        "type": "esrs:percentItemType",
        "period_type": "duration",
        "label": "GHG emission reduction target (Scope 1, 2, 3) relative to base year",
    },
    "E1-6_01_Scope1Emissions": {
        "name": "GHGScope1Emissions",
        "type": "esrs:massItemType",
        "period_type": "duration",
        "label": "Gross Scope 1 GHG emissions (tCO2e)",
    },
    "E1-6_02_Scope2LocationEmissions": {
        "name": "GHGScope2LocationBasedEmissions",
        "type": "esrs:massItemType",
        "period_type": "duration",
        "label": "Gross Scope 2 GHG emissions - location-based (tCO2e)",
    },
    "E1-6_03_Scope2MarketEmissions": {
        "name": "GHGScope2MarketBasedEmissions",
        "type": "esrs:massItemType",
        "period_type": "duration",
        "label": "Gross Scope 2 GHG emissions - market-based (tCO2e)",
    },
    "E1-6_04_Scope3Emissions": {
        "name": "GHGScope3Emissions",
        "type": "esrs:massItemType",
        "period_type": "duration",
        "label": "Gross Scope 3 GHG emissions (tCO2e)",
    },
    "E1-5_01_EnergyConsumption": {
        "name": "EnergyConsumptionTotal",
        "type": "esrs:energyItemType",
        "period_type": "duration",
        "label": "Total energy consumption (MWh)",
    },
    "E1-5_02_RenewableEnergyShare": {
        "name": "RenewableEnergyShare",
        "type": "esrs:percentItemType",
        "period_type": "duration",
        "label": "Share of renewable energy in total consumption",
    },
    "E1-8_01_InternalCarbonPrice": {
        "name": "InternalCarbonPrice",
        "type": "xbrli:monetaryItemType",
        "period_type": "instant",
        "balance": "debit",
        "label": "Internal carbon price (EUR/tonne CO2e)",
    },

    # ── E2 Pollution ──
    "E2-4_01_NOxEmissions": {
        "name": "NOxEmissions",
        "type": "esrs:massItemType",
        "period_type": "duration",
        "label": "NOx emissions (tonnes)",
    },
    "E2-4_02_SOxEmissions": {
        "name": "SOxEmissions",
        "type": "esrs:massItemType",
        "period_type": "duration",
        "label": "SOx emissions (tonnes)",
    },
    "E2-4_03_PMEmissions": {
        "name": "ParticulateMatterEmissionsTotal",
        "type": "esrs:massItemType",
        "period_type": "duration",
        "label": "PM emissions (tonnes)",
    },
    "E2-4_04_HazardousWasteGenerated": {
        "name": "HazardousWasteGenerated",
        "type": "esrs:massItemType",
        "period_type": "duration",
        "label": "Hazardous waste generated (tonnes)",
    },

    # ── E3 Water ──
    "E3-4_01_WaterWithdrawal": {
        "name": "WaterWithdrawalTotal",
        "type": "esrs:waterVolumeItemType",
        "period_type": "duration",
        "label": "Total water withdrawn (m3)",
    },
    "E3-4_03_WaterConsumption": {
        "name": "WaterConsumptionTotal",
        "type": "esrs:waterVolumeItemType",
        "period_type": "duration",
        "label": "Total water consumption (m3)",
    },
    "E3-4_05_WaterDischarge": {
        "name": "WaterDischargeTotal",
        "type": "esrs:waterVolumeItemType",
        "period_type": "duration",
        "label": "Total water discharged (m3)",
    },

    # ── E5 Circular Economy ──
    "E5-5_01_WasteGenerated": {
        "name": "WasteGeneratedTotal",
        "type": "esrs:massItemType",
        "period_type": "duration",
        "label": "Total waste generated (tonnes)",
    },
    "E5-5_04_WasteDiversionRate": {
        "name": "WasteDiversionRate",
        "type": "esrs:percentItemType",
        "period_type": "duration",
        "label": "Waste diversion rate from disposal",
    },

    # ── S1 Workforce ──
    "S1-5_01_TotalEmployees": {
        "name": "TotalEmployees",
        "type": "xbrli:decimalItemType",
        "period_type": "instant",
        "label": "Total number of employees",
    },
    "S1-7_01_InjuryRate": {
        "name": "InjuryRateRecordable",
        "type": "esrs:rateItemType",
        "period_type": "duration",
        "label": "Rate of recordable workplace injuries",
    },
    "S1-7_02_Fatalities": {
        "name": "FatalitiesWorkRelated",
        "type": "xbrli:decimalItemType",
        "period_type": "duration",
        "label": "Number of work-related fatalities",
    },
    "S1-5_06_TurnoverRate": {
        "name": "EmployeeTurnoverRate",
        "type": "esrs:percentItemType",
        "period_type": "duration",
        "label": "Employee turnover rate",
    },
    "S1-9_02_GenderDiversityManagement": {
        "name": "GenderDiversityManagement",
        "type": "esrs:percentItemType",
        "period_type": "instant",
        "label": "Share of women in management positions",
    },
    "S1-9_03_GenderPayGap": {
        "name": "GenderPayGapMean",
        "type": "esrs:percentItemType",
        "period_type": "duration",
        "label": "Mean gender pay gap",
    },

    # ── G1 Business Conduct ──
    "G1-3_01_CorruptionConvictions": {
        "name": "CorruptionConvictions",
        "type": "xbrli:decimalItemType",
        "period_type": "duration",
        "label": "Number of corruption/bribery convictions",
    },
    "G1-3_02_CorruptionFines": {
        "name": "CorruptionFines",
        "type": "xbrli:monetaryItemType",
        "period_type": "duration",
        "balance": "debit",
        "label": "Fines paid for corruption/bribery violations",
    },
    "G1-4_03_LobbyingExpenditure": {
        "name": "LobbyingExpenditure",
        "type": "xbrli:monetaryItemType",
        "period_type": "duration",
        "balance": "debit",
        "label": "Total lobbying expenditure",
    },
    "G1-2_02_AveragePaymentDays": {
        "name": "AveragePaymentDays",
        "type": "xbrli:decimalItemType",
        "period_type": "duration",
        "label": "Average supplier payment time (days)",
    },
}


def get_concept(datapoint_name: str) -> dict | None:
    """Get XBRL concept definition for a datapoint name."""
    if datapoint_name in ESRS_CONCEPTS:
        return ESRS_CONCEPTS[datapoint_name]
    # Try prefix match
    for key, val in ESRS_CONCEPTS.items():
        if key.startswith(datapoint_name):
            return val
    return None


def list_concepts_by_standard(std_id: str) -> list[dict]:
    """List all XBRL concepts for a given ESRS standard."""
    prefix = f"{std_id}-"
    concepts = []
    for key, val in ESRS_CONCEPTS.items():
        if key.startswith(prefix):
            concepts.append({"datapoint": key, **val})
    return concepts


def get_concept_count() -> dict:
    """Get concept counts per standard."""
    counts = {}
    for key in ESRS_CONCEPTS:
        std = key.split("-")[0] if "-" in key else "other"
        counts[std] = counts.get(std, 0) + 1
    return counts