from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum
import json

class FlowCategory(Enum):
    PROFILE = "profile"
    BUDGET = "budget"
    PROPERTY = "property"
    LOCATION = "location"
    TIMELINE = "timeline"
    LIFESTYLE = "lifestyle"
    INVESTMENT = "investment"
    PRIORITIES = "priorities"
    DECISION = "decision"
    CONTACT = "contact"

class QuestionType(Enum):
    SINGLE_CHOICE = "single_choice"
    MULTIPLE_CHOICE = "multiple_choice"
    TEXT_INPUT = "text_input"
    RANGE = "range"

class ConversationFlow:
    def __init__(self):
        self.categories = self._initialize_categories()
        self.questions = self._initialize_questions()
        self.current_category_index = 0
        self.current_question_index = 0
        self.responses = {}
        self.additional_notes = {}
        self.skipped_categories = []
        self.start_time = datetime.now()
        self.estimated_total_time = 10  # minutes

    def restart_flow(self):
        """Restart the flow from the beginning while keeping responses"""
        self.current_category_index = 0
        self.current_question_index = 0
        self.start_time = datetime.now()
        # Keep responses, additional_notes, and skipped_categories

    def _initialize_categories(self) -> List[Dict]:
        """Initialize the conversation categories with metadata"""
        return [
            {
                "id": FlowCategory.PROFILE.value,
                "name": "Profile",
                "description": "Understanding your situation",
                "estimated_time": 1.5,
                "icon": "👤",
                "is_optional": False
            },
            {
                "id": FlowCategory.BUDGET.value,
                "name": "Budget",
                "description": "Financial comfort zone",
                "estimated_time": 1,
                "icon": "💰",
                "is_optional": False
            },
            {
                "id": FlowCategory.PROPERTY.value,
                "name": "Property",
                "description": "Your dream property",
                "estimated_time": 1.5,
                "icon": "🏠",
                "is_optional": False
            },
            {
                "id": FlowCategory.LOCATION.value,
                "name": "Location",
                "description": "Perfect neighborhood",
                "estimated_time": 1,
                "icon": "📍",
                "is_optional": False
            },
            {
                "id": FlowCategory.TIMELINE.value,
                "name": "Timeline",
                "description": "Your property journey",
                "estimated_time": 0.5,
                "icon": "📅",
                "is_optional": False
            },
            {
                "id": FlowCategory.LIFESTYLE.value,
                "name": "Lifestyle",
                "description": "Your lifestyle needs",
                "estimated_time": 1,
                "icon": "🌟",
                "is_optional": False
            },
            {
                "id": FlowCategory.INVESTMENT.value,
                "name": "Investment",
                "description": "Investment goals",
                "estimated_time": 1,
                "icon": "📈",
                "is_optional": True  # Only for investors
            },
            {
                "id": FlowCategory.PRIORITIES.value,
                "name": "Priorities",
                "description": "Deal makers & breakers",
                "estimated_time": 1,
                "icon": "⭐",
                "is_optional": False
            },
            {
                "id": FlowCategory.DECISION.value,
                "name": "Decision",
                "description": "How you make decisions",
                "estimated_time": 0.5,
                "icon": "🤔",
                "is_optional": False
            },
            {
                "id": FlowCategory.CONTACT.value,
                "name": "Contact",
                "description": "How to reach you",
                "estimated_time": 1,
                "icon": "📱",
                "is_optional": False
            }
        ]

    def _initialize_questions(self) -> Dict[str, List[Dict]]:
        """Initialize all questions for each category"""
        return {
            FlowCategory.PROFILE.value: [
                {
                    "id": "profile_1",
                    "question": "Are you currently living in Dubai, or planning to move here?",
                    "type": QuestionType.SINGLE_CHOICE.value,
                    "options": [
                        {"label": "Already living here", "value": "already_here", "icon": "🏙️"},
                        {"label": "Planning to move", "value": "planning_move", "icon": "✈️"},
                        {"label": "Investing from abroad", "value": "investing_abroad", "icon": "🌍"}
                    ],
                    "has_other": True,
                    "other_prompt": "Tell us more about your situation",
                    "is_optional": False
                },
                {
                    "id": "profile_2",
                    "question": "Is this your first time buying property in Dubai?",
                    "type": QuestionType.SINGLE_CHOICE.value,
                    "options": [
                        {"label": "Yes, first time", "value": "first_time", "icon": "🆕"},
                        {"label": "I own property here", "value": "owns_property", "icon": "🏘️"},
                        {"label": "I've bought before but sold", "value": "previous_owner", "icon": "🔄"}
                    ],
                    "has_other": False,
                    "is_optional": False
                },
                {
                    "id": "profile_3",
                    "question": "Who will be living in this property?",
                    "type": QuestionType.SINGLE_CHOICE.value,
                    "options": [
                        {"label": "Just me", "value": "single", "icon": "👤"},
                        {"label": "Me and my partner", "value": "couple", "icon": "👥"},
                        {"label": "My family", "value": "family", "icon": "👨‍👩‍👧‍👦"},
                        {"label": "It's an investment", "value": "investment", "icon": "💼"}
                    ],
                    "has_other": True,
                    "other_prompt": "Tell us about who'll be living there",
                    "is_optional": False
                }
            ],
            FlowCategory.BUDGET.value: [
                {
                    "id": "budget_1",
                    "question": "What's your comfortable budget range?",
                    "type": QuestionType.SINGLE_CHOICE.value,
                    "options": [
                        {"label": "Under 1M AED", "value": "under_1m", "icon": "💵"},
                        {"label": "1M - 2M AED", "value": "1m_2m", "icon": "💵"},
                        {"label": "2M - 3.5M AED", "value": "2m_3.5m", "icon": "💵"},
                        {"label": "3.5M - 5M AED", "value": "3.5m_5m", "icon": "💵"},
                        {"label": "5M+ AED", "value": "5m_plus", "icon": "💵"},
                        {"label": "Flexible/Not sure", "value": "flexible", "icon": "🤷"}
                    ],
                    "has_other": True,
                    "other_prompt": "Share your budget thoughts",
                    "is_optional": False
                },
                {
                    "id": "budget_2",
                    "question": "How are you planning to purchase?",
                    "type": QuestionType.SINGLE_CHOICE.value,
                    "options": [
                        {"label": "Cash purchase", "value": "cash", "icon": "💳"},
                        {"label": "Will need a mortgage", "value": "mortgage", "icon": "🏦"},
                        {"label": "Mix of both", "value": "mix", "icon": "💰"}
                    ],
                    "has_other": False,
                    "is_optional": False
                },
                {
                    "id": "budget_3",
                    "question": "Have you spoken to any banks yet?",
                    "type": QuestionType.SINGLE_CHOICE.value,
                    "options": [
                        {"label": "Yes, pre-approved", "value": "pre_approved", "icon": "✅"},
                        {"label": "Planning to", "value": "planning", "icon": "📅"},
                        {"label": "Need guidance", "value": "need_guidance", "icon": "❓"},
                        {"label": "Rather not say", "value": "private", "icon": "🤐"}
                    ],
                    "has_other": False,
                    "is_optional": False,
                    "condition": {"budget_2": ["mortgage", "mix"]}  # Only ask if needs financing
                }
            ],
            FlowCategory.PROPERTY.value: [
                {
                    "id": "property_1",
                    "question": "Are you thinking apartment living or do you want your own villa?",
                    "type": QuestionType.SINGLE_CHOICE.value,
                    "options": [
                        {"label": "Apartment", "value": "apartment", "icon": "🏢"},
                        {"label": "Villa", "value": "villa", "icon": "🏡"},
                        {"label": "Townhouse", "value": "townhouse", "icon": "🏘️"},
                        {"label": "Open to suggestions", "value": "open", "icon": "🤔"}
                    ],
                    "has_other": True,
                    "other_prompt": "What type of property interests you?",
                    "is_optional": False
                },
                {
                    "id": "property_2",
                    "question": "How much space do you need?",
                    "type": QuestionType.SINGLE_CHOICE.value,
                    "options": [
                        {"label": "Cozy studio", "value": "studio", "icon": "🛏️"},
                        {"label": "1 bedroom", "value": "1br", "icon": "🛏️"},
                        {"label": "2 bedrooms", "value": "2br", "icon": "🛏️"},
                        {"label": "3 bedrooms", "value": "3br", "icon": "🛏️"},
                        {"label": "4 bedrooms", "value": "4br", "icon": "🛏️"},
                        {"label": "5+ bedrooms", "value": "5br_plus", "icon": "🛏️"}
                    ],
                    "has_other": False,
                    "is_optional": False
                },
                {
                    "id": "property_3",
                    "question": "Do you prefer shiny and new, or are established properties fine?",
                    "type": QuestionType.SINGLE_CHOICE.value,
                    "options": [
                        {"label": "Brand new only", "value": "new_only", "icon": "✨"},
                        {"label": "Relatively new (under 5 years)", "value": "relatively_new", "icon": "🆕"},
                        {"label": "Age doesn't matter if nice", "value": "age_flexible", "icon": "👍"}
                    ],
                    "has_other": False,
                    "is_optional": False
                }
            ],
            FlowCategory.LOCATION.value: [
                {
                    "id": "location_1",
                    "question": "What kind of vibe are you looking for?",
                    "type": QuestionType.SINGLE_CHOICE.value,
                    "options": [
                        {"label": "Beachside & resort feel", "value": "beachside", "icon": "🏖️"},
                        {"label": "Urban & city center", "value": "urban", "icon": "🏙️"},
                        {"label": "Family community", "value": "family_community", "icon": "👨‍👩‍👧"},
                        {"label": "Quiet & green", "value": "quiet_green", "icon": "🌳"}
                    ],
                    "has_other": True,
                    "other_prompt": "Describe your ideal neighborhood vibe",
                    "is_optional": False
                },
                {
                    "id": "location_2",
                    "question": "Tell me about your typical day - do you need to commute somewhere regularly?",
                    "type": QuestionType.SINGLE_CHOICE.value,
                    "options": [
                        {"label": "Yes, to DIFC/Downtown", "value": "difc_downtown", "icon": "🏢"},
                        {"label": "Yes, to Marina/JLT", "value": "marina_jlt", "icon": "🏢"},
                        {"label": "Yes, to Abu Dhabi", "value": "abu_dhabi", "icon": "🏢"},
                        {"label": "Work from home", "value": "wfh", "icon": "🏠"},
                        {"label": "Retired/flexible", "value": "flexible", "icon": "😌"},
                        {"label": "Multiple locations", "value": "multiple", "icon": "🚗"}
                    ],
                    "has_other": True,
                    "other_prompt": "Where do you need to commute to?",
                    "is_optional": False
                }
            ],
            FlowCategory.TIMELINE.value: [
                {
                    "id": "timeline_1",
                    "question": "When do you hope to move in?",
                    "type": QuestionType.SINGLE_CHOICE.value,
                    "options": [
                        {"label": "ASAP", "value": "asap", "icon": "🚀"},
                        {"label": "Next 3 months", "value": "3_months", "icon": "📅"},
                        {"label": "3-6 months", "value": "3_6_months", "icon": "📅"},
                        {"label": "6-12 months", "value": "6_12_months", "icon": "📅"},
                        {"label": "Just planning ahead", "value": "planning", "icon": "🔮"}
                    ],
                    "has_other": False,
                    "is_optional": False
                },
                {
                    "id": "timeline_2",
                    "question": "What's bringing you to the market now?",
                    "type": QuestionType.SINGLE_CHOICE.value,
                    "options": [
                        {"label": "Lease ending soon", "value": "lease_ending", "icon": "📝"},
                        {"label": "Family growing", "value": "family_growing", "icon": "👶"},
                        {"label": "Good time to invest", "value": "investment_timing", "icon": "📈"},
                        {"label": "Just got to Dubai", "value": "new_to_dubai", "icon": "✈️"},
                        {"label": "Been planning this", "value": "planned", "icon": "📋"}
                    ],
                    "has_other": True,
                    "other_prompt": "What's your motivation?",
                    "is_optional": False
                }
            ],
            FlowCategory.LIFESTYLE.value: [
                {
                    "id": "lifestyle_1",
                    "question": "Do schools play a part in your location choice?",
                    "type": QuestionType.SINGLE_CHOICE.value,
                    "options": [
                        {"label": "Very important", "value": "very_important", "icon": "🎓"},
                        {"label": "Somewhat important", "value": "somewhat", "icon": "📚"},
                        {"label": "Not a factor", "value": "not_factor", "icon": "❌"}
                    ],
                    "has_other": False,
                    "is_optional": False,
                    "condition": {"profile_3": ["family"]}  # Only ask families
                },
                {
                    "id": "lifestyle_2",
                    "question": "What would make your home perfect? (Pick what matters)",
                    "type": QuestionType.MULTIPLE_CHOICE.value,
                    "options": [
                        {"label": "Pool for weekends", "value": "pool", "icon": "🏊"},
                        {"label": "Gym to stay fit", "value": "gym", "icon": "💪"},
                        {"label": "Kids' play areas", "value": "kids_area", "icon": "🎮"},
                        {"label": "Pet-friendly", "value": "pet_friendly", "icon": "🐕"},
                        {"label": "Great views", "value": "views", "icon": "🌅"},
                        {"label": "Peaceful garden", "value": "garden", "icon": "🌿"}
                    ],
                    "has_other": True,
                    "other_prompt": "What else would make it perfect?",
                    "is_optional": True
                }
            ],
            FlowCategory.INVESTMENT.value: [
                {
                    "id": "investment_1",
                    "question": "What's your main goal with this investment?",
                    "type": QuestionType.SINGLE_CHOICE.value,
                    "options": [
                        {"label": "Rental income", "value": "rental", "icon": "💰"},
                        {"label": "Long-term appreciation", "value": "appreciation", "icon": "📈"},
                        {"label": "Holiday home", "value": "holiday", "icon": "🏖️"},
                        {"label": "Future residence", "value": "future_residence", "icon": "🏠"}
                    ],
                    "has_other": True,
                    "other_prompt": "Tell us about your investment goals",
                    "is_optional": False,
                    "condition": {"profile_3": ["investment"]}
                },
                {
                    "id": "investment_2",
                    "question": "Are you looking for something that rents easily?",
                    "type": QuestionType.SINGLE_CHOICE.value,
                    "options": [
                        {"label": "Yes, rental yield is key", "value": "yield_key", "icon": "🔑"},
                        {"label": "Nice to have", "value": "nice_to_have", "icon": "👍"},
                        {"label": "Not important", "value": "not_important", "icon": "🤷"}
                    ],
                    "has_other": False,
                    "is_optional": False,
                    "condition": {"profile_3": ["investment"]}
                }
            ],
            FlowCategory.PRIORITIES.value: [
                {
                    "id": "priorities_1",
                    "question": "What would make you say 'this is the one!'?",
                    "type": QuestionType.MULTIPLE_CHOICE.value,
                    "options": [
                        {"label": "Perfect location", "value": "location", "icon": "📍"},
                        {"label": "Great value", "value": "value", "icon": "💎"},
                        {"label": "Amazing view", "value": "view", "icon": "🌆"},
                        {"label": "Love the community", "value": "community", "icon": "🏘️"},
                        {"label": "Just feels right", "value": "feeling", "icon": "❤️"}
                    ],
                    "has_other": True,
                    "other_prompt": "What else would seal the deal?",
                    "is_optional": False
                },
                {
                    "id": "priorities_2",
                    "question": "What would make you walk away immediately?",
                    "type": QuestionType.MULTIPLE_CHOICE.value,
                    "options": [
                        {"label": "Too noisy", "value": "noisy", "icon": "🔊"},
                        {"label": "No parking", "value": "no_parking", "icon": "🚗"},
                        {"label": "Needs too much work", "value": "needs_work", "icon": "🔨"},
                        {"label": "Bad location", "value": "bad_location", "icon": "❌"},
                        {"label": "Over budget", "value": "over_budget", "icon": "💸"}
                    ],
                    "has_other": True,
                    "other_prompt": "What else is a deal breaker?",
                    "is_optional": True
                }
            ],
            FlowCategory.DECISION.value: [
                {
                    "id": "decision_1",
                    "question": "When you find the right place, what happens next?",
                    "type": QuestionType.SINGLE_CHOICE.value,
                    "options": [
                        {"label": "I can decide quickly", "value": "quick_decision", "icon": "⚡"},
                        {"label": "Need to discuss with partner", "value": "partner_discuss", "icon": "💑"},
                        {"label": "Need family approval", "value": "family_approval", "icon": "👨‍👩‍👧‍👦"},
                        {"label": "Want to think about it", "value": "think_about", "icon": "🤔"}
                    ],
                    "has_other": False,
                    "is_optional": False
                },
                {
                    "id": "decision_2",
                    "question": "How do you prefer to explore properties?",
                    "type": QuestionType.SINGLE_CHOICE.value,
                    "options": [
                        {"label": "In-person viewings", "value": "in_person", "icon": "🚶"},
                        {"label": "Virtual tours first", "value": "virtual_first", "icon": "💻"},
                        {"label": "Both work for me", "value": "both", "icon": "🔄"},
                        {"label": "Send me details first", "value": "details_first", "icon": "📧"}
                    ],
                    "has_other": False,
                    "is_optional": False
                }
            ],
            FlowCategory.CONTACT.value: [
                {
                    "id": "contact_1",
                    "question": "How would you prefer I share property options with you?",
                    "type": QuestionType.MULTIPLE_CHOICE.value,
                    "options": [
                        {"label": "WhatsApp messages", "value": "whatsapp", "icon": "📱"},
                        {"label": "Email with details", "value": "email", "icon": "📧"},
                        {"label": "Quick call", "value": "call", "icon": "📞"},
                        {"label": "All of the above", "value": "all", "icon": "✅"}
                    ],
                    "has_other": False,
                    "is_optional": False
                },
                {
                    "id": "contact_2",
                    "question": "When's usually good to reach you?",
                    "type": QuestionType.SINGLE_CHOICE.value,
                    "options": [
                        {"label": "Mornings", "value": "morning", "icon": "🌅"},
                        {"label": "Afternoons", "value": "afternoon", "icon": "☀️"},
                        {"label": "Evenings", "value": "evening", "icon": "🌙"},
                        {"label": "Weekends", "value": "weekends", "icon": "📅"},
                        {"label": "Anytime is fine", "value": "anytime", "icon": "⏰"}
                    ],
                    "has_other": False,
                    "is_optional": False
                }
            ]
        }

    def get_current_question(self) -> Optional[Dict]:
        """Get the current question based on flow state"""
        # Check if we've completed all categories
        if self.current_category_index >= len(self.categories):
            return None

        category = self.categories[self.current_category_index]
        category_id = category["id"]

        if category_id in self.questions:
            questions = self.questions[category_id]

            # Loop through questions in current category
            while self.current_question_index < len(questions):
                question = questions[self.current_question_index]

                # Check if question has conditions
                if "condition" in question:
                    # Check if conditions are met
                    condition_met = True
                    for key, values in question["condition"].items():
                        if key in self.responses:
                            response_value = self.responses[key]["value"] if isinstance(self.responses[key], dict) else self.responses[key]
                            if response_value not in values:
                                condition_met = False
                                break

                    if not condition_met:
                        # Skip this question
                        self.current_question_index += 1
                        continue

                return question

            # No more questions in this category, move to next
            self.current_category_index += 1
            self.current_question_index = 0
            return self.get_current_question()

        # Category has no questions, move to next
        self.current_category_index += 1
        self.current_question_index = 0
        return self.get_current_question()

    def process_response(self, question_id: str, response: Any, is_other: bool = False, other_text: str = None):
        """Process and store user response"""
        self.responses[question_id] = {
            "value": response,
            "is_other": is_other,
            "other_text": other_text,
            "timestamp": datetime.now().isoformat()
        }

        # Move to next question
        self.current_question_index += 1

        # Check if category is complete
        category = self.categories[self.current_category_index]
        category_id = category["id"]
        if self.current_question_index >= len(self.questions.get(category_id, [])):
            self.current_category_index += 1
            self.current_question_index = 0

    def add_category_note(self, category_id: str, note: str):
        """Add additional note for a category"""
        if category_id not in self.additional_notes:
            self.additional_notes[category_id] = []
        self.additional_notes[category_id].append({
            "note": note,
            "timestamp": datetime.now().isoformat()
        })

    def skip_category(self, category_id: str):
        """Skip a category"""
        self.skipped_categories.append(category_id)
        # Find and skip to next category
        for i, cat in enumerate(self.categories):
            if cat["id"] == category_id:
                if i == self.current_category_index:
                    self.current_category_index += 1
                    self.current_question_index = 0
                break

    def get_progress(self) -> Dict:
        """Calculate and return progress information"""
        total_categories = len(self.categories)
        completed_categories = self.current_category_index

        # Calculate total questions answered
        total_questions = 0
        answered_questions = len(self.responses)

        for cat_id, questions in self.questions.items():
            total_questions += len(questions)

        # Calculate time elapsed and remaining
        elapsed_time = (datetime.now() - self.start_time).total_seconds() / 60

        # Estimate remaining time based on categories left
        remaining_categories = total_categories - completed_categories - len(self.skipped_categories)
        avg_time_per_category = self.estimated_total_time / total_categories
        estimated_remaining = remaining_categories * avg_time_per_category

        return {
            "current_category": self.categories[self.current_category_index]["id"] if self.current_category_index < total_categories else "complete",
            "current_category_name": self.categories[self.current_category_index]["name"] if self.current_category_index < total_categories else "Complete",
            "categories_completed": completed_categories,
            "total_categories": total_categories,
            "questions_answered": answered_questions,
            "total_questions": total_questions,
            "percentage_complete": round((completed_categories / total_categories) * 100),
            "time_elapsed": round(elapsed_time, 1),
            "estimated_remaining": round(estimated_remaining, 1),
            "skipped_categories": self.skipped_categories
        }

    def get_timeline_status(self) -> List[Dict]:
        """Get status of all categories for timeline display"""
        timeline = []
        for i, category in enumerate(self.categories):
            status = "completed" if i < self.current_category_index else \
                    "active" if i == self.current_category_index else \
                    "skipped" if category["id"] in self.skipped_categories else \
                    "upcoming"

            timeline.append({
                "id": category["id"],
                "name": category["name"],
                "icon": category["icon"],
                "status": status,
                "is_optional": category["is_optional"]
            })

        return timeline

    def is_complete(self) -> bool:
        """Check if the conversation flow is complete"""
        return self.current_category_index >= len(self.categories)

    def get_summary(self) -> Dict:
        """Get a summary of all collected information"""
        return {
            "responses": self.responses,
            "additional_notes": self.additional_notes,
            "skipped_categories": self.skipped_categories,
            "completion_time": (datetime.now() - self.start_time).total_seconds() / 60,
            "is_complete": self.is_complete()
        }