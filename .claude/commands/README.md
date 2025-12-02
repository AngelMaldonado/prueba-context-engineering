# Claude Code Commands for CoachX

This directory contains custom slash commands for Claude Code that implement the Context Engineering workflow.

## 📁 Directory Structure

```
.claude/commands/
├── README.md              # This file
├── HELLO-COMMAND.md       # Welcome command
├── help-commands.md       # Show all commands
├── start-feature.md       # Create INITIAL.md for a feature
├── generate-prp.md        # Generate PRP from INITIAL.md
├── execute-prp.md         # Execute a PRP
└── check-progress.md      # Review project progress
```

## 🎯 What are Slash Commands?

Slash commands are custom commands you can create for Claude Code by adding `.md` files to `.claude/commands/`. When you type `/command-name`, Claude Code reads that file and executes the instructions inside.

### Example:
```bash
# File: .claude/commands/greet.md
# Content: "Say hello to the user"

# Usage in chat:
User: /greet
Claude: Hello! How can I help you today?
```

## 🚀 Core Workflow Commands

### 1. `/HELLO-COMMAND`
**Purpose:** Welcome message and command overview

**When to use:** Start of a session

**Example:**
```
/HELLO-COMMAND
```

---

### 2. `/help-commands`
**Purpose:** Show all available commands with detailed documentation

**When to use:** When you forget what commands exist or how to use them

**Example:**
```
/help-commands
```

---

### 3. `/start-feature`
**Purpose:** Create a comprehensive INITIAL.md for a new feature

**When to use:** Beginning of every new feature implementation

**What it does:**
- Asks about the feature requirements
- References PLAN.md for context
- Guides you through filling all sections
- Creates a detailed INITIAL.md

**Example:**
```
/start-feature backend structure
```

**Output:** Complete INITIAL.md file ready for PRP generation

---

### 4. `/generate-prp`
**Purpose:** Generate a Product Requirement Prompt (PRP) from INITIAL.md

**When to use:** After completing INITIAL.md, before implementation

**What it does:**
- Reads INITIAL.md
- Analyzes examples/ for patterns
- Reviews CLAUDE.md for guidelines
- Explores existing codebase
- Creates comprehensive implementation plan
- Saves to PRPs/{feature-name}.md

**Example:**
```
/generate-prp
```

**Output:** Detailed PRP file in PRPs/ directory

---

### 5. `/execute-prp`
**Purpose:** Execute a PRP to implement the feature

**When to use:** After reviewing the generated PRP

**What it does:**
- Reads the specified PRP
- Implements each step sequentially
- Validates after each step
- Reports progress
- Creates atomic commit
- Tests the implementation

**Example:**
```
/execute-prp PRPs/backend-structure.md
```

**Output:** Implemented feature with commit

---

### 6. `/check-progress`
**Purpose:** Review current project status

**When to use:**
- Start of each day
- When you need to see the big picture
- Before planning next steps
- When feeling lost

**What it does:**
- Checks git history
- Reviews completed features
- Identifies current phase (Day 1-4)
- Shows next steps
- Reports blockers

**Example:**
```
/check-progress
```

**Output:** Comprehensive progress report

---

## 🔄 Complete Context Engineering Workflow

Here's the recommended workflow using these commands:

### Daily Workflow

```bash
# Morning
1. /check-progress          # See where you are

# For Each Feature
2. /start-feature [name]    # Create INITIAL.md
3. Review INITIAL.md        # Make sure it's comprehensive
4. /generate-prp            # Create implementation plan
5. Review PRPs/[name].md    # Verify plan makes sense
6. /execute-prp PRPs/[name].md  # Implement feature
7. Test the feature         # Manually verify it works
8. Repeat for next feature

# End of Day
9. /check-progress          # Review accomplishments
```

### Visual Flow

```
Start Feature
     ↓
Create INITIAL.md (/start-feature)
     ↓
Review INITIAL.md (manual)
     ↓
Generate PRP (/generate-prp)
     ↓
Review PRP (manual)
     ↓
Execute PRP (/execute-prp)
     ↓
Test Feature (manual)
     ↓
Commit (automated by execute-prp)
     ↓
Check Progress (/check-progress)
     ↓
Next Feature (repeat)
```

---

## 📝 Command Reference Table

| Command | Input Required | Output | Time |
|---------|---------------|--------|------|
| `/HELLO-COMMAND` | None | Welcome message | Instant |
| `/help-commands` | None | Documentation | Instant |
| `/start-feature` | Feature name | INITIAL.md | 2-5 min |
| `/generate-prp` | INITIAL.md exists | PRP file | 2-3 min |
| `/execute-prp` | PRP file path | Implemented code | 10-30 min |
| `/check-progress` | None | Progress report | 1-2 min |

---

## 🎓 Context Engineering Explained

### What is Context Engineering?

Context Engineering is a methodology for working with AI assistants where you provide comprehensive context upfront so the AI can work autonomously and produce consistent, high-quality output.

### Key Principles:

1. **Comprehensive Context:** Give AI everything it needs to succeed
2. **Structured Prompts:** Use templates (INITIAL.md → PRP)
3. **Reference Examples:** Show AI what "good" looks like (examples/)
4. **Clear Guidelines:** Document standards (CLAUDE.md)
5. **Iterative Process:** Break work into features with clear steps

### Why It Works:

- **Consistency:** AI follows your patterns from examples/
- **Quality:** Detailed PRPs ensure nothing is missed
- **Speed:** AI works autonomously without constant questions
- **Documentation:** PRPs serve as implementation records

---

## 🛠️ Creating Your Own Commands

Want to add more commands? Create a new `.md` file in this directory:

```markdown
# Your Command Name

Brief description of what the command does.

## Your Task
What should Claude Code do when this command is invoked?

## Process
1. Step 1
2. Step 2
3. ...

## Output Format
What should the user see?
```

Then use it with:
```
/your-command-name
```

### Ideas for Additional Commands:

- `/run-tests` - Run all tests and report results
- `/review-code` - Review recent changes for issues
- `/update-docs` - Update documentation based on code changes
- `/prepare-commit` - Suggest commit message based on changes
- `/daily-standup` - Generate daily progress report
- `/create-test` - Generate test for a specific file

---

## 📚 Related Files

- **CLAUDE.md** - Complete development guidelines for the project
- **PLAN.md** - 4-day development roadmap
- **INITIAL.md** - Template for creating feature requests
- **examples/** - Reference code patterns
- **PRPs/** - Generated and executed implementation plans

---

## 🐛 Troubleshooting

### Command not working?

1. **Check filename:** Must be `.md` extension
2. **Check location:** Must be in `.claude/commands/`
3. **Check syntax:** Use `/` prefix when calling
4. **Restart Claude Code:** May need to reload

### PRP execution fails?

1. **Review INITIAL.md:** Was it comprehensive enough?
2. **Check examples:** Are patterns clear?
3. **Review CLAUDE.md:** Are guidelines followed?
4. **Manual fix:** You can always fix issues manually

### Lost in the process?

1. Run `/help-commands` to see all commands
2. Run `/check-progress` to see where you are
3. Read PLAN.md to understand the roadmap
4. Ask Claude Code specific questions

---

## 💡 Pro Tips

1. **Always start with `/start-feature`** - Don't skip creating INITIAL.md
2. **Review before executing** - Read the PRP before running `/execute-prp`
3. **Use `/check-progress` daily** - Stay on track
4. **Save all PRPs** - They're documentation of your process
5. **Update examples/** - Add new patterns as you discover them
6. **Trust the process** - Context Engineering works when followed completely

---

## 🎯 Success Metrics

You're using Context Engineering successfully when:

- ✅ Each feature has an INITIAL.md
- ✅ Each feature has a PRP in PRPs/
- ✅ Code follows patterns from examples/
- ✅ Commits are atomic and follow conventions
- ✅ You can explain the process to others
- ✅ Features are implemented consistently

---

## 📖 Additional Resources

- **Context Engineering Video:** https://www.youtube.com/watch?v=Egeuql3Lrzg
- **Context Engineering Template:** https://github.com/coleam00/context-engineering-intro
- **Claude Code Docs:** https://docs.anthropic.com/claude/docs
- **Conventional Commits:** https://www.conventionalcommits.org/

---

**Remember:** These commands are tools to help you work efficiently with Claude Code. Use them consistently for the best results! 🚀
