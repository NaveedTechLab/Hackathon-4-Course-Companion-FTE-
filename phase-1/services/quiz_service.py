from sqlalchemy.orm import Session
from models.quiz import Quiz, QuizQuestion, QuizAnswer
from models.progress import Progress, ProgressStatus
from models.content import Content
from typing import List, Dict, Any, Optional
import uuid
from datetime import datetime

class QuizService:
    def __init__(self):
        pass

    def get_quiz_by_id(self, db: Session, quiz_id: uuid.UUID) -> Optional[Quiz]:
        """Get a quiz by ID"""
        return db.query(Quiz).filter(Quiz.id == quiz_id).first()

    def get_quiz_with_questions(self, db: Session, quiz_id: uuid.UUID) -> Optional[Dict[str, Any]]:
        """Get a quiz with all its questions"""
        quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
        if not quiz:
            return None

        questions = db.query(QuizQuestion).filter(
            QuizQuestion.quiz_id == quiz_id
        ).order_by(QuizQuestion.question_order).all()

        # Get possible answers for each question
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

    def submit_quiz_answers(self, db: Session, user_id: uuid.UUID, quiz_id: uuid.UUID, answers: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Submit quiz answers and perform rule-based grading"""
        # Get the quiz and its questions
        quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
        if not quiz:
            raise ValueError("Quiz not found")

        # Get all questions for this quiz
        questions = db.query(QuizQuestion).filter(
            QuizQuestion.quiz_id == quiz_id
        ).order_by(QuizQuestion.question_order).all()

        # Create a mapping of question_id to question for easy lookup
        question_map = {q.id: q for q in questions}

        # Initialize grading results
        total_points = 0
        earned_points = 0
        question_results = []

        # Process each submitted answer
        for answer_data in answers:
            question_id = uuid.UUID(answer_data["question_id"]) if isinstance(answer_data["question_id"], str) else answer_data["question_id"]
            user_answer = answer_data["answer_text"]

            # Get the question
            if question_id not in question_map:
                continue  # Skip if question doesn't belong to this quiz

            question = question_map[question_id]

            # Get the correct answers for this question
            correct_answers = db.query(QuizAnswer).filter(
                QuizAnswer.question_id == question_id,
                QuizAnswer.is_correct == True
            ).all()

            # Determine if the user's answer is correct
            is_correct = False
            feedback = ""
            points_awarded = 0

            # For multiple choice questions, check if the answer matches any correct answer
            if question.question_type.value == "mcq":
                for correct_answer in correct_answers:
                    if user_answer.lower().strip() == correct_answer.answer_text.lower().strip():
                        is_correct = True
                        points_awarded = correct_answer.points_awarded
                        feedback = correct_answer.answer_text
                        break

            # For true/false questions
            elif question.question_type.value == "tf":
                user_bool = user_answer.lower().strip() in ['true', 'yes', '1', 't', 'y']
                for correct_answer in correct_answers:
                    correct_bool = correct_answer.answer_text.lower().strip() in ['true', 'yes', '1', 't', 'y']
                    if user_bool == correct_bool:
                        is_correct = True
                        points_awarded = correct_answer.points_awarded
                        feedback = correct_answer.answer_text
                        break

            # For fill-in-blank questions
            elif question.question_type.value == "fill_blank":
                for correct_answer in correct_answers:
                    if user_answer.lower().strip() == correct_answer.answer_text.lower().strip():
                        is_correct = True
                        points_awarded = correct_answer.points_awarded
                        feedback = correct_answer.answer_text
                        break
                    # Allow for slight variations in spelling
                    elif self._is_similar_answer(user_answer, correct_answer.answer_text):
                        is_correct = True
                        # Award partial points for similar answers
                        points_awarded = correct_answer.points_awarded * 0.8
                        feedback = f"Partially correct. Expected: {correct_answer.answer_text}"
                        break

            # For essay questions, we can only provide feedback as these typically require human grading
            elif question.question_type.value == "essay":
                is_correct = True  # Essay questions are marked as correct by default since they need human review
                points_awarded = question.points  # Assign full points, but these should be reviewed later
                feedback = "Essay submitted. Review pending."

            # Update totals
            total_points += question.points
            earned_points += points_awarded

            # Record the result for this question
            question_results.append({
                "question_id": question_id,
                "question_text": question.question_text,
                "user_answer": user_answer,
                "is_correct": is_correct,
                "points_awarded": points_awarded,
                "feedback": feedback,
                "question_points": question.points
            })

        # Calculate overall score
        score_percentage = (earned_points / total_points * 100) if total_points > 0 else 0

        # Record the quiz attempt in the progress system
        self._record_quiz_attempt(db, user_id, quiz_id, score_percentage, earned_points, total_points)

        return {
            "quiz_id": quiz_id,
            "user_id": user_id,
            "total_points": total_points,
            "earned_points": earned_points,
            "score_percentage": score_percentage,
            "question_results": question_results,
            "passed": score_percentage >= 70  # Assuming 70% is the passing threshold
        }

    def _is_similar_answer(self, user_answer: str, correct_answer: str, threshold: float = 0.8) -> bool:
        """Check if user answer is similar to correct answer using simple string similarity"""
        # Simple similarity check - in a real implementation, this could use more sophisticated NLP
        user_lower = user_answer.lower().strip()
        correct_lower = correct_answer.lower().strip()

        # Exact match
        if user_lower == correct_lower:
            return True

        # Check if one string is contained in the other
        if user_lower in correct_lower or correct_lower in user_lower:
            # Calculate ratio of matching length
            shorter_len = min(len(user_lower), len(correct_lower))
            longer_len = max(len(user_lower), len(correct_lower))
            if shorter_len / longer_len >= threshold:
                return True

        return False

    def _record_quiz_attempt(self, db: Session, user_id: uuid.UUID, quiz_id: uuid.UUID, score: float, earned_points: int, total_points: int):
        """Record quiz attempt in the progress system"""
        # Get the content associated with this quiz
        quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
        if not quiz:
            return

        # Update or create progress record for the quiz content
        progress = db.query(Progress).filter(
            Progress.user_id == user_id,
            Progress.content_id == quiz.content_id
        ).first()

        if progress:
            # Update existing progress
            progress.completion_percentage = score
            if score >= 100:
                progress.status = ProgressStatus.COMPLETED
            elif score > 0:
                progress.status = ProgressStatus.IN_PROGRESS
            else:
                progress.status = ProgressStatus.NOT_STARTED
        else:
            # Create new progress record
            progress = Progress(
                user_id=user_id,
                content_id=quiz.content_id,
                status=ProgressStatus.COMPLETED if score >= 100 else ProgressStatus.IN_PROGRESS,
                completion_percentage=score
            )
            db.add(progress)

        db.commit()

    def get_quiz_results(self, db: Session, user_id: uuid.UUID, quiz_id: uuid.UUID) -> Optional[Dict[str, Any]]:
        """Get quiz results for a user"""
        # This would typically come from a quiz attempt history
        # For now, we'll return the latest attempt information
        quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
        if not quiz:
            return None

        # Get the progress record for this quiz's content
        content_progress = db.query(Progress).filter(
            Progress.user_id == user_id,
            Progress.content_id == quiz.content_id
        ).first()

        if not content_progress:
            return None

        return {
            "quiz_id": quiz_id,
            "user_id": user_id,
            "score": float(content_progress.completion_percentage) if content_progress.completion_percentage else 0.0,
            "status": content_progress.status.value,
            "completed_at": content_progress.updated_at
        }

    def create_quiz(self, db: Session, content_id: uuid.UUID, title: str, instructions: str = None,
                    time_limit_minutes: int = None, max_attempts: int = 1) -> Quiz:
        """Create a new quiz"""
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
                             question_type: str, question_order: int = 0, points: int = 1) -> QuizQuestion:
        """Create a new quiz question"""
        from models.quiz import QuestionType
        question = QuizQuestion(
            quiz_id=quiz_id,
            question_text=question_text,
            question_type=QuestionType(question_type),
            question_order=question_order,
            points=points
        )
        db.add(question)
        db.commit()
        db.refresh(question)
        return question

    def create_quiz_answer(self, db: Session, question_id: uuid.UUID, answer_text: str,
                           is_correct: bool, points_awarded: int = 0) -> QuizAnswer:
        """Create a new quiz answer option"""
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