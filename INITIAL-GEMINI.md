# INITIAL: Gemini AI Integration

## Feature Overview
Integrate Google Gemini API to generate AI-powered responses for CoachX, combining RAG context with LLM capabilities.

## Objectives
1. Configure Gemini API client with proper authentication
2. Create a service module for Gemini interactions
3. Implement RAG-enhanced prompt generation
4. Handle API errors, rate limits, and retries
5. Add safety settings for appropriate content generation

## Technical Requirements

### Dependencies
- `google-generativeai` - Official Google Gemini Python SDK
- Use existing `.env` file for API key storage

### Module Structure
```
backend/app/ai/
├── __init__.py
├── rag.py (existing)
└── gemini.py (new)
```

### Core Functions

#### 1. `get_gemini_client()` - Singleton Pattern
- Initialize Gemini client with API key from environment
- Return cached client instance
- Handle authentication errors

#### 2. `generate_response(prompt: str, context: str = "", **kwargs) -> str`
- Main function to generate AI responses
- Combine user prompt with RAG context
- Return generated text
- Handle streaming (optional for future)

#### 3. `generate_with_rag(query: str, sport: Optional[str] = None, top_k: int = 3) -> str`
- Query RAG system for relevant context
- Format context for LLM prompt
- Generate response using context
- Return AI-generated response

### Gemini Configuration

#### Model Selection
- Use `gemini-1.5-flash` for fast responses (recommended for chat)
- Alternative: `gemini-1.5-pro` for complex reasoning

#### Generation Config
```python
generation_config = {
    "temperature": 0.7,  # Balanced creativity
    "top_p": 0.9,
    "top_k": 40,
    "max_output_tokens": 2048,
}
```

#### Safety Settings
```python
safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    }
]
```

### Prompt Engineering

#### System Prompt Template
```
You are CoachX, an expert personal training assistant specializing in {sport}.

You have access to official training knowledge from professional sources.

CONTEXT FROM KNOWLEDGE BASE:
{rag_context}

USER QUESTION:
{user_query}

Provide accurate, helpful, and motivating training advice based on the context above.
If the context doesn't contain relevant information, use your general knowledge but mention this.
Always prioritize safety and proper technique.
```

### Error Handling

1. **API Key Missing**: Raise clear error with instructions
2. **Rate Limits**: Implement exponential backoff retry
3. **Invalid Responses**: Return user-friendly error messages
4. **Network Errors**: Retry with timeout

### Environment Configuration

Update `backend/app/config.py`:
```python
class Settings(BaseSettings):
    # ... existing settings ...
    GEMINI_API_KEY: str
    GEMINI_MODEL: str = "gemini-1.5-flash"
```

## Integration Points

### With RAG System
- Import `query_knowledge` and `format_context_for_llm` from `app.ai.rag`
- Use RAG results to provide context to Gemini

### With FastAPI
- Add test endpoint: `GET /ai/chat?q=<query>&sport=<sport>`
- Combine RAG + Gemini in single endpoint

## Testing Strategy

### Manual Tests
1. Test basic generation without context
2. Test RAG-enhanced generation with boxing query
3. Test with different sports (crossfit, gym)
4. Test error handling (invalid API key, network error)

### Test Endpoint Example
```bash
# Test 1: Basic chat
curl "http://localhost:8000/ai/chat?q=how+to+improve+my+jab"

# Test 2: With sport filter
curl "http://localhost:8000/ai/chat?q=warmup+routine&sport=crossfit"

# Test 3: Complex query
curl "http://localhost:8000/ai/chat?q=create+a+3+day+split+for+beginners&sport=gym"
```

## Success Criteria
- ✅ Gemini client successfully authenticates with API key
- ✅ Basic text generation works without context
- ✅ RAG-enhanced generation provides relevant, contextualized responses
- ✅ Error handling gracefully manages API failures
- ✅ Test endpoint `/ai/chat` returns coherent responses
- ✅ Response quality is appropriate for fitness coaching

## Example Usage Flow

```python
from app.ai.gemini import generate_with_rag

# User asks about boxing technique
response = generate_with_rag(
    query="How do I throw a proper jab?",
    sport="boxing",
    top_k=3
)
# Expected: Detailed jab technique explanation using RAG context
```

## Gotchas and Considerations

1. **API Costs**: Gemini Flash is free tier up to certain limits, monitor usage
2. **Rate Limits**: Free tier has rate limits, implement retry logic
3. **Context Length**: Gemini 1.5 has large context window (1M tokens), but keep prompts reasonable
4. **Hallucinations**: Always combine with RAG context for factual accuracy
5. **Safety**: Ensure safety settings prevent inappropriate content
6. **Streaming**: Optional for future - real-time response streaming

## Documentation

### Environment Variables
Update `backend/.env.example`:
```
# Google Gemini API
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-1.5-flash
```

### Code Comments
- Document all functions with docstrings
- Include usage examples in docstrings
- Explain prompt engineering choices

## Future Enhancements (Out of Scope)
- Streaming responses for real-time chat
- Conversation history and multi-turn dialogue
- Fine-tuning on specific training data
- Image analysis for form checking (Gemini Vision)

## Resources
- Gemini API Docs: https://ai.google.dev/docs
- Python SDK: https://github.com/google/generative-ai-python
- Safety Settings: https://ai.google.dev/docs/safety_setting_gemini
