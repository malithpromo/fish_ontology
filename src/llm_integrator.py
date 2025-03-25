import os
import json
from typing import Optional, List, Dict
import requests
from dotenv import load_dotenv

class DeepSeekLLM:
    """
    DeepSeek Language Model Integrator for Fish Ontology Project
    """
    def __init__(self):
        """
        Initialize DeepSeek LLM 
        Loads API key from environment variables
        """
        load_dotenv()
        self.api_key = os.getenv('DEEPSEEK_API_KEY')
        if not self.api_key:
            raise ValueError("DeepSeek API key not found in environment variables")
        
        self.base_url = "https://api.deepseek.com/v1/chat/completions"
    
    def generate_response(
        self, 
        messages: List[Dict[str, str]], 
        model: str = "deepseek-chat",
        max_tokens: int = 500,
        temperature: float = 0.7
    ) -> Optional[str]:
        """
        Generate a response using DeepSeek LLM
        
        :param messages: List of message dictionaries 
        :param model: DeepSeek model to use
        :param max_tokens: Maximum tokens to generate
        :param temperature: Sampling temperature
        :return: Generated response or None
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        try:
            response = requests.post(self.base_url, headers=headers, json=payload)
            response.raise_for_status()
            
            result = response.json()
            if 'choices' in result and result['choices']:
                return result['choices'][0]['message']['content']
            return None
        
        except requests.RequestException as e:
            print(f"Error querying DeepSeek API: {e}")
            return None
    
    def generate_contextual_response(
        self, 
        query: str, 
        context: Optional[str] = None, 
        max_tokens: int = 500,
        temperature: float = 0.7
    ) -> Optional[str]:
        """
        Generate a contextual response using DeepSeek LLM
        
        :param query: User's original query
        :param context: Contextual information from RAG system
        :param max_tokens: Maximum tokens to generate
        :param temperature: Sampling temperature
        :return: Generated response or None
        """
        # Prepare messages with system and user context
        messages = [
            {
                "role": "system", 
                "content": """You are an expert marine biologist specializing in fish taxonomy and ecology. 
                Provide precise, scientifically accurate answers based on the given context. 
                If the context is insufficient, clearly state what additional information is needed."""
            }
        ]
        
        # Add context if available
        if context:
            messages.append({
                "role": "system", 
                "content": f"Contextual Information: {context}"
            })
        
        # Add user query
        messages.append({
            "role": "user", 
            "content": query
        })
        
        # Use generate_response method to get the LLM output
        return self.generate_response(
            messages, 
            max_tokens=max_tokens, 
            temperature=temperature
        )

def enhance_rag_response(rag_response: str, query: str) -> str:
    """
    Enhance RAG system response with LLM-generated insights
    
    :param rag_response: Original response from RAG system
    :param query: Original user query
    :return: Enhanced response
    """
    # Initialize LLM 
    llm = DeepSeekLLM()
    
    # Generate enhanced response
    enhanced_response = llm.generate_contextual_response(
        query, 
        context=rag_response
    )
    
    # Fallback if LLM generation fails
    if not enhanced_response:
        return rag_response
    
    return enhanced_response