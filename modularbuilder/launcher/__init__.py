"""Launcher module for discovering and launching applications.

This module provides functionality to discover all applications in a given
directory and launch them as background services. In future versions, it will
coordinate with the runner to manage application lifecycles based on DAGs.
"""

from .app_launcher import AppLauncher
from .cli import main

__all__ = ["AppLauncher", "main"]