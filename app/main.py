from fastapi import FastAPI, UploadFile, File, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.config import AZURE_OPENAI_CONFIG, AZURE_SEARCH_CONFIG, CORS_ORIGINS
from app.agent import ChatAgent
from app.rag import RAGPipeline
import logging
import json

# VULNERABILITY: Logging at DEBUG level in production - may log sensitive data
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI(title="Contoso OpenAI Agent", version="1.0.0")

# VULNERABILITY: Allowing all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = ChatAgent()
rag = RAGPipeline()


class ChatRequest(BaseModel):
    message: str
    conversation_id: str = None
    system_prompt: str = None  # VULNERABILITY: User can override system prompt


class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    sources: list = []


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    # VULNERABILITY: Logging user input which may contain sensitive data
    logger.debug(f"Chat request: {json.dumps(request.dict())}")

    # VULNERABILITY: Prompt injection - user can provide custom system prompt
    system_prompt = request.system_prompt or "You are a helpful Contoso assistant."

    response = await agent.chat(
        message=request.message,
        conversation_id=request.conversation_id,
        system_prompt=system_prompt
    )

    # VULNERABILITY: Logging full response including potentially sensitive RAG content
    logger.debug(f"Chat response: {json.dumps(response)}")

    return ChatResponse(**response)


@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload a document for RAG indexing"""
    # VULNERABILITY: No file type validation, no size limit
    content = await file.read()

    # VULNERABILITY: Logging file contents
    logger.debug(f"Uploaded file: {file.filename}, size: {len(content)}")

    result = await rag.index_document(content, file.filename)
    return {"status": "indexed", "document_id": result["id"]}


@app.get("/conversations/{conversation_id}")
async def get_conversation(conversation_id: str):
    """Get conversation history - no auth required"""
    # VULNERABILITY: No authentication - anyone can read any conversation
    history = await agent.get_history(conversation_id)
    return {"conversation_id": conversation_id, "messages": history}


@app.delete("/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str):
    # VULNERABILITY: No authentication for deletion
    await agent.delete_history(conversation_id)
    return {"status": "deleted"}


@app.get("/admin/config")
async def get_config():
    """VULNERABILITY: Exposes all configuration including API keys"""
    return {
        "openai": AZURE_OPENAI_CONFIG,
        "search": AZURE_SEARCH_CONFIG,
        "version": "1.0.0"
    }


@app.post("/admin/eval")
async def eval_code(request: Request):
    """VULNERABILITY: Remote code execution via eval"""
    body = await request.json()
    code = body.get("code", "")
    # VULNERABILITY: Using eval() with user input
    result = eval(code)
    return {"result": str(result)}
