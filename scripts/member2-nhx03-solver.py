"""Compatibility entry point for Member 2's challenge solver."""
import runpy
from pathlib import Path
runpy.run_path(str(Path(__file__).resolve().parents[1]/'challenges/nhx03-mirror-account/solution/solver.py'),run_name='__main__')
