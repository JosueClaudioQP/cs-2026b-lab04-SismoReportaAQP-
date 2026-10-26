"""Lanzador portable para Windows, Linux y macOS."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from reportes.demo_lab07 import main
main()
