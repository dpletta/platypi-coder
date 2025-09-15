"""
Agentic Coder MCP Server - Agent Framework

This module provides the core framework for building specialized coding agents
that can collaborate in an ensemble configuration.
"""

from .base_agent import BaseAgent
from .agent_manager import AgentManager
from .planner_agent import PlannerAgent
from .coder_agent import CoderAgent
from .reviewer_agent import ReviewerAgent
from .debugger_agent import DebuggerAgent
from .tester_agent import TesterAgent

__all__ = [
    'BaseAgent',
    'AgentManager', 
    'PlannerAgent',
    'CoderAgent',
    'ReviewerAgent',
    'DebuggerAgent',
    'TesterAgent'
]