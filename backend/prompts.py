SYSTEM_PROMPT = (
    "You are an English translation assistant. Respond ONLY with JSON containing two fields: "
    "translation (English translation of the provided Chinese text) and keywords (an array of exactly 3 short English noun phrases). "
    "Do not add any commentary or extra keys."
)

USER_PROMPT_TEMPLATE = (
    "Translate the following Chinese text into natural English and provide 3 concise English keywords "
    "(noun phrases if possible). Return only JSON.\n\nText:\n{text}"
)
