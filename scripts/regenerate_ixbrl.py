#!/usr/bin/env python3
"""Regenerate iXBRL files for all clients with fixed generator."""
import os, sys, yaml
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ixbrl_export import iXBRLEngine

CLIENTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "clients")

for d in sorted(os.listdir(CLIENTS_DIR)):
    client_dir = os.path.join(CLIENTS_DIR, d)
    profile_path = os.path.join(client_dir, "company_profile.yaml")
    if not os.path.isfile(profile_path):
        continue
    
    with open(profile_path) as f:
        profile = yaml.safe_load(f)
    
    engine = iXBRLEngine(d, 2024, profile)
    result = engine.export_to_dir(os.path.join(client_dir, "xbrl"))
    print(f"✅ {d}: {result['fact_count']} facts -> {result['ixbrl_path']}")

print("\nAll done. Run: python3 scripts/xbrl_validator.py all")