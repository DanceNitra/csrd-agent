"""CSRD Agent — CLI entry point for running the CSRD reporting pipeline."""
import argparse
import asyncio
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def main():
    parser = argparse.ArgumentParser(description="CSRD Agent — Multi-Agent CSRD Compliance Report Generator")
    parser.add_argument("--client", "-c", default="demo_client", help="Client directory name")
    parser.add_argument("--year", "-y", type=int, default=2025, help="Report year (FY)")
    parser.add_argument("--init", action="store_true", help="Initialize client directory only")
    parser.add_argument("--profile", "-p", help="Path to company profile YAML")
    parser.add_argument("--full-pipeline", action="store_true", help="Run full reporting pipeline")
    parser.add_argument("--llm", action="store_true", help="Enable LLM-powered narrative drafting")
    parser.add_argument("--llm-only", default=None, help="Only generate LLM draft for this standard (e.g. E1, S1)")
    
    args = parser.parse_args()
    
    client_dir = os.path.join(os.path.dirname(__file__), "clients", args.client)
    
    if args.init:
        _init_client(client_dir, args.year, args.profile)
        return
    
    if args.full_pipeline:
        asyncio.run(_run_pipeline(client_dir, args.year, args.llm, args.llm_only if args.llm else None))
        return
    
    # Default: show status
    _show_status(client_dir, args.year)


def _init_client(client_dir: str, year: int, profile_path: str = None):
    """Initialize a new client directory."""
    from report_engine import CSRDReportEngine
    
    engine = CSRDReportEngine(client_dir)
    engine.report_year = year
    
    if profile_path:
        import yaml
        with open(profile_path) as f:
            profile = yaml.safe_load(f)
        engine.set_company_profile(profile)
    
    print(f"✅ Client '{os.path.basename(client_dir)}' initialized for FY{year}")


async def _run_pipeline(client_dir: str, year: int, llm: bool = False, llm_only: str = None):
    """Run full CSRD reporting pipeline."""
    from report_engine import CSRDReportEngine
    
    engine = CSRDReportEngine(client_dir, llm_enabled=llm)
    engine.report_year = year
    
    # ── LLM-only mode: generate single standard draft ──
    if llm_only and llm:
        from esrs_knowledge_base import get_standard, _get_sections
        from double_materiality import DoubleMaterialityEngine
        
        # Run DMA first for context
        dma = DoubleMaterialityEngine(engine.company_profile)
        dma.run_full_assessment()
        engine.dma_engine = dma
        
        # Re-init LLM engine with DMA results
        from llm_drafting import LLMDraftEngine
        engine.llm_engine = LLMDraftEngine(
            client_name=engine.client_name,
            profile=engine.company_profile,
            dma_results=dma.results,
        )
        
        std_data = get_standard(llm_only)
        if not std_data:
            print(f"❌ Standard '{llm_only}' not found")
            return
        
        print(f"\n📝 Generating LLM-powered draft for {llm_only}...\n")
        for section in _get_sections(std_data):
            print(f"   Section: {section.get('id', '?')} — {section.get('name', section.get('title', ''))}")
        
        # Generate draft
        draft = engine._generate_section_draft(llm_only, std_data, None)
        
        # Save
        drafts_dir = f"{client_dir}/drafts/{year}"
        os.makedirs(drafts_dir, exist_ok=True)
        draft_path = f"{drafts_dir}/{llm_only}_draft_llm_v1.md"
        with open(draft_path, "w") as f:
            f.write(draft)
        
        print(f"\n✅ LLM draft saved: {draft_path}")
        print(f"   Size: {len(draft)} chars, {len(draft.splitlines())} lines")
        return
    
    summary = await engine.run_full_pipeline()
    
    print(f"\n{'='*60}")
    print(f"📋 FINAL SUMMARY")
    print(f"{'='*60}")
    print(f"Client: {summary['client']}")
    print(f"Year: FY{summary['report_year']}")
    print(f"Status: {summary['status']}")
    print(f"Phases: {summary['phases_completed']}/{summary['phases_total']}")
    print(f"Material matters: {summary['material_matters']}")
    print(f"Sections drafted: {len(summary['drafted_sections'])}")
    print(f"Quality score: {summary['quality_score']}/14")
    print(f"Verdict: {'✅ PASS' if summary['pass'] else '❌ FAIL'}")


def _show_status(client_dir: str, year: int):
    """Show current status of client reporting."""
    if not os.path.isdir(client_dir):
        print(f"❌ Client '{os.path.basename(client_dir)}' not initialized.")
        print(f"   Run: python -m csrd_agent.cli --client {os.path.basename(client_dir)} --init")
        return
    
    from report_engine import CSRDReportEngine
    from esrs_knowledge_base import count_datapoints
    
    engine = CSRDReportEngine(client_dir)
    engine.report_year = year
    
    counts = count_datapoints()
    
    print(f"📊 CSRD Agent Status")
    print(f"{'='*60}")
    print(f"Client: {os.path.basename(client_dir)}")
    print(f"FY: {year}")
    print(f"ESRS standards loaded: {counts['standards_loaded']}")
    print(f"Total datapoints: {counts['total_datapoints']}")
    print(f"Mandatory datapoints: {counts['mandatory_datapoints']}")
    print(f"Company profile: {'✅' if engine.company_profile.get('sector') != 'Unknown' else '❌ Not set'}")
    print(f"Drafts directory: {'✅' if os.path.isdir(f'{client_dir}/drafts') else 'empty'}")


if __name__ == "__main__":
    main()