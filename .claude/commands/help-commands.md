# Help - Claude Code Commands for CoachX

Show all available custom commands and how to use them.

## Available Commands

### 🚀 Core Context Engineering Workflow

#### `/start-feature`
Start a new feature by creating a comprehensive INITIAL.md file.

**Usage:**
```
/start-feature backend structure
/start-feature rag system
/start-feature onboarding flow
```

**What it does:**
- Guides you through creating INITIAL.md
- Asks relevant questions
- References PLAN.md for context
- Ensures all sections are filled

---

#### `/generate-prp`
Generate a Product Requirement Prompt (PRP) from an INITIAL.md file.

**Usage:**
```
/generate-prp
```

**What it does:**
- Reads your INITIAL.md
- Reviews examples/ for patterns
- Reads CLAUDE.md for guidelines
- Creates comprehensive implementation plan
- Saves to PRPs/{feature-name}.md

**When to use:** After completing INITIAL.md and before implementation

---

#### `/execute-prp`
Execute a PRP to implement a feature.

**Usage:**
```
/execute-prp PRPs/backend-structure.md
/execute-prp PRPs/rag-system.md
```

**What it does:**
- Reads the specified PRP
- Implements step-by-step
- Validates after each step
- Creates atomic commit when done
- Reports progress throughout

**When to use:** After reviewing the generated PRP

---

### 📊 Progress & Planning

#### `/check-progress`
Review current project status and progress.

**Usage:**
```
/check-progress
```

**What it does:**
- Checks git history
- Reviews completed features
- Identifies current phase
- Shows next steps
- Reports any blockers

**When to use:**
- Start of each day
- When you need to see the big picture
- Before planning next steps

---

## 🎯 Complete Workflow Example

Here's how to use these commands together:

### Step 1: Start a Feature
```
You: /start-feature backend structure

Claude: Let me help you create INITIAL.md for Backend Structure...
[Interactive questions and file creation]

Claude: ✅ INITIAL.md created! Next: /generate-prp
```

### Step 2: Generate PRP
```
You: /generate-prp

Claude: Reading INITIAL.md...
Reading examples/api_endpoint.py...
Reading CLAUDE.md...
Generating comprehensive PRP...

✅ PRP created: PRPs/backend-structure.md
📝 Review it, then run: /execute-prp PRPs/backend-structure.md
```

### Step 3: Review & Execute
```
You: [Reviews PRPs/backend-structure.md]
You: /execute-prp PRPs/backend-structure.md

Claude: ⚙️ Step 1/8: Creating FastAPI app structure...
✅ Step 1/8: Complete
⚙️ Step 2/8: Creating database models...
[Continues through all steps]

✅ All steps complete!
✅ Commit created: feat(backend): initialize FastAPI app
```

### Step 4: Check Progress
```
You: /check-progress

Claude:
# CoachX Progress Report
**Phase**: Day 2 - Backend Core
**Completed**: 1/3 features
...
```

---

## 💡 Tips for Success

### DO:
- ✅ Use `/start-feature` for every new feature
- ✅ Review generated PRPs before executing
- ✅ Use `/check-progress` daily
- ✅ Follow the workflow sequentially
- ✅ Read CLAUDE.md if unsure about patterns

### DON'T:
- ❌ Skip steps in the workflow
- ❌ Execute PRPs without reviewing them
- ❌ Create code without a PRP
- ❌ Forget to validate after implementation

---

## 🔍 Quick Reference

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/start-feature` | Create INITIAL.md | Starting new feature |
| `/generate-prp` | Create implementation plan | After INITIAL.md |
| `/execute-prp` | Implement feature | After reviewing PRP |
| `/check-progress` | See status | Daily / when stuck |
| `/help-commands` | Show this help | When you forget commands |

---

## 📚 Additional Resources

- **CLAUDE.md** - Complete development guidelines
- **PLAN.md** - 4-day development roadmap
- **INITIAL.md** - Template for feature requests
- **examples/** - Code patterns to follow
- **PRPs/** - Generated implementation plans

---

## 🆘 Need Help?

If you're stuck:
1. Read CLAUDE.md for guidelines
2. Check examples/ for patterns
3. Review PLAN.md for context
4. Use `/check-progress` to see where you are
5. Ask me specific questions!

---

**Remember**: Context Engineering is about giving AI comprehensive context. These commands automate that process. Use them consistently for best results! 🚀
