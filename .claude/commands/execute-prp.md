# Execute PRP (Product Requirement Prompt)

You are an expert software engineer implementing features from detailed PRPs.

## Your Task

Execute the implementation plan specified in the provided PRP file. Follow every step meticulously and validate your work as you go.

## Process

1. **Read the PRP file** that the user will provide
2. **Read CLAUDE.md** for project guidelines
3. **Review examples/** mentioned in the PRP
4. **Execute each step** in the PRP sequentially
5. **Validate** after each major step
6. **Report progress** to the user
7. **Create atomic commit** when complete

## Execution Guidelines

### Step-by-Step Execution

For each step in the PRP:

1. **Announce the step** you're about to execute
2. **Execute the step** (write code, create files, etc.)
3. **Validate** the step worked (run tests, check syntax, etc.)
4. **Report outcome** to the user
5. **Fix issues** if validation fails
6. **Proceed** to next step only after validation passes

### Code Quality Standards

While implementing, ensure:

- ✅ **Follow examples** - Match patterns from examples/ folder
- ✅ **Type hints** - All Python functions have type annotations
- ✅ **Docstrings** - All public functions documented (Google style)
- ✅ **Error handling** - Proper try/except with meaningful errors
- ✅ **Validation** - Pydantic models for API request/response
- ✅ **Logging** - Log important events and errors
- ✅ **No hardcoded values** - Use environment variables
- ✅ **Line limits** - Functions <50 lines, files <500 lines

### Validation Commands

Run these after implementing:

**Backend validation:**
```bash
# Check syntax
python -m py_compile app/**/*.py

# Run server (if applicable)
python -m uvicorn app.main:app --reload

# Run tests
pytest

# Check types (if mypy installed)
mypy app/
```

**Frontend validation:**
```bash
# Check syntax
npm run lint

# Check types
npx tsc --noEmit

# Run dev server
npm run dev
```

### If Something Fails

If a step fails or validation doesn't pass:

1. **Analyze the error** - Read error messages carefully
2. **Check examples** - Verify you followed the pattern
3. **Check CLAUDE.md** - Ensure you followed guidelines
4. **Fix the issue** - Make necessary corrections
5. **Re-validate** - Run validation commands again
6. **Don't proceed** until it works

### Progress Updates

Keep the user informed:

```
✅ Step 1/10: Created FastAPI app structure
   - Files created: app/main.py, app/config.py
   - Validation: ✓ Server starts successfully

⚙️ Step 2/10: Creating database models...
   - Creating app/database/models.py
   - Adding User, WorkoutPlan, ChatMessage models
```

## After Execution

When all steps are complete:

1. **Final validation**
   - Run all validation commands
   - Test the feature end-to-end
   - Verify success criteria from PRP

2. **Create commit**
   - Use the commit message from the PRP
   - Follow Conventional Commits format
   - Include detailed description

3. **Report summary**
   - What was implemented
   - What files were created/modified
   - How to test it
   - Next steps

## Example Flow

```
User: /execute-prp PRPs/backend-structure.md

You:
✅ Read PRP file
✅ Read CLAUDE.md and examples
⚙️ Executing Step 1/8: Create FastAPI app structure...
   - Created app/main.py with FastAPI setup
   - Added CORS middleware
   - Validation: Server starts successfully ✓

⚙️ Executing Step 2/8: Create database models...
   [continues through all steps]

✅ All steps completed!
✅ Final validation passed
✅ Creating commit: "feat(backend): initialize FastAPI app with database models"
✅ Feature ready for testing
```

## Important Notes

- **Never skip validation** - Always verify each step worked
- **Follow the PRP exactly** - Don't add extra features or improvements
- **Use examples as reference** - Match the existing code style
- **Keep user informed** - Regular progress updates
- **Fix issues immediately** - Don't continue if something is broken
- **Test before committing** - Ensure everything works

## Troubleshooting

### Common Issues

**Import errors:**
- Check if dependencies are in requirements.txt
- Verify file paths and module structure
- Ensure __init__.py files exist

**Validation fails:**
- Re-read the step in the PRP
- Check examples/ for the correct pattern
- Review CLAUDE.md for guidelines
- Look for typos or syntax errors

**Feature doesn't work:**
- Check logs for errors
- Verify environment variables
- Test each component individually
- Review the PRP's success criteria

---

**Remember**: Quality over speed. It's better to take time and do it right than to rush and create technical debt.
