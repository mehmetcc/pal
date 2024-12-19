import datetime
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from .llm import get_model, get_tokenizer

query_router = APIRouter()


class PostQueryRequest(BaseModel):
    input: str


@query_router.post("/query")
async def post_query(request: PostQueryRequest, model=Depends(get_model), tokenizer=Depends(get_tokenizer)):
    try:
        input_text = request.input

        inputs = tokenizer(input_text, return_tensors="pt")
        outputs = model.generate(**inputs)
        response_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

        return {
            "response": response_text,
            "created_at": datetime.datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error processing query: {str(e)}"
        )
