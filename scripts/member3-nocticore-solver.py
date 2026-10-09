"""Compatibility entry point for Member 3's evidence verifier."""
import runpy
from pathlib import Path
runpy.run_path(str(Path(__file__).resolve().parents[1]/'challenges/nhx06-nocticore/solution/solve.py'),run_name='__main__')
