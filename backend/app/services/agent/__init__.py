"""Agent orchestration service using OpenAI Agent SDK with Gemini.

This package provides:
- orchestrator: Agent configuration and execution with Gemini backend
- tools: Function tools for textbook search and retrieval

Components:
    - search_textbook: Function tool for semantic textbook search
    - AgentOrchestrator: Main agent orchestration class
    - get_orchestrator: Singleton factory for the orchestrator

Usage:
    from app.services.agent import get_orchestrator

    orchestrator = get_orchestrator()
    response = await orchestrator.chat("What is inverse kinematics?")
"""

from app.services.agent.orchestrator import AgentOrchestrator, get_orchestrator
from app.services.agent.tools import search_textbook

__all__ = ["AgentOrchestrator", "get_orchestrator", "search_textbook"]
