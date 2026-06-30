#!/usr/bin/env python3
from __future__ import annotations

import argparse
from typing import Any, Dict, List, Optional

import torch
from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer
import uvicorn


class Message(BaseModel):
    role: str
    content: str


class ChatCompletionRequest(BaseModel):
    model: Optional[str] = None
    messages: List[Message]
    temperature: float = 0.2
    max_tokens: int = 900


def create_app(model_name: str, device: str) -> FastAPI:
    app = FastAPI(title="Local Qwen OpenAI-Compatible Server")
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    dtype = torch.float16 if device.startswith("cuda") else torch.float32
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=dtype,
        device_map="auto" if device.startswith("cuda") else None,
        trust_remote_code=True,
    )
    if not device.startswith("cuda"):
        model = model.to(device)
    model.eval()

    @app.get("/health")
    def health() -> Dict[str, Any]:
        return {"status": "ok", "model": model_name, "device": device}

    @app.post("/v1/chat/completions")
    def chat(req: ChatCompletionRequest) -> Dict[str, Any]:
        messages = [item.model_dump() for item in req.messages]
        prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = tokenizer([prompt], return_tensors="pt").to(model.device)
        with torch.no_grad():
            output_ids = model.generate(
                **inputs,
                max_new_tokens=req.max_tokens,
                do_sample=req.temperature > 0,
                temperature=max(req.temperature, 0.01),
                pad_token_id=tokenizer.eos_token_id,
            )
        generated = output_ids[0][inputs.input_ids.shape[-1] :]
        content = tokenizer.decode(generated, skip_special_tokens=True).strip()
        return {
            "id": "local-qwen",
            "object": "chat.completion",
            "model": req.model or model_name,
            "choices": [{"index": 0, "message": {"role": "assistant", "content": content}, "finish_reason": "stop"}],
        }

    return app


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="Qwen/Qwen2.5-0.5B-Instruct")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=18082)
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    args = parser.parse_args()
    uvicorn.run(create_app(args.model, args.device), host=args.host, port=args.port)


if __name__ == "__main__":
    main()
