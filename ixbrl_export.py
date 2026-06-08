"""
CSRD iXBRL/ESEF Export Engine — generates Inline XBRL filings.

Produces iXBRL (Inline XBRL) HTML documents with embedded XBRL tags,
plus taxonomy schema and instance documents for ESMA ESEF compliance.

Architecture:
  iXBRLEngine
    ├── generate_ixbrl()       → Inline XBRL HTML document
    ├── generate_instance()     → XBRL instance XML
    └── generate_taxonomy_ref() → Reference to EFRAG ESRS taxonomy
"""

import json
import os
from datetime import datetime
from typing import Any, Optional

from xbrl_taxonomy import (
    ESRS_NS, ESRS_SCHEMA_LOCATION, ESRS_CONCEPTS, get_concept,
)

# ── Namespace strings used in XML/HTML ──
IX_NS = "http://www.xbrl.org/2013/inlineXBRL"
IX_NS_H = "http://www.w3.org/1999/xhtml"
XHTML_NS = "http://www.w3.org/1999/xhtml"
LINK_NS = "http://www.xbrl.org/2003/linkbase"


class iXBRLEngine:
    """Generate Inline XBRL (iXBRL) documents for ESEF-compliant CSRD filings."""

    def __init__(self, client_name: str, report_year: int, profile: dict[str, Any]):
        self.client_name = client_name
        self.report_year = report_year
        self.profile = profile
        self.entity_identifier = self._create_entity_id()
        self.period_end = f"{report_year}-12-31"
        self.period_start = f"{report_year - 1}-01-01"

    def _create_entity_id(self) -> str:
        """Create a stable entity identifier."""
        name_slug = self.client_name.lower().replace(" ", "-").replace("_", "-")
        return f"lei:{name_slug}-csrd-{self.report_year}"

    def _map_profile_to_facts(self) -> list[dict]:
        """Map company profile data to XBRL facts.

        Supports two profile formats:
        1. Legacy flat format (greenhouse_gas, energy, workforce, ...)
        2. New hierarchical format (esg_data.{scope1_emissions, ...})
        """
        facts = []
        p = self.profile

        # Helper: extract value from either flat or esg_data format
        def _val(flat_key: str, esg_key: str) -> float | None:
            """Try flat format first, then esg_data hierarchical format."""
            # Flat format - could be a number OR a dict {value: N, ...}
            val = p.get(flat_key, None)
            if val is not None:
                if isinstance(val, (int, float)):
                    return val
                if isinstance(val, dict):
                    return val.get("value", None)
            # esg_data format
            esg = p.get("esg_data", {})
            if esg_key in esg:
                item = esg[esg_key]
                if isinstance(item, dict):
                    return item.get("value", None)
                return item
            return None

        def _g(prefix: str, key: str) -> dict | None:
            """Get a sub-dict from either flat or esg_data format."""
            val = p.get(prefix, None)
            if isinstance(val, dict):
                return val
            esg = p.get("esg_data", {})
            if key in esg:
                item = esg[key]
                if isinstance(item, dict):
                    return {"value": item.get("value", 0)}
            return None

        # ── E1: Climate ──
        v = _val("scope1_emissions", "scope1_emissions")
        if v:
            facts.append({"concept": "GHGScope1Emissions", "value": v, "unit": "esrs:tCo2e", "decimals": 0})
        v = _val("scope2_emissions", "scope2_emissions")
        if v:
            facts.append({"concept": "GHGScope2LocationBasedEmissions", "value": v, "unit": "esrs:tCo2e", "decimals": 0})
        v = _val("scope3_emissions", "scope3_emissions")
        if v:
            facts.append({"concept": "GHGScope3Emissions", "value": v, "unit": "esrs:tCo2e", "decimals": 0})
        v = _val("greenhouse_gas_emissions", "greenhouse_gas_emissions")
        if v:
            facts.append({"concept": "GHGTotalEmissions", "value": v, "unit": "esrs:tCo2e", "decimals": 0})
        v = _val("energy_consumption", "energy_consumption")
        if v:
            facts.append({"concept": "EnergyConsumptionTotal", "value": v, "unit": "esrs:MWh", "decimals": 0})
        v = _val("ghg_intensity", "ghg_intensity")
        if v:
            facts.append({"concept": "GHGIntensity", "value": v, "unit": "esrs:tCo2ePerEur", "decimals": 4})

        # Legacy flat format fallback for E1
        ghg = p.get("greenhouse_gas", {})
        if isinstance(ghg, dict):
            if ghg.get("scope1_total"):
                facts.append({"concept": "GHGScope1Emissions", "value": ghg["scope1_total"], "unit": "esrs:tCo2e", "decimals": 0})
            if ghg.get("scope2_location_based"):
                facts.append({"concept": "GHGScope2LocationBasedEmissions", "value": ghg["scope2_location_based"], "unit": "esrs:tCo2e", "decimals": 0})
            if ghg.get("scope2_market_based"):
                facts.append({"concept": "GHGScope2MarketBasedEmissions", "value": ghg["scope2_market_based"], "unit": "esrs:tCo2e", "decimals": 0})
            if ghg.get("scope3_total_estimated"):
                facts.append({"concept": "GHGScope3Emissions", "value": ghg["scope3_total_estimated"], "unit": "esrs:tCo2e", "decimals": 0})
            if ghg.get("reduction_target_2030"):
                facts.append({"concept": "GHGReductionTarget2030", "value": ghg["reduction_target_2030"] / 100.0, "unit": "xbrli:pure", "decimals": 4})
            if ghg.get("carbon_price_internal"):
                facts.append({"concept": "InternalCarbonPrice", "value": ghg["carbon_price_internal"], "unit": "iso4217:EUR", "decimals": 2})

        energy = p.get("energy", {})
        if isinstance(energy, dict) and energy.get("total_generation_mwh"):
            facts.append({"concept": "EnergyConsumptionTotal", "value": energy["total_generation_mwh"], "unit": "esrs:MWh", "decimals": 0})

        # ── E2: Pollution ──
        v = _val("waste_total", "waste_total")
        if v:
            facts.append({"concept": "WasteGeneratedTotal", "value": v, "unit": "esrs:t", "decimals": 0})

        poll = p.get("pollution", {})
        if isinstance(poll, dict):
            if poll.get("nox_emissions"):
                facts.append({"concept": "NOxEmissions", "value": poll["nox_emissions"], "unit": "esrs:t", "decimals": 0})
            if poll.get("sox_emissions"):
                facts.append({"concept": "SOxEmissions", "value": poll["sox_emissions"], "unit": "esrs:t", "decimals": 0})
            if poll.get("pm10_emissions"):
                pm_total = (poll.get("pm10_emissions", 0) + poll.get("pm2_5_emissions", 0))
                facts.append({"concept": "ParticulateMatterEmissionsTotal", "value": pm_total, "unit": "esrs:t", "decimals": 0})
            if poll.get("hazardous_waste_generated"):
                facts.append({"concept": "HazardousWasteGenerated", "value": poll["hazardous_waste_generated"], "unit": "esrs:t", "decimals": 0})

        # ── E3: Water ──
        v = _val("water_withdrawal", "water_withdrawal")
        if v:
            facts.append({"concept": "WaterWithdrawalTotal", "value": v, "unit": "esrs:m3", "decimals": 0})

        water = p.get("water", {})
        if isinstance(water, dict):
            if water.get("total_withdrawal_m3"):
                facts.append({"concept": "WaterWithdrawalTotal", "value": water["total_withdrawal_m3"], "unit": "esrs:m3", "decimals": 0})
            if water.get("total_consumption_m3"):
                facts.append({"concept": "WaterConsumptionTotal", "value": water["total_consumption_m3"], "unit": "esrs:m3", "decimals": 0})
            if water.get("total_discharge_m3"):
                facts.append({"concept": "WaterDischargeTotal", "value": water["total_discharge_m3"], "unit": "esrs:m3", "decimals": 0})

        # ── E5: Circular Economy ──
        ce = p.get("circular_economy", {})
        if isinstance(ce, dict):
            if ce.get("waste_total_tonnes"):
                facts.append({"concept": "WasteGeneratedTotal", "value": ce["waste_total_tonnes"], "unit": "esrs:t", "decimals": 0})
            if ce.get("waste_diversion_rate_pct"):
                facts.append({"concept": "WasteDiversionRate", "value": ce["waste_diversion_rate_pct"] / 100.0, "unit": "xbrli:pure", "decimals": 4})

        # ── S1: Workforce ──
        emp = p.get("employees", 0)
        if emp:
            facts.append({"concept": "TotalEmployees", "value": emp, "unit": "xbrli:pure", "decimals": 0})

        v = _val("workforce_female_pct", "workforce_female_pct")
        if v:
            facts.append({"concept": "GenderDiversityManagement", "value": v / 100.0, "unit": "xbrli:pure", "decimals": 4})
        v = _val("workforce_injury_rate", "workforce_injury_rate")
        if v:
            facts.append({"concept": "InjuryRateRecordable", "value": v, "unit": "xbrli:pure", "decimals": 2})
        v = _val("workforce_fatalities", "workforce_fatalities")
        if v is not None:
            facts.append({"concept": "FatalitiesWorkRelated", "value": v, "unit": "xbrli:pure", "decimals": 0})

        wf = p.get("workforce", {})
        if isinstance(wf, dict):
            if wf.get("total_employees"):
                facts.append({"concept": "TotalEmployees", "value": wf["total_employees"], "unit": "xbrli:pure", "decimals": 0})
            if wf.get("injury_rate_per_100k_hours"):
                facts.append({"concept": "InjuryRateRecordable", "value": wf["injury_rate_per_100k_hours"], "unit": "xbrli:pure", "decimals": 2})
            if wf.get("fatalities") is not None:
                facts.append({"concept": "FatalitiesWorkRelated", "value": wf["fatalities"], "unit": "xbrli:pure", "decimals": 0})
            if wf.get("employee_turnover_pct"):
                facts.append({"concept": "EmployeeTurnoverRate", "value": wf["employee_turnover_pct"] / 100.0, "unit": "xbrli:pure", "decimals": 4})
            if wf.get("female_management_pct"):
                facts.append({"concept": "GenderDiversityManagement", "value": wf["female_management_pct"] / 100.0, "unit": "xbrli:pure", "decimals": 4})
            if wf.get("gender_pay_gap_mean_pct"):
                facts.append({"concept": "GenderPayGapMean", "value": wf["gender_pay_gap_mean_pct"] / 100.0, "unit": "xbrli:pure", "decimals": 4})

        # ── G1: Business Conduct ──
        rev = p.get("revenue", 0)
        if rev:
            facts.append({"concept": "RevenueTotal", "value": rev, "unit": "iso4217:EUR", "decimals": 0})

        bc = p.get("business_conduct", {})
        if isinstance(bc, dict):
            if bc.get("corruption_convictions") is not None:
                facts.append({"concept": "CorruptionConvictions", "value": bc["corruption_convictions"], "unit": "xbrli:pure", "decimals": 0})
            if bc.get("corruption_fines_eur"):
                facts.append({"concept": "CorruptionFines", "value": bc["corruption_fines_eur"], "unit": "iso4217:EUR", "decimals": 2})
            if bc.get("lobbying_expenditure_eur"):
                facts.append({"concept": "LobbyingExpenditure", "value": bc["lobbying_expenditure_eur"], "unit": "iso4217:EUR", "decimals": 2})
        if bc.get("average_payment_days"):
            facts.append({
                "concept": "AveragePaymentDays",
                "value": bc["average_payment_days"],
                "unit": "xbrli:pure",
                "decimals": 0,
            })

        return facts

    def _build_html_body(self, facts: list[dict]) -> str:
        """Build the iXBRL HTML body with tagged facts."""
        lines = [
            "<body>",
            f"  <h1>CSRD Sustainability Report — {self.client_name} (FY{self.report_year})</h1>",
            "",
        ]

        # ── Header section ──
        lines.extend([
            "  <h2>Entity Information</h2>",
            "  <table>",
            f"    <tr><td>Entity</td><td>{self.client_name}</td></tr>",
            f"    <tr><td>Reporting period</td><td>{self.period_start} to {self.period_end}</td></tr>",
            f"    <tr><td>Entity identifier</td><td>{self.entity_identifier}</td></tr>",
            "  </table>",
            "",
        ])

        # ── Group facts by standard ──
        std_labels = {
            "GHG": "E1 — Climate Change",
            "NOx": "E2 — Pollution",
            "SOx": "E2 — Pollution",
            "Particulate": "E2 — Pollution",
            "Hazardous": "E2 — Pollution",
            "Water": "E3 — Water &amp; Marine Resources",
            "Waste": "E5 — Resource Use &amp; Circular Economy",
            "TotalEmployees": "S1 — Own Workforce",
            "Injury": "S1 — Own Workforce",
            "Fatalities": "S1 — Own Workforce",
            "EmployeeTurnover": "S1 — Own Workforce",
            "Gender": "S1 — Own Workforce",
            "Corruption": "G1 — Business Conduct",
            "Lobbying": "G1 — Business Conduct",
            "AveragePayment": "G1 — Business Conduct",
            "InternalCarbon": "E1 — Climate Change",
            "GHGReduction": "E1 — Climate Change",
            "Energy": "E1 — Climate Change",
            "Transition": "E1 — Climate Change",
        }

        def _concept_std(concept: str) -> str:
            for prefix, label in std_labels.items():
                if concept.startswith(prefix):
                    return label
            return "Other"

        # Group and emit
        grouped = {}
        for fact in facts:
            std = _concept_std(fact["concept"])
            if std not in grouped:
                grouped[std] = []
            grouped[std].append(fact)

        for std_name in sorted(grouped.keys()):
            std_facts = grouped[std_name]
            lines.append(f"  <h2>{std_name}</h2>")
            lines.append("  <table border='1'>")
            lines.append("    <tr><th>Concept</th><th>Value</th><th>Unit</th></tr>")

            for fact in std_facts:
                concept_def = get_concept(fact["concept"])
                if concept_def:
                    concept_name = concept_def.get("name", fact["concept"])
                    label = concept_def.get("label", fact["concept"])
                else:
                    concept_name = fact["concept"]
                    label = fact["concept"]

                value_str = str(fact["value"])
                unit_str = fact["unit"].split(":")[-1] if ":" in fact["unit"] else fact["unit"]

                # iXBRL tag — use nonFraction for numeric facts, nonNumeric for text
                is_numeric = fact.get("unit") in ("iso4217:EUR",) or unit_str != "pure"
                if is_numeric:
                    ix_tag = (
                        f'<ix:nonFraction name="esrs:{concept_name}" '
                        f'contextRef="FY{self.report_year}" '
                        f'unitRef="u_{fact["unit"]}" '
                        f'decimals="{fact.get("decimals", 2)}" '
                        f'format="ixt:numdotdecimal">'
                        f'{value_str}'
                        f'</ix:nonFraction>'
                    )
                else:
                    # xbrli:pure or no unit — still use nonFraction with unitRef
                    unit_ref = f'u_{fact["unit"]}' if fact.get("unit") else "u_xbrli:pure"
                    ix_tag = (
                        f'<ix:nonFraction name="esrs:{concept_name}" '
                        f'contextRef="FY{self.report_year}" '
                        f'unitRef="{unit_ref}" '
                        f'decimals="{fact.get("decimals", 0)}">'
                        f'{value_str}'
                        f'</ix:nonFraction>'
                    )

                lines.append(f"    <tr><td>{label}</td><td>{ix_tag}</td><td>{unit_str}</td></tr>")

            lines.append("  </table>")
            lines.append("")

        lines.append("</body>")
        return "\n".join(lines)

    def _build_contexts(self) -> list[tuple[str, str, str]]:
        """Build XBRL context definitions (id, start_date, end_date)."""
        return [
            (f"FY{self.report_year}", self.period_start, self.period_end),
            (f"FY{self.report_year}_Instant", self.period_end, self.period_end),
        ]

    def _build_units(self, facts: list[dict]) -> dict:
        """Build unique unit references from facts."""
        units = {}
        for fact in facts:
            u = fact["unit"]
            if u in units:
                continue
            if u == "iso4217:EUR":
                units[u] = (
                    f'<xbrli:unit id="u_{u}">'
                    f'<xbrli:measure>iso4217:EUR</xbrli:measure>'
                    f'</xbrli:unit>'
                )
            elif u.startswith("esrs:"):
                units[u] = (
                    f'<xbrli:unit id="u_{u}">'
                    f'<xbrli:measure>{u}</xbrli:measure>'
                    f'</xbrli:unit>'
                )
            else:
                units[u] = (
                    f'<xbrli:unit id="u_{u}">'
                    f'<xbrli:measure>xbrli:pure</xbrli:measure>'
                    f'</xbrli:unit>'
                )
        return units

    def generate_ixbrl(self) -> str:
        """Generate complete Inline XBRL HTML document."""
        facts = self._map_profile_to_facts()

        # Build contexts
        contexts_xml = ""
        for ctx_id, start, end in self._build_contexts():
            if start == end:
                contexts_xml += (
                    f'<xbrli:context id="{ctx_id}">'
                    f'<xbrli:entity><xbrli:identifier scheme="http://www.lei.org">{self.entity_identifier}</xbrli:identifier></xbrli:entity>'
                    f'<xbrli:period><xbrli:instant>{end}</xbrli:instant></xbrli:period>'
                    f'</xbrli:context>\n    '
                )
            else:
                contexts_xml += (
                    f'<xbrli:context id="{ctx_id}">'
                    f'<xbrli:entity><xbrli:identifier scheme="http://www.lei.org">{self.entity_identifier}</xbrli:identifier></xbrli:entity>'
                    f'<xbrli:period><xbrli:startDate>{start}</xbrli:startDate><xbrli:endDate>{end}</xbrli:endDate></xbrli:period>'
                    f'</xbrli:context>\n    '
                )

        # Build units
        units_dict = self._build_units(facts)
        units_xml = "".join(units_dict.values())

        # Build body
        body_html = self._build_html_body(facts)

        # Assemble full iXBRL document
        ixbrl = f'''<?xml version="1.0" encoding="UTF-8"?>
<html xmlns="{XHTML_NS}"
      xmlns:ix="{IX_NS}"
      xmlns:esrs="{ESRS_NS['esrs']}"
      xmlns:xbrli="{ESRS_NS['xbrli']}"
      xmlns:iso4217="{ESRS_NS['iso4217']}"
      xmlns:xlink="{ESRS_NS['xlink']}"
      xmlns:ixt="http://www.xbrl.org/inlineXBRL/transformation/2020-02-12">
  <head>
    <title>CSRD Sustainability Report — {self.client_name} (FY{self.report_year})</title>
  </head>
  <ix:hidden>
    <xbrli:xbrl>
      {contexts_xml}
      {units_xml}
    </xbrli:xbrl>
  </ix:hidden>
{body_html}
</html>
'''
        return ixbrl

    def generate_instance(self) -> str:
        """Generate standalone XBRL instance document."""
        facts = self._map_profile_to_facts()

        contexts_xml = ""
        for ctx_id, start, end in self._build_contexts():
            if start == end:
                contexts_xml += (
                    f'<context id="{ctx_id}">'
                    f'<entity><identifier scheme="http://www.lei.org">{self.entity_identifier}</identifier></entity>'
                    f'<period><instant>{end}</instant></period>'
                    f'</context>\n  '
                )
            else:
                contexts_xml += (
                    f'<context id="{ctx_id}">'
                    f'<entity><identifier scheme="http://www.lei.org">{self.entity_identifier}</identifier></entity>'
                    f'<period><startDate>{start}</startDate><endDate>{end}</endDate></period>'
                    f'</context>\n  '
                )

        units_dict = self._build_units(facts)
        units_xml = "".join(units_dict.values())

        facts_xml = ""
        for fact in facts:
            concept_def = get_concept(fact["concept"])
            name = concept_def.get("name", fact["concept"]) if concept_def else fact["concept"]
            decimals = fact.get("decimals", 0)

            if fact.get("unit") in ("iso4217:EUR", "xbrli:pure"):
                facts_xml += (
                    f'  <esrs:{name} contextRef="FY{self.report_year}" '
                    f'unitRef="u_{fact["unit"]}" decimals="{decimals}">'
                    f'{fact["value"]}</esrs:{name}>\n'
                )
            else:
                facts_xml += (
                    f'  <esrs:{name} contextRef="FY{self.report_year}" '
                    f'unitRef="u_{fact["unit"]}" decimals="{decimals}">'
                    f'{fact["value"]}</esrs:{name}>\n'
                )

        instance = f'''<?xml version="1.0" encoding="UTF-8"?>
<xbrl
    xmlns="http://www.xbrl.org/2003/instance"
    xmlns:esrs="{ESRS_NS['esrs']}"
    xmlns:iso4217="{ESRS_NS['iso4217']}"
    xmlns:link="http://www.xbrl.org/2003/linkbase"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:xbrli="http://www.xbrl.org/2003/instance">
  <link:schemaRef
    xlink:type="simple"
    xlink:href="{ESRS_SCHEMA_LOCATION}"/>
  {contexts_xml}
  {units_xml}
{facts_xml}
</xbrl>
'''
        return instance

    def export_to_dir(self, output_dir: str) -> dict[str, Any]:
        """Generate all iXBRL export files and save to directory."""
        os.makedirs(output_dir, exist_ok=True)

        ixbrl_content = self.generate_ixbrl()
        instance_content = self.generate_instance()

        # Write files
        ixbrl_path = f"{output_dir}/{self.client_name}_{self.report_year}_ixbrl.html"
        with open(ixbrl_path, "w") as f:
            f.write(ixbrl_content)

        instance_path = f"{output_dir}/{self.client_name}_{self.report_year}_instance.xml"
        with open(instance_path, "w") as f:
            f.write(instance_content)

        fact_count = len(self._map_profile_to_facts())

        return {
            "ixbrl_path": ixbrl_path,
            "instance_path": instance_path,
            "fact_count": fact_count,
            "summary": (
                f"Generated iXBRL ({fact_count} tagged facts) and XBRL instance "
                f"for {self.client_name} FY{self.report_year}"
            ),
        }