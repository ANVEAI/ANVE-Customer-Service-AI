from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.callbacks import get_openai_callback
from typing import Dict, List, Tuple
import os
from dotenv import load_dotenv

load_dotenv()

class AIService:
    def __init__(self):
        self.llm = ChatOpenAI(
            temperature=0.7,
            model_name="gpt-3.5-turbo",
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        
        self.prompt_template = PromptTemplate(
            input_variables=["history", "input"],
            template="""You are a professional and helpful customer service AI assistant.
            Previous conversation:
            {history}
            
            Customer: {input}
            AI Assistant:"""
        )
        
        self.memory = ConversationBufferMemory()
        self.conversation = ConversationChain(
            llm=self.llm,
            memory=self.memory,
            prompt=self.prompt_template,
            verbose=True
        )

    async def generate_response(self, user_input: str, context: Dict = None) -> Tuple[str, float]:
        """Generate AI response and track token usage"""
        with get_openai_callback() as cb:
            response = self.conversation.predict(input=user_input)
            return response, cb.total_cost

    async def classify_intent(self, text: str) -> str:
        """Classify customer intent"""
        prompt = f"""Classify the customer intent from the following text into one of these categories:
        - Question
        - Complaint
        - Request
        - Feedback
        - Other
        
        Text: {text}
        
        Intent:"""
        
        response = await self.llm.apredict(prompt)
        return response.strip()

    async def analyze_sentiment(self, text: str) -> int:
        """Analyze sentiment and return score from -100 to 100"""
        prompt = f"""Analyze the sentiment of the following text and return a score from -100 (most negative) to 100 (most positive):
        
        Text: {text}
        
        Score:"""
        
        response = await self.llm.apredict(prompt)
        try:
            return int(response.strip())
        except ValueError:
            return 0

    async def should_escalate(self, conversation_history: List[str]) -> Tuple[bool, str]:
        """Determine if the conversation should be escalated"""
        conversation_text = "\n".join(conversation_history)
        prompt = f"""Based on the following conversation, determine if this needs to be escalated to a human agent.
        Return 'Yes' or 'No' followed by a brief reason.
        
        Conversation:
        {conversation_text}
        
        Decision:"""
        
        response = await self.llm.apredict(prompt)
        decision = response.lower().startswith("yes")
        reason = response.split("\n")[0].replace("Yes:", "").replace("No:", "").strip()
        return decision, reason

    def clear_memory(self):
        """Clear the conversation memory"""
        self.memory.clear() 