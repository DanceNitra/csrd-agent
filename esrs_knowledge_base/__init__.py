"""
ESRS Knowledge Base — load, query, and validate ESRS standards from YAML files.

Each ESRS standard is a .yaml file in esrs_knowledge_base/ with:
  - Standard metadata (name, category, total datapoints)
  - Sections with disclosure requirements
  - Individual datapoints with types and mandatory flags
"""
import os
import yaml
from typing import Optional

KNOWLEDGE_BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Cache loaded standards
_loaded_standards = {}


def _load_yaml(filename: str) -> Optional[dict]:
    """Load a YAML file from the knowledge base directory."""
    filepath = os.path.join(KNOWLEDGE_BASE_DIR, filename)
    if not os.path.isfile(filepath):
        return None
    with open(filepath, "r") as f:
        return yaml.safe_load(f)


def _get_sections(std_data: dict) -> list:
    """Get sections whether they use sections (list) or disclosure_requirements (dict) key."""
    sections = std_data.get("sections")
    if sections is not None:
        return sections
    dr = std_data.get("disclosure_requirements")
    if dr is not None:
        return [{**v, "id": k} for k, v in dr.items()]
    return []


def _standard_id(std_data: dict) -> str:
    """Extract standard ID regardless of format (dict or string)."""
    raw = std_data.get("standard", "")
    if isinstance(raw, dict):
        return raw.get("id", "")
    return raw


def _standard_category(std_data: dict) -> str:
    """Extract standard category regardless of format."""
    raw = std_data.get("standard", "")
    if isinstance(raw, dict):
        return raw.get("category", "")
    return std_data.get("category", "")


def load_all_standards() -> dict[str, dict]:
    """Load all ESRS standards from the knowledge base directory."""
    if _loaded_standards:
        return _loaded_standards
    
    standards = {}
    for filename in sorted(os.listdir(KNOWLEDGE_BASE_DIR)):
        if filename.endswith(".yaml") or filename.endswith(".yml"):
            data = _load_yaml(filename)
            if data:
                std_raw = data.get("standard", {})
                if isinstance(std_raw, dict):
                    std_id = std_raw.get("id", filename.replace(".yaml", ""))
                else:
                    std_id = std_raw
                standards[std_id] = data
    
    _loaded_standards.update(standards)
    return standards


def get_standard(standard_id: str) -> Optional[dict]:
    """Get a single ESRS standard by ID (e.g. 'E1', 'ESRS 2', 'S1')."""
    standards = load_all_standards()
    # Try exact match first
    if standard_id in standards:
        return standards[standard_id]
    # Try case-insensitive
    for k, v in standards.items():
        if k.upper() == standard_id.upper():
            return v
    return None


def get_all_datapoints() -> list[dict]:
    """Get ALL datapoints across all standards with their metadata."""
    standards = load_all_standards()
    datapoints = []
    for std_id, std_data in standards.items():
        for section in _get_sections(std_data):
            for dp in section.get("datapoints", []):
                datapoints.append({
                    "standard": std_id,
                    "section": section["id"],
                    "section_title": section.get("name", section.get("title", "")),
                    "name": dp["name"],
                    "description": dp.get("description", ""),
                    "type": dp.get("type", "narrative"),
                    "mandatory": dp.get("mandatory", False),
                    "unit": dp.get("unit"),
                })
    return datapoints


def get_datapoint(name: str) -> Optional[dict]:
    """Find a single datapoint by name across all standards."""
    for dp in get_all_datapoints():
        if dp["name"] == name:
            return dp
    return None


def get_mandatory_datapoints() -> list[dict]:
    """Get only mandatory datapoints."""
    return [dp for dp in get_all_datapoints() if dp["mandatory"]]


def get_datapoints_by_standard(standard_id: str) -> list[dict]:
    """Get all datapoints for a specific standard."""
    std = get_standard(standard_id)
    if not std:
        return []
    datapoints = []
    for section in _get_sections(std):
        for dp in section.get("datapoints", []):
            datapoints.append({
                "standard": standard_id,
                "section": section["id"],
                "section_title": section.get("name", section.get("title", "")),
                "name": dp["name"],
                "description": dp.get("description", ""),
                "type": dp.get("type", "narrative"),
                "mandatory": dp.get("mandatory", False),
                "unit": dp.get("unit"),
            })
    return datapoints


def count_datapoints() -> dict:
    """Count total, mandatory, and per-standard datapoints."""
    standards = load_all_standards()
    total = 0
    mandatory = 0
    per_standard = {}
    
    for std_id, std_data in standards.items():
        std_total = 0
        std_mandatory = 0
        for section in _get_sections(std_data):
            for dp in section.get("datapoints", []):
                std_total += 1
                total += 1
                if dp.get("mandatory", False):
                    std_mandatory += 1
                    mandatory += 1
        per_standard[std_id] = {"total": std_total, "mandatory": std_mandatory}
    
    return {
        "standards_loaded": len(standards),
        "total_datapoints": total,
        "mandatory_datapoints": mandatory,
        "per_standard": per_standard,
    }


def get_standards_summary() -> list[dict]:
    """Get a summary of all loaded standards."""
    standards = load_all_standards()
    return [
        {
            "id": _standard_id(std),
            "title": std.get("title", std.get("name", "")),
            "category": _standard_category(std),
            "always_material": std.get("always_material", False),
            "total_datapoints": len(get_datapoints_by_standard(_standard_id(std))),
        }
        for k, std in standards.items()
    ]


def validate_report_completeness(report_datapoints: list[str]) -> dict:
    """
    Validate which mandatory datapoints are covered by a report.
    
    Args:
        report_datapoints: List of datapoint names covered in the report.
    
    Returns:
        Dict with coverage stats and missing datapoints.
    """
    mandatory = get_mandatory_datapoints()
    covered = 0
    missing = []
    
    for dp in mandatory:
        if dp["name"] in report_datapoints:
            covered += 1
        else:
            missing.append(dp)
    
    return {
        "total_mandatory": len(mandatory),
        "covered": covered,
        "missing_count": len(missing),
        "completeness_pct": round((covered / len(mandatory)) * 100, 1) if mandatory else 100,
        "missing": missing,
    }