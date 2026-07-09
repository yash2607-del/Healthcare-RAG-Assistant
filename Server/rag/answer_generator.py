from langchain_ollama import ChatOllama
from rag.prompts import qa_prompt, contextualize_q_prompt
import os

class AnswerGenerator:
    """
    Manages the LLM used for generation and provides the conversational prompts.
    """
    def __init__(self, model_name="llama3", temperature=0.2):
        print(f"Initializing Answer Generator with model: {model_name}")
        self.llm = ChatOllama(model=model_name, temperature=temperature)
        
    def get_llm(self):
        return self.llm
        
    def get_qa_prompt(self):
        return qa_prompt
        
    def get_contextualize_q_prompt(self):
        return contextualize_q_prompt
