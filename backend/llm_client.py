import asyncio
import json
import os
from typing import List, Optional, Tuple

from openai import OpenAI

from prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE

BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
MODEL_NAME = "qwen-plus"


def _get_client() -> OpenAI:
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        raise RuntimeError("DASHSCOPE_API_KEY is not set. Please configure it in environment or backend/.env")
    return OpenAI(api_key=api_key, base_url=BASE_URL)


def _find_balanced_json_block(text: str) -> Optional[str]:
    start = text.find("{")
    if start == -1:
        return None
    depth = 0
    for idx in range(start, len(text)):
        char = text[idx]
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return text[start : idx + 1]
    return None


def _parse_model_output(raw_text: str) -> Optional[dict]:
    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        candidate = _find_balanced_json_block(raw_text)
        if not candidate:
            return None
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            return None


def _normalize_keywords(keywords: Optional[List]) -> List[str]:
    if not isinstance(keywords, list):
        keywords = []
    cleaned = [str(k or "").strip() for k in keywords]
    while len(cleaned) < 3:
        cleaned.append("")
    if len(cleaned) > 3:
        cleaned = cleaned[:3]
    return cleaned


def _build_messages(text: str) -> list:
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": USER_PROMPT_TEMPLATE.format(text=text)},
    ]


def _build_fix_messages(original_output: str) -> list:
    return [
        {
            "role": "system",
            "content": (
                "You strictly output valid JSON with two keys: translation (string) and "
                "keywords (array of exactly 3 strings)."
            ),
        },
        {
            "role": "user",
            "content": (
                "The previous model output was not valid JSON. Convert it into valid JSON with only "
                "translation and keywords (array length 3). Respond with JSON only.\n\n"
                f"Bad output:\n{original_output}"
            ),
        },
    ]


def _run_completion(client: OpenAI, messages: list) -> str:
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=0.2,
    )
    return response.choices[0].message.content or ""


async def translate_text(text: str) -> Tuple[str, List[str]]:
    client = _get_client()
    messages = _build_messages(text)
    raw_output = await asyncio.to_thread(_run_completion, client, messages)

    parsed = _parse_model_output(raw_output)
    if not parsed:
        fix_messages = _build_fix_messages(raw_output)
        fixed_output = await asyncio.to_thread(_run_completion, client, fix_messages)
        parsed = _parse_model_output(fixed_output)

    if not parsed:
        raise RuntimeError("Unable to parse model output into JSON after retry")

    translation = str(parsed.get("translation", "")).strip()
    keywords = _normalize_keywords(parsed.get("keywords"))
    return translation, keywords
