# PLAN.md - CoachX Development Roadmap

**Project:** CoachX - AI-Powered Personal Training Assistant  
**Timeline:** 4 days (December 2-5, 2024)  
**Daily Time:** 2-3 hours = 8-12 total hours  
**Goal:** Technical assessment demonstrating Context Engineering mastery

---

## 🎯 Project Goals

### Primary Objective

Demonstrate **advanced Context Engineering** and AI engineering skills through a fully functional MVP.

### Success Criteria

1. ✅ Project builds and runs locally with simple commands
2. ✅ Context Engineering properly applied (CLAUDE.md, examples/, PRPs)
3. ✅ All core features working (onboarding, RAG, plan generation, chat)
4. ✅ Clean, documented code with atomic commits
5. ✅ Professional README and documentation
6. ✅ Demonstrates RAG + LangChain + Gemini integration

### What Makes This Stand Out

- **Context Engineering** done right (not just lip service)
- **RAG implementation** with actual knowledge base
- **Clean architecture** with proper separation
- **Process documentation** showing methodology
- **Professional commits** following conventions

---

## 📅 Day-by-Day Breakdown

### **Day 1: Foundation** (Today - Monday) - 2.5 hours

**Goal:** Setup complete, ready to start coding

**Tasks:**

1. ⏱️ **30 min** - Project Structure & Git Setup

   - Create folder structure (backend/, frontend/, examples/, docs/)
   - Initialize Git with proper .gitignore
   - First commit: "chore: initialize project structure"

2. ⏱️ **45 min** - Context Engineering Setup

   - Create CLAUDE.md (DONE ✅)
   - Create PLAN.md (this file)
   - Create examples/ with reference patterns
   - Setup .claude/commands/ for PRPs
   - Commit: "docs: add context engineering foundation"

3. ⏱️ **45 min** - Create Examples

   - examples/api_endpoint.py
   - examples/database_model.py
   - examples/rag_query.py
   - examples/chat_conversation.json
   - examples/component.tsx
   - Commit: "docs: add reference examples for patterns"

4. ⏱️ **30 min** - Knowledge Base Preparation
   - Create knowledge_base/ structure
   - Add 2-3 documents per sport (boxing, crossfit, gym)
   - Basic content (can be simplified for MVP)
   - Commit: "feat: add knowledge base for RAG system"

**End of Day 1 Checklist:**

- [ ] Git repo initialized with all structure
- [ ] CLAUDE.md, PLAN.md, INITIAL.md created
- [ ] examples/ folder with 5 reference files
- [ ] knowledge_base/ with basic content
- [ ] 3-4 commits following conventions
- [ ] Ready to start coding with Claude Code

---

### **Day 2: Backend Core** (Tuesday) - 3 hours

**Goal:** Backend working with basic API and RAG

**Feature 1: Backend Structure & Database** (1 hour)

- INITIAL.md → PRP → Execute
- FastAPI app setup
- SQLAlchemy models (User, WorkoutPlan, ChatMessage)
- Database connection
- Basic health check endpoint
- Commit: "feat(backend): initialize FastAPI app with database models"

**Feature 2: RAG System** (1.5 hours)

- INITIAL.md → PRP → Execute
- ChromaDB setup with persistence
- Load knowledge base documents
- Implement embedding and retrieval
- Test query functionality
- Commit: "feat(rag): implement RAG system with ChromaDB"

**Feature 3: Gemini Integration** (30 min)

- INITIAL.md → PRP → Execute
- Setup Gemini API client
- Create prompt templates
- Test basic generation
- Add rate limiting consideration
- Commit: "feat(ai): integrate Gemini Flash for generation"

**End of Day 2 Checklist:**

- [ ] FastAPI server runs on localhost:8000
- [ ] Database models created and working
- [ ] RAG system can query knowledge base
- [ ] Gemini generates responses
- [ ] At least 3 API endpoints working
- [ ] 3 PRPs generated and documented
- [ ] 3 clean commits

---

### **Day 3: Features Integration** (Wednesday) - 3 hours

**Goal:** Core features working end-to-end

**Feature 4: Onboarding API** (1 hour)

- INITIAL.md → PRP → Execute
- POST /api/onboarding/start
- POST /api/onboarding/answer
- GET /api/onboarding/status
- Validation with Pydantic
- Commit: "feat(api): implement onboarding endpoints"

**Feature 5: Training Plan Generation** (1 hour)

- INITIAL.md → PRP → Execute
- POST /api/training/generate
- GET /api/training/plan/{user_id}
- RAG + Gemini integration
- Structured plan output
- Commit: "feat(api): implement training plan generation"

**Feature 6: Chat System** (1 hour)

- INITIAL.md → PRP → Execute
- POST /api/chat/message
- GET /api/chat/history/{user_id}
- RAG-powered responses
- Context-aware chat
- Commit: "feat(api): implement chat system with RAG"

**End of Day 3 Checklist:**

- [ ] All backend endpoints working
- [ ] Can complete onboarding via API
- [ ] Can generate training plan
- [ ] Can chat with AI
- [ ] RAG providing relevant context
- [ ] Logging implemented
- [ ] 3 PRPs documented
- [ ] 3 commits

---

### **Day 4: Frontend & Polish** (Thursday) - 3.5 hours

**Goal:** Complete MVP ready to submit

**Feature 7: Frontend Setup & Home** (45 min)

- INITIAL.md → PRP → Execute
- Next.js 14 setup with App Router
- Tailwind + Bred theme
- Home page with CTA
- API client setup
- Commit: "feat(frontend): initialize Next.js with home page"

**Feature 8: Onboarding Flow** (1 hour)

- INITIAL.md → PRP → Execute
- Chat-style onboarding interface
- Step progression
- Validation and error handling
- Commit: "feat(frontend): implement onboarding flow"

**Feature 9: Plan View & Chat** (1 hour)

- INITIAL.md → PRP → Execute
- Display generated plan
- Chat interface
- Message history
- Commit: "feat(frontend): implement plan view and chat"

**Feature 10: Final Polish** (45 min)

- Error handling
- Loading states
- Responsive design
- Final testing
- Commit: "feat: add error handling and polish UI"

**Documentation** (30 min)

- Write comprehensive README
- Create CONTEXT_ENGINEERING.md
- Add setup scripts (setup.sh, start.sh)
- Final commit: "docs: add comprehensive documentation"

**End of Day 4 Checklist:**

- [ ] Full app working end-to-end
- [ ] Can onboard, generate plan, chat
- [ ] UI looks professional
- [ ] README complete
- [ ] All PRPs saved in PRPs/ folder
- [ ] docs/CONTEXT_ENGINEERING.md written
- [ ] Ready for pull request

---

## 🎯 Feature Priority Matrix

### **Must Have** (Core MVP)

1. ✅ Onboarding chat (8 questions)
2. ✅ RAG system with knowledge base
3. ✅ AI plan generation
4. ✅ Chat interface
5. ✅ Basic database storage

### **Should Have** (If time permits)

6. ⚡ Weekly check-ins
7. ⚡ Plan export/download
8. ⚡ Better error messages

### **Nice to Have** (Skip for MVP)

- ❌ Authentication
- ❌ Multiple users
- ❌ Progress tracking
- ❌ Advanced analytics

---

## 🛠️ Technical Milestones

### Milestone 1: Foundation Complete (Day 1 EOD)

- ✅ All documentation written
- ✅ Project structure created
- ✅ Knowledge base ready
- ✅ Context Engineering setup complete
- ✅ Ready for Claude Code usage

### Milestone 2: Backend Working (Day 2 EOD)

- ✅ FastAPI app running
- ✅ Database models working
- ✅ RAG functional (can query knowledge base)
- ✅ AI services integrated
- ✅ Can generate plans via API

### Milestone 3: Full Stack Working (Day 3 EOD)

- ✅ All API endpoints complete
- ✅ Can complete onboarding
- ✅ Can generate and view plan
- ✅ Can chat with AI
- ✅ Basic functionality complete

### Milestone 4: MVP Complete (Day 4 EOD)

- ✅ Frontend connected to backend
- ✅ All features working
- ✅ Tested end-to-end
- ✅ Documentation complete
- ✅ Ready to submit

---

## 📊 Commits Strategy

### Commit Message Format

Follow **Conventional Commits**:

```
<type>(<scope>): <description>

[optional body]
```

**Types:**

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `chore`: Maintenance (setup, config)
- `test`: Adding tests
- `refactor`: Code restructuring

**Scopes:**

- `backend`: Backend code
- `frontend`: Frontend code
- `api`: API endpoints
- `rag`: RAG system
- `ai`: AI integration
- `db`: Database
- `docs`: Documentation

**Examples:**

```bash
feat(backend): initialize FastAPI app with database models
feat(rag): implement RAG system with ChromaDB
feat(api): implement onboarding endpoints
feat(frontend): initialize Next.js with home page
docs: add context engineering foundation
chore: setup project structure
```

### Expected Commit Count

**Day 1:** 3-4 commits (setup, docs, examples)  
**Day 2:** 3-4 commits (backend features)  
**Day 3:** 3-4 commits (more features)  
**Day 4:** 4-5 commits (frontend + polish)  
**Total:** 13-17 commits

Each commit should be:

- **Atomic**: One logical change
- **Descriptive**: Clear what was done
- **Working**: Code should compile/run

---

## 🎓 Context Engineering Application

### PRP Workflow for Each Feature

```
1. Write INITIAL.md (10-15 min)
   - Clear feature description
   - Reference examples
   - List documentation
   - Note gotchas

2. Generate PRP (2-3 min)
   - Run: /generate-prp INITIAL.md
   - Claude Code creates comprehensive plan

3. Review PRP (5 min)
   - Read the generated plan
   - Verify it makes sense
   - Check if anything missing

4. Execute PRP (10-30 min)
   - Run: /execute-prp PRPs/feature-name.md
   - Claude Code implements everything
   - Validates at each step

5. Test & Commit (5 min)
   - Verify feature works
   - Atomic commit with good message

6. Save PRP (1 min)
   - Keep PRP in PRPs/ folder
   - Shows your process
```

### What to Include in PRPs Folder

Save all generated PRPs:

```
PRPs/
├── 01-backend-structure.md
├── 02-rag-system.md
├── 03-gemini-integration.md
├── 04-onboarding-api.md
├── 05-plan-generation.md
├── 06-chat-system.md
├── 07-frontend-setup.md
├── 08-onboarding-flow.md
├── 09-plan-view.md
└── 10-final-polish.md
```

This demonstrates your Context Engineering process to evaluators.

---

## 📈 Risk Management

### Potential Blockers

1. **Gemini API Issues**

   - Mitigation: Test early on Day 2
   - Fallback: Use mock responses if needed
   - Rate limit: Max 15 RPM

2. **RAG Complexity**

   - Mitigation: Start simple, iterate
   - Fallback: Simple text search if ChromaDB fails
   - Test with small knowledge base first

3. **Frontend-Backend Integration**

   - Mitigation: Test API endpoints early
   - CORS setup: Configure on Day 2
   - Use proper API client pattern

4. **Time Management**
   - Mitigation: Stick to schedule
   - Skip "nice to have" features
   - Focus on core MVP

### Daily Check-ins

**End of Each Day:**

1. What got done? ✅
2. What's blocking? 🚫
3. What's next? ➡️
4. On track? 📊

---

## 🎯 Quality Standards

### Code Quality

- Type hints in all Python functions
- Proper error handling
- Meaningful variable names
- Comments for complex logic
- No hardcoded values

### Testing

- Test core business logic
- Test API endpoints
- Manual end-to-end testing
- Focus on happy path + critical errors

### Documentation

- Clear README with setup instructions
- CONTEXT_ENGINEERING.md explaining process
- Code comments where needed
- API endpoint documentation

---

## 📝 Deliverables Checklist

### Code

- [ ] Backend fully functional
- [ ] Frontend fully functional
- [ ] RAG system working
- [ ] AI integration working
- [ ] Clean, organized code

### Documentation

- [ ] Comprehensive README
- [ ] CONTEXT_ENGINEERING.md
- [ ] API documentation
- [ ] Setup instructions
- [ ] CV in docs/

### Context Engineering

- [ ] CLAUDE.md comprehensive
- [ ] examples/ with patterns
- [ ] PRPs/ with all generated plans
- [ ] Process clearly documented

### Git

- [ ] Atomic commits
- [ ] Conventional commit messages
- [ ] Clean history
- [ ] No sensitive data committed

### Pull Request

- [ ] Clear title
- [ ] Description with:
  - Project name
  - Your name
  - Project description
  - Setup instructions
  - Demo video/screenshots

---

## 🚀 Next Steps

**Right Now:**

1. ✅ Read this plan completely
2. ✅ Understand the timeline
3. ✅ Review CLAUDE.md
4. ⏩ Create examples/ folder
5. ⏩ Start Day 1 tasks

**When Starting Each Feature:**

1. Create INITIAL.md
2. Generate PRP with Claude Code
3. Review PRP
4. Execute PRP
5. Test, commit, document

**When Stuck:**

1. Check CLAUDE.md for patterns
2. Review examples/
3. Check relevant PRP
4. Consult documentation
5. Simplify if needed

---

## 💡 Success Tips

1. **Follow the plan** - It's tested and works
2. **Use Context Engineering** - That's what they're evaluating
3. **Keep it simple** - MVP over perfection
4. **Commit often** - Show your progress
5. **Document everything** - Process matters
6. **Test as you go** - Don't leave testing for last
7. **Ask for help** - Claude Code is your assistant

---

**Remember:** This is about demonstrating **Context Engineering mastery** and **AI engineering skills**, not building a perfect product.

You got this! 🚀
