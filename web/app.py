"""
CSRD Agent — Web Dashboard
FastAPI web app for SME CSRD Readiness Check + full pipeline management.
"""
import json, os, uuid, yaml
from datetime import datetime
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# ── App setup ──
BASE_DIR = Path(__file__).parent
PROJECT_DIR = BASE_DIR.parent
SESSIONS_DIR = BASE_DIR / "sessions"
SESSIONS_DIR.mkdir(exist_ok=True)

app = FastAPI(title="CSRD Agent — Readiness Check")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# ── Custom render: avoid Starlette's Jinja2 cache bug ──
import jinja2
_jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(str(BASE_DIR / "templates")),
    autoescape=True,
)

def render_html(name: str, **context):
    """Render a Jinja2 template to HTML string, then return HTMLResponse."""
    template = _jinja_env.get_template(name)
    html = template.render(**context)
    from fastapi.responses import HTMLResponse
    return HTMLResponse(html)

# ── Static files ──
static_dir = BASE_DIR / "static"
static_dir.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# ── Import project modules ──
import sys
sys.path.insert(0, str(PROJECT_DIR))

from esrs_knowledge_base import (
    load_all_standards, get_standards_summary, count_datapoints,
    get_standard, _get_sections,
)
from double_materiality import DoubleMaterialityEngine, SUSTAINABILITY_MATTERS
from ixbrl_export import iXBRLEngine

# ── Load ESRS knowledge base ──
ALL_STANDARDS = load_all_standards()
STANDARDS_SUMMARY = get_standards_summary()
DP_COUNTS = count_datapoints()

# ── Load real client benchmark data ──
BENCHMARK_DATA = {}
clients_dir = PROJECT_DIR / "clients"
if clients_dir.exists():
    for d in clients_dir.iterdir():
        profile_path = d / "company_profile.yaml"
        if profile_path.exists():
            try:
                with open(profile_path) as f:
                    profile = yaml.safe_load(f)
                sector = profile.get("sector", "Unknown")
                if sector not in BENCHMARK_DATA:
                    BENCHMARK_DATA[sector] = []
                BENCHMARK_DATA[sector].append({
                    "name": profile.get("name", d.name),
                    "revenue": profile.get("revenue", 0),
                    "employees": profile.get("employees", 0),
                    "country": profile.get("country", ""),
                })
            except Exception:
                pass

# ── SME questionnaire schema ──
SME_QUESTIONS = [
    # Section 1: Company Info
    {"id": "company_name", "section": "Company Info", "question": "Company name", "type": "text", "required": True},
    {"id": "country", "section": "Company Info", "question": "Country of registration", "type": "select", "options": ["AT", "BE", "BG", "HR", "CY", "CZ", "DK", "EE", "FI", "FR", "DE", "GR", "HU", "IE", "IT", "LV", "LT", "LU", "MT", "NL", "PL", "PT", "RO", "SK", "SI", "ES", "SE"], "required": True},
    {"id": "sector", "section": "Company Info", "question": "Industry sector", "type": "select", "options": ["Manufacturing", "Construction", "Wholesale & Retail", "Transport & Logistics", "Hospitality", "ICT & Technology", "Financial Services", "Professional Services", "Energy & Utilities", "Agriculture", "Healthcare", "Education", "Real Estate", "Other"], "required": True},
    {"id": "employees", "section": "Company Info", "question": "Number of employees (FTE)", "type": "number", "required": True},
    {"id": "revenue", "section": "Company Info", "question": "Annual revenue (EUR, in millions)", "type": "number", "required": True},
    
    # Section 2: Climate & Energy
    {"id": "has_ghg_data", "section": "Climate & Energy", "question": "Do you measure your greenhouse gas emissions?", "type": "select", "options": ["No", "Scope 1 only (direct)", "Scope 1+2 (energy)", "Scope 1+2+3 (full value chain)"], "required": False},
    {"id": "ghg_total", "section": "Climate & Energy", "question": "Total GHG emissions (tCO2e, if known)", "type": "number", "required": False},
    {"id": "energy_total_mwh", "section": "Climate & Energy", "question": "Total energy consumption (MWh per year)", "type": "number", "required": False},
    {"id": "has_renewable_energy", "section": "Climate & Energy", "question": "Do you purchase/use renewable energy?", "type": "select", "options": ["No", "Yes, partially (<50%)", "Yes, mostly (>50%)", "Yes, 100% renewable"], "required": False},
    
    # Section 3: Environmental
    {"id": "water_withdrawal_m3", "section": "Environment", "question": "Total water withdrawal (m³ per year)", "type": "number", "required": False},
    {"id": "waste_total_tonnes", "section": "Environment", "question": "Total waste generated (tonnes per year)", "type": "number", "required": False},
    {"id": "has_waste_separation", "section": "Environment", "question": "Do you separate waste for recycling?", "type": "select", "options": ["No", "Partially", "Yes, all waste streams"], "required": False},
    {"id": "has_environmental_policy", "section": "Environment", "question": "Do you have a formal environmental policy?", "type": "select", "options": ["No", "In development", "Yes, documented"], "required": False},
    
    # Section 4: Social & Workforce
    {"id": "female_workforce_pct", "section": "Social", "question": "Percentage of female employees (%)", "type": "number", "required": False},
    {"id": "has_hr_policy", "section": "Social", "question": "Do you have a formal HR policy (code of conduct, anti-discrimination)?", "type": "select", "options": ["No", "In development", "Yes, documented"], "required": False},
    {"id": "has_health_safety", "section": "Social", "question": "Do you track workplace injuries/incidents?", "type": "select", "options": ["No", "Partially", "Yes, systematically"], "required": False},
    {"id": "injury_rate", "section": "Social", "question": "Work-related injury rate (per 1000 employees, if tracked)", "type": "number", "required": False},
    {"id": "has_supplier_code", "section": "Social", "question": "Do you require suppliers to follow ethical/labour standards?", "type": "select", "options": ["No", "For some suppliers", "Yes, all suppliers"], "required": False},
    
    # Section 5: Governance
    {"id": "has_anti_corruption", "section": "Governance", "question": "Do you have an anti-corruption/anti-bribery policy?", "type": "select", "options": ["No", "In development", "Yes, documented"], "required": False},
    {"id": "has_whistleblowing", "section": "Governance", "question": "Do you have a whistleblowing mechanism?", "type": "select", "options": ["No", "In development", "Yes, operational"], "required": False},
    {"id": "has_esg_governance", "section": "Governance", "question": "Does management formally oversee ESG/sustainability issues?", "type": "select", "options": ["No", "Ad-hoc", "Yes, dedicated responsibility"], "required": False},
    {"id": "has_due_diligence", "section": "Governance", "question": "Do you conduct human rights / environmental due diligence?", "type": "select", "options": ["No", "Partially", "Yes, systematically"], "required": False},
]

# ── ESRS materiality mapping for SME (simplified) ──
SECTOR_STANDARD_MAP = {
    "Manufacturing": ["E1", "E2", "E3", "E5", "S1", "S2", "G1"],
    "Construction": ["E1", "E2", "E3", "E5", "S1", "S2", "G1"],
    "Wholesale & Retail": ["E1", "E2", "E5", "S1", "S2", "G1"],
    "Transport & Logistics": ["E1", "E2", "E3", "S1", "S2", "G1"],
    "Hospitality": ["E1", "E3", "E5", "S1", "G1"],
    "ICT & Technology": ["E1", "E5", "S1", "G1"],
    "Financial Services": ["E1", "S1", "G1"],
    "Professional Services": ["E1", "S1", "G1"],
    "Energy & Utilities": ["E1", "E2", "E3", "E4", "E5", "S1", "S2", "G1"],
    "Agriculture": ["E1", "E2", "E3", "E4", "S1", "S2", "G1"],
    "Healthcare": ["E1", "E3", "E5", "S1", "G1"],
    "Education": ["E1", "S1", "G1"],
    "Real Estate": ["E1", "E3", "E5", "S1", "G1"],
    "Other": ["E1", "S1", "G1"],
}


def compute_readiness_score(responses: dict) -> dict:
    """Compute CSRD Readiness Score from SME questionnaire responses.
    
    Returns:
        score: 0-100 overall readiness score
        by_standard: dict of {standard_id: {score, gap_items, mandatory_missing}}
        data_gaps: list of specific data gaps
        recommendations: prioritized action items
    """
    sector = responses.get("sector", "Other")
    relevant_standards = SECTOR_STANDARD_MAP.get(sector, ["E1", "S1", "G1"])
    employees = int(responses.get("employees", 0))
    revenue_m = float(responses.get("revenue", 0))
    
    # ── Scoring per standard ──
    by_standard = {}
    data_gaps = []
    score_items = []
    
    # E1: Climate
    e1_score = 0
    e1_max = 100
    ghg_answers = responses.get("has_ghg_data", "No")
    if ghg_answers != "No":
        e1_score += 25
        if "Scope 1+2" in ghg_answers or "Scope 1+2+3" in ghg_answers:
            e1_score += 10
        if "Scope 1+2+3" in ghg_answers:
            e1_score += 5
    else:
        data_gaps.append("No GHG emissions measurement — required for ESRS E1 disclosure")
    
    if responses.get("ghg_total"):
        e1_score += 15
    else:
        data_gaps.append("GHG emissions data missing (quantity)")
    
    if responses.get("energy_total_mwh"):
        e1_score += 15
    else:
        data_gaps.append("Energy consumption data missing")
    
    renewable = responses.get("has_renewable_energy", "No")
    if renewable != "No":
        e1_score += 10
    
    if responses.get("has_environmental_policy") == "Yes, documented":
        e1_score += 15
    elif responses.get("has_environmental_policy") == "In development":
        e1_score += 5
    else:
        data_gaps.append("No environmental/climate policy documented — ESRS E1-2 requires policies")
    
    by_standard["E1"] = {
        "score": min(100, e1_score),
        "max": e1_max,
        "material": "E1" in relevant_standards,
        "gap_items": [g for g in data_gaps if "GHG" in g or "Energy" in g or "climate" in g or "policy" in g],
    }
    
    # E3: Water
    if "E3" in relevant_standards:
        e3_score = 0
        e3_gaps = []
        if responses.get("water_withdrawal_m3"):
            e3_score += 40
        else:
            e3_gaps.append("Water withdrawal data missing — ESRS E3 requires water metrics")
        if responses.get("has_environmental_policy") in ("Yes, documented", "In development"):
            e3_score += 30
        if responses.get("has_waste_separation") != "No":
            e3_score += 30
        by_standard["E3"] = {"score": min(100, e3_score), "max": 100, "material": True, "gap_items": e3_gaps}
        if e3_gaps:
            data_gaps.extend(e3_gaps)
    
    # E2 + E5: Pollution & Circular economy
    if "E2" in relevant_standards or "E5" in relevant_standards:
        e2_score = 0
        e2_gaps = []
        if responses.get("waste_total_tonnes"):
            e2_score += 35
            if responses.get("has_waste_separation") in ("Partially", "Yes, all waste streams"):
                e2_score += 20
            if responses.get("has_waste_separation") == "Yes, all waste streams":
                e2_score += 15
        else:
            e2_gaps.append("Waste data missing — required for ESRS E2/E5")
        if responses.get("has_environmental_policy") in ("Yes, documented", "In development"):
            e2_score += 30
        std_id = "E2" if "E2" in relevant_standards else "E5"
        by_standard[std_id] = {"score": min(100, e2_score), "max": 100, "material": True, "gap_items": e2_gaps}
        if e2_gaps:
            data_gaps.extend(e2_gaps)
    
    # S1: Workforce
    s1_score = 0
    s1_gaps = []
    hr = responses.get("has_hr_policy", "No")
    hs = responses.get("has_health_safety", "No")
    female = responses.get("female_workforce_pct")
    
    if hr in ("Yes, documented", "In development"):
        s1_score += 20
        if hr == "Yes, documented":
            s1_score += 5
    else:
        s1_gaps.append("No formal HR policy — ESRS S1 requires workforce policies")
    
    if hs != "No":
        s1_score += 20
        if hs == "Yes, systematically":
            s1_score += 5
        if responses.get("injury_rate"):
            s1_score += 10
    else:
        s1_gaps.append("No injury/incident tracking — ESRS S1 requires health & safety metrics")
    
    if female:
        s1_score += 10
    
    if responses.get("has_supplier_code") != "No":
        s1_score += 10
    else:
        s1_gaps.append("No supplier ethical standards — ESRS S2 requires value chain worker disclosures")
    
    if employees > 0:
        s1_score += 10  # Knows employee count
    
    by_standard["S1"] = {
        "score": min(100, s1_score),
        "max": 100,
        "material": "S1" in relevant_standards,
        "gap_items": s1_gaps,
    }
    if s1_gaps:
        data_gaps.extend(s1_gaps)
    
    # G1: Business conduct
    g1_score = 0
    g1_gaps = []
    ac = responses.get("has_anti_corruption", "No")
    wb = responses.get("has_whistleblowing", "No")
    eg = responses.get("has_esg_governance", "No")
    dd = responses.get("has_due_diligence", "No")
    
    if ac in ("Yes, documented", "In development"):
        g1_score += 25
        if ac == "Yes, documented":
            g1_score += 5
    else:
        g1_gaps.append("No anti-corruption policy — ESRS G1 requires business conduct policies")
    
    if wb in ("Yes, operational", "In development"):
        g1_score += 20
        if wb == "Yes, operational":
            g1_score += 5
    else:
        g1_gaps.append("No whistleblowing mechanism — ESRS G1 requires reporting channels")
    
    if eg != "No":
        g1_score += 20
        if eg == "Yes, dedicated responsibility":
            g1_score += 5
    else:
        g1_gaps.append("No ESG governance — management oversight required for CSRD")
    
    if dd in ("Partially", "Yes, systematically"):
        g1_score += 20
    else:
        g1_gaps.append("No due diligence process — required under CSRD")
    
    by_standard["G1"] = {
        "score": min(100, g1_score),
        "max": 100,
        "material": "G1" in relevant_standards,
        "gap_items": g1_gaps,
    }
    if g1_gaps:
        data_gaps.extend(g1_gaps)
    
    # ── Overall score ──
    total_score = sum(s["score"] for s in by_standard.values())
    total_max = sum(s["max"] for s in by_standard.values())
    overall = round((total_score / total_max) * 100, 1) if total_max > 0 else 0
    
    # ── Recommendations ──
    recommendations = []
    # Top 3 priority items
    missing = {
        "GHG measurement": not ghg_answers or ghg_answers == "No",
        "Environmental policy": responses.get("has_environmental_policy") != "Yes, documented",
        "Anti-corruption policy": responses.get("has_anti_corruption") != "Yes, documented",
        "Whistleblowing channel": responses.get("has_whistleblowing") != "Yes, operational",
        "HR policy": responses.get("has_hr_policy") != "Yes, documented",
        "Health & safety tracking": responses.get("has_health_safety") != "Yes, systematically",
        "ESG governance": responses.get("has_esg_governance") != "Yes, dedicated responsibility",
        "Due diligence": responses.get("has_due_diligence") != "Yes, systematically",
    }
    
    priority_map = {
        "ESG governance": "Assign management responsibility for ESG — board/CEO-level ownership",
        "GHG measurement": "Start measuring GHG emissions (Scope 1+2 first, Scope 3 later)",
        "Environmental policy": "Draft and approve an environmental/climate policy",
        "Anti-corruption policy": "Implement anti-corruption policy and training",
        "Whistleblowing channel": "Set up a whistleblowing mechanism (can be third-party)",
        "HR policy": "Formalize HR policies (code of conduct, anti-discrimination)",
        "Health & safety tracking": "Implement systematic health & safety incident tracking",
        "Due diligence": "Establish human rights & environmental due diligence process",
    }
    
    for item, is_missing in missing.items():
        if is_missing:
            recommendations.append(priority_map.get(item, item))
    
    # Prioritize: governance first, then GHG, then policies
    rec_priority = [
        "ESG governance", "GHG measurement", "Environmental policy",
        "Anti-corruption policy", "Whistleblowing channel",
        "HR policy", "Health & safety tracking", "Due diligence",
    ]
    recommendations.sort(key=lambda r: next((i for i, p in enumerate(rec_priority) if p in r), 99))
    
    return {
        "overall": overall,
        "by_standard": by_standard,
        "data_gaps": data_gaps,
        "recommendations": recommendations[:8],
        "relevant_standards": relevant_standards,
        "sector": sector,
        "employees": employees,
        "revenue_m": revenue_m,
    }


def get_benchmark(sector: str) -> dict:
    """Get peer benchmark data for a sector."""
    sector_bench = BENCHMARK_DATA.get(sector, [])
    if not sector_bench:
        # Fallback: use all companies
        sector_bench = [item for items in BENCHMARK_DATA.values() for item in items]
    
    if not sector_bench:
        return None
    
    total_rev = sum(c["revenue"] for c in sector_bench)
    total_emp = sum(c["employees"] for c in sector_bench)
    count = len(sector_bench)
    
    return {
        "count": count,
        "avg_revenue_m": round(total_rev / count / 1e6, 1) if count else 0,
        "avg_employees": round(total_emp / count) if count else 0,
        "peers": [{"name": c["name"], "revenue_m": round(c["revenue"] / 1e6, 1), "employees": c["employees"], "country": c["country"]} for c in sector_bench],
    }


# ── Routes ──

@app.get("/")
async def index(request: Request):
    """Landing page."""
    return render_html("index.html",
        standards_count=DP_COUNTS["standards_loaded"],
        datapoints_total=DP_COUNTS["total_datapoints"],
        client_count=len(BENCHMARK_DATA) if BENCHMARK_DATA else 0,
    )


@app.get("/new")
async def new_assessment(request: Request):
    """SME onboarding form."""
    return render_html("sme_form.html",
        questions=SME_QUESTIONS,
        sections=["Company Info", "Climate & Energy", "Environment", "Social", "Governance"],
        standard_counts={s: len([q for q in SME_QUESTIONS if q["section"] == s]) for s in ["Company Info", "Climate & Energy", "Environment", "Social", "Governance"]},
    )


@app.post("/new")
async def submit_assessment(request: Request):
    """Process SME form, compute readiness, redirect to dashboard."""
    form = await request.form()
    responses = dict(form)
    
    # Validate required fields
    company_name = responses.get("company_name", "").strip()
    if not company_name:
        company_name = "Unnamed Company"
    
    # Run readiness assessment
    result = compute_readiness_score(responses)
    
    # Create session
    session_id = str(uuid.uuid4())[:8]
    session = {
        "id": session_id,
        "company": company_name,
        "created": datetime.now().isoformat(),
        "responses": responses,
        "readiness": result,
    }
    
    with open(SESSIONS_DIR / f"{session_id}.json", "w") as f:
        json.dump(session, f, indent=2, default=str)
    
    return RedirectResponse(url=f"/dashboard/{session_id}", status_code=303)


@app.get("/dashboard/{session_id}")
async def dashboard(request: Request, session_id: str):
    """Readiness Score + Data Gap Analysis dashboard."""
    session_path = SESSIONS_DIR / f"{session_id}.json"
    if not session_path.exists():
        return render_html("error.html",
            message="Session not found. Please start a new assessment.",
        )
    
    with open(session_path) as f:
        session = json.load(f)
    
    readiness = session["readiness"]
    
    # Get benchmark data
    benchmark = get_benchmark(readiness["sector"])
    
    # Generate a simple AI summary from the data
    score = readiness["overall"]
    if score >= 80:
        summary = f"Your company is well-prepared for CSRD compliance. Focus on closing remaining data gaps."
    elif score >= 50:
        summary = f"Moderate readiness — you have some foundational elements in place. Prioritize the top recommendations to improve your score."
    else:
        summary = f"Early stage — CSRD compliance will require significant preparation. Start with the highest-priority recommendations."
    
    return render_html("dashboard.html",
        session=session,
        readiness=readiness,
        benchmark=benchmark,
        summary=summary,
        score_color="green" if score >= 80 else "amber" if score >= 50 else "red",
    )


@app.get("/api/readiness/{session_id}")
async def api_readiness(session_id: str):
    """API endpoint for readiness data."""
    session_path = SESSIONS_DIR / f"{session_id}.json"
    if not session_path.exists():
        return {"error": "Session not found"}
    with open(session_path) as f:
        session = json.load(f)
    return session["readiness"]


@app.get("/api/benchmark/{sector}")
async def api_benchmark(sector: str):
    """API endpoint for benchmark data."""
    bench = get_benchmark(sector)
    if not bench:
        return {"error": "No benchmark data for this sector"}
    return bench


@app.get("/api/standards")
async def api_standards():
    """API: list all ESRS standards with datapoint counts."""
    return {
        "standards": DP_COUNTS["standards_loaded"],
        "datapoints": DP_COUNTS["total_datapoints"],
        "mandatory": DP_COUNTS["mandatory_datapoints"],
        "details": [{"id": s["id"], "name": s.get("title", s.get("name", "")), "datapoints": s.get("datapoint_count", 0)} for s in STANDARDS_SUMMARY],
    }


def run():
    """Entry point for CLI."""
    import uvicorn
    uvicorn.run("web.app:app", host="0.0.0.0", port=8080, reload=True)


if __name__ == "__main__":
    run()