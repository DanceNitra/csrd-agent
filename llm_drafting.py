"""
LLM-powered CSRD Drafting Engine — generates ESRS-compliant narrative reports.

Connects to Hermes custom provider (OpenAI-compatible API) to produce
professional sustainability report text from raw data + standard metadata.

Architecture:
  LLMDraftEngine
    ├── generate_section()  → full narrative per ESRS disclosure requirement
    ├── generate_datapoint() → specific answer per datapoint
    └── generate_summary()  → executive summary for the report
"""

import json
import os
from datetime import datetime
from typing import Any, Optional

from openai import OpenAI

# ── LLM Configuration ──
LLM_CONFIG = {
    "base_url": "https://ollama.com/v1",
    "api_key": "f29d0b4cd1114735ae5d2b15a247e067.QAOP32xwAa5zRhI6dDm9Nfcw",
    "model": "deepseek-v4-flash",
    "max_tokens": 8192,
    "temperature": 0.3,  # Low temp for compliance-grade consistency
}


def _get_client() -> OpenAI:
    """Create an OpenAI client configured for the Hermes provider."""
    return OpenAI(
        base_url=LLM_CONFIG["base_url"],
        api_key=LLM_CONFIG["api_key"],
    )


def _call_llm(system_prompt: str, user_prompt: str) -> str:
    """Call the LLM with system + user prompts, return content string."""
    client = _get_client()
    response = client.chat.completions.create(
        model=LLM_CONFIG["model"],
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        max_tokens=LLM_CONFIG["max_tokens"],
        temperature=LLM_CONFIG["temperature"],
    )
    content = response.choices[0].message.content
    return content.strip() if content else ""


# ── System-level prompt ──
SYSTEM_PROMPT_CSRD = """You are a senior CSRD/ESRS sustainability consultant at a Big4 firm.
Your job is to write professional, ESRS-compliant sustainability report narratives.

RULES:
1. Write in formal, professional business English — suitable for a published annual report
2. Every claim must be grounded in the data provided — never invent numbers
3. If data is unavailable, state "Data not yet available" or describe the data collection process
4. Follow ESRS structure: context → policy → actions → metrics → targets → financial effects
5. Use active voice, clear statements, evidence-based assertions
6. Include cross-references to other ESRS standards where relevant
7. Mark quantitative data gaps clearly with [DATA GAP: metric_name]
8. Maximum 3 paragraphs per datapoint, 2-5 sentences each
9. Reference EU regulatory framework where applicable
10. Never use placeholder text like "[DATA PENDING]" — write real narrative or identify gaps"""


class LLMDraftEngine:
    """Generate CSRD-compliant narrative content using LLM."""

    def __init__(self, client_name: str, profile: dict[str, Any], dma_results: dict[str, Any]):
        self.client_name = client_name
        self.profile = profile
        self.dma_results = dma_results
        self.sector = profile.get("sector", "General")
        self.employees = profile.get("employees", 0)
        self.revenue = profile.get("revenue", 0)
        self.countries = profile.get("countries", [])
        self.description = profile.get("description", "")

    def _build_context_blob(self, std_data: dict, section: dict) -> str:
        """Build a compact context string for the LLM."""
        lines = []
        lines.append(f"Client: {self.client_name}")
        lines.append(f"Sector: {self.sector}")
        lines.append(f"Employees: {self.employees:,}")
        lines.append(f"Revenue: €{self.revenue:,.0f}")
        lines.append(f"Countries: {', '.join(self.countries)}")
        if self.description:
            lines.append(f"Description: {self.description}")
        lines.append("")

        # Standard metadata
        std_name = std_data.get("name", std_data.get("title", ""))
        lines.append(f"Standard: {section.get('id', '?')} — {section.get('name', section.get('title', ''))}")
        lines.append(f"Standard Description: {section.get('description', std_data.get('description', ''))}")
        lines.append("")

        # Datapoints
        lines.append("Datapoints to address:")
        for dp in section.get("datapoints", []):
            mandatory = " [MANDATORY]" if dp.get("mandatory") else ""
            unit = f" [{dp['type']}]" if dp.get("type") else ""
            lines.append(f"  - {dp['name']}{mandatory}{unit}: {dp.get('question', dp.get('description', ''))}")
        lines.append("")

        # Materiality context
        iro_items = self.dma_results.get("iro_register", [])
        std_id = std_data.get("standard", "")
        if isinstance(std_id, dict):
            std_id = std_id.get("id", "")
        relevant_iro = [
            i for i in iro_items
            if i.get("standard", "").upper() == std_id.upper()
        ]
        if relevant_iro:
            lines.append("Materiality Assessment Results:")
            for iro in relevant_iro:
                lines.append(
                    f"  - Impact: {iro.get('impact_score', 'N/A')}/4 "
                    f"(threshold: {iro.get('impact_threshold', 'N/A')}) | "
                    f"Financial: {iro.get('financial_score', 'N/A')}/4 "
                    f"(threshold: {iro.get('financial_threshold', 'N/A')})"
                )
                lines.append(f"    Matter: {iro.get('matter', '')}")

        return "\n".join(lines)

    def generate_standard_report(self, std_data: dict, sections: list[dict]) -> str:
        """Generate full narrative for an entire ESRS standard in one LLM call."""
        std_name = std_data.get("title", std_data.get("name", "?"))
        std_id_raw = std_data.get("standard", "")
        std_id = std_id_raw if isinstance(std_id_raw, str) else std_id_raw.get("id", "")

        context_parts = [
            f"Client: {self.client_name}",
            f"Sector: {self.sector}",
            f"Employees: {self.employees:,}",
            f"Revenue: €{self.revenue:,.0f}",
            f"Countries: {', '.join(self.countries)}",
        ]
        if self.description:
            context_parts.append(f"Description: {self.description}")
        context_parts.append("")
        context_parts.append(f"Standard: {std_id} — {std_name}")
        context_parts.append(f"Description: {std_data.get('description', '')}")

        # List all disclosure requirements and their datapoints
        context_parts.append("")
        context_parts.append(f"DISCLOSURE REQUIREMENTS ({len(sections)}):")
        for sec in sections:
            sec_name = sec.get("name", sec.get("title", ""))
            context_parts.append(f"\n## {sec.get('id', '')} — {sec_name}")
            context_parts.append(f"   Description: {sec.get('description', '')}")
            context_parts.append(f"   Datapoints ({len(sec.get('datapoints', []))}):")
            for dp in sec.get("datapoints", []):
                mandatory = " [MANDATORY]" if dp.get("mandatory") else ""
                q = dp.get("question", dp.get("description", ""))
                context_parts.append(f"     - {dp['name']}{mandatory}: {q}")

        # Add company data relevant to this standard
        std_id_lower = std_id.lower().replace(" ", "_")
        
        # Map ESRS standard IDs to company_profile keys
        STD_DATA_MAP = {
            "e1": "greenhouse_gas",
            "e2": "pollution",
            "e3": "water",
            "e4": "biodiversity",
            "e5": "circular_economy",
            "s1": "workforce",
            "s2": "value_chain",
            "s3": "communities",
            "s4": "consumers",
            "g1": "business_conduct",
            "esrs_2": None,
        }
        profile_key = STD_DATA_MAP.get(std_id_lower)
        
        company_data = {}
        # Direct top-level keys (name, sector, etc.)
        for k in ("name", "sector", "sub_sector", "revenue", "employees", "countries", "description"):
            if k in self.profile:
                company_data[k] = self.profile[k]
        # Standard-specific data
        if profile_key and profile_key in self.profile:
            std_specific = self.profile[profile_key]
            if isinstance(std_specific, dict):
                company_data.update(std_specific)
        if company_data:
            context_parts.append("")
            context_parts.append("AVAILABLE COMPANY DATA:")
            for k, v in sorted(company_data.items()):
                if k in ("name", "sector", "description", "countries"):
                    continue
                if isinstance(v, dict):
                    context_parts.append(f"  {k}:")
                    for sk, sv in sorted(v.items()):
                        context_parts.append(f"    {sk}: {sv}")
                elif isinstance(v, list):
                    context_parts.append(f"  {k}: {', '.join(str(x) for x in v)}")
                else:
                    context_parts.append(f"  {k}: {v}")

        # Materiality context
        iro_items = self.dma_results.get("iro_register", [])
        relevant_iro = [
            i for i in iro_items
            if i.get("standard", "").upper() == std_id.upper()
        ]
        if relevant_iro:
            context_parts.append("")
            context_parts.append("MATERIALITY RESULTS:")
            for iro in relevant_iro:
                ctx_line = (
                    f"  Matter: {iro.get('matter', '')} | "
                    f"Impact: {iro.get('impact_score', 'N/A')}/4 | "
                    f"Financial: {iro.get('financial_score', 'N/A')}/4"
                )
                context_parts.append(ctx_line)

        context = "\n".join(context_parts)

        user_prompt = f"""You are writing the complete CSRD sustainability report section for standard {std_id} — {std_name}.

CONTEXT:
{context}

INSTRUCTIONS:
Write a comprehensive, professional narrative for EVERY disclosure requirement listed above.
For each DR:
- Start with "## {{DR_id}} — {{DR_name}}" as a markdown heading
- Write 2-4 paragraphs addressing all datapoints
- Integrate available company data into the narrative
- Where data is missing, mark it as [DATA GAP: field_name]
- Follow ESRS structure: context → policies → actions → metrics → targets → financial effects
- Cross-reference other ESRS standards where relevant

End with a brief transition paragraph noting how this standard connects to the next relevant topic.

Write the complete standard narrative now:"""

        return _call_llm(SYSTEM_PROMPT_CSRD, user_prompt)

    def generate_executive_summary(self, material_standards: list[str]) -> str:
        """Generate an executive summary for the full report."""
        profile_blob = (
            f"Client: {self.client_name}\n"
            f"Sector: {self.sector}\n"
            f"Employees: {self.employees:,}\n"
            f"Revenue: €{self.revenue:,.0f}\n"
            f"Operating in: {', '.join(self.countries)}\n"
        )
        if self.description:
            profile_blob += f"Description: {self.description}\n"

        user_prompt = f"""Generate a 1-page executive summary for a CSRD sustainability report.

COMPANY PROFILE:
{profile_blob}

MATERIAL STANDARDS (ranked by materiality):
{json.dumps(material_standards, indent=2)}

OUTPUT: Write an executive summary that:
1. Opens with the company's sustainability vision and commitment
2. Highlights key material topics and why they matter
3. Summarizes the double materiality assessment approach
4. Previews key findings and performance highlights
5. Concludes with future outlook and next reporting cycle targets
6. Total length: 4-6 paragraphs, max 500 words"""

        return _call_llm(SYSTEM_PROMPT_CSRD, user_prompt)

    def generate_data_gap_report(self, sections_with_gaps: list[dict]) -> str:
        """Generate a data gap analysis report based on [DATA GAP] markers."""
        gap_blob = json.dumps(sections_with_gaps, indent=2)

        user_prompt = f"""Generate a Data Gap Analysis report for {self.client_name}'s CSRD report.

GAPS IDENTIFIED:
{gap_blob}

OUTPUT: Write a structured gap report with:
1. Summary of data coverage (% complete vs missing)
2. Prioritized list of gaps by materiality (critical → nice-to-have)
3. Recommended data collection actions per gap
4. Estimated timeline to close each gap
5. Impact on report quality if gap remains open

Keep it actionable — the client should know exactly what to do next."""

        return _call_llm(SYSTEM_PROMPT_CSRD, user_prompt)


def drafting_summary_from_report(result: dict) -> str:
    """Generate a brief narrative summary of the drafting phase."""
    sections = result.get("output", {}).get("sections_drafted", [])
    if not sections:
        return "No sections were drafted."
    return (
        f"Generated {len(sections)} ESRS-compliant narrative sections with "
        f"LLM-powered drafting. Each section follows ESRS structure: "
        f"context → policies → actions → metrics → targets → financial effects."
    )