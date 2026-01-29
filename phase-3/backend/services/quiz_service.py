from sqlalchemy.orm import Session
from ..models.quiz import Quiz, QuizQuestion, QuizAnswer, QuizSubmission
from ..models.progress import Progress, ProgressStatus
from typing import List, Dict, Any, Optional
import uuid
from datetime import datetime
from enum import Enum

class QuestionType(Enum):
    MCQ = "mcq"  # Multiple Choice Question
    TF = "tf"    # True/False
    FILL_BLANK = "fill_blank"
    ESSAY = "essay"

class QuizService:
    """
    Service for quiz creation, management, and grading using deterministic rule-based evaluation
    """

    def __init__(self):
        pass

    def get_quiz_with_questions(self, db: Session, quiz_id: uuid.UUID) -> Optional[Dict[str, Any]]:
        """
        Get quiz details with all questions and possible answers
        """
        quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
        if not quiz:
            return None

        questions = db.query(QuizQuestion).filter(
            QuizQuestion.quiz_id == quiz_id
        ).order_by(QuizQuestion.question_order).all()

        quiz_data = {
            "quiz": quiz,
            "questions": []
        }

        for question in questions:
            answers = db.query(QuizAnswer).filter(
                QuizAnswer.question_id == question.id
            ).all()

            question_data = {
                "question": question,
                "answers": answers
            }
            quiz_data["questions"].append(question_data)

        return quiz_data

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
        quiz_data = self.get_quiz_with_questions(db, quiz_id)
        if not quiz_data:
            raise ValueError("Quiz not found")

        quiz = quiz_data["quiz"]
        questions = {q["question"].id: q for q in quiz_data["questions"]}

        total_possible_points = 0
        earned_points = 0
        graded_answers = []

        for answer_data in user_answers:
            question_id = uuid.UUID(answer_data["question_id"])
            user_answer = answer_data["answer_text"]

            if question_id not in questions:
                continue  # Skip answers to questions that don't exist

            question = questions[question_id]["question"]
            possible_answers = questions[question_id]["answers"]

            total_possible_points += question.points

            # Grade the answer based on question type
            is_correct, points_awarded, feedback = self._grade_single_answer(
                question, user_answer, possible_answers
            )

            if is_correct:
                earned_points += points_awarded

            graded_answers.append({
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

        # Record quiz submission
        submission = QuizSubmission(
            user_id=user_id,
            quiz_id=quiz_id,
            score=overall_score,
            max_score=100,
            submitted_at=datetime.utcnow(),
            attempt_number=1  # In a real implementation, this would track multiple attempts
        )
        db.add(submission)
        db.commit()

        # Update progress based on quiz result
        self._update_progress_after_quiz(db, user_id, quiz.content_id, overall_score)

        return {
            "quiz_id": quiz_id,
            "user_id": user_id,
            "overall_score": round(overall_score, 2),
            "max_score": total_possible_points,
            "earned_points": earned_points,
            "graded_answers": graded_answers,
            "breakdown": self._create_score_breakdown(graded_answers),
            "detailed_feedback": self._generate_overall_feedback(graded_answers, overall_score),
            "suggested_improvements": self._generate_suggestions(graded_answers),
            "misconceptions_identified": self._identify_misconceptions(graded_answers),
            "next_learning_recommendations": self._generate_recommendations(graded_answers),
            "confidence_level": self._calculate_confidence_level(overall_score),
            "grading_method": "rule_based"
        }

    def _grade_single_answer(
        self,
        question: QuizQuestion,
        user_answer: str,
        possible_answers: List[QuizAnswer]
    ) -> tuple[bool, int, str]:
        """
        Grade a single answer based on question type
        """
        if question.question_type == QuestionType.MCQ:
            return self._grade_mcq(user_answer, possible_answers)
        elif question.question_type == QuestionType.TF:
            return self._grade_true_false(user_answer, possible_answers)
        elif question.question_type == QuestionType.FILL_BLANK:
            return self._grade_fill_blank(user_answer, possible_answers)
        elif question.question_type == QuestionType.ESSAY:
            return self._grade_essay(user_answer, possible_answers)
        else:
            # Default to simple text comparison
            return self._grade_text_comparison(user_answer, possible_answers)

    def _grade_mcq(self, user_answer: str, possible_answers: List[QuizAnswer]) -> tuple[bool, int, str]:
        """
        Grade multiple choice question
        """
        user_answer_lower = user_answer.lower().strip()
        points_awarded = 0
        feedback = "Incorrect answer."

        for answer in possible_answers:
            answer_text_lower = answer.answer_text.lower().strip()

            if user_answer_lower == answer_text_lower and answer.is_correct:
                points_awarded = answer.points_awarded
                feedback = "Correct! Well done."
                return True, points_awarded, feedback

        # If no exact match, check if user selected a correct option (for multiple correct answers)
        for answer in possible_answers:
            if answer.is_correct and answer.answer_text.lower().strip() in user_answer_lower:
                points_awarded = answer.points_awarded
                feedback = "Partially correct. Consider reviewing the material for a complete answer."
                return True, points_awarded, feedback

        # Find the closest match for feedback
        correct_answers = [a for a in possible_answers if a.is_correct]
        if correct_answers:
            feedback = f"Incorrect. The correct answer was: {correct_answers[0].answer_text}"

        return False, points_awarded, feedback

    def _grade_true_false(self, user_answer: str, possible_answers: List[QuizAnswer]) -> tuple[bool, int, str]:
        """
        Grade true/false question
        """
        user_answer_lower = user_answer.lower().strip()
        points_awarded = 0
        feedback = "Incorrect answer."

        for answer in possible_answers:
            answer_text_lower = answer.answer_text.lower().strip()

            # Check various forms of true/false
            if answer.is_correct:
                if (
                    (answer_text_lower in ["true", "yes", "correct"] and
                     user_answer_lower in ["true", "yes", "correct", "t", "y"]) or
                    (answer_text_lower in ["false", "no", "incorrect"] and
                     user_answer_lower in ["false", "no", "incorrect", "f", "n"])
                ):
                    points_awarded = answer.points_awarded
                    feedback = "Correct! Well done."
                    return True, points_awarded, feedback

        if possible_answers:
            correct_answer = next((a for a in possible_answers if a.is_correct), possible_answers[0])
            feedback = f"Incorrect. The correct answer was: {correct_answer.answer_text}"

        return False, points_awarded, feedback

    def _grade_fill_blank(self, user_answer: str, possible_answers: List[QuizAnswer]) -> tuple[bool, int, str]:
        """
        Grade fill-in-the-blank question
        """
        if not user_answer.strip():
            return False, 0, "No answer provided."

        user_answer_lower = user_answer.lower().strip()
        points_awarded = 0
        feedback = "Incorrect answer."

        for answer in possible_answers:
            if not answer.is_correct:
                continue

            correct_text_lower = answer.answer_text.lower().strip()

            # Exact match
            if user_answer_lower == correct_text_lower:
                points_awarded = answer.points_awarded
                feedback = "Correct! Well done."
                return True, points_awarded, feedback

            # Partial match (allowing for minor differences)
            if correct_text_lower in user_answer_lower or user_answer_lower in correct_text_lower:
                points_awarded = int(answer.points_awarded * 0.8)  # Partial credit
                feedback = "Close! The answer was slightly different than expected."
                return True, points_awarded, feedback

            # Check for similarity (using simple word matching)
            correct_words = set(correct_text_lower.split())
            user_words = set(user_answer_lower.split())
            if len(correct_words.intersection(user_words)) / len(correct_words) >= 0.8:  # 80% word match
                points_awarded = int(answer.points_awarded * 0.7)  # Partial credit
                feedback = "Partially correct. Consider reviewing the exact terminology."
                return True, points_awarded, feedback

        if possible_answers:
            correct_answer = next((a for a in possible_answers if a.is_correct), possible_answers[0])
            feedback = f"Incorrect. Expected: {correct_answer.answer_text}"

        return False, points_awarded, feedback

    def _grade_essay(self, user_answer: str, possible_answers: List[QuizAnswer]) -> tuple[bool, int, str]:
        """
        Grade essay question with rule-based evaluation
        """
        if not user_answer.strip():
            return False, 0, "No answer provided."

        # For essay questions, we'll provide feedback but assign points based on presence of key concepts
        points_awarded = 0
        feedback = "Essay response received and will be reviewed."

        if len(user_answer) < 50:
            feedback = "Response is too short. Please provide more detail and explanation."
            return True, 1, feedback  # Give minimal points for attempting

        # Check if any key terms from correct answers appear in user response
        key_terms_found = 0
        total_key_terms = 0

        for answer in possible_answers:
            if answer.is_correct:
                # Extract key terms from correct answer (simplified approach)
                key_terms = [term.strip() for term in answer.answer_text.split() if len(term) > 3]
                total_key_terms += len(key_terms)

                for term in key_terms:
                    if term.lower() in user_answer.lower():
                        key_terms_found += 1

        if total_key_terms > 0:
            match_ratio = key_terms_found / total_key_terms
            points_awarded = int(possible_answers[0].points_awarded * min(match_ratio, 1.0)) if possible_answers else 0

            if match_ratio >= 0.8:
                feedback = "Strong response with good coverage of key concepts."
            elif match_ratio >= 0.5:
                feedback = "Good response but could include more key concepts."
            else:
                feedback = "Response needs more key concepts and details."

        return True, points_awarded, feedback

    def _grade_text_comparison(self, user_answer: str, possible_answers: List[QuizAnswer]) -> tuple[bool, int, str]:
        """
        Generic text comparison grading
        """
        if not user_answer.strip() or not possible_answers:
            return False, 0, "No answer provided or no correct answers defined."

        user_answer_lower = user_answer.lower().strip()
        points_awarded = 0
        feedback = "Incorrect answer."

        for answer in possible_answers:
            if not answer.is_correct:
                continue

            correct_text_lower = answer.answer_text.lower().strip()

            if user_answer_lower == correct_text_lower:
                points_awarded = answer.points_awarded
                feedback = "Correct! Well done."
                return True, points_awarded, feedback

            # Check for partial matches
            if correct_text_lower in user_answer_lower or user_answer_lower in correct_text_lower:
                points_awarded = int(answer.points_awarded * 0.8)
                feedback = "Partially correct."
                return True, points_awarded, feedback

        correct_answer = next((a for a in possible_answers if a.is_correct), possible_answers[0])
        feedback = f"Incorrect. Expected: {correct_answer.answer_text}"
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

    def _update_progress_after_quiz(self, db: Session, user_id: uuid.UUID, content_id: uuid.UUID, score: float):
        """
        Update progress after quiz completion
        """
        from decimal import Decimal

        # Get existing progress or create new
        progress = db.query(Progress).filter(
            Progress.user_id == user_id,
            Progress.content_id == content_id
        ).first()

        if progress:
            # Update existing progress
            progress.status = ProgressStatus.COMPLETED if score >= 70 else ProgressStatus.IN_PROGRESS
            progress.completion_percentage = Decimal(str(score))
            progress.updated_at = datetime.utcnow()
        else:
            # Create new progress record
            progress = Progress(
                user_id=user_id,
                content_id=content_id,
                status=ProgressStatus.COMPLETED if score >= 70 else ProgressStatus.IN_PROGRESS,
                completion_percentage=Decimal(str(score)),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.add(progress)

        db.commit()

    def get_quiz_results(self, db: Session, user_id: uuid.UUID, quiz_id: uuid.UUID) -> Optional[Dict[str, Any]]:
        """
        Get previously submitted quiz results
        """
        submission = db.query(QuizSubmission).filter(
            QuizSubmission.user_id == user_id,
            QuizSubmission.quiz_id == quiz_id
        ).order_by(QuizSubmission.submitted_at.desc()).first()

        if not submission:
            return None

        # Get the quiz questions for context
        quiz_data = self.get_quiz_with_questions(db, quiz_id)

        return {
            "quiz_id": quiz_id,
            "user_id": user_id,
            "score": float(submission.score),
            "max_score": submission.max_score,
            "percentage": float(submission.score) if submission.max_score else 0,
            "submitted_at": submission.submitted_at,
            "attempt_number": submission.attempt_number,
            "quiz_title": quiz_data["quiz"].title if quiz_data else "Unknown Quiz"
        }

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
        from ..models.quiz import QuestionType as QuizQuestionType

        question = QuizQuestion(
            quiz_id=quiz_id,
            question_text=question_text,
            question_type=QuizQuestionType(question_type),
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