from google import genai
from google.genai import types

from config.config import Config
from app.services.knowledge_service import search_knowledge


class AIService:

    def __init__(self):
        self.client = genai.Client(
            api_key=Config.GEMINI_API_KEY,
            http_options=types.HttpOptions(
                timeout=45000
            )
        )

        self.model = "gemini-3.6-flash"

    def generate_response(
        self,
        message: str,
        conversation_history: list | None = None
    ) -> str:

        try:
            conversation_history = conversation_history or []

            contents = []

            # Son konuşmaları gönder
            for item in conversation_history[-10:]:
                contents.append({
                    "role": item["role"],
                    "parts": [
                        {
                            "text": item["text"]
                        }
                    ]
                })

            # Knowledge Base
            knowledge = search_knowledge(message)

            knowledge_context = ""

            if knowledge:
                knowledge_context = (
                    "\n\nRELEVANT KNOWLEDGE BASE INFORMATION:\n"
                    f"{knowledge}\n\n"
                    "Use the knowledge base information when "
                    "it is relevant to the user's question. "
                    "Do not invent factual information.\n"
                )

            contents.append({
                "role": "user",
                "parts": [
                    {
                        "text": (
                            f"{Config.BUSINESS_CONTEXT}"
                            f"{knowledge_context}\n\n"
                            "Respond in the same language as the user.\n"
                            "Keep the answer clear and concise.\n\n"
                            f"User message:\n{message}"
                        )
                    }
                ]
            })

            print("GEMINI REQUEST START")

            response = self.client.models.generate_content(
                model=self.model,
                contents=contents,
                config=types.GenerateContentConfig(
                    max_output_tokens=500,
                    thinking_config=types.ThinkingConfig(
                        thinking_level="low"
                    )
                )
            )

            print("GEMINI REQUEST DONE")

            if not response or not response.text:
                return (
                    "I could not generate a response at the moment. "
                    "Please try again."
                )

            return response.text

        except Exception as e:
            print("AI SERVICE ERROR:", repr(e))

            return (
                "The AI service is temporarily unavailable. "
                "Please try again."
            )