"""Double Materiality Assessment Engine.

Implements the ESRS 1 Annex A methodology for assessing:
1. Impact Materiality (inside-out): how the company affects sustainability matters
2. Financial Materiality (outside-in): how sustainability matters affect the company

Outputs: Materiality Matrix + IRO Register
"""

from __future__ import annotations

from enum import Enum
from dataclasses import dataclass, field, asdict
from typing import Any
import json
from datetime import datetime


class MaterialityDimension(Enum):
    IMPACT = "impact"
    FINANCIAL = "financial"


class ImpactType(Enum):
    ACTUAL = "actual"       # Current, measurable impact
    POTENTIAL = "potential"  # Future, uncertain impact


class ImpactValence(Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"


class RiskOpportunityType(Enum):
    PHYSICAL = "physical"
    TRANSITION = "transition"
    REPUTATIONAL = "reputational"
    LIABILITY = "liability"
    OPPORTUNITY = "opportunity"


@dataclass
class ImpactAssessment:
    """Impact materiality assessment for a single sustainability matter."""
    impact_type: ImpactType
    valence: ImpactValence
    scale: int = 1
    scope: int = 1
    irremediability: int = 1
    likelihood: float = 0.5
    time_horizon: str = "short"

    @property
    def severity(self) -> float:
        base = self.scale * self.scope
        if (self.valence == ImpactValence.NEGATIVE
                and self.impact_type == ImpactType.ACTUAL):
            base *= self.irremediability
        return base

    @property
    def materiality_score(self) -> float:
        if self.impact_type == ImpactType.ACTUAL:
            return float(self.severity)
        return self.severity * self.likelihood

    def to_dict(self) -> dict[str, Any]:
        return {
            "impact_type": self.impact_type.value,
            "valence": self.valence.value,
            "scale": self.scale,
            "scope": self.scope,
            "irremediability": self.irremediability,
            "likelihood": self.likelihood,
            "time_horizon": self.time_horizon,
            "severity": self.severity,
            "materiality_score": self.materiality_score,
        }


@dataclass
class FinancialAssessment:
    """Financial materiality assessment for a single sustainability matter."""
    risk_type: RiskOpportunityType
    magnitude_eur: float = 0.0
    likelihood: float = 0.5
    time_horizon: str = "medium"
    dependency_rating: int = 1

    @property
    def expected_loss(self) -> float:
        return self.magnitude_eur * self.likelihood

    @property
    def materiality_score(self) -> float:
        return self.expected_loss * self.dependency_rating

    def to_dict(self) -> dict[str, Any]:
        return {
            "risk_type": self.risk_type.value,
            "magnitude_eur": self.magnitude_eur,
            "likelihood": self.likelihood,
            "time_horizon": self.time_horizon,
            "dependency_rating": self.dependency_rating,
            "expected_loss": self.expected_loss,
            "materiality_score": self.materiality_score,
        }


# ESRS 1 Appendix A — 60+ sustainability matters
SUSTAINABILITY_MATTERS: list[dict[str, Any]] = [
    {"id": "CLIM-01", "name": "Climate change mitigation", "domain": "E1"},
    {"id": "CLIM-02", "name": "Climate change adaptation", "domain": "E1"},
    {"id": "CLIM-03", "name": "Energy", "domain": "E1"},
    {"id": "POLL-01", "name": "Air pollution", "domain": "E2"},
    {"id": "POLL-02", "name": "Water pollution", "domain": "E2"},
    {"id": "POLL-03", "name": "Soil pollution", "domain": "E2"},
    {"id": "POLL-04", "name": "Substances of concern", "domain": "E2"},
    {"id": "POLL-05", "name": "Microplastics", "domain": "E2"},
    {"id": "WATR-01", "name": "Water consumption", "domain": "E3"},
    {"id": "WATR-02", "name": "Water withdrawals", "domain": "E3"},
    {"id": "WATR-03", "name": "Marine resources", "domain": "E3"},
    {"id": "BIOD-01", "name": "Land-use change", "domain": "E4"},
    {"id": "BIOD-02", "name": "Species impact", "domain": "E4"},
    {"id": "BIOD-03", "name": "Ecosystem services", "domain": "E4"},
    {"id": "BIOD-04", "name": "Deforestation", "domain": "E4"},
    {"id": "CIRC-01", "name": "Resource inflows (materials)", "domain": "E5"},
    {"id": "CIRC-02", "name": "Resource outflows (waste)", "domain": "E5"},
    {"id": "CIRC-03", "name": "Circular product design", "domain": "E5"},
    {"id": "WORK-01", "name": "Working conditions", "domain": "S1"},
    {"id": "WORK-02", "name": "Equal treatment", "domain": "S1"},
    {"id": "WORK-03", "name": "Health & safety", "domain": "S1"},
    {"id": "WORK-04", "name": "Training & skills", "domain": "S1"},
    {"id": "WORK-05", "name": "Work-life balance", "domain": "S1"},
    {"id": "WORK-06", "name": "Diversity & inclusion", "domain": "S1"},
    {"id": "WORK-07", "name": "Adequate wages", "domain": "S1"},
    {"id": "WORK-08", "name": "Social protection", "domain": "S1"},
    {"id": "WORK-09", "name": "Human rights due diligence", "domain": "S1"},
    {"id": "VCHN-01", "name": "Forced labor in supply chain", "domain": "S2"},
    {"id": "VCHN-02", "name": "Child labor in supply chain", "domain": "S2"},
    {"id": "VCHN-03", "name": "Safe working conditions (suppliers)", "domain": "S2"},
    {"id": "VCHN-04", "name": "Fair wages in supply chain", "domain": "S2"},
    {"id": "COMM-01", "name": "Community engagement", "domain": "S3"},
    {"id": "COMM-02", "name": "Indigenous rights", "domain": "S3"},
    {"id": "COMM-03", "name": "Land rights", "domain": "S3"},
    {"id": "COMM-04", "name": "Resettlement", "domain": "S3"},
    {"id": "CNSM-01", "name": "Product safety", "domain": "S4"},
    {"id": "CNSM-02", "name": "Data privacy", "domain": "S4"},
    {"id": "CNSM-03", "name": "Fair marketing", "domain": "S4"},
    {"id": "CNSM-04", "name": "Accessibility", "domain": "S4"},
    {"id": "GOVN-01", "name": "Anti-corruption", "domain": "G1"},
    {"id": "GOVN-02", "name": "Anti-bribery", "domain": "G1"},
    {"id": "GOVN-03", "name": "Whistleblower protection", "domain": "G1"},
    {"id": "GOVN-04", "name": "Supply chain ethics screening", "domain": "G1"},
    {"id": "GOVN-05", "name": "Lobbying & political engagement", "domain": "G1"},
    {"id": "GOVN-06", "name": "Payment practices", "domain": "G1"},
    {"id": "GOVN-07", "name": "Animal welfare", "domain": "G1"},
]


@dataclass
class MaterialityResult:
    """Complete materiality assessment for one sustainability matter."""
    matter_id: str
    matter_name: str
    domain: str
    impact_assessments: list[ImpactAssessment] = field(default_factory=list)
    financial_assessments: list[FinancialAssessment] = field(default_factory=list)

    @property
    def impact_materiality_score(self) -> float:
        if not self.impact_assessments:
            return 0.0
        return max(a.materiality_score for a in self.impact_assessments)

    @property
    def financial_materiality_score(self) -> float:
        if not self.financial_assessments:
            return 0.0
        return max(a.materiality_score for a in self.financial_assessments)

    @property
    def is_impact_material(self) -> bool:
        return self.impact_materiality_score >= 3.0

    @property
    def is_financially_material(self) -> bool:
        return self.financial_materiality_score >= 100000

    @property
    def is_material(self) -> bool:
        return self.is_impact_material or self.is_financially_material

    @property
    def materiality_type(self) -> str:
        if self.is_impact_material and self.is_financially_material:
            return "double_material"
        if self.is_impact_material:
            return "impact_only"
        if self.is_financially_material:
            return "financial_only"
        return "non_material"

    def to_dict(self) -> dict[str, Any]:
        return {
            "matter_id": self.matter_id,
            "matter_name": self.matter_name,
            "domain": self.domain,
            "impact_materiality_score": self.impact_materiality_score,
            "financial_materiality_score": self.financial_materiality_score,
            "is_impact_material": self.is_impact_material,
            "is_financially_material": self.is_financially_material,
            "materiality_type": self.materiality_type,
            "is_material": self.is_material,
            "impact_assessments": [a.to_dict() for a in self.impact_assessments],
            "financial_assessments": [a.to_dict() for a in self.financial_assessments],
        }


@dataclass
class IROEntry:
    """Impact, Risk, or Opportunity register entry."""
    id: str
    matter_id: str
    title: str
    description: str
    type: str
    materiality_result_id: str
    financial_impact_eur: float = 0.0
    mitigation_action: str = ""
    target_date: str = ""
    status: str = "identified"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class DoubleMaterialityAssessment:
    """Full double materiality assessment output."""
    company_name: str
    report_date: str = ""
    assessment_date: str = ""
    results: list[MaterialityResult] = field(default_factory=list)
    iro_register: list[IROEntry] = field(default_factory=list)

    @property
    def material_matters(self) -> list[MaterialityResult]:
        return [r for r in self.results if r.is_material]

    @property
    def double_material_matters(self) -> list[MaterialityResult]:
        return [r for r in self.results if r.materiality_type == "double_material"]

    @property
    def impact_material_matters(self) -> list[MaterialityResult]:
        return [r for r in self.results if r.is_impact_material]

    @property
    def financial_material_matters(self) -> list[MaterialityResult]:
        return [r for r in self.results if r.is_financially_material]

    def summary(self) -> dict[str, Any]:
        return {
            "company": self.company_name,
            "assessment_date": self.assessment_date,
            "total_matters_assessed": len(self.results),
            "double_material": len(self.double_material_matters),
            "impact_only": len([r for r in self.results if r.materiality_type == "impact_only"]),
            "financial_only": len([r for r in self.results if r.materiality_type == "financial_only"]),
            "non_material": len([r for r in self.results if r.materiality_type == "non_material"]),
            "material_standards": list(set(r.domain for r in self.material_matters)),
            "iro_count": len(self.iro_register),
        }

    def to_dict(self) -> dict[str, Any]:
        return {
            "company": self.company_name,
            "report_date": self.report_date,
            "assessment_date": self.assessment_date,
            "summary": self.summary(),
            "results": [r.to_dict() for r in self.results],
            "iro_register": [e.to_dict() for e in self.iro_register],
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)

    def save(self, path: str) -> None:
        with open(path, "w") as f:
            f.write(self.to_json())


class DoubleMaterialityEngine:
    """Orchestrates double materiality assessment for a company."""

    def __init__(self, company_name: str):
        self.company_name = company_name
        self._matters = {m["id"]: m for m in SUSTAINABILITY_MATTERS}

    def assess_matter(
        self,
        matter_id: str,
        impact_assessments: list[ImpactAssessment] | None = None,
        financial_assessments: list[FinancialAssessment] | None = None,
    ) -> MaterialityResult:
        matter = self._matters.get(matter_id)
        if not matter:
            raise ValueError(f"Unknown sustainability matter: {matter_id}")
        return MaterialityResult(
            matter_id=matter_id,
            matter_name=matter["name"],
            domain=matter["domain"],
            impact_assessments=impact_assessments or [],
            financial_assessments=financial_assessments or [],
        )

    def assess_all(
        self,
        company_profile: dict[str, Any] | None = None,
        auto_score: bool = True,
    ) -> DoubleMaterialityAssessment:
        results: list[MaterialityResult] = []
        iro_entries: list[IROEntry] = []
        sector = (company_profile or {}).get("sector", "general")

        for matter in SUSTAINABILITY_MATTERS:
            mid = matter["id"]
            if auto_score:
                impact = self._auto_impact_assessment(mid, sector)
                financial = self._auto_financial_assessment(mid, sector)
            else:
                impact = []
                financial = []

            result = MaterialityResult(
                matter_id=mid,
                matter_name=matter["name"],
                domain=matter["domain"],
                impact_assessments=impact,
                financial_assessments=financial,
            )
            results.append(result)

            if result.is_material:
                iro_id = f"IRO-{mid}-001"
                iro_type = "impact" if result.is_impact_material else "risk"
                iro_entries.append(IROEntry(
                    id=iro_id,
                    matter_id=mid,
                    title=f"{matter['name']} — Material Sustainability Matter",
                    description=f"Identified as {'double material' if result.materiality_type == 'double_material' else result.materiality_type}",
                    type=iro_type,
                    materiality_result_id=mid,
                ))

        return DoubleMaterialityAssessment(
            company_name=self.company_name,
            report_date="2026-06-22",
            assessment_date="2026-06-22",
            results=results,
            iro_register=iro_entries,
        )

    def _auto_impact_assessment(self, matter_id: str, sector: str) -> list[ImpactAssessment]:
        high_impact_sectors = {
            "E1": ["energy", "manufacturing", "aviation", "shipping", "mining", "chemicals"],
            "E2": ["chemicals", "manufacturing", "mining", "agriculture", "pharma"],
            "E3": ["agriculture", "beverages", "textiles", "mining", "chemicals"],
            "E4": ["agriculture", "mining", "construction", "forestry", "energy"],
            "E5": ["manufacturing", "retail", "packaging", "electronics", "automotive"],
            "S1": ["manufacturing", "retail", "hospitality", "logistics", "construction"],
            "S2": ["apparel", "electronics", "food", "mining", "manufacturing"],
            "S3": ["mining", "energy", "construction", "agriculture", "forestry"],
            "S4": ["pharma", "food", "tech", "financial", "healthcare"],
            "G1": ["energy", "defense", "construction", "pharma", "financial"],
        }
        domain = self._matters.get(matter_id, {}).get("domain", "")
        relevant = high_impact_sectors.get(domain, [])
        base_scale = 3 if sector in relevant else 1
        return [ImpactAssessment(
            impact_type=ImpactType.ACTUAL,
            valence=ImpactValence.NEGATIVE,
            scale=base_scale,
            scope=2,
            irremediability=2 if base_scale >= 3 else 1,
            likelihood=0.7,
        )]

    def _auto_financial_assessment(self, matter_id: str, sector: str) -> list[FinancialAssessment]:
        high_risk = {
            "E1": ["energy", "aviation", "shipping", "manufacturing"],
            "E2": ["chemicals", "pharma", "mining"],
            "E3": ["beverages", "agriculture", "textiles"],
            "E4": ["mining", "construction", "agriculture"],
            "E5": ["manufacturing", "packaging", "electronics"],
            "S1": ["manufacturing", "logistics", "retail"],
            "G1": ["energy", "defense", "financial"],
        }
        domain = self._matters.get(matter_id, {}).get("domain", "")
        relevant = high_risk.get(domain, [])
        base_magnitude = 10_000_000 if sector in relevant else 500_000
        return [FinancialAssessment(
            risk_type=RiskOpportunityType.TRANSITION,
            magnitude_eur=base_magnitude,
            likelihood=0.4 if sector in relevant else 0.2,
            dependency_rating=4 if sector in relevant else 2,
        )]