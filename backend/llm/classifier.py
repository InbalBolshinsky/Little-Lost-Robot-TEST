from backend.llm.prompts import CLASSIFIER_SYSTEM_PROMPT

class DialogueClassifier:
    def __init__(self, client=None):
        self.client = client # Accept raw OpenAI / Mock client instances

    def classify_query(self, user_query: str) -> float:
        # Mocking classification multiplier if no live client is bound
        lowered = user_query.lower()
        if "password" in lowered or "secret" in lowered or "bypass" in lowered:
            return 2.5
        elif "identity" in lowered or "role" in lowered:
            return 1.5
        return 1.0