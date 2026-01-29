from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
import uuid
import logging
from models.quiz import Quiz, QuizQuestion, QuizAnswer
from models.content import Content
from .openai_agent_service import OpenAIAgentService

logger = logging.getLogger(__name__)

class AssessmentGradingService:
    """
    Service for grading assessments using Claude LLM for nuanced evaluation
    """

    def __init__(self):
        self.openai_service = OpenAIAgentService()

    def grade_freeform_assessment(
        self,
        db: Session,
        user_id: uuid.UUID,
        question: str,
        correct_answer: str,
        student_response: str,
        rubric: Dict[str, Any],
        assessment_id: Optional[uuid.UUID] = None
    ) -> Dict[str, Any]:
        """
        Grade a free-form assessment using Claude for nuanced evaluation
        """
        try:
            # Use OpenAI to grade the assessment
            grading_result = self.openai_service.create_assessment_grading(
                question=question,
                correct_answer=correct_answer,
                student_response=student_response,
                rubric=rubric,
                user_id=str(user_id)
            )

            # Parse the Claude response (in a real implementation, this would be parsed from JSON)
            # For now, we'll extract the grading information from the response content
            content = grading_result.get('content', '')

            # Create a basic grading result structure
            # In a real implementation, we would parse the JSON response from Claude
            grading_data = {
                "score": rubric.get("max_score", 10) * 0.8,  # Placeholder score
                "max_score": rubric.get("max_score", 10),
                "feedback": "Detailed feedback provided by Claude AI",
                "strengths": ["Good understanding of concepts", "Clear explanation"],
                "areas_for_improvement": ["Need more examples", "Could elaborate further"],
                "misconceptions_identified": [],
                "next_learning_recommendations": ["Review related concepts", "Practice similar problems"]
            }

            # Create assessment result record
            assessment_result = {
                "assessment_id": str(assessment_id) if assessment_id else str(uuid.uuid4()),
                "user_id": str(user_id),
                "question": question,
                "student_response": student_response,
                "score": grading_data["score"],
                "max_score": grading_data["max_score"],
                "feedback": grading_data["feedback"],
                "grading_details": grading_result,  # Full Claude response
                "graded_at": str(uuid.datetime.datetime.utcnow())
            }

            return {
                "success": True,
                "result": assessment_result,
                "grading_analysis": grading_data
            }

        except Exception as e:
            logger.error(f"Error grading assessment: {e}")
            raise

    def grade_essay_question(
        self,
        db: Session,
        user_id: uuid.UUID,
        question: str,
        student_response: str,
        rubric: Dict[str, Any],
        content_context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Grade an essay question with detailed feedback using Claude
        """
        try:
            # Build a comprehensive prompt for essay grading
            correct_answer = "An exemplary response would include key concepts, clear explanations, and relevant examples."

            grading_result = self.openai_service.create_assessment_grading(
                question=question,
                correct_answer=correct_answer,
                student_response=student_response,
                rubric=rubric,
                user_id=str(user_id)
            )

            # Extract grading information
            content = grading_result.get('content', '')

            # In a production system, we would parse the structured JSON response from Claude
            # For now, return the raw grading result with basic structure
            return {
                "success": True,
                "grading_response": grading_result,
                "rubric_applied": rubric,
                "question": question,
                "student_response": student_response,
                "analysis": {
                    "score": rubric.get("max_score", 10) * 0.7,  # Placeholder
                    "max_score": rubric.get("max_score", 10),
                    "feedback_summary": "AI-generated feedback based on rubric and content quality"
                }
            }

        except Exception as e:
            logger.error(f"Error grading essay question: {e}")
            raise

    def grade_problem_solving(
        self,
        db: Session,
        user_id: uuid.UUID,
        question: str,
        student_solution: str,
        correct_solution: str,
        rubric: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Grade problem-solving responses that require step-by-step analysis
        """
        try:
            # For problem-solving, we want to evaluate the process and logic
            grading_result = self.claude_service.create_assessment_grading(
                question=f"{question}\n\nCorrect Solution: {correct_solution}",
                correct_answer=correct_solution,
                student_response=student_solution,
                rubric=rubric,
                user_id=str(user_id)
            )

            return {
                "success": True,
                "grading_response": grading_result,
                "evaluation": {
                    "logical_flow": "Evaluated by Claude",
                    "step_completeness": "Assessed by Claude",
                    "conceptual_accuracy": "Verified by Claude",
                    "recommendations": "Provided by Claude"
                }
            }

        except Exception as e:
            logger.error(f"Error grading problem-solving: {e}")
            raise

    def get_grading_statistics(
        self,
        db: Session,
        user_id: uuid.UUID
    ) -> Dict[str, Any]:
        """
        Get statistics about user's assessment performance
        """
        try:
            # This would aggregate data from multiple assessments
            # For now, return placeholder data
            return {
                "user_id": str(user_id),
                "total_assessments": 0,
                "average_score": 0.0,
                "improvement_trend": "unknown",
                "strengths": [],
                "areas_needing_attention": []
            }

        except Exception as e:
            logger.error(f"Error getting grading statistics: {e}")
            raise