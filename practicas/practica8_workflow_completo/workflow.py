#!/usr/bin/env python3
"""Práctica 8: Workflow Completo"""
import json, sys
from pathlib import Path
from datetime import datetime
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

with open('config.json') as f:
    config = json.load(f)

print("="*80)
print(f"PRÁCTICA 8: WORKFLOW COMPLETO - {config['proyecto']['nombre']}")
print("="*80)
print(f"Autor: {config['proyecto']['autor']}")
print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# TODO: Implementar workflow completo siguiendo el template de:
# plantillas/ejemplo_06_workflow_completo.py

print("📋 PASOS DEL WORKFLOW:")
for i, paso in enumerate(config['workflow']['pasos'], 1):
    print(f"  {i}. {paso}")

print(f"\n📂 Output: {config['workflow']['output_dir']}")
print("\n💡 Consulta ejemplo_06_workflow_completo.py en plantillas/")
