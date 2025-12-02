# Examples - Reference Patterns for CoachX

This folder contains **reference patterns** that Claude Code uses to understand how to write code for CoachX. These examples are **critical** for Context Engineering - they show the AI what "good code" looks like in your project.

## 🎯 Purpose

When Claude Code implements a feature, it:
1. Reads these examples to understand your patterns
2. Follows the same structure and conventions
3. Generates consistent, high-quality code

**Without examples:** Claude Code might use different patterns each time  
**With examples:** Claude Code follows YOUR standards consistently

---

## 📁 Files in This Folder

### `api_endpoint.py` - API Endpoint Pattern
**Use this when creating:** Any FastAPI endpoint

**Shows:**
- ✅ How to structure API routes with routers
- ✅ Pydantic models for request/response validation
- ✅ Custom validators for business logic
- ✅ Proper error handling with HTTPException
- ✅ Logging with context
- ✅ Type hints everywhere
- ✅ Comprehensive docstrings
- ✅ Database dependency injection

**Key patterns:**
```python
# Router setup
router = APIRouter(prefix="/api/resource", tags=["resource"])

# Pydantic validation
class RequestModel(BaseModel):
    field: str = Field(..., description="Field description")
    
    @validator('field')
    def validate_field(cls, v):
        # Custom validation
        return v

# Endpoint with proper error handling
@router.post("/endpoint", response_model=ResponseModel)
async def endpoint(request: RequestModel, db: Session = Depends(get_db)):
    try:
        # Business logic
        return response
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error message")
```

---

### `database_model.py` - SQLAlchemy Model Pattern
**Use this when creating:** Database models

**Shows:**
- ✅ SQLAlchemy 2.0 syntax with Mapped types
- ✅ Proper relationships (one-to-many, many-to-one)
- ✅ Timestamp fields (created_at, updated_at)
- ✅ Foreign key constraints
- ✅ Cascade delete behavior
- ✅ Helper methods (to_dict, __repr__)
- ✅ Comprehensive docstrings

**Key patterns:**
```python
# Model definition
class MyModel(Base):
    __tablename__ = "my_models"
    
    # Primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    
    # Foreign key
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # Regular fields
    field: Mapped[str] = mapped_column(String(50), nullable=False)
    
    # Timestamps (REQUIRED)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
    
    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="my_models")
```

---

### `chat_conversation.json` - Conversation Flow
**Use this when creating:** Onboarding system, chat interface

**Shows:**
- ✅ Complete conversation flow (8 steps)
- ✅ Expected message structure
- ✅ Validation rules for each input
- ✅ Error handling patterns
- ✅ UI/UX considerations
- ✅ State management
- ✅ API response formats

**Key patterns:**
```json
{
  "step": 1,
  "role": "assistant",
  "message": "Question text",
  "expects": "integer",
  "validation": {
    "min": 1,
    "max": 120,
    "error_message": "Error text"
  }
}
```

**Use this structure for:**
- Onboarding question flow
- Chat message format
- Validation rules
- User data collection

---

## 🎨 Additional Examples Needed (You Should Add)

As you develop, add more examples:

### `rag_query.py` - RAG System Pattern
**When you implement RAG, create this example showing:**
```python
# How to query ChromaDB
# How to embed text
# How to retrieve relevant documents
# How to format results
```

### `component.tsx` - React Component Pattern
**When you implement frontend, create this example showing:**
```typescript
// Functional component structure
// Props interface
// State management with Zustand
// API calls
// Error handling
// Loading states
// Tailwind styling with Bred theme
```

### `prompt_template.py` - AI Prompt Pattern
**When you implement AI generation, create this example showing:**
```python
# How to structure prompts
# How to include RAG context
# How to format user data
# How to handle AI responses
```

---

## 🔍 How Claude Code Uses These Examples

When you run `/generate-prp INITIAL.md`, Claude Code:

1. **Reads INITIAL.md** to understand what you want
2. **Explores examples/** to see your patterns
3. **Reads CLAUDE.md** for global rules
4. **Searches codebase** for similar implementations
5. **Creates PRP** combining all context
6. **Executes PRP** following your patterns

**Example:**
```
You write in INITIAL.md:
"Create an API endpoint for user onboarding"

Claude Code:
1. Reads examples/api_endpoint.py
2. Sees your FastAPI router pattern
3. Sees your Pydantic validation style
4. Sees your error handling approach
5. Generates endpoint following YOUR style
```

---

## ✅ Best Practices for Examples

### DO:
- ✅ Show complete, working code
- ✅ Include extensive comments
- ✅ Document all patterns at the end
- ✅ Add type hints everywhere
- ✅ Show error handling
- ✅ Include validation examples
- ✅ Add docstrings
- ✅ Keep examples realistic (not toy examples)

### DON'T:
- ❌ Copy random code from internet
- ❌ Show outdated patterns
- ❌ Include anti-patterns
- ❌ Skip error handling
- ❌ Forget type hints
- ❌ Use incomplete code
- ❌ Show code without context

---

## 🎯 When to Reference Examples in INITIAL.md

Always mention specific examples in your INITIAL.md:

```markdown
## EXAMPLES:
Reference these patterns from the examples/ folder:

1. **examples/api_endpoint.py**
   - Use the same FastAPI router pattern
   - Follow the Pydantic model validation structure
   - Copy the error handling approach

2. **examples/database_model.py**
   - Follow the SQLAlchemy model structure
   - Use the same relationship pattern
```

This tells Claude Code: "Look at this file and do it like that."

---

## 📊 Example Quality Checklist

Good examples should:
- [ ] Be complete and working (no placeholders)
- [ ] Include type hints
- [ ] Have comprehensive docstrings
- [ ] Show error handling
- [ ] Include comments explaining patterns
- [ ] Use project conventions (naming, structure)
- [ ] Be realistic (not oversimplified)
- [ ] Document key patterns at the end

---

## 🔄 Updating Examples

As your project evolves:

1. **Add new examples** for new patterns
2. **Update existing examples** if patterns change
3. **Remove outdated examples** to avoid confusion
4. **Keep examples in sync** with actual codebase

**Remember:** These examples are your "source of truth" for code style.

---

## 💡 Pro Tips

1. **Start Simple:** Begin with 3-4 core examples
2. **Add as Needed:** Create new examples when implementing new patterns
3. **Keep Updated:** Maintain examples as project evolves
4. **Be Specific:** Show actual project patterns, not generic code
5. **Document Well:** Add comments explaining WHY patterns exist
6. **Test Examples:** Make sure example code actually works

---

## 🚀 Current Status

**Completed Examples:**
- ✅ api_endpoint.py (FastAPI patterns)
- ✅ database_model.py (SQLAlchemy patterns)
- ✅ chat_conversation.json (Conversation flow)

**Needed Examples:**
- ⏳ rag_query.py (RAG implementation)
- ⏳ component.tsx (React components)
- ⏳ prompt_template.py (AI prompts)

**Add these as you implement each feature!**

---

## 📚 Additional Resources

- Context Engineering Guide: https://github.com/coleam00/context-engineering-intro
- FastAPI Best Practices: https://fastapi.tiangolo.com/tutorial/
- SQLAlchemy Patterns: https://docs.sqlalchemy.org/en/20/orm/
- Pydantic Validation: https://docs.pydantic.dev/latest/

---

**Remember:** The quality of your examples directly impacts the quality of Claude Code's output. Invest time in creating good examples - it pays off exponentially! 🎯
