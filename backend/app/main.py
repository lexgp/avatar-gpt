from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from app.llm import get_llm_reply

app = FastAPI()
api_router = APIRouter(prefix="/api")

class LLMRequest(BaseModel):
    text: str

@api_router.post("/llm")
async def llm_endpoint(request: LLMRequest):
    return get_llm_reply(request.text)

app.include_router(api_router)