import datetime
import logging
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from .llm import get_model, get_tokenizer

query_router = APIRouter()


class PostQueryRequest(BaseModel):
    input: str


# TODO: add Redis in the future
conversation_history = []


@query_router.post("/query")
async def post_query(request: PostQueryRequest, model=Depends(get_model), tokenizer=Depends(get_tokenizer)):
    try:
        input_text = request.input

        # Add user input to the history
        # TODO: add Redis in the future
        conversation_history.append({"role": "user", "content": input_text})

        context = input_text

        inputs = tokenizer(context, return_tensors="pt", truncation=True)
        outputs = model.generate(**inputs)
        response_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

        conversation_history.append({"role": "bot", "content": response_text})

        logging.info(f"User: {input_text}")
        logging.info(f"Bot: {response_text}")

        return {
            "response": response_text,
            "created_at": datetime.datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error processing query: {str(e)}")
