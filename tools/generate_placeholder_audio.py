#!/usr/bin/env python3
"""Backward-compatible entry point — delegates to generate_game_audio.py."""
import runpy
import os

runpy.run_path(os.path.join(os.path.dirname(__file__), "generate_game_audio.py"), run_name="__main__")
