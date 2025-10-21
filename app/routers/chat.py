from fastapi import APIRouter, HTTPException, Depends
from typing import Optional
import logging
from app.models import ChatMessage, ChatResponse, SessionInfo
from app.services.chat_service import ChatService

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/chat",
    tags=["chat"],
    responses={404: {"description": "Not found"}},
)

# Create a single instance of ChatService
chat_service = ChatService()

@router.post("/message", response_model=ChatResponse)
async def send_message(message: ChatMessage):
    """
    Send a message to the AI assistant and get a response
    """
    try:
        # Create session if not provided
        if not message.session_id:
            message.session_id = chat_service.create_session()

        # Process the message
        result = await chat_service.process_message(
            session_id=message.session_id,
            message=message.message,
            user_info=message.user_info
        )

        return ChatResponse(**result)

    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/session/create")
async def create_session():
    """
    Create a new chat session
    """
    try:
        session_id = chat_service.create_session()
        return {"session_id": session_id, "status": "created"}

    except Exception as e:
        logger.error(f"Error creating session: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/session/{session_id}")
async def get_session(session_id: str):
    """
    Get session information
    """
    try:
        session = chat_service.get_session(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

        return {
            "session_id": session["id"],
            "created_at": session["created_at"],
            "message_count": len(session["messages"]),
            "messages": session["messages"]
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting session: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/session/{session_id}")
async def clear_session(session_id: str):
    """
    Clear/delete a chat session
    """
    try:
        success = chat_service.clear_session(session_id)
        if not success:
            raise HTTPException(status_code=404, detail="Session not found")

        return {"status": "cleared", "session_id": session_id}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error clearing session: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sessions", response_model=list[SessionInfo])
async def get_all_sessions():
    """
    Get all active sessions (admin endpoint)
    """
    try:
        sessions = chat_service.get_all_sessions()
        return sessions

    except Exception as e:
        logger.error(f"Error getting sessions: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))