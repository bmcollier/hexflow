"""Skeletons module containing base application templates.

This module provides base classes and templates that can be extended
to create new micro-apps following standardized patterns. Currently
includes templates for http_base, casa, display, and processor applications.
"""

from . import http_base, casa, display

__all__ = ["http_base", "casa", "display"]