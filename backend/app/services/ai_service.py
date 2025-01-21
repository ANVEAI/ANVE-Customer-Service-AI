from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.messages import HumanMessage, SystemMessage
from typing import Dict, List, Optional
import time
from datetime import datetime

class AIService:
    def __init__(self, api_key: str):
        self.llm = ChatOpenAI(
            temperature=0.7,
            model="gpt-3.5-turbo",
            openai_api_key=api_key
        )
        
        self.messages = []
        self.system_prompt = "You are a helpful customer service AI assistant for ANVE. Be professional, friendly, and concise in your responses."
        
        # Create the chain using the new pattern
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            ("human", "{input}")
        ])
        
        self.chain = self.prompt | self.llm | StrOutputParser()
        
    async def process_message(self, message: str, context: Optional[Dict] = None) -> Dict:
        start_time = time.time()
        
        try:
            # Add context to the message if provided
            if context:
                message = f"Context: {context}\nUser message: {message}"
            
            # Add message to history
            self.messages.append(HumanMessage(content=message))
            
            # Get response from LangChain
            response = await self.chain.ainvoke({"input": message})
            
            # Calculate processing time
            processing_time = time.time() - start_time
            
            return {
                "response": response,
                "processing_time": processing_time,
                "timestamp": datetime.now().isoformat(),
                "success": True
            }
            
        except Exception as e:
            return {
                "response": str(e),
                "processing_time": time.time() - start_time,
                "timestamp": datetime.now().isoformat(),
                "success": False
            }
    
    def get_conversation_history(self) -> List[Dict]:
        return [{"role": msg.type, "content": msg.content} for msg in self.messages]
    
    def clear_conversation_history(self):
        self.messages = [] 