#!/usr/bin/env python3
"""Deprecated — use tools/generate_game_art.py (includes screenshots + trailer)."""
import runpy
import os

runpy.run_path(os.path.join(os.path.dirname(__file__), "generate_game_art.py"), run_name="__main__")
