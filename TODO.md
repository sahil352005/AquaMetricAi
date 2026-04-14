# AquaMetricAi - Grok Fallback Implementation TODO

Status: In Progress

## Approved Plan Summary
Implement fallback to Grok (via Groq API, free tier available) when OPENAI_API_KEY is missing. User has no OpenAI credits, prefers simple free model.

**Key Changes:**
- Prefer Grok if available, fallback logic
- Use 'grok-beta' model (powerful, free tier on Groq)
- Keep OpenAI embeddings or switch to compatible (Grok embeddings coming)
- Dependencies: Add langchain-groq==0.1.0

## Steps

### 1. [IN PROGRESS] Create this TODO.md ✅
### 2. Update .env.example with GROQ_API_KEY ✅
### 3. Edit config.py - Add GROQ support & provider logic ✅
### 4. Edit backend/agent.py - LLM init with provider switch ✅
### 5. Edit requirements.txt - Add langchain-groq ✅
### 6. pip install -r requirements.txt [PENDING]
### 7. Edit quickstart.py - Validate either key
### 8. pip install -r requirements.txt
### 9. python quickstart.py (test validation)
### 10. python app.py & test http://localhost:5000
### 11. Update README.md with new config info
### 12. attempt_completion

**Next Step:** Update .env.example

