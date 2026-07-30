from langchain_classic.chains.retrieval import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains.history_aware_retriever import create_history_aware_retriever
from langchain_core.runnables.history import RunnableWithMessageHistory
import sys
import os

# Ensure the Server directory is in the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag.answer_generator import AnswerGenerator
from history.file_history import get_session_history
from retrieval.retriever import AdvancedRetriever

class RAGChain:
    """
    Constructs the final conversational RAG chain.
    """
    def __init__(self):
        print("Initializing Conversational RAG Chain...")
        
        # 1. Initialize Generator (LLM) and Prompts
        self.generator = AnswerGenerator()
        llm = self.generator.get_llm()
        
        # 2. Initialize Retriever
        self.advanced_retriever = AdvancedRetriever(llm=llm)
        retriever = self.advanced_retriever.get_retriever()
        
        # 3. Create History-Aware Retriever to rephrase follow-ups!
        history_aware_retriever = create_history_aware_retriever(
            llm, retriever, self.generator.get_contextualize_q_prompt()
        )
        
        # 4. Create Question-Answering Chain
        self.question_answer_chain = create_stuff_documents_chain(
            llm, self.generator.get_qa_prompt()
        )
        
        # 5. Combine into Final RAG Chain
        self.rag_chain = create_retrieval_chain(
            history_aware_retriever, self.question_answer_chain
        )
        
        # 5. Wrap with Message History
        self.conversational_rag_chain = RunnableWithMessageHistory(
            self.rag_chain,
            get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer",
        )
        
    def invoke(self, query: str, session_id: str = "default_user"):
        """
        Executes the RAG pipeline for a given query and session.
        """
        print(f"Executing Fast RAG Chain for session: '{session_id}', Query: '{query}'")
        response = self.conversational_rag_chain.invoke(
            {"input": query},
            config={"configurable": {"session_id": session_id}}
        )
        return response

if __name__ == "__main__":
    # Simple test for the chain
    chain = RAGChain()
    
    query = "What is the price of VITAMIN D TOTAL?"
    print(f"\nUser: {query}")
    res = chain.invoke(query, session_id="test_session_1")
    print(f"AI: {res['answer']}")
    
    follow_up = "What about B12?"
    print(f"\nUser: {follow_up}")
    res2 = chain.invoke(follow_up, session_id="test_session_1")
    print(f"AI: {res2['answer']}")
