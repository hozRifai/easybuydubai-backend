from typing import List, Dict, Optional
from datetime import datetime
import uuid
import logging
from app.services.openai_service import OpenAIService
from app.services.conversation_flow import ConversationFlow
from app.services.user_categorization import UserCategorization

logger = logging.getLogger(__name__)

class ChatService:
    def __init__(self):
        self.openai_service = OpenAIService()
        self.user_categorization = UserCategorization()
        # In production, you'd store sessions in Redis or a database
        self.sessions: Dict[str, Dict] = {}
        self.conversation_flows: Dict[str, ConversationFlow] = {}

    def create_session(self, session_id: Optional[str] = None) -> str:
        """Create a new chat session"""
        if not session_id:
            session_id = str(uuid.uuid4())

        self.sessions[session_id] = {
            "id": session_id,
            "messages": [],
            "created_at": datetime.utcnow().isoformat(),
            "metadata": {}
        }

        return session_id

    def get_session(self, session_id: str) -> Optional[Dict]:
        """Get a chat session by ID"""
        return self.sessions.get(session_id)

    async def process_message(
        self,
        session_id: str,
        message: str,
        user_info: Optional[Dict] = None
    ) -> Dict:
        """
        Process a user message and return AI response

        Args:
            session_id: Session identifier
            message: User's message
            user_info: Optional user information

        Returns:
            Dictionary with response and session info
        """
        try:
            # Get or create session
            session = self.get_session(session_id)
            if not session:
                session_id = self.create_session(session_id)
                session = self.get_session(session_id)

            # Add user message to history
            user_message = {
                "role": "user",
                "content": message,
                "timestamp": datetime.utcnow().isoformat()
            }
            session["messages"].append(user_message)

            # Prepare messages for OpenAI (without timestamps)
            messages_for_ai = [
                {"role": msg["role"], "content": msg["content"]}
                for msg in session["messages"]
            ]

            # Get AI response
            ai_response = await self.openai_service.get_chat_response(messages_for_ai)

            # Add AI response to history
            assistant_message = {
                "role": "assistant",
                "content": ai_response,
                "timestamp": datetime.utcnow().isoformat()
            }
            session["messages"].append(assistant_message)

            # Analyze conversation for lead qualification (every 5 messages)
            lead_analysis = None
            if len(session["messages"]) > 5 and len(session["messages"]) % 5 == 0:
                lead_analysis = await self.openai_service.analyze_requirements(messages_for_ai)

            return {
                "session_id": session_id,
                "response": ai_response,
                "lead_analysis": lead_analysis,
                "message_count": len(session["messages"])
            }

        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            # Get current message count, defaulting to 0 if session doesn't exist
            current_session = self.get_session(session_id)
            msg_count = len(current_session["messages"]) if current_session else 0

            return {
                "session_id": session_id,
                "error": str(e),
                "response": "I apologize, but I encountered an error. Please try again.",
                "message_count": msg_count
            }

    def clear_session(self, session_id: str) -> bool:
        """Clear a chat session"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False

    def get_all_sessions(self) -> List[Dict]:
        """Get all active sessions (for admin purposes)"""
        return [
            {
                "id": session["id"],
                "created_at": session["created_at"],
                "message_count": len(session["messages"]),
                "last_message": session["messages"][-1]["timestamp"] if session["messages"] else None
            }
            for session in self.sessions.values()
        ]