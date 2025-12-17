# Claude Code Subagents

This directory contains specialized Claude Code subagents for automating various tasks in the Physical AI & Humanoid Robotics Textbook project.

## Available Subagents

### Content & Documentation

| Agent | Purpose | Trigger Phrases |
|-------|---------|-----------------|
| **content-writer** | Generate educational Markdown chapters | "write a chapter", "create content", "draft section" |
| **translator** | Translate content to Roman Urdu | "translate to Roman Urdu", "convert to Urdu" |

### Knowledge Management

| Agent | Purpose | Trigger Phrases |
|-------|---------|-----------------|
| **librarian** | Ingest content into RAG knowledge base | "learn the book", "ingest docs", "update knowledge base" |

### Development

| Agent | Purpose | Trigger Phrases |
|-------|---------|-----------------|
| **backend-engineer** | FastAPI backend development | "create endpoint", "fix backend", "add API" |
| **frontend-specialist** | Docusaurus/React frontend work | "add component", "update UI", "style page" |
| **openai-sdk-expert** | OpenAI Agents SDK integration | "create agent", "add tool", "implement handoff" |
| **openai-agents-architect** | Agent architecture design | "design agent system", "refactor agents" |
| **chatkit-integration-engineer** | ChatKit UI integration | "add chat widget", "configure ChatKit" |

### DevOps & Configuration

| Agent | Purpose | Trigger Phrases |
|-------|---------|-----------------|
| **publisher** | Build and deploy Docusaurus site | "publish", "deploy", "go live" |
| **project-lead-agent-configurator** | Create/update agent definitions | "create agent", "update agent config" |

## Usage Examples

### Generate New Chapter
```
User: Write a new chapter on 'Introduction to ROS 2' for beginners

[content-writer agent is invoked]
```

### Translate Content
```
User: Translate the ROS 2 chapter to Roman Urdu

[translator agent is invoked]
```

### Update Knowledge Base
```
User: Librarian, please learn the new chapters in book/docs/

[librarian agent is invoked]
```

### Deploy Site
```
User: Publish the updated book to GitHub Pages

[publisher agent is invoked]
```

## Agent Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Claude Code CLI                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │  content-   │  │ translator  │  │  librarian  │         │
│  │   writer    │  │             │  │             │         │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘         │
│         │                │                │                 │
│         ▼                ▼                ▼                 │
│  ┌─────────────────────────────────────────────┐           │
│  │              book/docs/                      │           │
│  │         (Markdown Content)                   │           │
│  └─────────────────────────────────────────────┘           │
│                         │                                   │
│                         ▼                                   │
│  ┌─────────────────────────────────────────────┐           │
│  │           Qdrant Vector DB                   │           │
│  │         (RAG Knowledge Base)                 │           │
│  └─────────────────────────────────────────────┘           │
│                         │                                   │
│                         ▼                                   │
│  ┌─────────────────────────────────────────────┐           │
│  │            FastAPI Backend                   │           │
│  │   /chat  /personalize  /translate           │           │
│  └─────────────────────────────────────────────┘           │
│                         │                                   │
│  ┌─────────────┐       │                                   │
│  │  publisher  │───────┼─────────────────────┐             │
│  └─────────────┘       │                     │             │
│                        ▼                     ▼             │
│  ┌─────────────────────────────────────────────┐           │
│  │           Docusaurus Site                    │           │
│  │         (GitHub Pages)                       │           │
│  └─────────────────────────────────────────────┘           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Creating New Agents

To create a new subagent, use the **project-lead-agent-configurator**:

```
User: Create a new agent called 'quiz-generator' that creates practice quizzes from chapter content
```

Or manually create a file in `.claude/agents/` with this structure:

```markdown
---
name: agent-name
description: Brief description of when to use this agent
model: sonnet
color: blue
---

[Agent instructions and responsibilities]
```

## Best Practices

1. **Be Specific**: Use clear trigger phrases when invoking agents
2. **One Task at a Time**: Each agent specializes in one domain
3. **Verify Output**: Check agent output before committing changes
4. **Chain Agents**: Complex tasks may require multiple agents in sequence

## Related Resources

- [Claude Code Documentation](https://docs.anthropic.com/claude-code)
- [Project Constitution](../.specify/memory/constitution.md)
- [Spec-Driven Development Workflow](../specs/README.md)
