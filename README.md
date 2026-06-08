# CSRD Agent — Multi-Agent CSRD/ESRS Compliance Document Factory

> **Auto-generates EU CSRD sustainability reports using a multi-agent system.**
> Research → Write → Review → Deliver — kompletné CSRD reporty z raw dát.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                   CSRD Report Engine                │
├──────────┬──────────┬──────────┬──────────┬─────────┤
│ Research │   DMA    │  Write   │  Review  │ Deliver │
│  Scout   │  Agent   │  Agent   │  Agent   │  Agent  │
│ (Kael)   │ (Orin)   │ (Mira)   │ (Voss)   │(Aldric) │
└──────────┴──────────┴──────────┴──────────┴─────────┘
```

## 🚀 Quick Start

```bash
# Clone + setup
git clone git@github.com:DanceNitra/csrd-agent.git
cd csrd-agent
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Init knowledge base
python3 -c "from esrs_knowledge_base import init_kb; init_kb()"

# Run for a client
python3 -m csrd_agent.cli --client ACS_Energy --year 2025
```

## 📊 Market

| Metric | Value |
|--------|-------|
| Addressable companies | ~50,000 (EU) |
| Total market | €5-8B/year |
| Software-addressable | €1-3B/year |
| Competitor price range | €15k-300k+/yr |
| Our price range | €5k-100k/yr |

## 🧱 Repo Structure

```
csrd-agent/
├── agent_definitions.py     — CSRD agent roles & prompts
├── esrs_knowledge_base/     — ESRS standards as YAML
├── double_materiality.py    — Double Materiality Assessment engine
├── report_engine.py         — Main pipeline orchestrator
├── xbrl_tagger.py           — XBRL/ESEF tagging
├── templates/               — Report templates per ESRS standard
├── clients/                 — Per-client data directories
└── cli.py                   — CLI entry point
```

## 💰 Pricing

| Tier | Price/yr | Target |
|------|----------|--------|
| Lite | €5k-15k | SMEs (<250 emp) |
| Pro | €15k-40k | Mid-market (250-1k) |
| Enterprise | €40k-100k | Large (1k+) |
| White-Label | Custom | Big4 consulting |

## 📋 License

Proprietary — DanceNitra s.r.o.