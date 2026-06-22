"""CSRD Agent CLI — Typer command interface.

Usage:
    csrd kb summary               # Show knowledge base stats
    csrd dma assess --company "ACS Energy" --sector energy   # Run DMA
    csrd dma assess --company "ACS Energy" --sector energy --output report.json
    csrd roster                    # Show active agent roster
"""

from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from csrd_agent.esrs_knowledge_base.loader import get_knowledge_base
from csrd_agent.dma import DoubleMaterialityEngine, ImpactAssessment, FinancialAssessment, ImpactType, ImpactValence, RiskOpportunityType
from csrd_agent.agents.definitions import AGENTS, agent_roster

app = typer.Typer(help="CSRD Agent — Multi-agent compliance report generator")
console = Console()


# ── Knowledge Base Commands ──

@app.command()
def summary():
    """Show ESRS knowledge base summary."""
    kb = get_knowledge_base()
    s = kb.summary()

    console.print(Panel.fit("[bold cyan]CSRD ESRS Knowledge Base[/bold cyan]"))
    table = Table(title=f"Standards ({s['total_datapoints']} total datapoints)")
    table.add_column("Standard", style="cyan")
    table.add_column("Title", style="green")
    table.add_column("Category", style="yellow")
    table.add_column("Datapoints", style="white", justify="right")
    table.add_column("Mandatory", style="white", justify="right")

    for std in s["standards"]:
        table.add_row(
            std["standard"],
            std["title"],
            std["category"],
            str(std["datapoint_count"]),
            str(std["required_count"]),
        )

    console.print(table)
    console.print(f"[bold]Total:[/bold] {len(s['standards'])} standards, "
                  f"[bold]{s['total_datapoints']}[/bold] datapoints "
                  f"({s['mandatory_datapoints']} mandatory, "
                  f"{s['optional_datapoints']} optional)")


@app.command()
def standard(std_id: str):
    """Show details for a specific ESRS standard."""
    kb = get_knowledge_base()
    std = kb.get_standard(std_id)
    if not std:
        console.print(f"[red]Unknown standard: {std_id}[/red]")
        raise typer.Exit(1)

    console.print(Panel.fit(f"[bold cyan]{std.id} — {std.title}[/bold cyan]"))
    console.print(f"Category: {std.category} | Mandatory: {std.mandatory}")
    console.print(f"Datapoints: {len(std.datapoints)} ({len(std.required_datapoints)} required)")

    table = Table(title="Datapoints")
    table.add_column("ID", style="cyan")
    table.add_column("Disclosure", style="green")
    table.add_column("Type", style="yellow")
    table.add_column("Required", style="white", justify="center")
    table.add_column("XBRL Tag", style="dim")

    for dp in std.datapoints:
        table.add_row(
            dp.id,
            dp.disclosure[:70],
            dp.type,
            "✅" if dp.required else "⬜",
            dp.xbrl_tag or "",
        )

    console.print(table)


# ── Double Materiality Assessment Commands ──

@app.command()
def dma(
    company: str = typer.Option(..., "--company", "-c", help="Company name"),
    sector: str = typer.Option("general", "--sector", "-s",
                                help="Sector for heuristic scoring (energy, manufacturing, etc.)"),
    output: str = typer.Option(None, "--output", "-o", help="Save assessment JSON to path"),
):
    """Run double materiality assessment for a company."""
    console.print(f"[bold cyan]Double Materiality Assessment[/bold cyan] — {company} ({sector})")

    engine = DoubleMaterialityEngine(company)
    profile = {"sector": sector, "company_name": company}
    assessment = engine.assess_all(company_profile=profile, auto_score=True)

    # Summary panel
    s = assessment.summary()
    console.print(Panel.fit(
        f"[bold]Company:[/bold] {s['company']}\n"
        f"[bold]Date:[/bold] {s['assessment_date']}\n"
        f"[bold]Matters assessed:[/bold] {s['total_matters_assessed']}\n"
        f"[bold]Double material:[/bold] [red]{s['double_material']}[/red] | "
        f"[bold]Impact only:[/bold] {s['impact_only']} | "
        f"[bold]Financial only:[/bold] {s['financial_only']} | "
        f"[bold]Non-material:[/bold] {s['non_material']}\n"
        f"[bold]IRO entries:[/bold] {s['iro_count']}\n"
        f"[bold]Material standards:[/bold] {', '.join(s['material_standards'])}",
        title="Assessment Summary",
    ))

    # Material matters table
    table = Table(title="Material Sustainability Matters")
    table.add_column("Matter", style="cyan")
    table.add_column("Domain", style="green")
    table.add_column("Impact Score", style="yellow", justify="right")
    table.add_column("Financial Score", style="white", justify="right")
    table.add_column("Type", style="magenta")

    for r in assessment.material_matters:
        table.add_row(
            r.matter_name[:50],
            r.domain,
            f"{r.impact_materiality_score:.1f}",
            f"€{r.financial_materiality_score:,.0f}",
            r.materiality_type.replace("_", " ").title(),
        )

    console.print(table)

    if output:
        assessment.save(output)
        console.print(f"[green]Assessment saved to {output}[/green]")

    return assessment


# ── Agent Roster ──

@app.command()
def roster():
    """Show active CSRD agent roster."""
    console.print(Panel.fit("[bold cyan]CSRD Agent Roster[/bold cyan]"))

    table = Table()
    table.add_column("Agent", style="cyan")
    table.add_column("Role", style="green")
    table.add_column("Description", style="white")
    table.add_column("Active", style="yellow", justify="center")

    for agent in AGENTS:
        table.add_row(
            agent.name,
            agent.title,
            agent.description[:60],
            "✅" if agent.active else "❌",
        )

    console.print(table)
    console.print(f"\n[dim]{len(AGENTS)} agents loaded[/dim]")


# ── Pipeline Command ──

@app.command()
def pipeline(
    company: str = typer.Option(..., "--company", "-c", help="Company name"),
    sector: str = typer.Option("general", "--sector", "-s", help="Sector"),
):
    """Run full CSRD pipeline: DMA → Assessment → Summary."""
    console.print(f"[bold green]CSRD Pipeline: {company}[/bold green]")

    # Step 1: DMA
    console.print("\n[bold]Step 1:[/bold] Double Materiality Assessment...")
    engine = DoubleMaterialityEngine(company)
    profile = {"sector": sector}
    assessment = engine.assess_all(company_profile=profile, auto_score=True)
    s = assessment.summary()
    console.print(f"  → {s['double_material']} double material matters identified")

    # Step 2: Standards mapping
    console.print(f"[bold]Step 2:[/bold] Mapping material standards...")
    material_standards = s["material_standards"]
    kb = get_knowledge_base()
    for std_id in material_standards:
        std = kb.get_standard(std_id)
        if std:
            console.print(f"  → [cyan]{std.id}[/cyan]: {len(std.datapoints)} datapoints "
                         f"({len(std.required_datapoints)} mandatory)")

    # Step 3: Summary
    console.print(f"\n[bold]Step 3:[/bold] Report summary")
    table = Table()
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    table.add_row("Company", company)
    table.add_row("Sector", sector.title())
    table.add_row("Standards required", f"{len(material_standards)}")
    table.add_row("Total ESRS datapoints", str(kb.total_datapoints))
    table.add_row("Mandatory datapoints", str(len(kb.mandatory_datapoints)))
    table.add_row("IRO entries", str(s["iro_count"]))
    console.print(table)


# ── Main Entry ──

if __name__ == "__main__":
    app()