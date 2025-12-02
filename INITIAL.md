# INITIAL.md Template

This file is a template for creating feature requests that will be used to generate PRPs (Product Requirement Prompts) with Claude Code.

---

## How to Use This Template

1. **Copy this template** for each new feature
2. **Fill in all sections** with specific details
3. **Be comprehensive** - more detail = better PRP
4. **Reference examples** from examples/ folder
5. **Run:** `/generate-prp INITIAL.md` in Claude Code
6. **Review the generated PRP** before executing

---

## Template Structure

```markdown
# INITIAL.md - [Feature Name]

## FEATURE:

[Describe EXACTLY what you want to build]

- Be specific about functionality
- Include input/output formats
- Mention UI requirements (if frontend)
- Specify any constraints or limits
- Define success criteria

## EXAMPLES:

[Reference files in examples/ that show patterns to follow]

- List specific files: examples/api_endpoint.py
- Explain what to copy from each example
- Point out specific patterns or structures
- Mention what NOT to do (anti-patterns)

## DOCUMENTATION:

[Include all relevant documentation URLs]

- Official docs for libraries/frameworks
- API references
- Related blog posts or tutorials
- Database schemas (if relevant)
- Any other resources

## OTHER CONSIDERATIONS:

[Important details that AI might miss]

- Edge cases to handle
- Common gotchas for this feature
- Performance considerations
- Security concerns
- Testing requirements
- Integration points with other features
- Rate limits or quotas
- Error handling specifics
```

---

# Example: First Feature (Backend Structure)

Below is a complete example for your FIRST feature. Use this as reference.

---

# INITIAL.md - Backend Structure & Database Setup

## FEATURE:

Create the foundational backend structure for CoachX with FastAPI and SQLAlchemy.

**Requirements:**

1. **FastAPI Application Setup**

   - Initialize FastAPI app with CORS middleware
   - Setup proper project structure (app/ directory)
   - Create config.py for environment variables
   - Add main.py as entry point
   - Include health check endpoint: GET /health

2. **Database Models (SQLAlchemy)**

   - User model with fields:

     - id (Integer, primary key)
     - name (String, max 50 chars)
     - age (Integer, 1-120)
     - sport (String, enum: boxing/crossfit/gym/calisthenics/running)
     - experience_level (String, enum: beginner/intermediate/advanced)
     - goals (String, 200 chars)
     - days_per_week (Integer, 1-7)
     - created_at (DateTime)
     - updated_at (DateTime)

   - WorkoutPlan model with fields:

     - id (Integer, primary key)
     - user_id (ForeignKey to User)
     - plan_data (JSON - flexible structure)
     - duration_weeks (Integer)
     - created_at (DateTime)

   - ChatMessage model with fields:
     - id (Integer, primary key)
     - user_id (ForeignKey to User)
     - role (String: "user" or "assistant")
     - message (Text)
     - created_at (DateTime)

3. **Database Connection**

   - SQLite database: coachx.db
   - Connection pooling setup
   - Create tables on startup
   - Database session management

4. **Configuration**

   - Environment variables from .env file
   - Pydantic BaseSettings for config
   - CORS configuration for localhost:3000

5. **Directory Structure**
   ```
   backend/
   ├── app/
   │   ├── __init__.py
   │   ├── main.py
   │   ├── config.py
   │   ├── database/
   │   │   ├── __init__.py
   │   │   ├── connection.py
   │   │   └── models.py
   │   └── api/
   │       └── __init__.py
   ├── requirements.txt
   ├── .env.example
   └── pytest.ini
   ```

**Success Criteria:**

- Server runs on localhost:8000
- GET /health returns {"status": "healthy"}
- Database file created automatically
- Models have proper relationships
- Can create a test user in database
- Type hints on all functions
- Proper error handling

## EXAMPLES:

Reference these patterns from the examples/ folder:

1. **examples/api_endpoint.py**

   - Use the same FastAPI router pattern
   - Follow the Pydantic model validation structure
   - Copy the error handling approach
   - Use similar docstrings

2. **examples/database_model.py**
   - Follow the SQLAlchemy model structure
   - Use the same relationship pattern
   - Copy the created_at/updated_at pattern
   - Use similar type hints

Key patterns to follow:

- All endpoints have try/except with HTTPException
- All models have created_at and updated_at timestamps
- Use Pydantic for request/response validation
- Functions under 50 lines
- Type hints everywhere

## DOCUMENTATION:

Essential documentation to reference:

1. **FastAPI:**

   - Main docs: https://fastapi.tiangolo.com/
   - CORS: https://fastapi.tiangolo.com/tutorial/cors/
   - Database: https://fastapi.tiangolo.com/tutorial/sql-databases/
   - Pydantic: https://fastapi.tiangolo.com/tutorial/body/

2. **SQLAlchemy 2.0:**

   - Docs: https://docs.sqlalchemy.org/en/20/
   - Models: https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html
   - Relationships: https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html
   - Sessions: https://docs.sqlalchemy.org/en/20/orm/session_basics.html

3. **Pydantic V2:**
   - Docs: https://docs.pydantic.dev/latest/
   - Settings: https://docs.pydantic.dev/latest/concepts/pydantic_settings/
   - Validation: https://docs.pydantic.dev/latest/concepts/validators/

## OTHER CONSIDERATIONS:

**Critical Gotchas:**

1. **SQLAlchemy 2.0 Changes**

   - Use `from sqlalchemy.orm import DeclarativeBase` not old declarative_base
   - Use `Mapped[type]` for type hints
   - Relationships need `back_populates` on both sides

2. **Environment Variables**

   - Create .env.example (without sensitive values)
   - Never commit .env file
   - Use python-dotenv to load .env
   - Validate all env vars with Pydantic Settings

3. **CORS Configuration**

   - Must allow localhost:3000 for frontend
   - Allow credentials if using cookies
   - Specify allowed methods and headers

4. **Database Sessions**

   - Use dependency injection for sessions
   - Always close sessions properly
   - Handle transaction rollback on errors

5. **Testing Requirements**

   - Create pytest.ini configuration
   - Setup test database (separate from dev)
   - Write basic test for health endpoint
   - Test database models can be created

6. **Performance**

   - Use connection pooling
   - Add database indexes on foreign keys
   - Use async database if needed later

7. **Error Handling**

   - Catch SQLAlchemy errors and convert to HTTP errors
   - Log errors with proper context
   - Return user-friendly error messages

8. **Type Hints**
   - Use proper return types for all functions
   - Use Optional[] for nullable fields
   - Import from typing module

**File Organization:**

- Keep database logic in database/ module
- Keep API routes in api/ module
- Config in root of app/
- No file over 500 lines
- Tests in tests/ subdirectories

**Validation:**
After implementation, verify:

1. `python app/main.py` starts server
2. `curl http://localhost:8000/health` returns 200
3. Database file created in root
4. Can import models successfully
5. No linting errors
6. Tests pass with pytest

---

# How to Use This

1. **Save this as INITIAL.md** in your project root
2. **Open Claude Code** in your project
3. **Run command:** `/generate-prp INITIAL.md`
4. **Wait** for PRP generation (2-3 minutes)
5. **Review** the generated PRP in PRPs/ folder
6. **Execute** with `/execute-prp PRPs/backend-structure.md`
7. **Test** that everything works
8. **Commit** with message: `feat(backend): initialize FastAPI app with database models`

---

# Tips for Writing Good INITIAL.md Files

✅ **DO:**

- Be specific and detailed
- Reference examples explicitly
- Include documentation links
- Mention gotchas and edge cases
- Define clear success criteria
- Think about testing

❌ **DON'T:**

- Be vague ("make it good")
- Assume AI knows your preferences
- Skip documentation links
- Forget about error handling
- Leave out validation requirements

**Remember:** The quality of your PRP depends on the quality of your INITIAL.md!
