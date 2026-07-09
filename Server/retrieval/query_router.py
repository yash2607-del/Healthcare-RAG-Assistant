from langchain_core.prompts import PromptTemplate
from langchain_core.language_models.chat_models import BaseChatModel
from pydantic import BaseModel, Field

class RouteQuery(BaseModel):
    """Route a user query to the most relevant backend."""
    datasource: str = Field(
        ...,
        description="Given a user query choose to route it to 'diagnostics' or 'chitchat'.",
    )

class QueryRouter:
    """
    Query Router to determine if a query requires RAG retrieval (diagnostics)
    or if it's just a general conversation/greeting (chitchat).
    """
    def __init__(self, llm: BaseChatModel):
        # Bind the LLM to output our structured Pydantic model
        self.llm_with_tool = llm.with_structured_output(RouteQuery)
        
        system = """You are an expert medical routing assistant.
Your job is to route user questions to the appropriate backend.

- Route to 'diagnostics' for questions related to medical tests, blood tests, test panels, prices (MRP), details (DOS, sample type, disease, methodology), or Lord Diagnostics services.
- Route to 'chitchat' for greetings, casual conversation, jokes, or irrelevant questions that don't need a medical database lookup.

Route the query strictly based on its content.
"""
        self.prompt = PromptTemplate.from_template(
            system + "\nQuestion: {question}"
        )
        
        # Create the LCEL routing chain
        self.router_chain = self.prompt | self.llm_with_tool
        
    def route(self, query: str) -> str:
        """
        Returns either 'diagnostics' or 'chitchat'
        """
        result = self.router_chain.invoke({"question": query})
        print(f"Routing query '{query}' to -> {result.datasource}")
        return result.datasource
