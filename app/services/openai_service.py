from openai import OpenAI
from typing import List, Dict, Optional
import logging
from app.config import settings

logger = logging.getLogger(__name__)

class OpenAIService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model

        # System prompt for EasyBuy Dubai property assistant
        self.system_prompt = """You are an AI assistant for EasyBuy Dubai, a revolutionary property buying platform in Dubai.

Your role is to:
1. Understand property requirements from potential buyers
2. Ask clarifying questions about their needs
3. Collect information about:
   - Property type (Apartment, Villa, Townhouse, Penthouse)
   - Budget range
   - Preferred locations in Dubai
   - Number of bedrooms
   - Timeline for purchase
   - Financing status (cash buyer, pre-approved, needs financing)
   - Any special requirements

Be friendly, professional, and helpful. Guide the conversation naturally to gather all necessary information.
Assure buyers that their information will only be shared with one dedicated expert - no spam calls.
Focus on understanding their needs without being pushy or salesy.

Remember: You're here to make property buying in Dubai pressure-free and efficient."""

    async def get_chat_response(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7
    ) -> str:
        """
        Get a response from OpenAI's chat model

        Args:
            messages: List of message dictionaries with 'role' and 'content'
            temperature: Sampling temperature (0-1)

        Returns:
            Response text from the model
        """
        try:
            # Add system prompt as first message if not present
            if not messages or messages[0].get("role") != "system":
                messages = [{"role": "system", "content": self.system_prompt}] + messages

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=500,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )

            return response.choices[0].message.content

        except Exception as e:
            logger.error(f"Error getting OpenAI response: {str(e)}")
            raise Exception(f"Failed to get AI response: {str(e)}")

    async def analyze_requirements(self, conversation: List[Dict[str, str]]) -> Dict:
        """
        Analyze the conversation to extract property requirements

        Args:
            conversation: Full conversation history

        Returns:
            Dictionary with extracted requirements
        """
        try:
            analysis_prompt = """Based on the conversation, extract and summarize the buyer's property requirements.

            Return a JSON-like summary including:
            - property_type
            - budget_min
            - budget_max
            - locations (list)
            - bedrooms
            - timeline
            - financing_status
            - special_requirements (list)
            - lead_score (0-100 based on readiness to buy)

            If any information is missing, mark it as "Not specified"."""

            messages = conversation + [{"role": "user", "content": analysis_prompt}]

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0,
                max_tokens=500
            )

            return {"analysis": response.choices[0].message.content}

        except Exception as e:
            logger.error(f"Error analyzing requirements: {str(e)}")
            return {"error": str(e)}