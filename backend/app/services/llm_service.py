import os
from openai import AsyncOpenAI
from app.services.prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE
from app.schemas import GeneratedArticleSchema

# Instancia o client do OpenAI (assume que OPENAI_API_KEY está no ambiente ou .env)
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY", "dummy-key"))

async def generate_article_from_raw(source: str, title: str, content: str) -> dict:
    """
    Calls the LLM with Structured Outputs to guarantee the correct JSON response.
    """
    user_prompt = USER_PROMPT_TEMPLATE.format(source=source, title=title, content=content)
    
    response = await client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        response_format=GeneratedArticleSchema,
        temperature=0.2 # Lower temperature for factual strictness
    )
    
    parsed_article = response.choices[0].message.parsed
    return parsed_article.dict() if parsed_article else None
