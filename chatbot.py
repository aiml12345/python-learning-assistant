import os
from openai import OpenAI
from config import (
    PYTHON_KEYWORDS,
    KNOWLEDGE_BASE,
    NON_PYTHON_RESPONSE,
    UNKNOWN_PYTHON_RESPONSE,
    OPENROUTER_MODEL,
    OPENROUTER_TEMPERATURE,
    OPENROUTER_BASE_URL
)

def get_response(user_input):
    """
    Hybrid chatbot brain:
    1. Check if question is Python-related
    2. Check local knowledge base for instant answer (smart matching)
    3. If no match, ask OpenRouter AI
    """
    
    user_input_lower = user_input.lower()
    
    # --- Step 1: Domain Filter ---
    is_python = any(keyword in user_input_lower for keyword in PYTHON_KEYWORDS)
    
    if not is_python:
        return NON_PYTHON_RESPONSE
    
    # --- Step 2: Knowledge Base Lookup (Smart Matching) ---
    # This prevents "class" from matching inside "metaclass"
    for keyword, answer in KNOWLEDGE_BASE.items():
        # Find where the keyword appears in the question
        index = user_input_lower.find(keyword)
        
        if index != -1:
            # Check if it's a whole word, not part of a bigger word
            before = index - 1
            after = index + len(keyword)
            
            # Is the character before the keyword a letter? (e.g., "meta" + "class")
            is_word_start = (before < 0) or (not user_input_lower[before].isalpha())
            
            # Is the character after the keyword a letter? (e.g., "class" + "es")
            is_word_end = (after >= len(user_input_lower)) or (not user_input_lower[after].isalpha())
            
            # Only match if it's a complete word
            if is_word_start and is_word_end:
                return answer
    
    # --- Step 3: OpenRouter AI Fallback ---
    api_key = os.getenv("OPENROUTER_API_KEY")
    
    if not api_key or api_key == "sk-or-v1-your_actual_key_here":
        return UNKNOWN_PYTHON_RESPONSE
    
    try:
        client = OpenAI(
            base_url=OPENROUTER_BASE_URL,
            api_key=api_key
        )
        
        response = client.chat.completions.create(
            model=OPENROUTER_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a Python Learning Assistant named PyGuide. "
                        "You ONLY answer questions related to Python programming. "
                        "If the user asks about anything else (politics, weather, jokes, etc.), "
                        "politely refuse and remind them you only answer Python questions. "
                        "Keep answers beginner-friendly, under 150 words, and include a simple "
                        "code example whenever possible. Use markdown formatting."
                    )
                },
                {"role": "user", "content": user_input}
            ],
            temperature=OPENROUTER_TEMPERATURE
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return (
            f"⚠️ **AI Error**: {str(e)}\n\n"
            "Falling back to local knowledge base.\n\n"
            + UNKNOWN_PYTHON_RESPONSE
        )