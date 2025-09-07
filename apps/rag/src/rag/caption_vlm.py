import base64
import json
import os

from openai import OpenAI
from openai.types.chat import ChatCompletionUserMessageParam, \
    ChatCompletionSystemMessageParam, ChatCompletionContentPartTextParam, ChatCompletionContentPartImageParam

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
VLM_MODEL = os.getenv("VLM_MODEL", "gpt-4o")

CAPTION_PROMPT = (
    "You are an expert technical captioner. Extract visible text verbatim, "
    "then provide one short caption and a dense 3-5 sentence caption. "
    "Return strict JSON with keys: global_caption_short, global_caption_dense, "
    "text_in_image (array), entities (array of strings), tags (array of strings)."
)


def caption_image_png(png_bytes: bytes) -> dict:
    b64_image = base64.b64encode(png_bytes).decode("utf-8")
    data_uri = f"data:image/png;base64,{b64_image}"
    resp = client.chat.completions.create(
        model=VLM_MODEL,
        messages=[
            ChatCompletionSystemMessageParam(role="system", content=CAPTION_PROMPT),
            ChatCompletionUserMessageParam(
                role="user",
                content=[
                    ChatCompletionContentPartTextParam(type="text", text= "Caption this image as JSON."),
                    ChatCompletionContentPartImageParam(type="image_url", image_url={"url": data_uri, "detail": "high"})
                ]
            )

        ],
        response_format={"type": "json_object"}
    )
    return json.loads(resp.choices[0].message.content)
