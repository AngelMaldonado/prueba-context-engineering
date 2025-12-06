# PRP: Dockerize CoachX for Universal Compatibility

## 📋 Objective

Dockerize CoachX to eliminate dependency issues across Windows/macOS/Linux and provide a simple one-command installation experience for evaluators.

## 🎯 Scope

**Include:**
- ✅ Dockerfile for backend (Python 3.12 slim)
- ✅ docker-compose.yml to orchestrate backend + frontend
- ✅ .dockerignore files for optimized builds
- ✅ Completely rewritten README focused on Docker-first approach
- ✅ Keep manual setup as alternative option

**Exclude:**
- ❌ Complex multi-stage builds
- ❌ Kubernetes configurations
- ❌ Advanced Docker optimizations
- ❌ Elaborate health checks

## 📝 Execution Plan

### Step 1: Create Backend Dockerfile

**File:** `backend/Dockerfile`

**Content:**
```dockerfile
# Use Python 3.12 slim for better compatibility than Alpine
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies needed for compilation
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Validation:**
```bash
cd backend
docker build -t coachx-backend .
docker run -p 8000:8000 coachx-backend
# Verify: curl http://localhost:8000/health
```

---

### Step 2: Create Frontend Dockerfile

**File:** `frontend/Dockerfile`

**Content:**
```dockerfile
FROM node:20-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY . .

# Expose port
EXPOSE 5173

# Run dev server (simpler than build for MVP)
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
```

**Validation:**
```bash
cd frontend
docker build -t coachx-frontend .
docker run -p 5173:5173 coachx-frontend
# Verify: open http://localhost:5173
```

---

### Step 3: Create docker-compose.yml

**File:** `docker-compose.yml` (root directory)

**Content:**
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    container_name: coachx-backend
    ports:
      - "8000:8000"
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - DATABASE_URL=sqlite:///./coachx.db
      - CHROMA_PERSIST_DIRECTORY=./chroma_db
      - ALLOWED_ORIGINS=http://localhost:5173
    volumes:
      - ./backend:/app
      - backend_data:/app/coachx.db
      - chroma_data:/app/chroma_db
    restart: unless-stopped

  frontend:
    build: ./frontend
    container_name: coachx-frontend
    ports:
      - "5173:5173"
    environment:
      - VITE_API_URL=http://localhost:8000
    volumes:
      - ./frontend:/app
      - /app/node_modules
    depends_on:
      - backend
    restart: unless-stopped

volumes:
  backend_data:
  chroma_data:
```

**Validation:**
```bash
# Create .env with API key
echo "GEMINI_API_KEY=your_key_here" > .env

# Start services
docker-compose up -d

# Check logs
docker-compose logs -f

# Verify services
curl http://localhost:8000/health
curl http://localhost:5173

# Stop services
docker-compose down
```

---

### Step 4: Create .dockerignore Files

**File:** `backend/.dockerignore`

```
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
*.egg-info/
.pytest_cache/
.coverage
htmlcov/
.env
*.db
chroma_db/
.git/
.gitignore
README.md
docs/
```

**File:** `frontend/.dockerignore`

```
node_modules/
npm-debug.log*
.DS_Store
dist/
.env.local
.vite/
.git/
.gitignore
README.md
```

---

### Step 5: Create .env.example

**File:** `.env.example` (root directory)

```
# Google Gemini API Key
# Get your free key at: https://aistudio.google.com/app/apikey
GEMINI_API_KEY=your_api_key_here
```

---

### Step 6: Rewrite README.md

**File:** `README.md`

**Structure:**
1. Hero section with logo and personal story
2. The Problem (why CoachX exists)
3. Quick Start with Docker (primary method)
4. How to Use
5. Features
6. Tech Stack
7. Alternative Manual Setup
8. Troubleshooting
9. Context Engineering info

**Key sections:**

```markdown
# 🥊 CoachX - Your AI Training Assistant

![CoachX Logo](docs/screenshots/logo.png)

> **Born from frustration.** As someone who trains boxing and CrossFit, I got tired of bad trainers and losing my workout conversations with LLMs. CoachX keeps your training history, learns your goals, and never forgets your routine.
>
> — Manuel Cortez

## 💪 The Problem

I train boxing and CrossFit regularly, but:
- 🥊 Many trainers lack proper knowledge
- 💬 I ask ChatGPT for help, but conversations get lost
- 📝 Can't save my routines or track progress
- 🤦 The LLM forgets what I want each time I start over

**The Solution:** CoachX - A persistent AI training coach that remembers you.

## 🚀 Quick Start (Docker)

**Prerequisites:**
- Docker Desktop ([Download](https://www.docker.com/products/docker-desktop/))
- Google Gemini API Key ([Get Free Key](https://aistudio.google.com/app/apikey))

**3 Steps:**

1. **Clone & Configure**
   ```bash
   git clone https://github.com/cortezxm/prueba-context-engineering.git
   cd prueba-context-engineering
   cp .env.example .env
   # Edit .env and add your GEMINI_API_KEY
   ```

2. **Launch**
   ```bash
   docker-compose up
   ```

3. **Use**
   - Open http://localhost:5173
   - Start your onboarding!

**Stop:**
```bash
docker-compose down
```

## 📖 How to Use

### 1️⃣ Complete Onboarding
- Answer 8 questions about your fitness background
- Takes 2-3 minutes
- Creates your personalized profile

### 2️⃣ Generate Workout Plan
- Click "Generate Workout Plan" button
- Choose duration (1-2 weeks for token optimization)
- Add custom notes (optional: exercise preferences, equipment, language, etc.)
- Get your AI-powered routine in 10-20 seconds

### 3️⃣ Chat with CoachX
- Ask about exercise technique
- Get nutrition advice
- Request modifications
- CoachX remembers your profile and goals!

### 4️⃣ Track Your Progress
- View weekly overview
- Check daily workout details
- Follow the progression plan

## ✨ Features

- 🤖 **AI-Powered Plans**: Google Gemini 2.5 Flash generates personalized routines
- 💬 **Conversational Onboarding**: Natural chat-style profile creation
- 🧠 **RAG System**: Sport-specific knowledge base (boxing, CrossFit, gym, calisthenics, running)
- 💾 **Persistent Memory**: Your profile and training history are saved
- 🔄 **Adaptive**: Plans consider your experience level, goals, and available days
- 🎯 **Smart Chat**: Context-aware answers based on your profile

## 🛠️ Tech Stack

**Backend:**
- FastAPI 0.115 (Python web framework)
- SQLite + SQLAlchemy 2.0 (database)
- Google Gemini Flash 2.5 (LLM)
- ChromaDB (vector database)
- LangChain 0.3 (RAG orchestration)

**Frontend:**
- Vite 5 + React 18 + TypeScript
- Tailwind CSS 3
- Axios (HTTP client)

**Deployment:**
- Docker + Docker Compose
- Single-user MVP architecture

## 🔧 Alternative: Manual Setup

<details>
<summary>Click to expand manual installation</summary>

**Prerequisites:**
- Python 3.11 or 3.12 ([Download](https://www.python.org/downloads/))
  - ⚠️ **Windows:** Python 3.13 not supported (missing pre-built wheels)
- Node.js 18+ ([Download](https://nodejs.org/))
- Google Gemini API Key

**Run:**
```bash
# Linux/macOS
python3 main.py

# Windows
python main.py
```

The launcher will:
1. Check requirements
2. Create virtual environments
3. Install dependencies
4. Launch both servers

**Access:**
- Frontend: http://localhost:5173
- Backend: http://localhost:8000/docs

**Reset Profile:**
```bash
# Delete database
rm backend/coachx.db backend/chroma_db -rf
```

</details>

## 🐛 Troubleshooting

### Docker Issues

**Port already in use:**
```bash
# Kill processes on ports
# macOS/Linux
lsof -ti:8000 | xargs kill
lsof -ti:5173 | xargs kill

# Windows (PowerShell)
Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess | Stop-Process
Get-Process -Id (Get-NetTCPConnection -LocalPort 5173).OwningProcess | Stop-Process

# Or change ports in docker-compose.yml
```

**Backend won't start:**
```bash
# Check logs
docker-compose logs backend

# Common issues:
# 1. Invalid GEMINI_API_KEY in .env
# 2. Port 8000 in use
# 3. Missing .env file
```

**Frontend can't connect to backend:**
- Ensure backend is running: `curl http://localhost:8000/health`
- Check VITE_API_URL in docker-compose.yml
- Restart: `docker-compose restart frontend`

**Rebuild from scratch:**
```bash
docker-compose down -v
docker-compose build --no-cache
docker-compose up
```

### Manual Setup Issues

**Python 3.13 on Windows:**
- Error: "Compiler cl cannot compile programs"
- Solution: Use Python 3.11 or 3.12
- Download: [Python 3.12.7](https://www.python.org/downloads/release/python-3127/)

**Permission errors:**
```bash
# Linux/macOS
rm -rf backend/venv
python3 main.py

# Windows
rmdir /s backend\venv
python main.py
```

## 🎓 About This Project

This project demonstrates Context Engineering best practices:
- **Clear Documentation**: CLAUDE.md guides AI development
- **Structured PRPs**: Problem Resolution Plans for complex tasks
- **AI Integration**: RAG + LLM for intelligent responses
- **Production Ready**: Docker containerization for deployment

Built as a technical assessment to showcase full-stack development with modern AI integration.

## 📄 License

MIT License

---

**Built with 💪 by Manuel Cortez** | [GitHub](https://github.com/cortezxm) | [LinkedIn](https://linkedin.com/in/cortezxm)
```

---

### Step 7: Final Validation

**Complete test sequence:**

1. **Build:**
   ```bash
   docker-compose build --no-cache
   ```

2. **Start:**
   ```bash
   docker-compose up -d
   ```

3. **Verify:**
   ```bash
   # Wait for services to start
   sleep 15

   # Check backend
   curl http://localhost:8000/health
   # Expected: {"status":"healthy"}

   # Check frontend
   curl -I http://localhost:5173
   # Expected: HTTP/1.1 200 OK
   ```

4. **Functional Test:**
   - Open http://localhost:5173
   - Complete onboarding (8 questions)
   - Generate workout plan
   - Test chat
   - Verify data persists after restart:
     ```bash
     docker-compose restart
     ```

5. **Cleanup:**
   ```bash
   docker-compose down -v
   ```

---

## 📦 Deliverables

### New Files
- [ ] `backend/Dockerfile`
- [ ] `backend/.dockerignore`
- [ ] `frontend/Dockerfile`
- [ ] `frontend/.dockerignore`
- [ ] `docker-compose.yml`
- [ ] `.env.example`

### Modified Files
- [ ] `README.md` (complete rewrite)

### Commits
- Commit 1: "feat(docker): add Dockerfiles for backend and frontend"
- Commit 2: "feat(docker): add docker-compose configuration"
- Commit 3: "docs: rewrite README with Docker-first approach and personal story"

---

## ⏱️ Time Estimate

- Create Dockerfiles: 15 min
- Create docker-compose.yml: 10 min
- Test build and run: 10 min
- Rewrite README: 20 min
- Final validation: 10 min
- **Total: ~65 minutes**

---

## ✅ Success Criteria

1. ✅ `docker-compose up` starts both services without errors
2. ✅ Frontend accessible at http://localhost:5173
3. ✅ Backend accessible at http://localhost:8000
4. ✅ Onboarding flow works correctly
5. ✅ Workout plan generation works
6. ✅ Chat with RAG works
7. ✅ Data persists between container restarts
8. ✅ README is clear, direct, and tells Manuel's story
9. ✅ Works on Windows, macOS, Linux without modifications
10. ✅ Evaluators only need Docker + API key to run

---

**Ready to execute?**
