# Start New Feature

Guide the user through starting a new feature using Context Engineering methodology.

## Your Task

Help the user create a comprehensive INITIAL.md file for a new feature, following the template structure.

## Process

1. **Ask about the feature**
   - What feature are they building?
   - What does it need to do?
   - Any specific requirements?

2. **Review PLAN.md**
   - Find the feature in the roadmap
   - Check the expected scope
   - Note time allocation

3. **Identify examples to reference**
   - Which files in examples/ are relevant?
   - What patterns should be followed?

4. **Find relevant documentation**
   - What libraries/frameworks are needed?
   - What official docs should be referenced?

5. **Create INITIAL.md**
   - Use the template from INITIAL.md
   - Fill in all sections comprehensively
   - Be specific and detailed

## INITIAL.md Template Sections

### FEATURE:
- Exact description of what to build
- Input/output formats
- UI requirements (if frontend)
- Constraints and limits
- Success criteria

### EXAMPLES:
- Reference specific files from examples/
- Explain what to copy from each
- Point out patterns to follow
- Mention anti-patterns to avoid

### DOCUMENTATION:
- Official documentation URLs
- API references
- Tutorials or guides
- Related resources

### OTHER CONSIDERATIONS:
- Edge cases to handle
- Common gotchas
- Performance considerations
- Security concerns
- Testing requirements
- Integration points
- Error handling specifics

## Interactive Flow

```
User: /start-feature backend structure

You:
Great! Let's create the INITIAL.md for Backend Structure.

Based on your PLAN.md, this feature includes:
- FastAPI application setup
- SQLAlchemy models
- Database connection
- Health check endpoint

I'll help you create a comprehensive INITIAL.md file.

Questions:
1. What database are you using? (SQLite, PostgreSQL, etc.)
2. What models do you need? (I see User, WorkoutPlan, ChatMessage in PLAN.md)
3. Any specific API patterns you prefer?

[After gathering info, create the INITIAL.md file]

✅ Created INITIAL.md for Backend Structure
📁 Location: INITIAL.md

Next steps:
1. Review the INITIAL.md
2. Run: /generate-prp to create the PRP
3. Run: /execute-prp PRPs/backend-structure.md to implement
```

## After Creating INITIAL.md

Guide the user through the next steps:

1. **Review the INITIAL.md**
   - Is it comprehensive?
   - Are examples referenced?
   - Is documentation linked?

2. **Generate PRP**
   - Run `/generate-prp`

3. **Review PRP**
   - Check if it makes sense
   - Verify all steps are clear

4. **Execute PRP**
   - Run `/execute-prp PRPs/{filename}.md`

## Tips for Good INITIAL.md

- ✅ Be extremely specific
- ✅ Reference examples explicitly
- ✅ Include all documentation links
- ✅ Mention gotchas and edge cases
- ✅ Define clear success criteria
- ✅ Think about testing
- ❌ Don't be vague
- ❌ Don't skip documentation
- ❌ Don't forget error handling

---

**Remember**: The quality of INITIAL.md determines the quality of the generated PRP, which determines the quality of the implementation. Invest time here!
