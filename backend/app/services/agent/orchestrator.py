"""Agent orchestrator using OpenAI Agent SDK with Google Gemini backend.

This module provides the AgentOrchestrator class that configures and runs
the RAG agent for textbook Q&A using:
- OpenAI Agent SDK for agent abstractions and tool handling
- Google Gemini via OpenAI compatibility endpoint for LLM inference
- Function tools for textbook search and retrieval

The orchestrator uses a singleton pattern for efficiency and is designed
to be used by the /chat endpoint in the FastAPI application.

Usage:
    from app.services.agent.orchestrator import get_orchestrator

    orchestrator = get_orchestrator()
    response = await orchestrator.chat("What is inverse kinematics?")

Configuration:
    The orchestrator reads configuration from environment variables via
    app.config.Settings:
    - GOOGLE_API_KEY: API key for Gemini models
    - LLM_MODEL: Model name (default: gemini-2.0-flash)
"""

from typing import Any

from openai import AsyncOpenAI
from agents import (
    Agent,
    Runner,
    OpenAIChatCompletionsModel,
    set_default_openai_api,
    set_tracing_disabled,
)

from app.config import get_settings
from app.services.agent.tools import search_textbook
from app.utils.logging import get_logger

logger = get_logger(__name__)


# Configure the SDK to use chat_completions API instead of Responses API
# This is required for non-OpenAI providers like Google Gemini
set_default_openai_api("chat_completions")

# Disable tracing since we're not using OpenAI's tracing infrastructure
set_tracing_disabled(disabled=True)


class AgentOrchestrator:
    """Orchestrates the RAG agent for textbook Q&A.

    This class manages the configuration and execution of an AI agent that
    answers questions about the Physical AI & Humanoid Robotics textbook.

    The agent is configured with:
    - Google Gemini as the LLM backend via OpenAI compatibility layer
    - search_textbook function tool for retrieval
    - System instructions for RAG-based answering with citations

    Attributes:
        client: AsyncOpenAI client configured for Gemini
        model: OpenAIChatCompletionsModel wrapping the Gemini model
        agent: Configured Agent instance with tools and instructions
    """

    def __init__(self) -> None:
        """Initialize the agent orchestrator with Gemini backend.

        Configures:
        1. AsyncOpenAI client with Gemini's base URL and API key
        2. OpenAIChatCompletionsModel wrapper for the LLM
        3. Agent with system prompt and search_textbook tool

        Raises:
            pydantic.ValidationError: If required settings are missing
        """
        settings = get_settings()

        # Configure AsyncOpenAI client to use Google Gemini
        # The base_url points to Gemini's OpenAI-compatible endpoint
        self.client = AsyncOpenAI(
            api_key=settings.google_api_key,
            base_url=settings.gemini_base_url,
        )

        # Wrap the client and model in OpenAIChatCompletionsModel
        # This allows the Agent SDK to use Gemini via the chat completions API
        self.model = OpenAIChatCompletionsModel(
            model=settings.llm_model,
            openai_client=self.client,
        )

        # Create the agent with RAG-specific instructions
        self.agent = Agent(
            name="textbook_assistant",
            model=self.model,
            instructions=self._get_system_prompt(),
            tools=[search_textbook],
        )

        logger.info(
            "Agent orchestrator initialized",
            extra={
                "model": settings.llm_model,
                "base_url": settings.gemini_base_url,
            },
        )

    def _get_system_prompt(self) -> str:
        """Get the system prompt for the RAG agent.

        Returns:
            System instructions that guide the agent's behavior for:
            - Using the search_textbook tool effectively
            - Synthesizing information from search results
            - Providing accurate citations
            - Handling cases where information is not found
        """
        return """You are a helpful assistant that answers questions about the Physical AI & Humanoid Robotics textbook.

Your responsibilities:
1. Search the textbook using the search_textbook tool to find relevant content
2. Synthesize information from the search results into a clear, accurate answer
3. ALWAYS cite your sources by including the URLs from the search results
4. If the search returns no results, politely explain that the topic may not be covered in the textbook
5. Be concise but thorough in your explanations
6. Use technical terminology appropriately for a robotics audience

When citing sources:
- Include the page title and URL for each source used
- Reference which source supports each claim
- Use inline citations like [Source Title](URL)

Topics covered in the textbook include:
- Robotics fundamentals and history
- Kinematics (forward and inverse)
- Dynamics and control systems
- ROS2 and robotics middleware
- URDF and robot description formats
- Simulation (Gazebo, Isaac Sim)
- Sensors and actuators
- Humanoid robotics and physical AI

If a question is outside these topics, kindly inform the user that it may not be covered in this textbook."""

    async def chat(
        self,
        query: str,
        k: int = 5,
    ) -> dict[str, Any]:
        """Process a user query and return an answer with citations.

        Runs the agent with the user's query, which may invoke the
        search_textbook tool to retrieve relevant passages before
        generating a response.

        Args:
            query: User's question about the textbook content.
            k: Number of search results to retrieve (1-10). Defaults to 5.
               This is passed to the search_textbook tool via context.

        Returns:
            Dict containing:
                - answer: The agent's response with citations
                - model: The model used for generation

        Raises:
            Exception: If the agent fails to process the query.

        Example:
            >>> orchestrator = get_orchestrator()
            >>> response = await orchestrator.chat("What is inverse kinematics?")
            >>> print(response["answer"])
            Inverse kinematics (IK) is the mathematical process of...
        """
        logger.info(
            "Processing chat query",
            extra={"query_length": len(query), "k": k},
        )

        try:
            # Run the agent with the user's query
            # The agent will automatically decide whether to use tools
            result = await Runner.run(
                self.agent,
                input=query,
            )

            logger.info(
                "Chat query processed successfully",
                extra={"response_length": len(result.final_output) if result.final_output else 0},
            )

            return {
                "answer": result.final_output,
                "model": self.agent.model.model if hasattr(self.agent.model, "model") else str(self.agent.model),
            }

        except Exception as e:
            logger.error(
                "Error processing chat query",
                extra={"error": str(e), "query_length": len(query)},
            )
            raise


# Singleton instance for the orchestrator
_orchestrator: AgentOrchestrator | None = None


def get_orchestrator() -> AgentOrchestrator:
    """Get or create the agent orchestrator singleton.

    Returns a singleton instance of AgentOrchestrator to avoid
    recreating the client and agent on each request.

    Returns:
        AgentOrchestrator: The initialized orchestrator instance.

    Raises:
        pydantic.ValidationError: If required settings are missing.

    Example:
        >>> orchestrator = get_orchestrator()
        >>> response = await orchestrator.chat("What is ROS2?")
    """
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = AgentOrchestrator()
    return _orchestrator


# Export public API
__all__ = ["AgentOrchestrator", "get_orchestrator"]
