"""Runner module for executing workflows based on DAGs.

This module contains functionality to run complete workflows by executing
each micro-app in the correct order and managing data flow between them.
Acts as a controller, directing each app where to pass its output.
"""

from .router import Router
from .dag_parser import DAGParser, DAGDefinition

__all__ = ["Router", "DAGParser", "DAGDefinition"]

