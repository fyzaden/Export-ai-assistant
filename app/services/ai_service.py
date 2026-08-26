from google import genai

from config.config import Config


class AIService:
    def __init__(self):
        self.client = genai.Client(
            api_key=Config.GEMINI_API_KEY
        )

        self.model = "gemini-3.6-flash"

    def generate_response(self, message: str) -> str:
        response = self.client.models.generate_content(
            model=self.model,
            contents=[
                {
                    "role": "user",
                    "parts": [
                        {
                            "text": (
                                f"{Config.BUSINESS_CONTEXT}\n\n"
                                "Respond in the same language as the user. "
                                "The user message is:\n\n"
                                f"{message}"
                            )
                        }
                    ]
                }
            ]
        )

        return response.text