import datetime
from fastapi import APIRouter
from pydantic import BaseModel
from settings.llm_service import llm_service

router = APIRouter()


class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    model: str = "qwen4b"
    message: str


@router.post("/chat")
async def chat(req: ChatRequest):
    times = datetime.datetime.now()
    print(req.message)
    print(type(req.message))

    # 这里后面接Qwen
    result = llm_service.chat(req.message)
    print(datetime.datetime.now() - times)
    return {
        "code": 200,
        "msg": "success",
        "data": {
            "answer": result
        }
    }