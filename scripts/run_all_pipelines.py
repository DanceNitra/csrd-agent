#!/usr/bin/env python3
"""Run full CSRD pipeline for all real clients in parallel."""
import asyncio, json, os, sys, yaml
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Also go to project root (scripts/ is a subfolder of the project)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from report_engine import CSRDReportEngine

COMPANIES = ["Enel", "Volkswagen_Group", "Siemens", "Iberdrola", "TotalEnergies"]

async def run_one(name: str) -> dict:
    client_dir = f"clients/{name}"
    print(f"\n{'='*60}")
    print(f"🏢 {name}")
    print(f"{'='*60}")

    # Load profile
    with open(f"{client_dir}/company_profile.yaml") as f:
        profile = yaml.safe_load(f)

    engine = CSRDReportEngine(client_dir, llm_enabled=True)
    engine.report_year = 2024
    engine.company_profile = profile
    engine.dma_engine.set_company_profile(profile)
    engine.dma_engine.run_full_assessment()
    engine._reinit_llm()

    # Phase 1-4: already done (skip)
    print("  Phases 1-4: skipping (already have LLM drafts)")

    # Phase 5: Quality Audit
    print("  Phase 5: Quality Audit...", end=" ", flush=True)
    await engine.phase_quality_audit()
    print(f"OK")

    # Phase 6: iXBRL
    print("  Phase 6: iXBRL/ESEF Export...", end=" ", flush=True)
    ix = await engine.phase_ixbrl_export()
    
    # Check XBRL output
    xbrl_dir = f"{client_dir}/xbrl"
    files = {}
    for fn in os.listdir(xbrl_dir):
        files[fn] = os.path.getsize(f"{xbrl_dir}/{fn}")
    
    print(f"OK ({ix['output']['fact_count']} facts)")

    summary = engine.generate_executive_summary()
    return {
        "name": name,
        "profile": {
            "revenue": profile.get("revenue", 0),
            "employees": profile.get("employees", 0),
            "sector": profile.get("sector", ""),
        },
        "score": summary["quality_score"],
        "pass": summary["pass"],
        "phases": summary["phases_completed"],
        "xbrl_facts": ix["output"]["fact_count"],
        "xbrl_files": files,
        "dma_matters": summary["material_matters"],
        "drafts": len(summary["drafted_sections"]),
    }

async def main():
    results = []
    for co in COMPANIES:
        try:
            r = await run_one(co)
            results.append(r)
        except Exception as e:
            print(f"  ❌ FAILED: {e}")
            results.append({"name": co, "error": str(e)})
    
    # Summary table
    print(f"\n{'='*70}")
    print(f"📊 CSRD AGENT — REAL CLIENT PIPELINE SUMMARY")
    print(f"{'='*70}")
    print(f"{'Client':<25} {'Sector':<20} {'Rev(€B)':<10} {'Emp':<8} {'Score':<8} {'XBRL':<6}")
    print(f"{'-'*25} {'-'*20} {'-'*10} {'-'*8} {'-'*8} {'-'*6}")
    
    total_rev = 0
    total_emp = 0
    total_xbrl = 0
    for r in results:
        if "error" in r:
            print(f"{r['name']:<25} {'❌ ERROR':<20}")
            continue
        rev_b = r["profile"]["revenue"] / 1e9
        emp_k = r["profile"]["employees"] // 1000
        score_str = f"{r['score']}/14 {chr(10004) if r['pass'] else chr(10008)}"
        print(f"{r['name']:<25} {r['profile']['sector'][:20]:<20} {rev_b:<10.1f} {emp_k:<8,} {score_str:<8} {r['xbrl_facts']:<6}")
        total_rev += r["profile"]["revenue"]
        total_emp += r["profile"]["employees"]
        total_xbrl += r["xbrl_facts"]
    
    print(f"{'-'*25} {'-'*20} {'-'*10} {'-'*8} {'-'*8} {'-'*6}")
    print(f"{'TOTAL':<25} {'':<20} {total_rev/1e9:<10.1f} {total_emp//1000:<8,} {'':<8} {total_xbrl:<6}")
    
    # Save results
    with open("clients/pipeline_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved: clients/pipeline_results.json")
    
    # Print iXBRL files
    print(f"\n📁 Generated iXBRL files:")
    for r in results:
        if "xbrl_files" in r:
            for fn, size in r["xbrl_files"].items():
                print(f"  clients/{r['name']}/xbrl/{fn} ({size:,} bytes)")

if __name__ == "__main__":
    asyncio.run(main())