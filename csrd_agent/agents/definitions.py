"""CSRD Agent Definitions — 6 multi-agent roles for CSRD compliance.

Maps the Vault Company OS agent roles to CSRD-specific responsibilities.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class AgentRole(Enum):
    CSRD_RESEARCH_SCOUT = "research_scout"
    ESRS_WRITER = "esrs_writer"
    DOUBLE_MATERIALITY = "double_materiality"
    CROSS_REFERENCE = "cross_reference"
    DATA_INTEGRATION = "data_integration"
    CSRD_AUDITOR = "csrd_auditor"


@dataclass
class Agent:
    """An agent role in the CSRD compliance pipeline."""
    role: AgentRole
    name: str
    title: str
    description: str
    vault_origin: str
    expertise: list[str] = field(default_factory=list)
    tools: list[str] = field(default_factory=list)
    active: bool = True

    def to_dict(self) -> dict[str, Any]:
        return {
            "role": self.role.value,
            "name": self.name,
            "title": self.title,
            "description": self.description,
            "vault_origin": self.vault_origin,
            "expertise": self.expertise,
            "tools": self.tools,
            "active": self.active,
        }


# Pre-defined CSRD agent roster
AGENTS: list[Agent] = [
    Agent(
        role=AgentRole.CSRD_RESEARCH_SCOUT,
        name="Shadow Kael",
        title="CSRD Research Scout",
        description="Monitoruje EFRAG Knowledge Hub, ESRS zmeny, Omnibus simplifikáciu, a regulačný vývoj",
        vault_origin="Shadow Kael",
        expertise=["EFRAG", "ESRS taxonomy", "Omnibus proposal", "ESMA XBRL", "EU legislative process"],
        tools=["web_search", "web_scrape", "cron"],
    ),
    Agent(
        role=AgentRole.ESRS_WRITER,
        name="Sage Mira",
        title="ESRS Writer Agent",
        description="Píše narrative sekcie reportov z datapointov — E1-E5, S1-S4, G1",
        vault_origin="Sage Mira",
        expertise=["sustainability reporting", "ESRS narrative", "XBRL/iXBRL", "disclosure drafting"],
        tools=["csrd_knowledge_base", "jinja2_templates", "client_data"],
    ),
    Agent(
        role=AgentRole.DOUBLE_MATERIALITY,
        name="High Priest Orin",
        title="Double Materiality Agent",
        description="Analyzes impact + financial materiality, generuje IRO matrix a materiality matrix",
        vault_origin="High Priest Orin",
        expertise=["double materiality", "ESRS 1 Annex A", "impact assessment", "financial risk", "IRO register"],
        tools=["dma_engine", "company_profile", "materiality_matrix"],
    ),
    Agent(
        role=AgentRole.CROSS_REFERENCE,
        name="Dame Elara",
        title="Cross-Reference Agent",
        description="Prepája datapointy s evidence files, vytvára audit trail a version control",
        vault_origin="Dame Elara",
        expertise=["audit trail", "data lineage", "version control", "evidence management"],
        tools=["git", "evidence_filer", "datapoint_mapper"],
    ),
    Agent(
        role=AgentRole.DATA_INTEGRATION,
        name="King Aldric",
        title="Data Integration Agent",
        description="Ťahá data z ERP, HR, energy SCADA, supply chain platforiem",
        vault_origin="King Aldric",
        expertise=["ERP integration", "SAP", "HR systems", "SCADA", "API connectors", "ETL"],
        tools=["erp_connector", "csv_importer", "api_scraper", "data_validator"],
    ),
    Agent(
        role=AgentRole.CSRD_AUDITOR,
        name="Sergeant Voss",
        title="CSRD Audit Agent",
        description="QA proti ESRS štandardom (1,178 datapointov), XBRL validácia, limited assurance readiness",
        vault_origin="Sergeant Voss",
        expertise=["ESRS compliance audit", "XBRL validation", "datapoint coverage", "assurance readiness"],
        tools=["quality_scorer", "xbrl_validator", "gap_analyzer", "datapoint_checklist"],
    ),
]


def get_agent(role: AgentRole | str) -> Agent | None:
    """Get agent definition by role enum or string."""
    if isinstance(role, str):
        try:
            role = AgentRole(role)
        except ValueError:
            return None
    for agent in AGENTS:
        if agent.role == role:
            return agent
    return None


def get_agent_by_name(name: str) -> Agent | None:
    """Get agent definition by display name."""
    for agent in AGENTS:
        if agent.name.lower() == name.lower():
            return agent
    return None


def agent_roster() -> dict[str, Any]:
    """Return full agent roster as dict."""
    return {a.role.value: a.to_dict() for a in AGENTS}