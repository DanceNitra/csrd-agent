"""ESRS Knowledge Base — Loader and Data Models.

Loads all 11 ESRS standard YAML files and provides typed access
to datapoints, metrics, and disclosure requirements.
"""

from __future__ import annotations

import os
import yaml
from pathlib import Path
from typing import Any

KB_DIR = Path(__file__).parent


class Metric:
    """A single quantifiable metric within a datapoint."""

    def __init__(self, name: str, unit: str, metric_type: str,
                 base_year: str | None = None, description: str | None = None):
        self.name = name
        self.unit = unit
        self.metric_type = metric_type
        self.base_year = base_year
        self.description = description

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "unit": self.unit,
            "type": self.metric_type,
            "base_year": self.base_year,
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Metric":
        return cls(
            name=d["name"],
            unit=d.get("unit", ""),
            metric_type=d.get("type", "float"),
            base_year=d.get("base_year"),
            description=d.get("description"),
        )


class Datapoint:
    """A single ESRS datapoint (disclosure requirement)."""

    def __init__(self, _id: str, disclosure: str, description: str,
                 dp_type: str, required: bool, xbrl_tag: str | None = None,
                 evidence_required: bool = False,
                 metrics: list[Metric] | None = None,
                 sub_fields: list[dict] | None = None):
        self.id = _id
        self.disclosure = disclosure
        self.description = description
        self.type = dp_type
        self.required = required
        self.xbrl_tag = xbrl_tag
        self.evidence_required = evidence_required
        self.metrics = metrics or []
        self.sub_fields = sub_fields or []

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "disclosure": self.disclosure,
            "description": self.description,
            "type": self.type,
            "required": self.required,
            "xbrl_tag": self.xbrl_tag,
            "evidence_required": self.evidence_required,
            "metrics": [m.to_dict() for m in self.metrics],
            "sub_fields": self.sub_fields,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Datapoint":
        raw_metrics = d.get("metrics", [])
        if isinstance(raw_metrics, list) and all(isinstance(m, dict) for m in raw_metrics):
            metrics = [Metric.from_dict(m) for m in raw_metrics]
        else:
            metrics = []
        return cls(
            _id=d["id"],
            disclosure=d["disclosure"],
            description=d["description"],
            dp_type=d.get("type", "narrative"),
            required=d.get("required", False),
            xbrl_tag=d.get("xbrl_tag"),
            evidence_required=d.get("evidence_required", False),
            metrics=metrics,
            sub_fields=d.get("sub_fields"),
        )


class ESRSStandard:
    """A single ESRS standard with its datapoints."""

    def __init__(self, _id: str, title: str, category: str,
                 mandatory: bool, datapoints: list[Datapoint]):
        self.id = _id
        self.title = title
        self.category = category
        self.mandatory = mandatory
        self.datapoints = datapoints

    @property
    def required_datapoints(self) -> list[Datapoint]:
        return [dp for dp in self.datapoints if dp.required]

    @property
    def optional_datapoints(self) -> list[Datapoint]:
        return [dp for dp in self.datapoints if not dp.required]

    def to_dict(self) -> dict[str, Any]:
        return {
            "standard": self.id,
            "title": self.title,
            "category": self.category,
            "mandatory": self.mandatory,
            "datapoint_count": len(self.datapoints),
            "required_count": len(self.required_datapoints),
        }


class ESGKnowledgeBase:
    """In-memory ESRS knowledge base with all 12 standards."""

    def __init__(self):
        self._standards: dict[str, ESRSStandard] = {}
        self._load_all()

    def _load_all(self) -> None:
        for yaml_path in sorted(KB_DIR.glob("*.yaml")):
            try:
                with open(yaml_path) as f:
                    raw = yaml.safe_load(f)
                if not raw:
                    continue
                datapoints = [Datapoint.from_dict(dp) for dp in raw.get("datapoints", [])]
                std = ESRSStandard(
                    _id=raw["standard"],
                    title=raw.get("title", ""),
                    category=raw.get("category", "unknown"),
                    mandatory=raw.get("mandatory", False),
                    datapoints=datapoints,
                )
                self._standards[std.id] = std
            except Exception as e:
                print(f"Warning: failed to load {yaml_path}: {e}")

    @property
    def all_datapoints(self) -> list[Datapoint]:
        return [dp for s in self._standards.values() for dp in s.datapoints]

    @property
    def total_datapoints(self) -> int:
        return len(self.all_datapoints)

    @property
    def mandatory_datapoints(self) -> list[Datapoint]:
        return [dp for dp in self.all_datapoints if dp.required]

    def get_standard(self, std_id: str) -> ESRSStandard | None:
        return self._standards.get(std_id)

    def get_datapoint(self, dp_id: str) -> Datapoint | None:
        for dp in self.all_datapoints:
            if dp.id == dp_id:
                return dp
        return None

    def standards_by_category(self, category: str) -> list[ESRSStandard]:
        return [s for s in self._standards.values() if s.category == category]

    def summary(self) -> dict[str, Any]:
        return {
            "standards": [s.to_dict() for s in self._standards.values()],
            "total_datapoints": self.total_datapoints,
            "mandatory_datapoints": len(self.mandatory_datapoints),
            "optional_datapoints": self.total_datapoints - len(self.mandatory_datapoints),
        }

    def __getitem__(self, key: str) -> ESRSStandard:
        if key not in self._standards:
            raise KeyError(f"Unknown standard: {key}")
        return self._standards[key]

    def __len__(self) -> int:
        return len(self._standards)

    def __iter__(self):
        return iter(self._standards.values())


# Module-level singleton
_kb: ESGKnowledgeBase | None = None


def get_knowledge_base() -> ESGKnowledgeBase:
    global _kb
    if _kb is None:
        _kb = ESGKnowledgeBase()
    return _kb