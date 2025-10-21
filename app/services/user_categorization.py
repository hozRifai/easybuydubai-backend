from typing import Dict, List, Optional, Any
from datetime import datetime

class UserCategorization:
    """Categorize users based on their responses to determine lead quality and persona"""

    def __init__(self):
        self.scoring_weights = {
            "timeline": 30,  # How soon they want to buy
            "budget_clarity": 20,  # Clear budget vs flexible
            "financing_ready": 15,  # Pre-approved or cash
            "property_clarity": 15,  # Know what they want
            "decision_speed": 10,  # Can decide quickly
            "engagement": 10  # Completeness of responses
        }

    def categorize_user(self, responses: Dict, additional_notes: Dict, completion_info: Dict) -> Dict:
        """Main categorization function"""

        # Calculate lead score
        lead_score = self._calculate_lead_score(responses)

        # Determine buyer type
        buyer_type = self._determine_buyer_type(lead_score, responses)

        # Identify persona
        persona = self._identify_persona(responses)

        # Determine urgency level
        urgency = self._determine_urgency(responses)

        # Identify service needs
        service_needs = self._identify_service_needs(responses)

        # Generate recommendations
        recommendations = self._generate_recommendations(buyer_type, persona, service_needs)

        return {
            "lead_score": lead_score,
            "buyer_type": buyer_type,
            "persona": persona,
            "urgency_level": urgency,
            "service_needs": service_needs,
            "recommendations": recommendations,
            "categorized_at": datetime.now().isoformat()
        }

    def _calculate_lead_score(self, responses: Dict) -> int:
        """Calculate lead score from 0-100"""
        score = 0

        # Timeline scoring (30 points max)
        timeline_response = responses.get("timeline_1", {}).get("value")
        timeline_scores = {
            "asap": 30,
            "3_months": 25,
            "3_6_months": 15,
            "6_12_months": 10,
            "planning": 5
        }
        score += timeline_scores.get(timeline_response, 0)

        # Budget clarity (20 points max)
        budget_response = responses.get("budget_1", {}).get("value")
        if budget_response and budget_response != "flexible":
            score += 20
        elif budget_response == "flexible":
            score += 10

        # Financing readiness (15 points max)
        payment_method = responses.get("budget_2", {}).get("value")
        bank_status = responses.get("budget_3", {}).get("value")

        if payment_method == "cash":
            score += 15
        elif bank_status == "pre_approved":
            score += 15
        elif payment_method in ["mortgage", "mix"] and bank_status == "planning":
            score += 10
        elif payment_method in ["mortgage", "mix"]:
            score += 5

        # Property clarity (15 points max)
        property_type = responses.get("property_1", {}).get("value")
        bedrooms = responses.get("property_2", {}).get("value")

        if property_type and property_type != "open":
            score += 8
        if bedrooms:
            score += 7

        # Decision speed (10 points max)
        decision = responses.get("decision_1", {}).get("value")
        decision_scores = {
            "quick_decision": 10,
            "partner_discuss": 7,
            "family_approval": 5,
            "think_about": 3
        }
        score += decision_scores.get(decision, 0)

        # Engagement score (10 points max)
        total_responses = len(responses)
        if total_responses >= 20:
            score += 10
        elif total_responses >= 15:
            score += 8
        elif total_responses >= 10:
            score += 5
        else:
            score += 3

        return min(100, score)  # Cap at 100

    def _determine_buyer_type(self, lead_score: int, responses: Dict) -> Dict:
        """Determine the type of buyer based on score and responses"""

        # Check if they've already been looking
        looking_status = responses.get("timeline_2", {}).get("value")

        if lead_score >= 80:
            return {
                "type": "serious_buyer",
                "label": "Serious Buyer",
                "description": "Ready to purchase, clear requirements, financing sorted",
                "priority": "high",
                "follow_up": "immediate"
            }
        elif lead_score >= 60:
            return {
                "type": "active_looker",
                "label": "Active Looker",
                "description": "Actively searching, some clarity needed",
                "priority": "medium-high",
                "follow_up": "within_24_hours"
            }
        elif lead_score >= 40:
            return {
                "type": "early_explorer",
                "label": "Early Explorer",
                "description": "Researching options, longer timeline",
                "priority": "medium",
                "follow_up": "within_week"
            }
        else:
            return {
                "type": "info_seeker",
                "label": "Information Seeker",
                "description": "Just browsing, gathering information",
                "priority": "low",
                "follow_up": "nurture_campaign"
            }

    def _identify_persona(self, responses: Dict) -> Dict:
        """Identify user persona based on responses"""

        # Check primary indicators
        who_living = responses.get("profile_3", {}).get("value")
        first_time = responses.get("profile_2", {}).get("value")
        budget = responses.get("budget_1", {}).get("value")
        property_type = responses.get("property_1", {}).get("value")
        schools = responses.get("lifestyle_1", {}).get("value")
        investment_goal = responses.get("investment_1", {}).get("value")

        personas = []

        # Family-focused
        if who_living == "family" or schools in ["very_important", "somewhat"]:
            personas.append({
                "type": "family_focused",
                "label": "Family-Focused Buyer",
                "key_needs": ["schools", "safe_community", "family_amenities"]
            })

        # Investment-minded
        if who_living == "investment" or investment_goal:
            personas.append({
                "type": "investment_minded",
                "label": "Investment-Minded",
                "key_needs": ["roi_potential", "rental_yield", "location_growth"]
            })

        # Luxury seeker
        if budget in ["3.5m_5m", "5m_plus"] and property_type == "villa":
            personas.append({
                "type": "luxury_seeker",
                "label": "Luxury Seeker",
                "key_needs": ["premium_locations", "high_end_amenities", "exclusivity"]
            })

        # First-timer
        if first_time == "first_time":
            personas.append({
                "type": "first_timer",
                "label": "First-Time Buyer",
                "key_needs": ["guidance", "education", "trusted_advisor"]
            })

        # Value hunter
        if budget in ["under_1m", "1m_2m"] and who_living != "investment":
            personas.append({
                "type": "value_hunter",
                "label": "Value Hunter",
                "key_needs": ["affordable_options", "payment_plans", "emerging_areas"]
            })

        # Upgrader
        if first_time == "owns_property":
            personas.append({
                "type": "upgrader",
                "label": "Property Upgrader",
                "key_needs": ["better_location", "more_space", "lifestyle_upgrade"]
            })

        # Return primary persona or default
        if personas:
            return personas[0]
        else:
            return {
                "type": "general_buyer",
                "label": "General Buyer",
                "key_needs": ["suitable_property", "fair_price", "good_location"]
            }

    def _determine_urgency(self, responses: Dict) -> Dict:
        """Determine urgency level based on timeline and motivation"""

        timeline = responses.get("timeline_1", {}).get("value")
        reason = responses.get("timeline_2", {}).get("value")

        # High urgency indicators
        high_urgency_reasons = ["lease_ending", "new_to_dubai"]
        immediate_timelines = ["asap", "3_months"]

        if timeline in immediate_timelines or reason in high_urgency_reasons:
            return {
                "level": "high",
                "label": "High Urgency",
                "action": "immediate_attention",
                "reason": reason
            }
        elif timeline == "3_6_months":
            return {
                "level": "moderate",
                "label": "Moderate Urgency",
                "action": "regular_follow_up",
                "reason": reason
            }
        else:
            return {
                "level": "low",
                "label": "Low Urgency",
                "action": "nurture_campaign",
                "reason": reason
            }

    def _identify_service_needs(self, responses: Dict) -> List[str]:
        """Identify what services the user needs"""

        services = []

        # Check financing needs
        payment_method = responses.get("budget_2", {}).get("value")
        bank_status = responses.get("budget_3", {}).get("value")

        if payment_method in ["mortgage", "mix"]:
            if bank_status == "need_guidance":
                services.append("mortgage_assistance")
            elif bank_status == "planning":
                services.append("bank_introduction")

        # Check if first-timer
        first_time = responses.get("profile_2", {}).get("value")
        if first_time == "first_time":
            services.append("full_guidance")
            services.append("legal_assistance")

        # Check viewing preference
        viewing_pref = responses.get("decision_2", {}).get("value")
        if viewing_pref == "virtual_first":
            services.append("virtual_tours")
        elif viewing_pref == "in_person":
            services.append("property_viewings")

        # Investment services
        if responses.get("profile_3", {}).get("value") == "investment":
            services.append("investment_analysis")
            services.append("rental_management")

        # Default services
        if not services:
            services.append("property_matching")
            services.append("viewing_arrangement")

        return services

    def _generate_recommendations(self, buyer_type: Dict, persona: Dict, service_needs: List[str]) -> Dict:
        """Generate recommendations for how to handle this lead"""

        recommendations = {
            "agent_type": "",
            "initial_action": "",
            "properties_to_show": "",
            "follow_up_strategy": "",
            "key_talking_points": []
        }

        # Agent type recommendation
        if "investment_minded" in persona.get("type", ""):
            recommendations["agent_type"] = "Investment specialist"
        elif "luxury_seeker" in persona.get("type", ""):
            recommendations["agent_type"] = "Luxury property expert"
        elif "family_focused" in persona.get("type", ""):
            recommendations["agent_type"] = "Family homes specialist"
        else:
            recommendations["agent_type"] = "General property consultant"

        # Initial action based on buyer type
        if buyer_type["type"] == "serious_buyer":
            recommendations["initial_action"] = "Call immediately and arrange viewings"
            recommendations["properties_to_show"] = "5-7 best matches, ready to visit"
        elif buyer_type["type"] == "active_looker":
            recommendations["initial_action"] = "Send curated property selection"
            recommendations["properties_to_show"] = "3-5 strong options"
        else:
            recommendations["initial_action"] = "Send welcome email with market guide"
            recommendations["properties_to_show"] = "2-3 examples to gauge interest"

        # Follow-up strategy
        recommendations["follow_up_strategy"] = buyer_type["follow_up"]

        # Key talking points based on persona
        if persona["type"] == "family_focused":
            recommendations["key_talking_points"] = [
                "School proximity and quality",
                "Safe, family-friendly communities",
                "Parks and recreational facilities"
            ]
        elif persona["type"] == "investment_minded":
            recommendations["key_talking_points"] = [
                "ROI and rental yields",
                "Growth potential areas",
                "Developer reputation and track record"
            ]
        elif persona["type"] == "first_timer":
            recommendations["key_talking_points"] = [
                "Step-by-step buying process",
                "Ownership laws and regulations",
                "Hidden costs and fees"
            ]
        else:
            recommendations["key_talking_points"] = [
                "Property features and amenities",
                "Location advantages",
                "Value proposition"
            ]

        return recommendations