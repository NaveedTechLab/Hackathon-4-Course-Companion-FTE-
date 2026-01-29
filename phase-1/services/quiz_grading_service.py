from sqlalchemy.orm import Session
from models.quiz import Quiz, QuizQuestion, QuizAnswer
from models.content import Content
from typing import List, Dict, Any, Optional
import uuid
import json
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class QuizGradingService:
    """
    Service for grading quizzes using rule-based evaluation (no LLM calls)
    """

    def __init__(self):
        pass

    def grade_quiz_submission(
        self,
        db: Session,
        user_id: uuid.UUID,
        quiz_id: uuid.UUID,
        user_answers: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Grade a quiz submission using rule-based evaluation
        """
        # Get the quiz and its questions
        quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
        if not quiz:
            raise ValueError("Quiz not found")

        questions = db.query(QuizQuestion).filter(
            QuizQuestion.quiz_id == quiz_id
        ).order_by(QuizQuestion.question_order).all()

        if not questions:
            raise ValueError("No questions found for this quiz")

        # Create a mapping of question_id to question for easy lookup
        question_map = {q.id: q for q in questions}

        # Grade each answer
        graded_results = []
        total_possible_points = 0
        earned_points = 0

        for answer in user_answers:
            question_id = answer.get("question_id")
            user_answer = answer.get("answer_text", "")

            if question_id not in question_map:
                continue  # Skip answers to questions that don't exist

            question = question_map[question_id]
            total_possible_points += question.points

            # Get correct answers for this question
            correct_answers = db.query(QuizAnswer).filter(
                QuizAnswer.question_id == question_id,
                QuizAnswer.is_correct == True
            ).all()

            # Grade the answer based on question type
            is_correct, points_awarded, feedback = self._grade_single_answer(
                question, user_answer, correct_answers
            )

            if is_correct:
                earned_points += points_awarded

            graded_results.append({
                "question_id": question_id,
                "question_text": question.question_text,
                "user_answer": user_answer,
                "is_correct": is_correct,
                "points_awarded": points_awarded,
                "points_possible": question.points,
                "feedback": feedback,
                "question_type": question.question_type.value
            })

        # Calculate overall score
        overall_score = (earned_points / total_possible_points * 100) if total_possible_points > 0 else 0

        return {
            "quiz_id": quiz_id,
            "user_id": user_id,
            "overall_score": round(overall_score, 2),
            "max_score": total_possible_points,
            "earned_points": earned_points,
            "graded_answers": graded_results,
            "breakdown": self._create_score_breakdown(graded_results),
            "detailed_feedback": self._generate_overall_feedback(graded_results, overall_score),
            "suggested_improvements": self._generate_suggestions(graded_results),
            "misconceptions_identified": self._identify_misconceptions(graded_results),
            "next_learning_recommendations": self._generate_recommendations(graded_results),
            "confidence_level": self._calculate_confidence_level(overall_score),
            "grading_method": "rule_based"
        }

    def _grade_single_answer(
        self,
        question: QuizQuestion,
        user_answer: str,
        correct_answers: List[QuizAnswer]
    ) -> tuple[bool, int, str]:
        """
        Grade a single answer based on question type
        """
        if question.question_type.value == "mcq":  # Multiple Choice Question
            return self._grade_mcq(user_answer, correct_answers)
        elif question.question_type.value == "tf":  # True/False
            return self._grade_true_false(user_answer, correct_answers)
        elif question.question_type.value == "fill_blank":
            return self._grade_fill_blank(user_answer, correct_answers)
        elif question.question_type.value == "essay":
            return self._grade_essay(user_answer, correct_answers)
        else:
            # Default to simple text comparison
            return self._grade_text_comparison(user_answer, correct_answers)

    def _grade_mcq(self, user_answer: str, correct_answers: List[QuizAnswer]) -> tuple[bool, int, str]:
        """
        Grade multiple choice question
        """
        user_answer_lower = user_answer.lower().strip()
        points_awarded = 0
        feedback = "Incorrect answer."

        for correct_answer in correct_answers:
            correct_text_lower = correct_answer.answer_text.lower().strip()

            if user_answer_lower == correct_text_lower:
                points_awarded = correct_answer.points_awarded
                feedback = "Correct! Well done."
                return True, points_awarded, feedback

        # If no exact match, check if user selected a correct option (for multiple correct answers)
        for correct_answer in correct_answers:
            if correct_answer.answer_text.lower().strip() in user_answer_lower:
                points_awarded = correct_answer.points_awarded
                feedback = "Partially correct. Consider reviewing the material for a complete answer."
                return True, points_awarded, feedback

        # Find the closest match for feedback
        if correct_answers:
            feedback = f"Incorrect. The correct answer was: {correct_answers[0].answer_text}"

        return False, points_awarded, feedback

    def _grade_true_false(self, user_answer: str, correct_answers: List[QuizAnswer]) -> tuple[bool, int, str]:
        """
        Grade true/false question
        """
        user_answer_lower = user_answer.lower().strip()
        points_awarded = 0
        feedback = "Incorrect answer."

        for correct_answer in correct_answers:
            correct_text_lower = correct_answer.answer_text.lower().strip()

            # Check various forms of true/false
            if (
                (correct_text_lower in ["true", "yes", "correct"] and
                 user_answer_lower in ["true", "yes", "correct", "t", "y"]) or
                (correct_text_lower in ["false", "no", "incorrect"] and
                 user_answer_lower in ["false", "no", "incorrect", "f", "n"])
            ):
                points_awarded = correct_answer.points_awarded
                feedback = "Correct! Well done."
                return True, points_awarded, feedback

        if correct_answers:
            correct_value = correct_answers[0].answer_text
            feedback = f"Incorrect. The correct answer was: {correct_value}"

        return False, points_awarded, feedback

    def _grade_fill_blank(self, user_answer: str, correct_answers: List[QuizAnswer]) -> tuple[bool, int, str]:
        """
        Grade fill-in-the-blank question
        """
        if not user_answer.strip():
            return False, 0, "No answer provided."

        user_answer_lower = user_answer.lower().strip()
        points_awarded = 0
        feedback = "Incorrect answer."

        for correct_answer in correct_answers:
            correct_text_lower = correct_answer.answer_text.lower().strip()

            # Exact match
            if user_answer_lower == correct_text_lower:
                points_awarded = correct_answer.points_awarded
                feedback = "Correct! Well done."
                return True, points_awarded, feedback

            # Partial match (allowing for minor differences)
            if correct_text_lower in user_answer_lower or user_answer_lower in correct_text_lower:
                points_awarded = correct_answer.points_awarded * 0.8  # Partial credit
                feedback = "Close! The answer was slightly different than expected."
                return True, int(points_awarded), feedback

            # Check for similarity (using simple word matching)
            correct_words = set(correct_text_lower.split())
            user_words = set(user_answer_lower.split())
            if len(correct_words.intersection(user_words)) / len(correct_words) >= 0.8:  # 80% word match
                points_awarded = correct_answer.points_awarded * 0.7  # Partial credit
                feedback = "Partially correct. Consider reviewing the exact terminology."
                return True, int(points_awarded), feedback

        if correct_answers:
            feedback = f"Incorrect. Expected: {correct_answers[0].answer_text}"

        return False, points_awarded, feedback

    def _grade_essay(self, user_answer: str, correct_answers: List[QuizAnswer]) -> tuple[bool, int, str]:
        """
        Grade essay question with rule-based evaluation
        """
        if not user_answer.strip():
            return False, 0, "No answer provided."

        # For essay questions, we'll provide feedback but assign points based on presence of key concepts
        # This is a simplified approach - in a real system, you might have more sophisticated rubrics
        points_awarded = 0
        feedback = "Essay response received."

        if len(user_answer) < 50:
            feedback = "Response is too short. Please provide more detail and explanation."
            return True, 1, feedback  # Give minimal points for attempting

        # Check if any key terms from correct answers appear in user response
        key_terms_found = 0
        total_key_terms = 0

        for correct_answer in correct_answers:
            # Extract key terms from correct answer (simplified approach)
            key_terms = [term.strip() for term in correct_answer.answer_text.split() if len(term) > 3]
            total_key_terms += len(key_terms)

            for term in key_terms:
                if term.lower() in user_answer.lower():
                    key_terms_found += 1

        if total_key_terms > 0:
            match_ratio = key_terms_found / total_key_terms
            points_awarded = int(correct_answers[0].points_awarded * min(match_ratio, 1.0) if correct_answers else 0)

            if match_ratio >= 0.8:
                feedback = "Strong response with good coverage of key concepts."
            elif match_ratio >= 0.5:
                feedback = "Good response but could include more key concepts."
            else:
                feedback = "Response needs more key concepts and details."

        return True, points_awarded, feedback

    def _grade_text_comparison(self, user_answer: str, correct_answers: List[QuizAnswer]) -> tuple[bool, int, str]:
        """
        Generic text comparison grading
        """
        if not user_answer.strip() or not correct_answers:
            return False, 0, "No answer provided or no correct answers defined."

        user_answer_lower = user_answer.lower().strip()
        points_awarded = 0
        feedback = "Incorrect answer."

        for correct_answer in correct_answers:
            correct_text_lower = correct_answer.answer_text.lower().strip()

            if user_answer_lower == correct_text_lower:
                points_awarded = correct_answer.points_awarded
                feedback = "Correct! Well done."
                return True, points_awarded, feedback

            # Check for partial matches
            if correct_text_lower in user_answer_lower or user_answer_lower in correct_text_lower:
                points_awarded = correct_answer.points_awarded * 0.8
                feedback = "Partially correct."
                return True, int(points_awarded), feedback

        feedback = f"Incorrect. Expected: {correct_answers[0].answer_text}"
        return False, points_awarded, feedback

    def _create_score_breakdown(self, graded_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Create a breakdown of scores by question type
        """
        breakdown = {}
        for result in graded_results:
            q_type = result["question_type"]
            if q_type not in breakdown:
                breakdown[q_type] = {
                    "possible_points": 0,
                    "earned_points": 0,
                    "count": 0
                }

            breakdown[q_type]["possible_points"] += result["points_possible"]
            breakdown[q_type]["earned_points"] += result["points_awarded"]
            breakdown[q_type]["count"] += 1

        return [
            {
                "question_type": q_type,
                "possible_points": data["possible_points"],
                "earned_points": data["earned_points"],
                "count": data["count"],
                "percentage": round((data["earned_points"] / data["possible_points"] * 100) if data["possible_points"] > 0 else 0, 2)
            }
            for q_type, data in breakdown.items()
        ]

    def _generate_overall_feedback(self, graded_results: List[Dict[str, Any]], overall_score: float) -> str:
        """
        Generate overall feedback based on quiz performance
        """
        correct_count = sum(1 for r in graded_results if r["is_correct"])
        total_count = len(graded_results)

        if overall_score >= 90:
            return "Excellent work! You demonstrated strong understanding of the material."
        elif overall_score >= 80:
            return "Great job! You have a good grasp of the concepts with room for minor improvements."
        elif overall_score >= 70:
            return "Good effort! You understand the main concepts but should review some areas."
        elif overall_score >= 60:
            return "Fair performance. Focus on reviewing the areas where you had difficulties."
        else:
            return "More practice needed. Review the material and try again."

    def _generate_suggestions(self, graded_results: List[Dict[str, Any]]) -> List[str]:
        """
        Generate suggestions for improvement based on incorrect answers
        """
        suggestions = []

        for result in graded_results:
            if not result["is_correct"]:
                suggestions.append(f"Review the concept related to: {result['question_text'][:50]}...")

        # Add general suggestions based on performance
        incorrect_count = sum(1 for r in graded_results if not r["is_correct"])
        if incorrect_count > len(graded_results) * 0.5:
            suggestions.extend([
                "Consider reviewing the entire section or chapter",
                "Try additional practice questions on these topics",
                "Seek additional resources or examples for better understanding"
            ])

        return suggestions

    def _identify_misconceptions(self, graded_results: List[Dict[str, Any]]) -> List[str]:
        """
        Identify potential misconceptions based on incorrect answers
        """
        misconceptions = []
        for result in graded_results:
            if not result["is_correct"]:
                misconceptions.append(f"Possible misunderstanding of: {result['question_text'][:60]}...")

        return misconceptions

    def _generate_recommendations(self, graded_results: List[Dict[str, Any]]) -> List[str]:
        """
        Generate next learning recommendations based on performance
        """
        recommendations = []
        incorrect_questions = [r for r in graded_results if not r["is_correct"]]

        if len(incorrect_questions) > 0:
            recommendations.append("Review the material for incorrectly answered questions")
            recommendations.append("Practice similar questions to reinforce understanding")

        if len(incorrect_questions) > len(graded_results) * 0.3:  # More than 30% incorrect
            recommendations.append("Consider revisiting the foundational concepts before proceeding")

        return recommendations

    def _calculate_confidence_level(self, overall_score: float) -> str:
        """
        Calculate confidence level based on overall score
        """
        if overall_score >= 90:
            return "high"
        elif overall_score >= 70:
            return "medium"
        else:
            return "low"

    def get_quiz_results(self, db: Session, user_id: uuid.UUID, quiz_id: uuid.UUID) -> Optional[Dict[str, Any]]:
        """
        Get previously submitted quiz results
        """
        # This would typically come from a QuizSubmission model
        # For now, we'll return a mock implementation
        from models.quiz_submission import QuizSubmission

        submission = db.query(QuizSubmission).filter(
            QuizSubmission.user_id == user_id,
            QuizSubmission.quiz_id == quiz_id
        ).order_by(QuizSubmission.submitted_at.desc()).first()

        if submission:
            return {
                "quiz_id": quiz_id,
                "user_id": user_id,
                "score": submission.score,
                "max_score": submission.max_score,
                "submission_date": submission.submitted_at,
                "attempts_count": submission.attempt_number
            }

        return None

    def create_quiz(self, db: Session, content_id: uuid.UUID, title: str, instructions: str = None,
                    time_limit_minutes: int = None, max_attempts: int = 1) -> Quiz:
        """
        Create a new quiz
        """
        quiz = Quiz(
            content_id=content_id,
            title=title,
            instructions=instructions,
            time_limit_minutes=time_limit_minutes,
            max_attempts=max_attempts
        )
        db.add(quiz)
        db.commit()
        db.refresh(quiz)
        return quiz

    def create_quiz_question(self, db: Session, quiz_id: uuid.UUID, question_text: str,
                             question_type: str, points: int = 1, question_order: int = 0) -> QuizQuestion:
        """
        Create a new quiz question
        """
        from models.quiz import QuestionType
        question = QuizQuestion(
            quiz_id=quiz_id,
            question_text=question_text,
            question_type=QuestionType(question_type),
            points=points,
            question_order=question_order
        )
        db.add(question)
        db.commit()
        db.refresh(question)
        return question

    def create_quiz_answer(self, db: Session, question_id: uuid.UUID, answer_text: str,
                           is_correct: bool, points_awarded: int = 0) -> QuizAnswer:
        """
        Create a new quiz answer option
        """
        answer = QuizAnswer(
            question_id=question_id,
            answer_text=answer_text,
            is_correct=is_correct,
            points_awarded=points_awarded
        )
        db.add(answer)
        db.commit()
        db.refresh(answer)
        return answer