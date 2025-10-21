from fastapi import APIRouter, HTTPException, Depends
from typing import Optional, Dict, Any
import logging
from pydantic import BaseModel
from app.services.conversation_flow import ConversationFlow
from app.services.user_categorization import UserCategorization

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/conversation",
    tags=["conversation"],
    responses={404: {"description": "Not found"}},
)

# Store conversation flows in memory (in production, use Redis/database)
conversation_flows: Dict[str, ConversationFlow] = {}
user_categorizations = UserCategorization()

class AnswerRequest(BaseModel):
    session_id: str
    question_id: str
    answer: Any
    is_other: bool = False
    other_text: Optional[str] = None

class CategoryNoteRequest(BaseModel):
    session_id: str
    category_id: str
    note: str

class ScheduleRequest(BaseModel):
    session_id: str
    phone_number: str
    preferred_time: str
    contact_method: str

@router.post("/start")
async def start_conversation(session_id: str):
    """Start a new conversation flow"""
    try:
        if session_id not in conversation_flows:
            conversation_flows[session_id] = ConversationFlow()
        else:
            # Session exists - restart from beginning while keeping responses
            flow = conversation_flows[session_id]
            flow.restart_flow()

        flow = conversation_flows[session_id]

        return {
            "session_id": session_id,
            "status": "started",
            "estimated_time": flow.estimated_total_time,
            "timeline": flow.get_timeline_status(),
            "current_question": flow.get_current_question(),
            "progress": flow.get_progress(),
            "responses": flow.responses  # Include existing responses
        }
    except Exception as e:
        logger.error(f"Error starting conversation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/question/{session_id}")
async def get_current_question(session_id: str):
    """Get the current question in the flow"""
    try:
        if session_id not in conversation_flows:
            raise HTTPException(status_code=404, detail="Session not found")

        flow = conversation_flows[session_id]
        question = flow.get_current_question()

        if not question and flow.is_complete():
            # Flow is complete, run categorization
            summary = flow.get_summary()
            categorization = user_categorizations.categorize_user(
                summary["responses"],
                summary["additional_notes"],
                summary
            )

            return {
                "status": "complete",
                "summary": summary,
                "categorization": categorization,
                "timeline": flow.get_timeline_status(),
                "progress": flow.get_progress()
            }

        return {
            "status": "in_progress",
            "question": question,
            "timeline": flow.get_timeline_status(),
            "progress": flow.get_progress()
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting question: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/answer")
async def submit_answer(request: AnswerRequest):
    """Submit an answer to the current question"""
    try:
        if request.session_id not in conversation_flows:
            raise HTTPException(status_code=404, detail="Session not found")

        flow = conversation_flows[request.session_id]

        # Process the response
        flow.process_response(
            request.question_id,
            request.answer,
            request.is_other,
            request.other_text
        )

        # Get next question
        next_question = flow.get_current_question()

        if not next_question and flow.is_complete():
            # Flow is complete, run categorization
            summary = flow.get_summary()
            categorization = user_categorizations.categorize_user(
                summary["responses"],
                summary["additional_notes"],
                summary
            )

            return {
                "session_id": request.session_id,
                "status": "complete",
                "summary": summary,
                "categorization": categorization,
                "timeline": flow.get_timeline_status(),
                "progress": flow.get_progress()
            }

        return {
            "session_id": request.session_id,
            "status": "in_progress",
            "next_question": next_question,
            "timeline": flow.get_timeline_status(),
            "progress": flow.get_progress(),
            "responses": flow.responses
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error submitting answer: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/category-note")
async def add_category_note(request: CategoryNoteRequest):
    """Add additional note for a category"""
    try:
        if request.session_id not in conversation_flows:
            raise HTTPException(status_code=404, detail="Session not found")

        flow = conversation_flows[request.session_id]
        flow.add_category_note(request.category_id, request.note)

        return {
            "status": "success",
            "message": "Note added successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error adding category note: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/skip-category/{session_id}/{category_id}")
async def skip_category(session_id: str, category_id: str):
    """Skip a category in the flow"""
    try:
        if session_id not in conversation_flows:
            raise HTTPException(status_code=404, detail="Session not found")

        flow = conversation_flows[session_id]
        flow.skip_category(category_id)

        # Get next question after skipping
        next_question = flow.get_current_question()

        return {
            "session_id": session_id,
            "status": "skipped",
            "next_question": next_question,
            "timeline": flow.get_timeline_status(),
            "progress": flow.get_progress()
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error skipping category: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/timeline/{session_id}")
async def get_timeline_status(session_id: str):
    """Get the current timeline status"""
    try:
        if session_id not in conversation_flows:
            raise HTTPException(status_code=404, detail="Session not found")

        flow = conversation_flows[session_id]

        return {
            "timeline": flow.get_timeline_status(),
            "progress": flow.get_progress()
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting timeline: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/schedule-later")
async def schedule_for_later(request: ScheduleRequest):
    """Schedule the conversation to continue later"""
    try:
        if request.session_id not in conversation_flows:
            raise HTTPException(status_code=404, detail="Session not found")

        flow = conversation_flows[request.session_id]
        summary = flow.get_summary()

        # In production, this would:
        # 1. Save the session state to database
        # 2. Send WhatsApp message with continuation link
        # 3. Set up reminder

        # For now, we'll return a success response
        return {
            "status": "scheduled",
            "message": f"We'll reach out to you on {request.contact_method}",
            "phone": request.phone_number,
            "preferred_time": request.preferred_time,
            "progress_saved": summary
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error scheduling for later: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/summary/{session_id}")
async def get_conversation_summary(session_id: str):
    """Get complete conversation summary with categorization"""
    try:
        if session_id not in conversation_flows:
            raise HTTPException(status_code=404, detail="Session not found")

        flow = conversation_flows[session_id]
        summary = flow.get_summary()

        if flow.is_complete():
            categorization = user_categorizations.categorize_user(
                summary["responses"],
                summary["additional_notes"],
                summary
            )

            return {
                "summary": summary,
                "categorization": categorization,
                "is_complete": True
            }

        return {
            "summary": summary,
            "is_complete": False
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting summary: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))