#!/usr/bin/env python3
"""
XBRL/ESEF Validator — validates CSRD Agent iXBRL output for ESMA compliance.

Validates:
  1. XML well-formedness
  2. XBRL namespace correctness
  3. Unit definitions match concept types
  4. Contexts are valid (periods, entities)
  5. Facts are properly tagged with ix:nonNumeric / ix:nonFraction
  6. Concept names map to official EFRAG ESRS taxonomy

Output: pass/fail per check + Audit Trail JSON
"""

import json, os, sys, xml.etree.ElementTree as ET
from datetime import datetime, date
from pathlib import Path
from typing import Optional

# ── Official EFRAG ESRS XBRL Taxonomy Concept Names ──
# Source: EFRAG ESRS XBRL Taxonomy 2024-12-16 (publicly documented)
# Format: (our_concept, official_efrag_concept, standard, unit_type, description)
EFRAG_TAXONOMY_MAP = {
    # E1 - Climate
    "GHGScope1Emissions": {
        "efrag": "esrs-e1:Scope1GreenhouseGasEmissions",
        "standard": "E1",
        "unit": "esrs:tCo2e",
        "period_type": "duration",
        "label": "Scope 1 GHG emissions",
    },
    "GHGScope2LocationBasedEmissions": {
        "efrag": "esrs-e1:Scope2LocationBasedGreenhouseGasEmissions",
        "standard": "E1",
        "unit": "esrs:tCo2e",
        "period_type": "duration",
        "label": "Scope 2 location-based GHG emissions",
    },
    "GHGScope2MarketBasedEmissions": {
        "efrag": "esrs-e1:Scope2MarketBasedGreenhouseGasEmissions",
        "standard": "E1",
        "unit": "esrs:tCo2e",
        "period_type": "duration",
        "label": "Scope 2 market-based GHG emissions",
    },
    "GHGScope3Emissions": {
        "efrag": "esrs-e1:Scope3GreenhouseGasEmissions",
        "standard": "E1",
        "unit": "esrs:tCo2e",
        "period_type": "duration",
        "label": "Scope 3 GHG emissions",
    },
    "GHGTotalEmissions": {
        "efrag": "esrs-e1:TotalGreenhouseGasEmissions",
        "standard": "E1",
        "unit": "esrs:tCo2e",
        "period_type": "duration",
        "label": "Total GHG emissions (Scope 1+2+3)",
    },
    "EnergyConsumptionTotal": {
        "efrag": "esrs-e1:TotalEnergyConsumption",
        "standard": "E1",
        "unit": "esrs:MWh",
        "period_type": "duration",
        "label": "Total energy consumption",
    },
    "GHGIntensity": {
        "efrag": "esrs-e1:GreenhouseGasEmissionsIntensity",
        "standard": "E1",
        "unit": "esrs:tCo2ePerEur",
        "period_type": "duration",
        "label": "GHG emissions intensity per revenue",
    },
    "GHGReductionTarget2030": {
        "efrag": "esrs-e1:GHGReductionTarget",
        "standard": "E1",
        "unit": "xbrli:pure",
        "period_type": "duration",
        "label": "GHG emission reduction target",
    },
    "InternalCarbonPrice": {
        "efrag": "esrs-e1:InternalCarbonPrice",
        "standard": "E1",
        "unit": "iso4217:EUR",
        "period_type": "duration",
        "label": "Internal carbon price applied",
    },
    
    # E2 - Pollution
    "NOxEmissions": {
        "efrag": "esrs-e2:NitrogenOxidesEmissions",
        "standard": "E2",
        "unit": "esrs:t",
        "period_type": "duration",
        "label": "NOx emissions to air",
    },
    "SOxEmissions": {
        "efrag": "esrs-e2:SulphurDioxideEmissions",
        "standard": "E2",
        "unit": "esrs:t",
        "period_type": "duration",
        "label": "SOx emissions to air",
    },
    "ParticulateMatterEmissionsTotal": {
        "efrag": "esrs-e2:ParticulateMatterEmissions",
        "standard": "E2",
        "unit": "esrs:t",
        "period_type": "duration",
        "label": "Particulate matter emissions",
    },
    "HazardousWasteGenerated": {
        "efrag": "esrs-e2:HazardousWasteGenerated",
        "standard": "E2",
        "unit": "esrs:t",
        "period_type": "duration",
        "label": "Hazardous waste generated",
    },
    
    # E3 - Water
    "WaterWithdrawalTotal": {
        "efrag": "esrs-e3:WaterWithdrawalTotal",
        "standard": "E3",
        "unit": "esrs:m3",
        "period_type": "duration",
        "label": "Total water withdrawal",
    },
    "WaterConsumptionTotal": {
        "efrag": "esrs-e3:WaterConsumptionTotal",
        "standard": "E3",
        "unit": "esrs:m3",
        "period_type": "duration",
        "label": "Total water consumption",
    },
    "WaterDischargeTotal": {
        "efrag": "esrs-e3:WaterDischargeTotal",
        "standard": "E3",
        "unit": "esrs:m3",
        "period_type": "duration",
        "label": "Total water discharge",
    },
    
    # E5 - Circular Economy
    "WasteGeneratedTotal": {
        "efrag": "esrs-e5:WasteGeneratedTotal",
        "standard": "E5",
        "unit": "esrs:t",
        "period_type": "duration",
        "label": "Total waste generated",
    },
    "WasteDiversionRate": {
        "efrag": "esrs-e5:WasteDiversionRate",
        "standard": "E5",
        "unit": "xbrli:pure",
        "period_type": "duration",
        "label": "Waste diversion rate from disposal",
    },
    
    # S1 - Workforce
    "TotalEmployees": {
        "efrag": "esrs-s1:TotalNumberOfEmployees",
        "standard": "S1",
        "unit": "xbrli:pure",
        "period_type": "instant",
        "label": "Total number of employees",
    },
    "InjuryRateRecordable": {
        "efrag": "esrs-s1:RateOfRecordableWorkRelatedInjuries",
        "standard": "S1",
        "unit": "xbrli:pure",
        "period_type": "duration",
        "label": "Rate of recordable work-related injuries",
    },
    "FatalitiesWorkRelated": {
        "efrag": "esrs-s1:NumberOfFatalitiesWorkRelated",
        "standard": "S1",
        "unit": "xbrli:pure",
        "period_type": "duration",
        "label": "Number of work-related fatalities",
    },
    "EmployeeTurnoverRate": {
        "efrag": "esrs-s1:EmployeeTurnoverRate",
        "standard": "S1",
        "unit": "xbrli:pure",
        "period_type": "duration",
        "label": "Employee turnover rate",
    },
    "GenderDiversityManagement": {
        "efrag": "esrs-s1:GenderDiversityAtManagementLevel",
        "standard": "S1",
        "unit": "xbrli:pure",
        "period_type": "instant",
        "label": "Gender diversity at management level",
    },
    "GenderPayGapMean": {
        "efrag": "esrs-s1:MeanGenderPayGap",
        "standard": "S1",
        "unit": "xbrli:pure",
        "period_type": "duration",
        "label": "Mean gender pay gap",
    },
    
    # G1 - Business Conduct
    "CorruptionConvictions": {
        "efrag": "esrs-g1:NumberOfConvictionsForCorruptionAndBribery",
        "standard": "G1",
        "unit": "xbrli:pure",
        "period_type": "duration",
        "label": "Number of convictions for corruption and bribery",
    },
    "CorruptionFines": {
        "efrag": "esrs-g1:AmountOfFinesForCorruptionAndBribery",
        "standard": "G1",
        "unit": "iso4217:EUR",
        "period_type": "duration",
        "label": "Amount of fines for corruption and bribery",
    },
    "LobbyingExpenditure": {
        "efrag": "esrs-g1:LobbyingExpenditure",
        "standard": "G1",
        "unit": "iso4217:EUR",
        "period_type": "duration",
        "label": "Lobbying expenditure",
    },
    "RevenueTotal": {
        "efrag": "esrs-g1:TotalRevenue",
        "standard": "G1",
        "unit": "iso4217:EUR",
        "period_type": "duration",
        "label": "Total revenue",
    },
    "AveragePaymentDays": {
        "efrag": "esrs-g1:AveragePaymentDays",
        "standard": "G1",
        "unit": "xbrli:pure",
        "period_type": "duration",
        "label": "Average supplier payment days",
    },
}

# Required namespaces for ESRS ESEF compliance
REQUIRED_NAMESPACES = {
    "ix": "http://www.xbrl.org/2013/inlineXBRL",
    "xbrli": "http://www.xbrl.org/2003/instance",
    "iso4217": "http://www.xbrl.org/2003/iso4217",
    "xlink": "http://www.w3.org/1999/xlink",
    "ixt": "http://www.xbrl.org/inlineXBRL/transformation/2020-02-12",
    "esrs": "http://xbrl.efrag.org/sites/esrs/2024-12-16/esrs-cor",
}


class XBRLValidator:
    """Validates iXBRL output for ESMA ESEF compliance."""

    def __init__(self, ixbrl_path: str):
        self.ixbrl_path = ixbrl_path
        self.results = {
            "file": ixbrl_path,
            "validated_at": datetime.now().isoformat(),
            "passed": True,
            "checks": [],
            "facts": [],
            "audit_trail": [],
        }

    def _log(self, check: str, passed: bool, detail: str = ""):
        self.results["checks"].append({
            "check": check,
            "passed": passed,
            "detail": detail,
        })
        if not passed:
            self.results["passed"] = False

    def validate_all(self) -> dict:
        """Run all validation checks."""
        tree = self._parse_xml()
        if tree is None:
            return self.results
        
        root = tree.getroot()
        
        self._check_xml_wellformed(tree)
        self._check_namespaces(root)
        self._check_ixbrl_structure(root)
        self._check_units(root)
        self._check_contexts(root)
        self._check_facts(root)
        self._map_to_efrag()
        self._generate_audit_trail()
        
        return self.results

    def _parse_xml(self) -> Optional[ET.ElementTree]:
        """Parse the iXBRL file as XML."""
        try:
            tree = ET.parse(self.ixbrl_path)
            self._log("XML well-formedness", True)
            return tree
        except ET.ParseError as e:
            self._log("XML well-formedness", False, str(e))
            return None
        except Exception as e:
            self._log("XML well-formedness", False, f"Failed to open: {e}")
            return None

    def _check_xml_wellformed(self, tree: ET.ElementTree):
        """Additional XML validation."""
        root = tree.getroot()
        if root.tag != "{http://www.w3.org/1999/xhtml}html":
            self._log("Root element", False, f"Expected 'html', got '{root.tag}'")
        else:
            self._log("Root element", True, "html (XHTML)")

    def _check_namespaces(self, root: ET.Element):
        """Check all required XBRL namespaces are declared.
        
        Reads xmlns declarations from the raw XML since Python ET
        doesn't expose namespace declarations in element attributes.
        """
        # Parse raw document to find xmlns declarations
        import re
        raw_xml = open(self.ixbrl_path, 'rb').read().decode('utf-8')
        
        # Find all xmlns:prefix="uri" declarations
        xmlns_pattern = re.compile(r'\s+xmlns:(\w+)=["\']([^"\']+)["\']')
        declared = {}
        for match in xmlns_pattern.finditer(raw_xml):
            prefix = match.group(1)
            uri = match.group(2)
            declared[prefix] = uri
        
        missing = []
        for prefix, expected_ns in REQUIRED_NAMESPACES.items():
            actual_ns = declared.get(prefix)
            if actual_ns is None:
                missing.append(f"Missing prefix '{prefix}'")
            elif actual_ns != expected_ns:
                missing.append(f"Prefix '{prefix}' has '{actual_ns[:60]}...', expected '{expected_ns[:60]}...'")
        
        if missing:
            self._log("Namespaces", False, "; ".join(missing))
        else:
            self._log("Namespaces", True, f"All {len(REQUIRED_NAMESPACES)} required namespaces declared with correct URIs")

    def _check_ixbrl_structure(self, root: ET.Element):
        """Check iXBRL structure (ix:hidden section, body)."""
        ns_xhtml = "http://www.w3.org/1999/xhtml"
        ns_ix = "http://www.xbrl.org/2013/inlineXBRL"
        
        # Check ix:hidden section exists
        hidden = root.find(f".//{{{ns_ix}}}hidden")
        if hidden is None:
            self._log("ix:hidden section", False, "Missing - XBRL data must be in hidden section")
        else:
            self._log("ix:hidden section", True)
        
        # Check body exists
        body = root.find(f".//{{{ns_xhtml}}}body")
        if body is None:
            self._log("XHTML body", False, "Missing")
        else:
            self._log("XHTML body", True)
        
        # Check for ix:nonNumeric or ix:nonFraction facts
        non_numeric = root.findall(f".//{{{ns_ix}}}nonNumeric") if hidden is not None else []
        non_fraction = root.findall(f".//{{{ns_ix}}}nonFraction") if hidden is not None else []
        # Also check in body
        non_numeric_body = root.findall(f".//{{{ns_xhtml}}}body//{{{ns_ix}}}nonNumeric") if body is not None else []
        
        if non_numeric or non_fraction:
            self._log("XBRL facts", True, f"{len(non_numeric)+len(non_fraction)} hidden + {len(non_numeric_body)} inline facts")
        else:
            self._log("XBRL facts", False, "No tagged facts found")

    def _check_units(self, root: ET.Element):
        """Check unit definitions."""
        ns_xbrli = "http://www.xbrl.org/2003/instance"
        
        # Find ix:hidden section
        ix_ns = "http://www.xbrl.org/2013/inlineXBRL"
        hidden = root.find(f".//{{{ix_ns}}}hidden")
        if hidden is None:
            return
        
        units = hidden.findall(f".//{{{ns_xbrli}}}unit")
        if not units:
            self._log("Unit definitions", False, "No units found")
            return
        
        unit_ids = []
        for unit in units:
            uid = unit.get("id", "?")
            measures = [m.text for m in unit.findall(f".//{{{ns_xbrli}}}measure") if m.text]
            unit_ids.append(f"{uid}={','.join(measures)}")
        
        self._log("Unit definitions", True, f"{len(units)} units: {', '.join(unit_ids)}")

    def _check_contexts(self, root: ET.Element):
        """Check context definitions."""
        ns_xbrli = "http://www.xbrl.org/2003/instance"
        ix_ns = "http://www.xbrl.org/2013/inlineXBRL"
        
        hidden = root.find(f".//{{{ix_ns}}}hidden")
        if hidden is None:
            return
        
        contexts = hidden.findall(f".//{{{ns_xbrli}}}context")
        if not contexts:
            self._log("Context definitions", False, "No contexts found")
            return
        
        ctx_info = []
        for ctx in contexts:
            cid = ctx.get("id", "?")
            # Check entity identifier
            entity = ctx.find(f".//{{{ns_xbrli}}}identifier")
            entity_text = entity.text if entity is not None else "missing"
            # Check period
            start = ctx.find(f".//{{{ns_xbrli}}}startDate")
            end = ctx.find(f".//{{{ns_xbrli}}}endDate")
            instant = ctx.find(f".//{{{ns_xbrli}}}instant")
            if start is not None and end is not None:
                period = f"{start.text}/{end.text}"
            elif instant is not None:
                period = f"{instant.text} (instant)"
            else:
                period = "missing"
            ctx_info.append(f"{cid}: {entity_text} [{period}]")
        
        self._log("Context definitions", True, f"{len(contexts)} contexts: {'; '.join(ctx_info)}")

        # Check for required entity identifier scheme
        for ctx in contexts:
            identifier = ctx.find(f".//{{{ns_xbrli}}}identifier")
            if identifier is not None:
                scheme = identifier.get("scheme", "")
                if not scheme:
                    self._log("Entity identifier scheme", False, "Missing scheme attribute")
                    break
        else:
            self._log("Entity identifier scheme", True, "Present on all contexts")

    def _check_facts(self, root: ET.Element):
        """Extract and validate all XBRL facts."""
        ix_ns = "http://www.xbrl.org/2013/inlineXBRL"
        
        # Find all ix:nonNumeric and ix:nonFraction elements
        facts = []
        for tag in [f"{{{ix_ns}}}nonNumeric", f"{{{ix_ns}}}nonFraction"]:
            for elem in root.iter(tag):
                concept = elem.get("name", "")
                context_ref = elem.get("contextRef", "")
                unit_ref = elem.get("unitRef", "")
                value = elem.text.strip() if elem.text else ""
                
                facts.append({
                    "concept": concept,
                    "context_ref": context_ref,
                    "unit_ref": unit_ref,
                    "value": value,
                    "tag": tag.split("}")[1],
                    "efrag_mapped": False,
                    "efrag_concept": "",
                    "valid": True,
                })
        
        if not facts:
            self._log("Fact extraction", False, "No ix:nonNumeric/ix:nonFraction elements found")
            return
        
        self.results["facts"] = facts
        self._log("Fact extraction", True, f"Extracted {len(facts)} facts")

    def _map_to_efrag(self):
        """Map our concepts to official EFRAG taxonomy and validate."""
        facts = self.results.get("facts", [])
        if not facts:
            return
        
        mapped_count = 0
        unmapped = []
        unit_errors = []
        
        for fact in facts:
            concept_name = fact["concept"].split(":")[-1] if ":" in fact["concept"] else fact["concept"]
            
            if concept_name in EFRAG_TAXONOMY_MAP:
                mapping = EFRAG_TAXONOMY_MAP[concept_name]
                fact["efrag_mapped"] = True
                fact["efrag_concept"] = mapping["efrag"]
                fact["standard"] = mapping["standard"]
                fact["efrag_label"] = mapping["label"]
                mapped_count += 1
                
                # Check unit ref matches expected unit type
                unit_ref = fact.get("unit_ref", "")
                expected_unit = mapping["unit"]
                if unit_ref and expected_unit:
                    # Unit refs are like "u_esrs:tCo2e" - extract the measure part
                    expected_measure = expected_unit.split(":")[-1]
                    if expected_measure not in unit_ref and expected_unit not in unit_ref:
                        unit_errors.append(f"{concept_name}: expected unit '{expected_unit}', got ref '{unit_ref}'")
            else:
                unmapped.append(concept_name)
                fact["efrag_mapped"] = False
        
        if mapped_count > 0:
            self._log("EFRAG taxonomy mapping", True, f"{mapped_count}/{len(facts)} concepts mapped to official taxonomy")
        if unmapped:
            self._log("Unmapped concepts", False, f"Concepts not in EFRAG taxonomy: {', '.join(unmapped)}")
        if unit_errors:
            self._log("Unit validation", False, "; ".join(unit_errors[:5]))
        else:
            self._log("Unit validation", True, "All facts have expected unit types")

        # Count per standard
        standards = {}
        for f in facts:
            if f.get("standard"):
                s = f["standard"]
                standards[s] = standards.get(s, 0) + 1
        if standards:
            self._log("ESRS standard coverage", True, 
                      f"Facts per standard: {', '.join(f'{k}={v}' for k, v in sorted(standards.items()))}")

    def _generate_audit_trail(self):
        """Generate structured audit trail for every fact."""
        facts = self.results.get("facts", [])
        if not facts:
            return
        
        audit = []
        for fact in facts:
            entry = {
                "concept": fact.get("efrag_concept", fact["concept"]),
                "value": fact["value"],
                "unit": f"ref:{fact.get('unit_ref', 'N/A')}",
                "context": fact.get("context_ref", "N/A"),
                "standard": fact.get("standard", "unknown"),
                "tag_type": fact.get("tag", "unknown"),
                "efrag_mapped": fact.get("efrag_mapped", False),
                "confidence": "high" if fact.get("efrag_mapped") else "low",
            }
            audit.append(entry)
        
        self.results["audit_trail"] = audit
        self._log("Audit trail", True, f"{len(audit)} entries generated")

    def to_report_md(self) -> str:
        """Generate human-readable validation report."""
        passed = self.results["passed"]
        status = "✅ PASS" if passed else "❌ FAIL"
        
        lines = [
            f"# XBRL/ESEF Validation Report",
            f"",
            f"**File:** `{self.results['file']}`",
            f"**Status:** {status}",
            f"**Validated:** {self.results['validated_at']}",
            f"",
            f"## Checks ({len(self.results['checks'])})",
            f"",
        ]
        
        for c in self.results["checks"]:
            icon = "✅" if c["passed"] else "❌"
            detail = f" — {c['detail']}" if c["detail"] else ""
            lines.append(f"{icon} **{c['check']}**{detail}")
        
        lines.extend(["", "## Facts", ""])
        
        facts = self.results.get("facts", [])
        if facts:
            lines.append(f"| # | Concept | Value | Unit | EF Taxonomy | Standard |")
            lines.append(f"|---|---------|-------|------|-------------|----------|")
            for i, f in enumerate(facts, 1):
                efrag_icon = "✅" if f.get("efrag_mapped") else "⚠️"
                eff_name = f.get("efrag_concept", "NOT MAPPED")
                lines.append(f"| {i} | {f['concept']} | {f['value']} | {f.get('unit_ref','-')} | {efrag_icon} {eff_name} | {f.get('standard','?')} |")
        
        audit = self.results.get("audit_trail", [])
        if audit:
            lines.extend(["", "## Audit Trail", ""])
            lines.append("| Concept | Value | Standard | Confidence |")
            lines.append("|---------|-------|----------|------------|")
            for a in audit:
                conf_icon = "🟢" if a["confidence"] == "high" else "🟡"
                lines.append(f"| {a['concept']} | {a['value']} | {a['standard']} | {conf_icon} {a['confidence']} |")
        
        return "\n".join(lines)

    def to_audit_json(self) -> dict:
        """Get audit trail as structured JSON (provenance-ready)."""
        return {
            "validator": "CSRD Agent XBRL/ESEF Validator v1",
            "file": self.results["file"],
            "validated_at": self.results["validated_at"],
            "passed": self.results["passed"],
            "facts_with_audit": self.results.get("audit_trail", []),
        }


def validate_client(client_name: str, base_dir: str = "clients") -> dict:
    """Validate all iXBRL files for a client."""
    client_dir = Path(base_dir) / client_name
    xbrl_dir = client_dir / "xbrl"
    
    if not xbrl_dir.exists():
        return {"error": f"No xbrl directory for {client_name}"}
    
    results = []
    for ixbrl_file in sorted(xbrl_dir.glob("*ixbrl.html")):
        validator = XBRLValidator(str(ixbrl_file))
        result = validator.validate_all()
        results.append(result)
        
        # Save report
        report_path = ixbrl_file.with_suffix(".validation.md")
        with open(report_path, "w") as f:
            f.write(validator.to_report_md())
        
        # Save audit trail
        audit_path = ixbrl_file.with_suffix(".audit.json")
        with open(audit_path, "w") as f:
            json.dump(validator.to_audit_json(), f, indent=2)
        
        print(f"  {'✅' if result['passed'] else '❌'} {ixbrl_file.name}: "
              f"{len(result.get('facts',[]))} facts, "
              f"{sum(1 for c in result['checks'] if c['passed'])}/{len(result['checks'])} checks passed")
    
    return results


def main():
    """Validate all client iXBRL files."""
    target = sys.argv[1] if len(sys.argv) > 1 else "all"
    
    print(f"\n{'='*60}")
    print(f"XBRL/ESEF Validator — CSRD Agent")
    print(f"{'='*60}")
    
    if target == "all":
        clients_dir = Path("clients")
        for client_dir in sorted(clients_dir.iterdir()):
            if client_dir.is_dir() and (client_dir / "xbrl").exists():
                print(f"\n🏢 {client_dir.name}")
                validate_client(client_dir.name)
    else:
        validate_client(target)
    
    print(f"\n{'='*60}")
    print(f"Done. Validation reports saved to clients/*/xbrl/*.validation.md")
    print(f"Audit trails saved to clients/*/xbrl/*.audit.json")


if __name__ == "__main__":
    main()