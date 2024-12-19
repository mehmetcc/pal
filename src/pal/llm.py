import logging
import os

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


_model = None
_tokenizer = None


def load_model():
    logging.info("Started loading the model and the tokenizer.")
    global _model, _tokenizer
    model_path = "./src/models/Llama-3.2-3B-Instruct-uncensored"

    try:
        logging.info(f"Model path: {model_path}")
        _tokenizer = AutoTokenizer.from_pretrained(model_path)
        _model = AutoModelForCausalLM.from_pretrained(model_path,
                                                      device_map={
                                                          "": torch.device("cpu")},
                                                      low_cpu_mem_usage=True,
                                                      torch_dtype=torch.float16)
        logging.info("Model and tokenizer loaded successfully!")
    except Exception as e:
        logging.error(f"Error loading the model: {str(e)}")
        raise RuntimeError("Failed to load model")


def _get_model():
    if _model is None:
        raise RuntimeError("Model is not loaded!")
    return _model


def _get_tokenizer():
    if _tokenizer is None:
        raise RuntimeError("Tokenizer is not loaded!")
    return _tokenizer


async def get_model():
    return _get_model()


async def get_tokenizer():
    return _get_tokenizer()
