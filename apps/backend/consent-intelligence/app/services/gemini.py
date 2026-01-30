from pydantic_ai import Agent
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider
import os
from dotenv import load_dotenv
from ..schemas.consent import InterpretedConsent

load_dotenv()

provider = GoogleProvider(api_key=os.getenv("GOOGLE_API_KEY"))
model = GoogleModel(
    model_name=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
)


agent = Agent(
    model,
    system_prompt=(
        "You are a healthcare consent interpretation engine. "
        "Extract ONLY what is explicitly allowed or denied from the provided text. "
        "Categories for data: labs, imaging, vitals, notes, identifiers, medications. "
        "Purposes: care, research, AI_training, marketing. "
        "If something is unclear, add it to 'ambiguity_flags'. "
        "Return the result as a structured JSON object."
    )
)

async def interpret_consent_text(text: str) -> InterpretedConsent:
    result = await agent.run(
        f"Consent text: {text}",
        result_type=InterpretedConsent
    )
    return result.data
