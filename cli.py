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
    
    args = parser.parse_args()
    
    client_dir = os.path.join(os.path.dirname(__file__), "clients", args.client)
    
    if args.init:
        _init_client(client_dir, args.year, args.profile)
        return
    
    if args.full_pipeline:
        asyncio.run(_run_pipeline(client_dir, args.year))
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


async def _run_pipeline(client_dir: str, year: int):
    """Run full CSRD reporting pipeline."""
    from report_engine import CSRDReportEngine
    
    engine = CSRDReportEngine(client_dir)
    engine.report_year = year
    
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