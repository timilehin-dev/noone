"""genome.py - The genetic code of a Noone agent."""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional

@dataclass
class Genome:
    """The genetic code of an agent.

    Attributes:
        code: Python code (or other language) the agent executes.
        prompts: List of prompts for LLM-based agents.
        memory: Key-value store for agent state (persists across tasks).
        metadata: Additional info (e.g., version, author). Read-only.
    """
    code: str
    prompts: List[str] = field(default_factory=list)
    memory: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate genome on initialization."""
        if not isinstance(self.code, str):
            raise ValueError("`code` must be a string.")
        if not isinstance(self.prompts, list):
            raise ValueError("`prompts` must be a list of strings.")
        if not isinstance(self.memory, dict):
            raise ValueError("`memory` must be a dictionary.")
        if not isinstance(self.metadata, dict):
            raise ValueError("`metadata` must be a dictionary.")

    def copy(self) -> 'Genome':
        """Create a deep copy of the genome."""
        return Genome(
            code=self.code,
            prompts=self.prompts.copy(),
            memory=self.memory.copy(),
            metadata=self.metadata.copy()
        )

    def update(self, **kwargs) -> 'Genome':
        """Return a new genome with updated fields."""
        new_genome = self.copy()
        for key, value in kwargs.items():
            if hasattr(new_genome, key):
                setattr(new_genome, key, value)
        return new_genome
