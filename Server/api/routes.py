from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from rag.chain import RAGChain
from retrieval.query_router import QueryRouter
from rag.answer_generator import AnswerGenerator
import traceback

router = APIRouter()

# Initialize our AI components once when the server starts
print("Loading AI Components for API...")
rag_chain = RAGChain()
answer_generator = AnswerGenerator()
query_router = QueryRouter(llm=answer_generator.get_llm())
print("AI Components Loaded!")

# Request/Response Models
class ChatRequest(BaseModel):
    query: str
    session_id: str = "default_session"

class ChatResponse(BaseModel):
    answer: str
    source: str # Indicates if it used RAG ('diagnostics') or bypassed it ('chitchat')

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        # 1. Route the query (Does it need database retrieval or is it just a greeting?)
        route = query_router.route(request.query)
        
        if route == "diagnostics":
            # 2. Use full RAG pipeline (Retrieval + Generation + History)
            response = rag_chain.invoke(request.query, session_id=request.session_id)
            answer = response["answer"]
        else:
            # 3. Handle casual conversation without expensive retrieval
            answer = "Hello! I am the AI assistant for Lord Diagnostics. I can help you with pricing, test details, and other information about our services. How can I help you today?"
            
        return ChatResponse(answer=answer, source=route)
        
    except Exception as e:
        print(f"Error during chat processing: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Internal server error while processing your request.")

@router.get("/health")
async def health_check():
    return {"status": "ok", "message": "Lord Diagnostics API is running."}
