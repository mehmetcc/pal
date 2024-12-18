
from contextlib import asynccontextmanager

from fastapi import FastAPI
from transformers import AutoModelForCausalLM, AutoTokenizer


_model = None
_tokenizer = None


@asynccontextmanager
async def load_model(app: FastAPI):
    global _model, _tokenizer
    model_path = "../../phi-4"

    try:
        _tokenizer = AutoTokenizer.from_pretrained(model_path)
        _model = AutoModelForCausalLM.from_pretrained(
            model_path, trust_remote_code=True)
        print("Model and tokenizer loaded successfully!")
    except Exception as e:
        print(f"Error loading the model: {str(e)}")
        raise RuntimeError("Failed to load model")


async def get_model():
    if _model is None:
        raise RuntimeError("Model is not loaded!")
    return _model


async def get_tokenizer():
    if _tokenizer is None:
        raise RuntimeError("Model is not loaded!")
    return _tokenizer
