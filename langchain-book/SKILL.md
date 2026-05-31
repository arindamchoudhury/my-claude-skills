---
name: langchain-book
description: >
  Use when writing, planning, or structuring a technical book about LangChain, LangGraph, AI agents,
  or LLM application development in Python. Triggers on: "write a chapter on", "plan a book about
  LangChain", "outline a book on AI agents", "write the introduction chapter", "write exercises for
  this chapter", "structure a LangChain tutorial book", "I want to write a book about LangGraph",
  "help me write a technical book on agents", or any request to create, draft, or review chapters,
  sections, code examples, or exercises for a LangChain/LangGraph/AI agents book.
---

# LangChain & AI Agents Book Writing Skill

## What this skill is for

Writing a technical, code-first book on LangChain, LangGraph, and AI agent development in Python.
Based on analysis of the leading books in this space (2024–2026):

- *Learning LangChain* — Oshin & Campos (O'Reilly, 2025)
- *Generative AI with LangChain* 2nd Ed — Auffarth & Kuligin (Packt, 2025)
- *AI Agents and Applications* — Infante (Manning, 2026)
- *Designing Multi-Agent Systems* — Dibia (2025)
- *Generative AI Design Patterns* — Lakshmanan & Hapke (2025)

---

## Proven Book Structure

Every successful LangChain book follows this 5-part arc. Adapt chapter count and depth to your target audience (beginner / intermediate / advanced).

```
Part 1 — Foundation          (what LangChain is, env setup, first call)
Part 2 — Core Components     (prompts, chains, memory, RAG, embeddings)
Part 3 — Agents              (tools, ReAct, custom tools, LangSmith)
Part 4 — LangGraph           (state machines, workflows, HITL, persistence)
Part 5 — Production & Scale  (multi-agent, MCP, deployment, eval, observability)
```

Each part ends with a **mini-project** that uses everything covered so far.
The final chapter is always a **capstone project** — a complete, production-ready agent.

---

## Standard Chapter Template

Every chapter follows this structure. Adapt the depth to the topic.

```markdown
# Chapter N: <Title>

## What you'll learn
- Bullet list of 3–5 concrete outcomes

## The problem we're solving
One paragraph framing — WHY this exists, what breaks without it.
Use a real-world scenario the reader has faced.

## Concept overview
Short prose (200–400 words). Use an analogy or diagram description.
Don't repeat what the code will show — explain what's happening beneath.

## Minimal working example
The simplest possible code that demonstrates the concept.
Always include: imports, env loading, and a runnable main block.

## Building up
2–4 progressively more complete examples.
Each example should add ONE new idea, not several at once.

## Under the hood (optional)
For non-obvious internals worth understanding.
Keep short — readers can skip this box.

## Real-world example
A practical scenario close to what the reader will actually build.
Must use current LangChain 1.x / LangGraph 1.x APIs.

## Common pitfalls
3–5 bullet points. Each: what goes wrong, why, how to fix it.

## Exercises
3 exercises: one recall, one apply, one extend.

## Summary
3–5 bullet points recapping what was covered.
Last sentence: what the next chapter builds on top of.
```

---

## Code Standards

All code in the book must follow these rules — this is what distinguishes
books that age well from ones that are stale on release day.

### Imports and setup
```python
# Always use the 1.x pattern
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

load_dotenv()

# NOT the old pattern (deprecated in 0.x):
# from langchain_openai import ChatOpenAI
# model = ChatOpenAI(model="gpt-4")
```

### Model initialization
```python
# Standard — works across OpenAI, Anthropic, Google
model = init_chat_model("gpt-5-nano")   # or "gpt-5.4-nano" for latest

# With options
model = init_chat_model("gpt-5-nano", temperature=0)
```

### Every code block must be:
- **Runnable** — copy-paste into a file and it runs
- **Version-pinned in comments** — add `# LangChain 1.3+` when using 1.x-only APIs
- **Complete** — include all imports, never truncate with `# ... rest of code`
- **Tested against current versions** — langchain>=1.3, langgraph>=1.2

### LCEL / Runnable chains (Part 2+)
```python
from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model

prompt = ChatPromptTemplate.from_template("Tell me about {topic}")
model  = init_chat_model("gpt-5-nano")
chain  = prompt | model
result = chain.invoke({"topic": "LangChain"})
```

### LangGraph (Part 4+)
```python
from langgraph.graph import StateGraph, END
from typing import TypedDict

class State(TypedDict):
    messages: list

graph = StateGraph(State)
# Add nodes, edges, compile
```

---

## Audience Calibration

Before writing any chapter, establish which reader you're writing for:

| Level | Background | Entry point | Tone |
|---|---|---|---|
| **Beginner** | Python but no LLMs | Chapter 1 from scratch | Patient, analogy-heavy |
| **Intermediate** | Used OpenAI API directly | Start from chains/LCEL | Efficient, show patterns |
| **Advanced** | Built LLM apps before | Focus on LangGraph, production | Peer-to-peer, tradeoff-focused |

State the target level explicitly at the start of each chapter draft.

---

## Writing Process (follow in order)

### Step 1 — Outline the chapter
Before writing prose, produce:
1. The "problem we're solving" paragraph
2. Bullet list of all code examples (name + what it demonstrates)
3. Bullet list of pitfalls to cover
4. The 3 exercises

Get user sign-off on the outline before writing the full chapter.

### Step 2 — Write the code first
Write every code example before writing any surrounding prose.
Run it mentally against the current API. Flag anything that needs verification.
Use the code as the skeleton — prose explains what the code shows.

### Step 3 — Write the prose
Fill in around the code. Keep prose tight:
- One idea per paragraph
- No restating what the code already shows
- Use bold for the first mention of every new term

### Step 4 — Write the exercises
Three tiers:
1. **Recall** — "What does X return when Y?" (can answer from reading)
2. **Apply** — "Modify the example to do Z" (requires running code)
3. **Extend** — "Build a small feature that..." (open-ended, no single answer)

### Step 5 — Version check
Flag any API or import that might change. Add inline comments like:
```python
# API stable as of langchain 1.3 / langgraph 1.2 (May 2026)
```

---

## Standard Part / Chapter Map

Use this as the default skeleton. Add or remove chapters based on scope.

### Part 1: Foundation
- Ch 1: What Is LangChain? (ecosystem overview, when to use it, setup)
- Ch 2: Your First LLM Call (init_chat_model, invoke, stream, batch)
- Ch 3: Prompt Templates (ChatPromptTemplate, system/human messages, few-shot)
- Ch 4: Output Parsers (StrOutputParser, JSON, Pydantic structured output)

### Part 2: Core Components
- Ch 5: LCEL and Chains (pipe operator, Runnable interface, composition)
- Ch 6: Conversation Memory (message history, trimming, summarization)
- Ch 7: Embeddings and Vector Stores (OpenAIEmbeddings, Chroma, FAISS)
- Ch 8: Document Loading and Splitting (loaders, RecursiveCharacterTextSplitter)
- Ch 9: RAG — Retrieval-Augmented Generation (retrievers, full RAG chain)

### Part 3: Agents
- Ch 10: What Are Agents? (ReAct loop, planning, observation)
- Ch 11: Built-in Tools (Tavily search, Python REPL, calculator)
- Ch 12: Custom Tools (@tool decorator, StructuredTool, tool schemas)
- Ch 13: Debugging with LangSmith (tracing, evaluating, fixing)
- Mini-project: Personal Research Agent

### Part 4: LangGraph
- Ch 14: Introduction to LangGraph (state, nodes, edges, compile)
- Ch 15: Conditional Routing (conditional_edges, branching logic)
- Ch 16: Persistence and Checkpointing (MemorySaver, thread_id)
- Ch 17: Human-in-the-Loop (interrupt_before, interrupt_after, resume)
- Ch 18: Streaming and Async (astream, astream_events)
- Mini-project: Multi-step Research and Writing Agent

### Part 5: Production and Scale
- Ch 19: Multi-Agent Systems (supervisor pattern, handoffs, subgraphs)
- Ch 20: Model Context Protocol / MCP (langchain-mcp-adapters, uvx servers)
- Ch 21: Evaluation and Testing (LangSmith evals, pytest for agents)
- Ch 22: Deployment and Observability (LangGraph API, LangSmith monitoring)
- Capstone: Production Email Assistant Agent (end-to-end)

---

## LangChain Ecosystem Reference (May 2026)

Key packages, current versions, and what they're for:

| Package | Version | Purpose |
|---|---|---|
| `langchain` | 1.3.2 | Core framework, init_chat_model |
| `langchain-core` | 1.4.0 | Base interfaces, LCEL, Runnables |
| `langchain-openai` | 1.2.2 | OpenAI models |
| `langchain-anthropic` | 1.4.4 | Claude models |
| `langchain-google-genai` | 4.2.4 | Gemini models |
| `langchain-tavily` | 0.2.18 | Tavily search tool |
| `langchain-community` | 0.4.2 | Community integrations (being sunset) |
| `langgraph` | 1.2.2 | Agent/workflow orchestration |
| `langsmith` | 0.8.6 | Tracing, evaluation, monitoring |
| `langchain-mcp-adapters` | 0.2.2 | MCP server integration |

Python: 3.12 or 3.13 (3.14 not yet supported by LangChain — issue #34441).
Primary model: `gpt-5-nano` (very inexpensive). Newer: `gpt-5.4-nano` (March 2026).

---

## Common Patterns Worth a Chapter or Section

These appear in every major LangChain book — include at least one example of each:

**RAG pipeline** — the most-requested pattern
```
load docs → split → embed → store → retrieve → prompt → generate
```

**ReAct agent loop** — foundation of all agents
```
thought → action → observation → thought → ... → answer
```

**LangGraph state machine** — foundation of production agents
```
state → node → conditional edge → node → END
```

**Supervisor multi-agent**
```
supervisor → delegate to specialist agent → collect result → next agent or END
```

**Human-in-the-loop**
```
agent runs → hits checkpoint → pauses → human reviews/edits → resumes
```

---

## Anti-patterns to Avoid

- **Don't use deprecated 0.x imports** — `from langchain_openai import ChatOpenAI` without `init_chat_model` wrapper
- **Don't skip environment setup** — every chapter that uses API keys must show `load_dotenv()`
- **Don't write untested code** — flag any example you're not certain compiles
- **Don't explain what the code says** — prose explains WHY, not WHAT
- **Don't write exercises with a single right answer for "Extend"** — keeps the book fresh for readers at different levels
- **Don't mix 0.x and 1.x patterns** in the same book
- **Don't ignore LangSmith** — at minimum mention it when debugging becomes non-trivial
