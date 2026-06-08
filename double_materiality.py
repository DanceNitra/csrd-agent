"""
Double Materiality Assessment (DMA) Engine — per ESRS 1 Appendix A.

Two dimensions:
  1. Impact Materiality (Inside-Out): Company activities affect people/environment
  2. Financial Materiality (Outside-In): Sustainability matters affect company's finances

6-step process: Context → Stakeholder → Impact Assessment → Financial Assessment → Matrix → Gap
"""
import json
from typing import Optional

from esrs_knowledge_base import load_all_standards, get_all_datapoints


# ── ESRS 1 Appendix A — Sustainability Matters ──
# Full list of matters to screen for materiality
SUSTAINABILITY_MATTERS = [
    # Environmental
    {"id": "E1_C1", "topic": "Climate change", "sub_topic": "Climate change adaptation", "domain": "environmental"},
    {"id": "E1_C2", "topic": "Climate change", "sub_topic": "Climate change mitigation", "domain": "environmental"},
    {"id": "E1_C3", "topic": "Climate change", "sub_topic": "Energy", "domain": "environmental"},
    {"id": "E2_P1", "topic": "Pollution", "sub_topic": "Pollution of air", "domain": "environmental"},
    {"id": "E2_P2", "topic": "Pollution", "sub_topic": "Pollution of water", "domain": "environmental"},
    {"id": "E2_P3", "topic": "Pollution", "sub_topic": "Pollution of soil", "domain": "environmental"},
    {"id": "E2_P4", "topic": "Pollution", "sub_topic": "Substances of concern", "domain": "environmental"},
    {"id": "E2_P5", "topic": "Pollution", "sub_topic": "Substances of very high concern", "domain": "environmental"},
    {"id": "E2_P6", "topic": "Pollution", "sub_topic": "Microplastics", "domain": "environmental"},
    {"id": "E3_W1", "topic": "Water and marine resources", "sub_topic": "Water consumption", "domain": "environmental"},
    {"id": "E3_W2", "topic": "Water and marine resources", "sub_topic": "Water withdrawals", "domain": "environmental"},
    {"id": "E3_W3", "topic": "Water and marine resources", "sub_topic": "Water discharges", "domain": "environmental"},
    {"id": "E3_W4", "topic": "Water and marine resources", "sub_topic": "Ocean water resources", "domain": "environmental"},
    {"id": "E4_B1", "topic": "Biodiversity and ecosystems", "sub_topic": "Climate change drivers", "domain": "environmental"},
    {"id": "E4_B2", "topic": "Biodiversity and ecosystems", "sub_topic": "Land-use change", "domain": "environmental"},
    {"id": "E4_B3", "topic": "Biodiversity and ecosystems", "sub_topic": "Freshwater use", "domain": "environmental"},
    {"id": "E4_B4", "topic": "Biodiversity and ecosystems", "sub_topic": "Direct exploitation", "domain": "environmental"},
    {"id": "E4_B5", "topic": "Biodiversity and ecosystems", "sub_topic": "Invasive species", "domain": "environmental"},
    {"id": "E4_B6", "topic": "Biodiversity and ecosystems", "sub_topic": "Pollution", "domain": "environmental"},
    {"id": "E5_R1", "topic": "Resource use and circular economy", "sub_topic": "Resource inflows, including circular economy", "domain": "environmental"},
    {"id": "E5_R2", "topic": "Resource use and circular economy", "sub_topic": "Resource outflows, including waste", "domain": "environmental"},
    # Social
    {"id": "S1_W1", "topic": "Own workforce", "sub_topic": "Working conditions - secure employment", "domain": "social"},
    {"id": "S1_W2", "topic": "Own workforce", "sub_topic": "Working conditions - working time", "domain": "social"},
    {"id": "S1_W3", "topic": "Own workforce", "sub_topic": "Working conditions - adequate wages", "domain": "social"},
    {"id": "S1_W4", "topic": "Own workforce", "sub_topic": "Working conditions - social dialogue", "domain": "social"},
    {"id": "S1_W5", "topic": "Own workforce", "sub_topic": "Working conditions - collective bargaining", "domain": "social"},
    {"id": "S1_W6", "topic": "Own workforce", "sub_topic": "Working conditions - work-life balance", "domain": "social"},
    {"id": "S1_W7", "topic": "Own workforce", "sub_topic": "Working conditions - health and safety", "domain": "social"},
    {"id": "S1_W8", "topic": "Own workforce", "sub_topic": "Equal treatment - diversity", "domain": "social"},
    {"id": "S1_W9", "topic": "Own workforce", "sub_topic": "Equal treatment - gender equality, equal pay", "domain": "social"},
    {"id": "S1_W10", "topic": "Own workforce", "sub_topic": "Equal treatment - training, skills development", "domain": "social"},
    {"id": "S1_W11", "topic": "Own workforce", "sub_topic": "Equal treatment - employment inclusion", "domain": "social"},
    {"id": "S1_W12", "topic": "Own workforce", "sub_topic": "Other work-related rights - child labour", "domain": "social"},
    {"id": "S1_W13", "topic": "Own workforce", "sub_topic": "Other work-related rights - forced labour", "domain": "social"},
    {"id": "S1_W14", "topic": "Own workforce", "sub_topic": "Other work-related rights - privacy", "domain": "social"},
    {"id": "S2_V1", "topic": "Workers in the value chain", "sub_topic": "All own workforce sub-topics applied to value chain", "domain": "social"},
    {"id": "S3_C1", "topic": "Affected communities", "sub_topic": "Communities' economic, social and cultural rights", "domain": "social"},
    {"id": "S3_C2", "topic": "Affected communities", "sub_topic": "Communities' civil and political rights", "domain": "social"},
    {"id": "S3_C3", "topic": "Affected communities", "sub_topic": "Rights of indigenous peoples", "domain": "social"},
    {"id": "S4_U1", "topic": "Consumers and end-users", "sub_topic": "Information-related impacts, privacy, freedom of expression", "domain": "social"},
    {"id": "S4_U2", "topic": "Consumers and end-users", "sub_topic": "Personal safety, health impacts", "domain": "social"},
    {"id": "S4_U3", "topic": "Consumers and end-users", "sub_topic": "Social inclusion, non-discrimination", "domain": "social"},
    {"id": "S4_U4", "topic": "Consumers and end-users", "sub_topic": "Responsible marketing practices", "domain": "social"},
    # Governance
    {"id": "G1_B1", "topic": "Business conduct", "sub_topic": "Corporate culture", "domain": "governance"},
    {"id": "G1_B2", "topic": "Business conduct", "sub_topic": "Supplier relationships, payment practices", "domain": "governance"},
    {"id": "G1_B3", "topic": "Business conduct", "sub_topic": "Corruption and bribery", "domain": "governance"},
    {"id": "G1_B4", "topic": "Business conduct", "sub_topic": "Political engagement, lobbying", "domain": "governance"},
    {"id": "G1_B5", "topic": "Business conduct", "sub_topic": "Whistleblower protection", "domain": "governance"},
    {"id": "G1_B6", "topic": "Business conduct", "sub_topic": "Animal welfare", "domain": "governance"},
]

MATTER_TO_STANDARD = {
    "E1": "E1", "E2": "E2", "E3": "E3", "E4": "E4", "E5": "E5",
    "S1": "S1", "S2": "S2", "S3": "S3", "S4": "S4",
    "G1": "G1",
}


class DoubleMaterialityEngine:
    """
    Runs the Double Materiality Assessment process.
    
    6-step workflow:
    1. Context mapping — company profile, value chain, business model
    2. Stakeholder engagement — identify affected stakeholders
    3. Impact materiality — assess severity + likelihood for each matter
    4. Financial materiality — assess dependency + risk magnitude
    5. Materiality matrix — combine both and validate
    6. Gap analysis — map material IROs to ESRS datapoints
    """
    
    def __init__(self, company_profile: Optional[dict] = None):
        self.company_profile = company_profile or {
            "name": "Unknown Company",
            "sector": "Unknown",
            "employees": 0,
            "revenue": 0,
            "countries": [],
        }
        self.results = {
            "status": "not_started",
            "company": self.company_profile["name"],
            "material_matters": [],
            "non_material_matters": [],
            "materiality_matrix": None,
            "iro_register": [],
            "gap_analysis": None,
        }
    
    # ── Step 1: Context Mapping ──
    
    def set_company_profile(self, profile: dict):
        """Set company profile for materiality assessment."""
        self.company_profile.update(profile)
        self.results["company"] = profile.get("name", self.company_profile["name"])
    
    # ── Step 2-4: Full DMA Run ──
    
    def run_full_assessment(self, impact_scores: Optional[dict] = None,
                            financial_scores: Optional[dict] = None) -> dict:
        """
        Run the full double materiality assessment.
        
        Args:
            impact_scores: Dict of matter_id -> impact_score (0-5)
            financial_scores: Dict of matter_id -> financial_score (0-5)
        
        If scores not provided, generates from company profile heuristics.
        """
        scores = {}
        
        for matter in SUSTAINABILITY_MATTERS:
            mid = matter["id"]
            imp = impact_scores.get(mid) if impact_scores else None
            fin = financial_scores.get(mid) if financial_scores else None
            
            if imp is None:
                imp = self._estimate_impact(matter)
            if fin is None:
                fin = self._estimate_financial(matter)
            
            scores[mid] = {
                "impact": min(5.0, max(0, imp)),
                "financial": min(5.0, max(0, fin)),
                "matter": matter,
            }
        
        # Determine materiality threshold
        material_matters = []
        non_material_matters = []
        
        for mid, score in scores.items():
            combined = score["impact"] + score["financial"]
            if combined >= 3.0:  # Threshold
                material_matters.append(score)
                # Default standard mapping
                matter = score["matter"]
                std_prefix = matter["id"].split("_")[0]
                score["recommended_standard"] = MATTER_TO_STANDARD.get(std_prefix, "ESRS 2")
            else:
                non_material_matters.append(score)
        
        # Build IRO register
        iro_register = self._build_iro_register(material_matters)
        
        # Gap analysis
        gap = self._run_gap_analysis(material_matters)
        
        self.results = {
            "status": "completed",
            "company": self.company_profile["name"],
            "material_matters": material_matters,
            "non_material_matters": non_material_matters,
            "materiality_matrix": {
                "description": "Impact (x) vs Financial (y) materiality",
                "threshold": 3.0,
                "all_scores": {mid: {"impact": s["impact"], "financial": s["financial"]}
                              for mid, s in scores.items()},
            },
            "iro_register": iro_register,
            "gap_analysis": gap,
        }
        
        return self.results
    
    def _estimate_impact(self, matter: dict) -> float:
        """Estimate impact materiality score based on company sector and profile."""
        sector = self.company_profile.get("sector", "").lower()
        employees = self.company_profile.get("employees", 0)
        sub_topic = matter.get("sub_topic", "").lower()
        
        # Sector-based heuristics
        if "manufacturing" in sector or "industrial" in sector:
            if "climate" in sub_topic or "pollution" in sub_topic or "energy" in sub_topic:
                return 3.5 + (1.0 if "mitigation" in sub_topic else 0.0)
            if "biodiversity" in sub_topic or "water" in sub_topic:
                return 3.0
        elif "financial" in sector or "bank" in sector or "insurance" in sector:
            if "climate" in sub_topic or "governance" in sub_topic:
                return 3.0
        elif "energy" in sector or "oil" in sector or "gas" in sector:
            if "climate" in sub_topic or "pollution" in sub_topic:
                return 4.5
            return 3.0
        elif "tech" in sector or "software" in sector:
            if "consumer" in sub_topic or "privacy" in sub_topic or "workforce" in sub_topic:
                return 3.0
        elif "retail" in sector or "consumer" in sector:
            if "supply" in sub_topic or "value chain" in sub_topic or "consumer" in sub_topic:
                return 3.5
        elif "health" in sector or "pharma" in sector:
            if "consumer" in sub_topic or "privacy" in sub_topic or "health" in sub_topic:
                return 3.5
        
        # Default — most matters are somewhat material
        if "workforce" in sub_topic or "employee" in sub_topic or "equal" in sub_topic:
            return 2.5 + (0.5 if employees > 1000 else 0)
        if "corruption" in sub_topic or "business" in sub_topic or "culture" in sub_topic:
            return 2.5
        
        return 1.5  # Default low materiality
    
    def _estimate_financial(self, matter: dict) -> float:
        """Estimate financial materiality score based on company profile."""
        sector = self.company_profile.get("sector", "").lower()
        revenue = self.company_profile.get("revenue", 0)
        sub_topic = matter.get("sub_topic", "").lower()
        
        # Sector + regulation-based
        if "climate" in sub_topic:
            # CSRD + EU ETS + carbon pricing creates financial risk
            return 3.5
        if "pollution" in sub_topic:
            if "manufacturing" in sector or "energy" in sector:
                return 3.5
        if "supply" in sub_topic or "value chain" in sub_topic:
            # CSDDD creates liability
            return 3.0
        if "corruption" in sub_topic or "bribery" in sub_topic:
            return 3.0
        if "governance" in sub_topic or "business" in sub_topic:
            return 2.5
        if "workforce" in sub_topic or "employee" in sub_topic:
            return 2.0 + (0.5 if revenue > 500_000_000 else 0)
        
        return 1.5
    
    def _build_iro_register(self, material_matters: list) -> list:
        """Build IRO (Impacts, Risks, Opportunities) register from material matters."""
        iro_list = []
        for i, score in enumerate(material_matters):
            matter = score["matter"]
            iro_list.append({
                "id": f"IRO-{i+1:03d}",
                "matter_id": matter["id"],
                "topic": matter["topic"],
                "sub_topic": matter["sub_topic"],
                "impact_score": score["impact"],
                "financial_score": score["financial"],
                "combined_score": score["impact"] + score["financial"],
                "standard": score.get("recommended_standard", "ESRS 2"),
                "type": "risk" if score["financial"] > score["impact"] else "impact",
            })
        return sorted(iro_list, key=lambda x: x["combined_score"], reverse=True)
    
    def _run_gap_analysis(self, material_matters: list) -> dict:
        """Map material matters to ESRS datapoints and identify data gaps."""
        all_dps = get_all_datapoints()
        relevant_standards = set()
        for ms in material_matters:
            std = ms.get("recommended_standard", "")
            if std:
                relevant_standards.add(std)
        
        # Count datapoints per relevant standard
        dp_coverage = {}
        for dp in all_dps:
            std = dp["standard"]
            if std in relevant_standards:
                dp_coverage.setdefault(std, {"total": 0, "mandatory": 0, "data_available": 0})
                dp_coverage[std]["total"] += 1
                if dp["mandatory"]:
                    dp_coverage[std]["mandatory"] += 1
        
        return {
            "relevant_standards": list(relevant_standards),
            "datapoint_coverage": dp_coverage,
            "estimated_data_readiness": "low" if len(relevant_standards) > 3 else "medium",
        }
    
    def to_report_md(self) -> str:
        """Generate a markdown report of the DMA results."""
        lines = [
            f"# Double Materiality Assessment — {self.company_profile.get('name', 'Unknown')}",
            "",
            f"**Sector:** {self.company_profile.get('sector', 'Unknown')}",
            f"**Status:** {self.results.get('status', 'not_started')}",
            "",
            "---",
            "",
            "## Summary",
            "",
            f"Material matters identified: {len(self.results.get('material_matters', []))}",
            f"Non-material matters: {len(self.results.get('non_material_matters', []))}",
            "",
            "## Materiality Matrix",
            "",
        ]
        
        # Top material matters
        for score in self.results.get("material_matters", [])[:10]:
            matter = score["matter"]
            lines.append(f"- **{matter['topic']} — {matter['sub_topic']}** | Impact: {score['impact']:.1f} | Financial: {score['financial']:.1f}")
        
        lines.append("")
        lines.append("## IRO Register")
        lines.append("")
        for iro in self.results.get("iro_register", []):
            lines.append(f"- **{iro['id']}** ({iro['topic']}): Impact {iro['impact_score']:.1f}, Financial {iro['financial_score']:.1f} → {iro['standard']}")
        
        lines.append("")
        lines.append("## Gap Analysis")
        gap = self.results.get("gap_analysis", {})
        lines.append(f"Relevant standards: {', '.join(gap.get('relevant_standards', []))}")
        lines.append(f"Data readiness: {gap.get('estimated_data_readiness', 'unknown')}")
        
        return "\n".join(lines)