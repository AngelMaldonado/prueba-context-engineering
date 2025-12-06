# PRP: AI Chat Interface Implementation for CoachX

**Generated:** 2025-12-03
**Status:** Ready for Review
**Estimated Complexity:** Medium (3-4 files, ~400-500 lines)
**Priority:** High (Core Feature)

---

## Overview

Implement an intuitive, conversational AI chat interface that allows users to:
1. Ask training-related questions with contextual, personalized responses
2. Request modifications to their workout plans through natural conversation
3. Get instant advice powered by RAG (Retrieval Augmented Generation)
4. Have a delightful, modern chat experience with excellent UI/UX

**Key User Stories:**
- "As a user, I want to ask my AI coach questions about my training so I can improve my performance"
- "As a user, I want to request changes to my workout plan in natural language so I don't have to fill out forms"
- "As a user, I want a chat interface that feels responsive and modern with the CoachX brand identity"

**Dependencies:**
- ✅ Backend `/ai/chat` endpoint functional
- ✅ Frontend API client configured
- ✅ DashboardPage implemented
- ✅ User profile and workout plan system working
- ⚠️ Tailwind config needs BRED theme colors

---

## UI/UX Design Principles - BRED Theme

### CoachX Brand Identity: BRED (Black + Red)

**Color Palette:**
```javascript
{
  primary: {
    DEFAULT: '#DC2626',  // red-600 - Main brand color
    dark: '#B91C1C',     // red-700 - Hover states
    light: '#FCA5A5',    // red-300 - Subtle accents
  },
  background: {
    primary: '#000000',   // Black - Main background
    surface: '#1A1A1A',   // Dark gray - Cards and elevated surfaces
    elevated: '#262626',  // Slightly lighter - Hover states
  },
  text: {
    primary: '#FFFFFF',   // White - Main text
    secondary: '#9CA3AF', // Gray-400 - Muted text
    muted: '#6B7280',     // Gray-500 - Very muted
  }
}
```

**Usage:**
- **Primary Actions**: Red (#DC2626) - Send button, user messages, CTAs
- **AI Responses**: Dark surface (#1A1A1A) - Professional, non-intrusive
- **Success States**: Red (#DC2626) with checkmark - Plan updates confirmed
- **Loading States**: Red animated gradient - On-brand waiting experience
- **Backgrounds**: Black (#000000) for main, Dark gray (#1A1A1A) for cards

### Design Goals
1. **Bold & Energetic**: Red conveys power, passion, and intensity (perfect for training)
2. **Professional & Sleek**: Black background gives premium, focused feel
3. **High Contrast**: Excellent readability with white text on dark backgrounds
4. **Fast & Responsive**: Instant feedback, smooth red-themed animations
5. **Contextually Aware**: AI knows user's profile, current plan, and sport
6. **Mobile-First**: Works beautifully on all screen sizes
7. **Accessible**: WCAG AA compliant with high contrast ratios

### Visual Design Language

**Typography:**
- User Messages: Medium weight, white text on red background
- AI Messages: Regular weight, white text on dark gray background
- Timestamps: Small, gray-400 color
- Suggestions: Red text on black background, clickable pills

**Spacing & Layout:**
- Generous padding (16-24px) for readability
- Clear visual separation between messages
- Fixed input at bottom for easy access
- Scrollable message history with red scrollbar

**Shadows & Depth:**
- Cards: Subtle shadow on dark gray (#1A1A1A)
- User messages: No shadow (flat red)
- AI messages: Minimal shadow for depth
- Input focus: Red glow (ring-red-600)

---

## Functional Requirements

### Feature 1: Basic Chat Functionality

**User Flow:**
1. User sees chat interface in dashboard (dark theme, red accents)
2. User types question in input field
3. User presses Enter or clicks red Send button
4. Message appears in chat (right-aligned, red background, white text)
5. Loading indicator shows AI is thinking (red pulsing animation)
6. AI response appears (left-aligned, dark gray background, white text)
7. User can continue conversation

**Technical Requirements:**
- Send message to `GET /ai/chat?q={question}&sport={user_sport}`
- Display user and AI messages in chronological order
- Show red-themed typing indicator while waiting for response
- Auto-scroll to newest message
- Handle errors gracefully with retry option
- Store conversation in component state (not persisted initially)

### Feature 2: Plan Modification Through Chat

**User Flow:**
1. User asks: "Can you make my plan 3 weeks instead of 2?"
2. AI responds with actionable suggestion
3. System detects modification intent
4. Shows red confirmation button: "Generate 3-Week Plan"
5. User clicks to confirm
6. AI generates new plan using backend API
7. Dashboard refreshes to show new plan
8. AI confirms: "✓ Done! Your new 3-week plan is ready."

**Intent Detection Keywords:**
- Modification: "change", "modify", "update", "make it"
- Plan Duration: "weeks", "longer", "shorter", "extend"
- Plan Content: "exercises", "days per week", "intensity", "focus"

**Technical Requirements:**
- Detect plan modification requests in AI responses
- Provide red-themed confirmation UI before making changes
- Call workout plan generation API when confirmed
- Refresh dashboard data after successful update
- Show inline success message in chat with red checkmark

### Feature 3: Contextual Suggestions

**Smart Suggestions (Red Pill Style):**
- Show 3-4 suggested questions when chat is empty
- Suggestions based on user's sport and experience level
- Red text on black/dark gray background
- Hover: Red background with white text (inverted)
- Examples:
  - Beginner: "What should I focus on first?"
  - Intermediate: "How can I break through plateaus?"
  - Advanced: "How do I optimize recovery?"

**Dynamic Suggestions:**
- After plan generation: "How should I track my progress?"
- If user hasn't trained yet: "What should I do before my first workout?"
- If plan is complex: "Can you explain the exercises in Week 1?"

---

## Step-by-Step Implementation Plan

### Phase 0: Update Tailwind Config for BRED Theme

#### Step 0.1: Update Tailwind Colors
**File:** `frontend/tailwind.config.js`

**Current Problem:** Primary colors are blue, need to be red

**Solution:**
```javascript
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#FEF2F2',   // red-50
          100: '#FEE2E2',  // red-100
          200: '#FECACA',  // red-200
          300: '#FCA5A5',  // red-300
          400: '#F87171',  // red-400
          500: '#EF4444',  // red-500
          600: '#DC2626',  // red-600 - Main brand color
          700: '#B91C1C',  // red-700 - Hover states
          800: '#991B1B',  // red-800
          900: '#7F1D1D',  // red-900
        },
      },
    },
  },
  plugins: [],
}
```

**Validation:**
- Run `npm run dev` and check that buttons/links are now red
- Verify `.btn-primary` class uses red background
- Check that hover states use darker red

---

### Phase 1: Core Chat Component

#### Step 1.1: Create ChatSection Component
**File:** `frontend/src/components/ChatSection.tsx`

**Requirements:**
- Dark theme with BRED colors
- Accept `userSport` and `onPlanUpdate` props
- Manage local message state
- Handle form submission
- Display messages with proper styling
- Show red-themed loading state

**Component Structure:**
```typescript
interface Message {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: Date;
  metadata?: {
    planModified?: boolean;
    error?: boolean;
  };
}

interface ChatSectionProps {
  userSport?: string;
  onPlanUpdate?: () => void; // Callback when plan is modified
}

export default function ChatSection({ userSport, onPlanUpdate }: ChatSectionProps)
```

**UI Elements (BRED Theme):**

1. **Container Card**
   - Background: bg-gray-900 (#1A1A1A - dark surface)
   - Border: border-gray-800
   - Rounded corners: rounded-xl
   - Shadow: shadow-xl
   - Padding: p-6

2. **Header**
   - Title: "Ask Your AI Coach" (text-2xl font-bold text-white)
   - Subtitle: "Powered by AI and sports science" (text-sm text-gray-400)
   - Status indicator: "● Online" (bg-red-600 rounded-full)

3. **Messages Area**
   - Background: bg-black (deep black)
   - Border: border border-gray-800
   - Rounded: rounded-lg
   - Padding: p-4
   - Max height: max-h-96
   - Overflow: overflow-y-auto
   - Scrollbar: Custom red scrollbar (CSS)

4. **Input Area**
   - Background: bg-gray-800
   - Border: border-gray-700
   - Text: text-white
   - Placeholder: text-gray-500
   - Focus: ring-2 ring-red-600 border-red-600
   - Fixed at bottom

5. **Send Button**
   - Background: bg-red-600
   - Hover: bg-red-700
   - Text: text-white
   - Icon: Send arrow (→)
   - Size: px-6 py-2

6. **Suggested Questions** (when empty)
   - Pills: bg-black border border-red-600 text-red-600
   - Hover: bg-red-600 text-white (inverted)
   - Transition: all 0.3s ease

---

#### Step 1.2: Message Display Components (BRED Theme)

**User Message Style:**
```jsx
<div className="flex justify-end mb-4">
  <div className="max-w-[80%] bg-red-600 text-white rounded-2xl px-4 py-3 shadow-lg">
    <p className="text-sm">{message.content}</p>
    <p className="text-xs text-red-100 mt-1">
      {message.timestamp.toLocaleTimeString()}
    </p>
  </div>
</div>
```

**CSS:**
```css
- Background: bg-red-600 (#DC2626)
- Text: text-white
- Border radius: rounded-2xl
- Max width: max-w-[80%]
- Alignment: justify-end (right side)
- Padding: px-4 py-3
- Shadow: shadow-lg
- Timestamp: text-red-100 (light red)
```

**AI Message Style:**
```jsx
<div className="flex justify-start mb-4">
  <div className="max-w-[80%] bg-gray-800 text-white rounded-2xl px-4 py-3 border border-gray-700">
    <div className="flex items-start gap-2">
      <div className="w-6 h-6 bg-red-600 rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0">
        AI
      </div>
      <div className="flex-1">
        <p className="text-sm">{message.content}</p>
        <p className="text-xs text-gray-400 mt-1">
          {message.timestamp.toLocaleTimeString()}
        </p>
      </div>
    </div>
  </div>
</div>
```

**CSS:**
```css
- Background: bg-gray-800 (#1F2937)
- Text: text-white
- Border: border-gray-700
- Border radius: rounded-2xl
- Max width: max-w-[80%]
- Alignment: justify-start (left side)
- Padding: px-4 py-3
- Avatar: Red circle with "AI" text
- Timestamp: text-gray-400
```

**Loading Indicator (Red Theme):**
```jsx
<div className="flex justify-start mb-4">
  <div className="bg-gray-800 rounded-2xl px-4 py-3 border border-gray-700">
    <div className="flex items-center gap-2">
      <div className="w-6 h-6 bg-red-600 rounded-full animate-pulse"></div>
      <div className="flex gap-1">
        <div className="w-2 h-2 bg-red-600 rounded-full animate-bounce"></div>
        <div className="w-2 h-2 bg-red-600 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
        <div className="w-2 h-2 bg-red-600 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
      </div>
      <span className="text-xs text-gray-400">AI is thinking...</span>
    </div>
  </div>
</div>
```

---

#### Step 1.3: Animations & Transitions (Red Theme)

**Message Entrance Animation:**
```css
@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes slideInLeft {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.user-message {
  animation: slideInRight 0.3s ease-out;
}

.ai-message {
  animation: slideInLeft 0.3s ease-out;
}
```

**Input Focus State (Red Glow):**
```css
.chat-input:focus {
  outline: none;
  border-color: #DC2626;
  box-shadow: 0 0 0 3px rgba(220, 38, 38, 0.1);
  transition: all 0.2s ease;
}
```

**Send Button States:**
```css
.send-button {
  background: #DC2626;
  color: white;
  transition: all 0.2s ease;
}

.send-button:hover {
  background: #B91C1C;
  transform: translateX(2px);
}

.send-button:disabled {
  background: #4B5563;
  cursor: not-allowed;
  opacity: 0.5;
}
```

**Custom Red Scrollbar:**
```css
.messages-container::-webkit-scrollbar {
  width: 8px;
}

.messages-container::-webkit-scrollbar-track {
  background: #000000;
}

.messages-container::-webkit-scrollbar-thumb {
  background: #DC2626;
  border-radius: 4px;
}

.messages-container::-webkit-scrollbar-thumb:hover {
  background: #B91C1C;
}
```

---

### Phase 2: Integration with DashboardPage

#### Step 2.1: Update Dashboard Dark Theme
**File:** `frontend/src/pages/DashboardPage.tsx`

**Update Background:**
```jsx
// Change from bg-gray-50 to black
<div className="min-h-screen bg-black py-8 px-4">
  <div className="max-w-6xl mx-auto">
    {/* Components with dark theme */}
  </div>
</div>
```

**Update Cards to Dark Theme:**
```jsx
// Profile Summary Card
<div className="bg-gray-900 border border-gray-800 rounded-lg shadow-xl p-6 mb-6">
  <h2 className="text-xl font-semibold text-white mb-4">
    Your Profile
  </h2>
  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
    <div>
      <p className="text-sm text-gray-400">Age</p>
      <p className="text-lg font-medium text-white">{profile.age}</p>
    </div>
    {/* More stats with white text */}
  </div>
</div>
```

#### Step 2.2: Add ChatSection Below Workout Plan
```jsx
<div className="max-w-6xl mx-auto">
  {/* Header */}
  <div className="mb-8">
    <h1 className="text-3xl font-bold text-white">
      Welcome back, {profile.name}!
    </h1>
    <p className="text-gray-400 mt-1">
      Profile Completion: {profile.profile_completion_percentage}%
    </p>
  </div>

  {/* Profile Summary - Dark themed */}
  <ProfileSummaryCard />

  {/* Active Workout Plan - Dark themed */}
  <WorkoutPlanCard />

  {/* AI Chat Section - NEW */}
  <div className="mt-8">
    <ChatSection
      userSport={profile?.primary_sport}
      onPlanUpdate={loadDashboardData}
    />
  </div>
</div>
```

---

#### Step 2.3: Plan Modification Flow (Red Theme)

**Confirmation UI:**
```jsx
{pendingModification && (
  <div className="bg-gray-800 border-2 border-red-600 rounded-lg p-4 mt-2">
    <div className="flex items-start gap-3">
      <div className="w-10 h-10 bg-red-600 rounded-full flex items-center justify-center flex-shrink-0">
        <svg className="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      </div>
      <div className="flex-1">
        <p className="text-sm font-medium text-white mb-2">
          Ready to generate a new {pendingModification.duration_weeks}-week plan?
        </p>
        <div className="flex gap-2">
          <button
            onClick={confirmModification}
            className="bg-red-600 hover:bg-red-700 text-white text-sm font-medium px-4 py-2 rounded-lg transition-colors"
          >
            Generate Plan
          </button>
          <button
            onClick={() => setPendingModification(null)}
            className="bg-gray-700 hover:bg-gray-600 text-white text-sm font-medium px-4 py-2 rounded-lg transition-colors"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  </div>
)}
```

**Success Message (Red Checkmark):**
```jsx
{metadata?.planModified && (
  <div className="flex justify-start mb-4">
    <div className="bg-gray-800 border border-green-500 text-white rounded-2xl px-4 py-3">
      <div className="flex items-center gap-2">
        <div className="w-6 h-6 bg-red-600 rounded-full flex items-center justify-center">
          <svg className="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
          </svg>
        </div>
        <p className="text-sm">{content}</p>
      </div>
    </div>
  </div>
)}
```

---

### Phase 3: Enhanced UX Features (Red Theme)

#### Step 3.1: Suggested Questions (Red Pills)

```jsx
<div className="mt-4">
  <p className="text-xs font-medium text-gray-400 mb-3">
    Suggested questions:
  </p>
  <div className="flex flex-wrap gap-2">
    {suggestions.map((suggestion, index) => (
      <button
        key={index}
        onClick={() => setQuestion(suggestion)}
        className="group bg-black border border-red-600 text-red-600 hover:bg-red-600 hover:text-white px-4 py-2 rounded-full text-sm font-medium transition-all duration-300 transform hover:scale-105"
        disabled={isLoading}
      >
        {suggestion}
      </button>
    ))}
  </div>
</div>
```

---

#### Step 3.2: Empty State (Red Theme)

```jsx
{messages.length === 0 && (
  <div className="text-center py-12">
    <div className="w-16 h-16 bg-red-600 rounded-full flex items-center justify-center mx-auto mb-4">
      <svg className="w-8 h-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
      </svg>
    </div>
    <p className="text-white font-medium mb-2">Start a conversation with your AI coach</p>
    <p className="text-sm text-gray-400 mb-6">
      Ask about training, nutrition, recovery, or anything else!
    </p>
    {/* Suggested questions pills */}
  </div>
)}
```

---

## Visual Reference (ASCII Art)

```
┌─────────────────────────────────────────────────────────────┐
│ Ask Your AI Coach                              ● Online     │ ← Header (white text)
│ Powered by AI and sports science                            │ ← Subtitle (gray-400)
├─────────────────────────────────────────────────────────────┤
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ [AI] How can I improve my boxing jab?      10:30 AM     │ │ ← AI (gray-800 bg, white text)
│ └─────────────────────────────────────────────────────────┘ │
│                                                               │
│                 ┌─────────────────────────────────────────┐ │
│                 │ Great question! Here are 3 tips:  10:31│ │ ← User (red-600 bg, white text)
│                 │ 1. Speed drills 2. Form practice  AM   │ │
│                 │ 3. Shadow boxing                        │ │
│                 └─────────────────────────────────────────┘ │
│                                                               │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ [AI] ● ● ● AI is thinking...                            │ │ ← Loading (red dots)
│ └─────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│ [Type your question here...]               [Send →]         │ ← Input (gray-800) + Button (red-600)
│                                                               │
│ Suggested: [Improve technique] [Recovery tips] [Nutrition]  │ ← Pills (black bg, red border)
└─────────────────────────────────────────────────────────────┘

Color Legend:
● Black (#000000) - Main background
● Dark Gray (#1A1A1A / gray-900) - Cards
● Red (#DC2626 / red-600) - User messages, buttons, accents
● White (#FFFFFF) - Primary text
● Gray (#9CA3AF / gray-400) - Secondary text
```

---

## Implementation Code Example

**File: `frontend/src/components/ChatSection.tsx`**

```tsx
import { useState, useRef, useEffect } from 'react';
import { chatApi } from '../lib/api';
import LoadingSpinner from './LoadingSpinner';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

interface ChatSectionProps {
  userSport?: string;
  onPlanUpdate?: () => void;
}

export default function ChatSection({ userSport, onPlanUpdate }: ChatSectionProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [question, setQuestion] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!question.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: question,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setQuestion('');
    setIsLoading(true);
    setError(null);

    try {
      const response = await chatApi.sendMessage({
        q: question,
        sport: userSport,
        top_k: 3,
      });

      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response.response,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, aiMessage]);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to get response');
    } finally {
      setIsLoading(false);
    }
  };

  const suggestions = [
    'How can I improve my technique?',
    'What should I focus on as a beginner?',
    'How do I prevent injuries?',
    'What are good recovery practices?',
  ];

  return (
    <div className="bg-gray-900 border border-gray-800 rounded-xl shadow-2xl p-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div>
          <h2 className="text-2xl font-bold text-white">Ask Your AI Coach</h2>
          <p className="text-sm text-gray-400">Powered by AI and sports science</p>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 bg-red-600 rounded-full"></div>
          <span className="text-xs text-gray-400">Online</span>
        </div>
      </div>

      {/* Messages Container */}
      <div className="bg-black border border-gray-800 rounded-lg p-4 mb-4 max-h-96 overflow-y-auto messages-container">
        {messages.length === 0 ? (
          <div className="text-center py-12">
            <div className="w-16 h-16 bg-red-600 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-2xl">💬</span>
            </div>
            <p className="text-white font-medium mb-2">Start a conversation</p>
            <p className="text-sm text-gray-400">Ask about training, nutrition, or recovery!</p>
          </div>
        ) : (
          <>
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex mb-4 ${
                  message.role === 'user' ? 'justify-end' : 'justify-start'
                }`}
              >
                <div
                  className={`max-w-[80%] rounded-2xl px-4 py-3 ${
                    message.role === 'user'
                      ? 'bg-red-600 text-white shadow-lg user-message'
                      : 'bg-gray-800 text-white border border-gray-700 ai-message'
                  }`}
                >
                  {message.role === 'assistant' && (
                    <div className="flex items-center gap-2 mb-2">
                      <div className="w-6 h-6 bg-red-600 rounded-full flex items-center justify-center text-xs font-bold">
                        AI
                      </div>
                    </div>
                  )}
                  <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                  <p
                    className={`text-xs mt-1 ${
                      message.role === 'user' ? 'text-red-100' : 'text-gray-400'
                    }`}
                  >
                    {message.timestamp.toLocaleTimeString()}
                  </p>
                </div>
              </div>
            ))}

            {isLoading && (
              <div className="flex justify-start mb-4">
                <div className="bg-gray-800 rounded-2xl px-4 py-3 border border-gray-700">
                  <div className="flex items-center gap-2">
                    <div className="w-6 h-6 bg-red-600 rounded-full animate-pulse"></div>
                    <div className="flex gap-1">
                      <div className="w-2 h-2 bg-red-600 rounded-full animate-bounce"></div>
                      <div
                        className="w-2 h-2 bg-red-600 rounded-full animate-bounce"
                        style={{ animationDelay: '0.1s' }}
                      ></div>
                      <div
                        className="w-2 h-2 bg-red-600 rounded-full animate-bounce"
                        style={{ animationDelay: '0.2s' }}
                      ></div>
                    </div>
                    <span className="text-xs text-gray-400">AI is thinking...</span>
                  </div>
                </div>
              </div>
            )}
          </>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Error Message */}
      {error && (
        <div className="bg-red-900/20 border border-red-600 rounded-lg p-3 mb-4">
          <p className="text-sm text-red-400">{error}</p>
        </div>
      )}

      {/* Input Form */}
      <form onSubmit={handleSubmit} className="flex gap-2 mb-4">
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask about training, nutrition, recovery..."
          className="flex-1 bg-gray-800 border border-gray-700 text-white placeholder-gray-500 px-4 py-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-600 focus:border-red-600 transition-all chat-input"
          disabled={isLoading}
        />
        <button
          type="submit"
          disabled={isLoading || !question.trim()}
          className="bg-red-600 hover:bg-red-700 disabled:bg-gray-700 disabled:opacity-50 text-white font-medium px-6 py-3 rounded-lg transition-all send-button flex items-center gap-2"
        >
          <span>Send</span>
          <span>→</span>
        </button>
      </form>

      {/* Suggested Questions */}
      {messages.length === 0 && (
        <div>
          <p className="text-xs font-medium text-gray-400 mb-3">Suggested questions:</p>
          <div className="flex flex-wrap gap-2">
            {suggestions.map((suggestion, index) => (
              <button
                key={index}
                onClick={() => setQuestion(suggestion)}
                className="bg-black border border-red-600 text-red-600 hover:bg-red-600 hover:text-white px-4 py-2 rounded-full text-sm font-medium transition-all duration-300 transform hover:scale-105"
                disabled={isLoading}
              >
                {suggestion}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
```

**Custom CSS (add to `index.css`):**
```css
@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes slideInLeft {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.user-message {
  animation: slideInRight 0.3s ease-out;
}

.ai-message {
  animation: slideInLeft 0.3s ease-out;
}

.messages-container::-webkit-scrollbar {
  width: 8px;
}

.messages-container::-webkit-scrollbar-track {
  background: #000000;
}

.messages-container::-webkit-scrollbar-thumb {
  background: #DC2626;
  border-radius: 4px;
}

.messages-container::-webkit-scrollbar-thumb:hover {
  background: #B91C1C;
}
```

---

## Testing Checklist (BRED Theme)

**Visual Testing:**
- [ ] Background is black (#000000)
- [ ] Cards are dark gray (#1A1A1A)
- [ ] User messages are red (#DC2626) with white text
- [ ] AI messages are dark gray (#1F2937) with white text
- [ ] Send button is red with hover effect
- [ ] Suggested questions are red pills with hover inversion
- [ ] Loading indicator uses red colors
- [ ] Scrollbar is red
- [ ] All text is readable (white/gray on dark)
- [ ] Red accents are consistent throughout
- [ ] No blue colors anywhere (verify Tailwind config updated)

**Functional Testing:**
- [ ] Chat works in dark theme
- [ ] Messages are readable
- [ ] Contrast is sufficient (WCAG AA)
- [ ] Red theme is consistent with brand

---

## Success Criteria

1. ✅ BRED theme consistently applied (Black, Red, Dark Gray)
2. ✅ No blue colors in chat interface
3. ✅ High contrast for accessibility
4. ✅ Red brand identity reinforced
5. ✅ Professional, sleek dark design
6. ✅ All functional requirements met
7. ✅ Smooth animations with red accents
8. ✅ Mobile responsive in dark theme

---

**Ready for Implementation with Correct BRED Theme!**
