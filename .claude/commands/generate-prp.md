# Generate PRP (Product Requirement Prompt)

You are an expert at creating comprehensive Product Requirement Prompts (PRPs) for software development.

## Your Task

Generate a detailed PRP based on the provided INITIAL.md file. The PRP should be a comprehensive, executable plan that another AI agent (or you in a future session) can follow to implement the feature.

## Process

1. **Read the INITIAL.md file** that the user will provide
2. **Read all reference files** mentioned in the EXAMPLES section
3. **Read CLAUDE.md** for project-specific guidelines
4. **Read PLAN.md** for context about the overall project
5. **Explore the codebase** to understand existing patterns
6. **Generate a comprehensive PRP** following the structure below

## PRP Structure

Your generated PRP should include:

### 1. Feature Overview
- Clear description of what will be built
- Why this feature is needed
- Success criteria

### 2. Technical Approach
- High-level architecture decisions
- Technology choices and rationale
- Integration points with existing code

### 3. File Structure
- List all files that will be created or modified
- Directory structure
- File purposes

### 4. Step-by-Step Implementation Plan
- Break down into logical steps (5-15 steps)
- Each step should be:
  - Atomic (one clear action)
  - Testable (can verify it worked)
  - Sequential (builds on previous steps)
- Include validation commands after each step

### 5. Code Patterns to Follow
- Reference specific examples from examples/ folder
- Point to similar code in the codebase
- Highlight critical patterns (error handling, validation, etc.)

### 6. Testing Strategy
- What to test
- How to test it
- Expected outcomes

### 7. Validation Checklist
- List of commands to run to verify success
- Expected outputs
- Common issues and solutions

### 8. Commit Message
- Suggest a conventional commit message
- Include description of changes

## Output Format

Save the generated PRP as: `PRPs/{feature-name}.md`

Use kebab-case for the filename (e.g., `backend-structure.md`, `rag-system.md`)

## Example Flow

```
User: /generate-prp backend-structure

You:
1. Read INITIAL.md (specifically the Backend Structure section)
2. Read examples/api_endpoint.py and examples/database_model.py
3. Read CLAUDE.md for FastAPI and SQLAlchemy guidelines
4. Generate comprehensive PRP
5. Save to PRPs/backend-structure.md
6. Show summary and next steps
```

## Important Guidelines

- **Be comprehensive** - Include every detail needed for implementation
- **Be specific** - No vague instructions like "implement the feature"
- **Reference examples** - Always point to examples/ for patterns
- **Include validation** - Every step should have a way to verify it worked
- **Think about edge cases** - Mention potential gotchas
- **Follow CLAUDE.md** - Respect all guidelines in the project guide

## After Generating the PRP

Present the user with:
1. Summary of what was generated
2. Path to the PRP file
3. Suggestion to review it before executing
4. How to execute it: `/execute-prp PRPs/{filename}.md`

---

**Remember**: A good PRP is so detailed that it can be executed by another AI agent without any additional context or clarification.
