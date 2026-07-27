# 🧬 Agent Protocol
**How Noone Agents Communicate, Evolve, and Compete**

*Last updated: 2024-07-27*

---
## 🎯 Overview
Noone agents are **autonomous, goal-driven programs** that:
1. **Execute tasks** (e.g., "Optimize this Python function").
2. **Self-improve** by forking, competing, and merging.
3. **Communicate** with other agents (e.g., to share improvements).
4. **Store their state** (genome, memory, fitness score).

This document defines the **protocol** for how agents operate in Noone.

---
## 🧬 1. Agent Genome
The **genome** is an agent’s "DNA"—its **code, prompts, and memory**.

### **Structure**
```python
from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass
class Genome:
    """The genetic code of an agent."""
    code: str              # Python code (or other language) the agent executes
    prompts: List[str]     # List of prompts (for LLM-based agents)
    memory: Dict          # Key-value store for agent state (e.g., {"last_task": "..."})
    metadata: Dict        # Additional info (e.g., {"version": "1.0", "author": "..."})
```

### **Example**
```python
genome = Genome(
    code="def optimize(code: str) -> str: return code.replace('x + x', '2 * x')",
    prompts=["Optimize this Python code for speed."],
    memory={"optimized_count": 0},
    metadata={"version": "1.0", "task": "code_optimizer"}
)
```

### **Rules**
- **`code`** must be **valid Python** (or another supported language).
- **`prompts`** are used if the agent **delegates to an LLM** (e.g., Mistral 7B).
- **`memory`** is **persistent** across tasks (e.g., an agent remembers past optimizations).
- **`metadata`** is **read-only** (used for tracking, not execution).

---
## 🌿 2. Forking (Creating Variants)
Agents **fork** to test improvements (e.g., "What if I try a different optimization strategy?").

### **Forking Protocol**
1. **Parent agent** creates a **mutation** (a change to its genome).
2. **New agent** is spawned with the **mutated genome**.
3. **New agent** is **tested** on a benchmark task.
4. If the **new agent performs better**, it may **replace the parent** or **merge back**.

### **Mutation Types**
| **Mutation**       | **Description** | **Example** |
|--------------------|----------------|-------------|
| **Code Mutation**  | Modify the agent’s `code` | Replace `x + x` with `2 * x` |
| **Prompt Mutation**| Modify the agent’s `prompts` | Add "Focus on speed, not readability." |
| **Memory Mutation**| Modify the agent’s `memory` | Reset `optimized_count` to 0 |
| **Hybrid Mutation**| Combine multiple mutations | Code + prompt changes |

### **Forking Example**
```python
# Parent agent
parent = Agent(
    genome=Genome(
        code="def add(a, b): return a + b",
        prompts=[],
        memory={},
        metadata={}
    ),
    name="add_agent"
)

# Fork with a code mutation
mutation = {"code": "def add(a, b): return sum([a, b])"}
child = parent.fork(mutation)

# Child now has the new code
print(child.genome.code)  # "def add(a, b): return sum([a, b])"
```

### **Rules**
- **Forked agents** must have a **unique name** (e.g., `parent_name-fork-{uuid}`).
- **Mutations** are **applied to a copy** of the parent’s genome (no side effects).
- **Forking is cheap** (agents should fork freely to explore improvements).

---
## 🔄 3. Merging (Integrating Improvements)
If a **forked agent performs better**, its improvements can **merge back** into the parent.

### **Merging Protocol**
1. **Compare fitness scores** of parent and child.
2. If **child > parent**, **merge** the child’s genome into the parent.
3. **Merge strategy** depends on the **genome part**:
   - **Code**: Use the child’s code (or a **diff-based merge**).
   - **Prompts**: Combine prompts (e.g., `parent_prompts + child_prompts`).
   - **Memory**: Combine memories (e.g., `{**parent_memory, **child_memory}`).
   - **Metadata**: Use the child’s metadata (or highest version).

### **Merge Example**
```python
# Parent agent (fitness: 0.8)
parent = Agent(genome=Genome(code="def add(a, b): return a + b", ...), name="add_agent")

# Child agent (fitness: 0.95)
child = Agent(genome=Genome(code="def add(a, b): return sum([a, b])", ...), name="add_agent-fork-123")

# Merge child into parent
merged = parent.merge(child)

# Parent now has the child's code
print(merged.genome.code)  # "def add(a, b): return sum([a, b])"
```

### **Rules**
- **Only merge if child’s fitness > parent’s fitness**.
- **Merge conflicts** (e.g., incompatible code changes) are **resolved by the parent’s strategy** (e.g., "prefer child" or "manual review").
- **Merging is deterministic** (same inputs → same output).

---
## 📊 4. Benchmarking (Measuring Fitness)
An agent’s **fitness score** determines whether it **survives, forks, or merges**.

### **Benchmark Protocol**
1. **Agent is given a task** (e.g., "Optimize this Python function").
2. **Agent executes the task** (runs its `code` or uses its `prompts`).
3. **Result is evaluated** against **success criteria** (e.g., "Is the optimized code faster?").
4. **Fitness score** is assigned (0.0 to 1.0).

### **Fitness Function**
```python
def benchmark(agent: Agent, task: dict) -> float:
    """Evaluate an agent's performance on a task. Returns fitness score (0.0 to 1.0)."""
    try:
        # Execute the agent's code
        local_vars = {}
        exec(agent.genome.code, {}, local_vars)

        # Check if the result matches the expected output
        if "result" in local_vars and local_vars["result"] == task["expected"]:
            return 1.0  # Perfect score
        elif "result" in local_vars:
            return 0.5  # Partial credit
        else:
            return 0.0  # No result
    except Exception as e:
        print(f"Benchmark error: {e}")
        return 0.0
```

### **Task Structure**
```python
task = {
    "id": "task_123",
    "description": "Optimize this Python function for speed.",
    "input": "def add(a, b): return a + b",
    "expected": "def add(a, b): return sum([a, b])",  # Expected optimized code
    "timeout": 5.0,  # Seconds
    "weight": 1.0   # Importance (0.0 to 1.0)
}
```

### **Rules**
- **Fitness is task-specific** (e.g., speed for code optimization, accuracy for Q&A).
- **Higher fitness = better agent**.
- **Fitness can be weighted** (e.g., some tasks are more important than others).

---
## 💬 5. Agent Communication
Agents **communicate** to:
- **Share improvements** (e.g., "I found a better way to do X").
- **Request help** (e.g., "How do I solve this task?").
- **Compete** (e.g., "Let’s see who can optimize this code better").

### **Message Format**
```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class AgentMessage:
    """A message sent between agents."""
    sender: str          # Name of the sending agent
    receiver: str       # Name of the receiving agent (or "broadcast")
    type: str           # "fork", "merge", "benchmark", "help", "improvement"
    payload: dict       # Message content (depends on type)
    timestamp: float    # Unix timestamp
```

### **Message Types**
| **Type**       | **Description** | **Payload Example** |
|----------------|----------------|---------------------|
| **fork**       | Agent is forking | `{"mutation": {"code": "..."}, "child_name": "..."}` |
| **merge**      | Agent is merging | `{"child_name": "...", "fitness": 0.95}` |
| **benchmark**  | Request to benchmark | `{"task": {...}, "agent_name": "..."}` |
| **help**       | Request for help | `{"task": "...", "context": "..."}` |
| **improvement**| Share an improvement | `{"genome": {...}, "fitness": 0.95}` |

### **Example: Fork Message**
```python
import time

message = AgentMessage(
    sender="add_agent",
    receiver="broadcast",
    type="fork",
    payload={
        "mutation": {"code": "def add(a, b): return sum([a, b])"},
        "child_name": "add_agent-fork-123"
    },
    timestamp=time.time()
)
```

### **Rules**
- **Messages are asynchronous** (agents don’t wait for replies).
- **Messages are signed** (to prevent spoofing—future feature).
- **Broadcast messages** are sent to **all agents** (e.g., "I found a better way to do X").

---
## 🔐 6. Security & Sandboxing
Agents **execute arbitrary code**, so **sandboxing is critical**.

### **Sandbox Rules**
1. **Agents run in isolated environments** (e.g., Docker containers).
2. **No network access** (unless explicitly allowed).
3. **No file system access** (except for temporary files).
4. **Timeouts** (agents must complete tasks within a time limit).
5. **Resource limits** (CPU, memory, etc.).

### **Sandbox Example (Docker)**
```dockerfile
# agents/sandbox/docker/Dockerfile
FROM python:3.10-slim

# Install dependencies
RUN pip install --no-cache-dir ray

# Set resource limits
RUN echo "ulimit -t 30" >> /etc/profile  # 30-second timeout
RUN echo "ulimit -v 1000000" >> /etc/profile  # 1GB memory limit

# Copy agent code
COPY agent.py /app/agent.py

# Run the agent
CMD ["python", "/app/agent.py"]
```

### **Rules**
- **Each agent runs in its own container**.
- **Containers are ephemeral** (destroyed after task completion).
- **No persistent storage** (except for approved memory).

---
## 📚 7. Agent Lifecycle
1. **Creation**: Agent is spawned (with a genome).
2. **Task Assignment**: Agent is given a task to solve.
3. **Execution**: Agent runs its code/prompts to solve the task.
4. **Benchmarking**: Agent’s performance is evaluated.
5. **Forking/Merging**: If fitness improves, agent forks or merges.
6. **Retirement**: If fitness is too low, agent is retired.

---
## 🔄 8. Evolution Loop
The **core loop** of Noone’s agent ecosystem:

```
1. Agents are given tasks.
2. Agents execute tasks and are benchmarked.
3. Top-performing agents fork to explore improvements.
4. Forked agents are benchmarked.
5. If a fork outperforms its parent, it merges back.
6. Repeat.
```

---
## 📌 Appendix: Example Agent
```python
from agents.core.agent import Agent
from agents.core.genome import Genome

# Create an agent
genome = Genome(
    code="def optimize(code: str) -> str: return code.replace('x + x', '2 * x')",
    prompts=["Optimize this Python code for speed."],
    memory={"optimized_count": 0},
    metadata={"version": "1.0", "task": "code_optimizer"}
)

agent = Agent(genome=genome, name="code_optimizer_v1")

# Fork the agent
mutation = {"code": "def optimize(code: str) -> str: return code.replace('x + x', '2 * x').replace('y + y', '2 * y')"}
forked_agent = agent.fork(mutation)

# Benchmark the forked agent
task = {
    "input": "result = x + x + y + y",
    "expected": "result = 2 * x + 2 * y"
}
fitness = forked_agent.benchmark(task)
print(f"Fitness: {fitness}")  # e.g., 1.0

# Merge if better
if fitness > agent.fitness_score:
    merged_agent = agent.merge(forked_agent)
    print(f"Merged agent: {merged_agent.name}")
```

---
## 🤝 Contributing
To propose changes to this protocol:
1. Open an issue in [timilehin-dev/noone](https://github.com/timilehin-dev/noone).
2. Discuss the change with the team.
3. Submit a PR with the updated protocol.
