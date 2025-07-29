import os
from dotenv import load_dotenv

load_dotenv()

class GeminiResolver:
    def __init__(self):
        import google.generativeai as genai
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel("gemini-2.5-flash-lite")

    def get_resolution(self, issue):
        prompt = f"""You are a security expert. \
Here is a code issue:\nFile: {issue['file']}\nRule: {issue['rule_id']}\nMessage: {issue['message']}\nCode:\n{issue['code']}\nSuggest a fix or mitigation in 2-3 sentences."""
        response = self.model.generate_content(prompt)
        return response.text.strip()

# In the future, you can add an OpenAIResolver class here with the same interface.

def get_model(provider="gemini"):
    if provider == "gemini":
        return GeminiResolver()
    # elif provider == "openai":
    #     return OpenAIResolver()
    else:
        raise ValueError(f"Unknown provider: {provider}")
