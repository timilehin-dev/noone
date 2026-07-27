"""test_genome.py - Tests for the Genome dataclass."""

import pytest
from agents.core.genome import Genome


# =============================================================================
# 🧪 Test Genome Initialization
# =============================================================================

def test_genome_initialization():
    """Test that a Genome can be initialized with valid data."""
    genome = Genome(
        code="def add(a, b): return a + b",
        prompts=["Optimize this code."],
        memory={"count": 0},
        metadata={"version": "1.0"}
    )
    assert genome.code == "def add(a, b): return a + b"
    assert genome.prompts == ["Optimize this code."]
    assert genome.memory == {"count": 0}
    assert genome.metadata == {"version": "1.0"}


def test_genome_initialization_with_defaults():
    """Test that Genome can be initialized with default values."""
    genome = Genome(code="print('hello')")
    assert genome.code == "print('hello')"
    assert genome.prompts == []
    assert genome.memory == {}
    assert genome.metadata == {}


# =============================================================================
# ❌ Test Genome Validation
# =============================================================================

def test_genome_invalid_code():
    """Test that non-string code raises ValueError."""
    with pytest.raises(ValueError, match="`code` must be a string."):
        Genome(code=123)  # Not a string


def test_genome_invalid_prompts():
    """Test that non-list prompts raise ValueError."""
    with pytest.raises(ValueError, match="`prompts` must be a list of strings."):
        Genome(code="print('hello')", prompts="not a list")


def test_genome_invalid_memory():
    """Test that non-dict memory raises ValueError."""
    with pytest.raises(ValueError, match="`memory` must be a dictionary."):
        Genome(code="print('hello')", memory="not a dict")


def test_genome_invalid_metadata():
    """Test that non-dict metadata raises ValueError."""
    with pytest.raises(ValueError, match="`metadata` must be a dictionary."):
        Genome(code="print('hello')", metadata="not a dict")


# =============================================================================
# 🔄 Test Genome Methods
# =============================================================================

def test_genome_copy():
    """Test that copy() creates a deep copy of the genome."""
    genome = Genome(
        code="def add(a, b): return a + b",
        prompts=["Optimize this."],
        memory={"count": 0},
        metadata={"version": "1.0"}
    )
    genome_copy = genome.copy()

    # Modify the copy
    genome_copy.code = "def add(a, b): return sum([a, b])"
    genome_copy.prompts.append("New prompt.")
    genome_copy.memory["count"] = 1
    genome_copy.metadata["version"] = "2.0"

    # Original should be unchanged
    assert genome.code == "def add(a, b): return a + b"
    assert genome.prompts == ["Optimize this."]
    assert genome.memory == {"count": 0}
    assert genome.metadata == {"version": "1.0"}


def test_genome_update():
    """Test that update() returns a new genome with updated fields."""
    genome = Genome(
        code="def add(a, b): return a + b",
        prompts=["Optimize this."],
        memory={"count": 0},
        metadata={"version": "1.0"}
    )
    updated_genome = genome.update(
        code="def add(a, b): return sum([a, b])",
        memory={"count": 1}
    )

    # Check updated fields
    assert updated_genome.code == "def add(a, b): return sum([a, b])"
    assert updated_genome.memory == {"count": 1}

    # Check unchanged fields
    assert updated_genome.prompts == ["Optimize this."]
    assert updated_genome.metadata == {"version": "1.0"}


def test_genome_update_nonexistent_field():
    """Test that update() ignores nonexistent fields."""
    genome = Genome(code="print('hello')")
    updated_genome = genome.update(nonexistent_field="value")
    assert updated_genome.code == "print('hello')"
    assert not hasattr(updated_genome, "nonexistent_field")


# =============================================================================
# 🧩 Test Edge Cases
# =============================================================================

def test_genome_empty_prompts():
    """Test that empty prompts list is valid."""
    genome = Genome(code="print('hello')", prompts=[])
    assert genome.prompts == []


def test_genome_empty_memory():
    """Test that empty memory dict is valid."""
    genome = Genome(code="print('hello')", memory={})
    assert genome.memory == {}


def test_genome_empty_metadata():
    """Test that empty metadata dict is valid."""
    genome = Genome(code="print('hello')", metadata={})
    assert genome.metadata == {}


def test_genome_nested_memory():
    """Test that nested memory dictionaries are preserved."""
    genome = Genome(
        code="print('hello')",
        memory={"nested": {"key": "value"}}
    )
    assert genome.memory["nested"]["key"] == "value"


def test_genome_multiline_code():
    """Test that multiline code is preserved."""
    code = """def add(a, b):
    return a + b

print(add(1, 2))"""
    genome = Genome(code=code)
    assert genome.code == code
