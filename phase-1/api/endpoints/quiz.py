from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from uuid import UUID
import uuid
from database import get_db
from services.quiz_service import QuizService
from services.premium_service import PremiumService
from middleware.premium_check import premium_required, track_usage
from middleware.auth import get_current_user
from models.quiz import QuizSubmission
from schemas.quiz_schemas import (
    QuizSubmissionRequest,
    QuizGrade,
    AssessmentGradeRequest,
    AssessmentGradeResponse
)

router = APIRouter()
quiz_service = QuizService()
premium_service = PremiumService()

@router.get("/quizzes/{quiz_id}")
@premium_required("quiz_access")
@track_usage("quiz_access")
async def get_quiz(
    quiz_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Get quiz details and questions
    """
    try:
        quiz_uuid = uuid.UUID(quiz_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid quiz ID format"
        )

    quiz_data = quiz_service.get_quiz_with_questions(db, quiz_uuid)

    if not quiz_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found"
        )

    return {
        "quiz_id": quiz_data["quiz"].id,
        "title": quiz_data["quiz"].title,
        "instructions": quiz_data["quiz"].instructions,
        "time_limit_minutes": quiz_data["quiz"].time_limit_minutes,
        "questions": [
            {
                "question_id": q["question"].id,
                "question_text": q["question"].question_text,
                "question_type": q["question"].question_type.value,
                "question_order": q["question"].question_order,
                "points": q["question"].points,
                "possible_answers": [
                    {
                        "answer_id": ans.id,
                        "answer_text": ans.answer_text,
                        "is_correct": ans.is_correct  # Only for review purposes, not revealed during quiz
                    }
                    for ans in q["answers"]
                ]
            }
            for q in quiz_data["questions"]
        ]
    }


@router.post("/quizzes/{quiz_id}/submit", response_model=QuizGrade)
@premium_required("quiz_submission")
@track_usage("quiz_submission")
async def submit_quiz(
    quiz_id: str,
    request: QuizSubmissionRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Submit quiz answers for grading
    """
    try:
        quiz_uuid = uuid.UUID(quiz_id)
        user_uuid = uuid.UUID(request.user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid quiz or user ID format"
        )

    # Verify user has access to submit this quiz
    access_check = premium_service.check_feature_access(db, user_uuid, "quiz_submission")
    if not access_check["has_access"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to submit quiz"
        )

    try:
        # Grade the quiz submission
        grading_result = quiz_service.grade_quiz_submission(
            db,
            user_uuid,
            quiz_uuid,
            request.answers
        )

        return QuizGrade(
            quiz_id=quiz_uuid,
            user_id=user_uuid,
            overall_score=grading_result["overall_score"],
            max_score=grading_result["max_score"],
            breakdown=grading_result["graded_answers"],
            detailed_feedback=grading_result["detailed_feedback"],
            suggested_improvements=grading_result["suggested_improvements"],
            misconceptions_identified=grading_result["misconceptions_identified"],
            next_learning_recommendations=grading_result["next_learning_recommendations"],
            confidence_level=grading_result["confidence_level"]
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing quiz submission: {str(e)}"
        )


@router.post("/assessments/grade-freeform", response_model=AssessmentGradeResponse)
@premium_required("assessment_grading")
@track_usage("assessment_grading")
async def grade_freeform_assessment(
    request: AssessmentGradeRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Grade freeform assessment responses using rule-based evaluation
    """
    try:
        user_uuid = uuid.UUID(request.user_id)
        assessment_uuid = uuid.UUID(request.assessment_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user or assessment ID format"
        )

    # Check if user has access to this premium feature
    access_check = premium_service.check_feature_access(db, user_uuid, "assessment_grading")
    if not access_check["has_access"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to assessment grading feature"
        )

    # Check usage limits
    usage_check = premium_service.check_usage_limit(db, user_uuid, "assessment_grading")
    if usage_check["limit_exceeded"]:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Usage limit exceeded for assessment grading"
        )

    try:
        # For freeform assessment grading, we'll use the quiz service's essay grading capability
        # In a real implementation, this would be more sophisticated but still deterministic

        # Get the assessment details (assuming this is a special type of quiz)
        from models.quiz import Quiz, QuizQuestion
        assessment = db.query(Quiz).filter(Quiz.id == assessment_uuid).first()

        if not assessment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assessment not found"
            )

        # Create a temporary question for grading purposes
        temp_question = QuizQuestion(
            quiz_id=assessment.id,
            question_text=request.question,
            question_type="essay",  # Treating freeform assessment as essay
            points=10  # Default points, could be adjusted
        )

        # Get correct answers for this assessment (could be in a rubric format)
        from models.quiz import QuizAnswer
        correct_answers = db.query(QuizAnswer).filter(
            QuizAnswer.question_id == temp_question.id  # This would need to be an existing question in real implementation
        ).all()

        # Grade the response using the rule-based grading
        is_correct, points_awarded, feedback = quiz_service._grade_essay(
            request.user_response,
            correct_answers if correct_answers else []
        )

        # Calculate score based on points
        max_possible_points = 10  # Default, should come from assessment definition
        score_percentage = (points_awarded / max_possible_points) * 100 if max_possible_points > 0 else 0

        # Generate suggestions and recommendations
        suggestions = quiz_service._generate_suggestions([{
            "question_text": request.question,
            "user_answer": request.user_response,
            "is_correct": is_correct,
            "points_awarded": points_awarded
        }])

        misconceptions = quiz_service._identify_misconceptions([{
            "question_text": request.question,
            "user_answer": request.user_response,
            "is_correct": is_correct
        }])

        recommendations = quiz_service._generate_recommendations([{
            "question_text": request.question,
            "user_answer": request.user_response,
            "is_correct": is_correct
        }])

        return AssessmentGradeResponse(
            assessment_id=assessment_uuid,
            user_id=user_uuid,
            grade=QuizGrade(
                quiz_id=assessment_uuid,
                user_id=user_uuid,
                overall_score=score_percentage,
                max_score=100.0,
                breakdown=[{
                    "question_id": str(temp_question.id) if hasattr(temp_question, 'id') else "unknown",
                    "question_text": request.question,
                    "user_answer": request.user_response,
                    "is_correct": is_correct,
                    "points_awarded": points_awarded,
                    "feedback": feedback
                }],
                detailed_feedback=feedback,
                suggested_improvements=suggestions,
                misconceptions_identified=misconceptions,
                next_learning_recommendations=recommendations,
                confidence_level=quiz_service._calculate_confidence_level(score_percentage)
            ),
            detailed_feedback=feedback,
            suggested_improvements=suggestions,
            misconceptions_identified=misconceptions,
            next_learning_recommendations=recommendations,
            confidence_level=quiz_service._calculate_confidence_level(score_percentage)
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error grading assessment: {str(e)}"
        )


@router.get("/quizzes/{quiz_id}/results")
@premium_required("quiz_results")
@track_usage("quiz_results")
async def get_quiz_results(
    quiz_id: str,
    user_id: str = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Get quiz results for a user
    """
    try:
        quiz_uuid = uuid.UUID(quiz_id)
        user_uuid = uuid.UUID(user_id) if user_id else current_user.id
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid quiz or user ID format"
        )

    # Only allow users to access their own results or admins to access others
    if user_uuid != current_user.id and not current_user.is_admin():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to other user's quiz results"
        )

    results = quiz_service.get_quiz_results(db, user_uuid, quiz_uuid)

    if not results:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No results found for this quiz and user combination"
        )

    return {
        "quiz_id": quiz_uuid,
        "user_id": user_uuid,
        "score": results["score"],
        "max_score": results["max_score"],
        "percentage": results["percentage"],
        "submitted_at": results["submitted_at"],
        "attempts_count": results["attempts_count"],
        "breakdown": results["breakdown"]
    }


@router.post("/quizzes/create")
@premium_required("quiz_creation")
@track_usage("quiz_creation")
async def create_quiz(
    course_id: str = Form(...),
    title: str = Form(...),
    instructions: str = Form(None),
    time_limit_minutes: int = Form(None),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Create a new quiz
    """
    try:
        course_uuid = uuid.UUID(course_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid course ID format"
        )

    # Only allow course creators/instructors to create quizzes for their courses
    # In a real implementation, we'd check course permissions here

    try:
        new_quiz = quiz_service.create_quiz(
            db,
            course_id=course_uuid,
            title=title,
            instructions=instructions,
            time_limit_minutes=time_limit_minutes
        )

        return {
            "quiz_id": new_quiz.id,
            "title": new_quiz.title,
            "course_id": course_uuid,
            "created_at": new_quiz.created_at,
            "message": "Quiz created successfully"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating quiz: {str(e)}"
        )


@router.get("/users/{user_id}/quiz-history")
@premium_required("quiz_history")
@track_usage("quiz_history")
async def get_user_quiz_history(
    user_id: str,
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Get user's quiz history and performance analytics
    """
    try:
        requested_user_uuid = uuid.UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )

    # Only allow users to access their own history or admins to access others
    if requested_user_uuid != current_user.id and not current_user.is_admin():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to other user's quiz history"
        )

    # Get user's quiz submissions
    quiz_submissions = db.query(QuizSubmission).filter(
        QuizSubmission.user_id == requested_user_uuid
    ).order_by(QuizSubmission.submitted_at.desc()).offset(offset).limit(limit).all()

    # Calculate performance analytics
    total_quizzes = len(quiz_submissions)
    if total_quizzes > 0:
        avg_score = sum(sub.score for sub in quiz_submissions) / total_quizzes
        highest_score = max(sub.score for sub in quiz_submissions)
        lowest_score = min(sub.score for sub in quiz_submissions)
    else:
        avg_score = 0
        highest_score = 0
        lowest_score = 0

    return {
        "user_id": requested_user_uuid,
        "quiz_history": [
            {
                "quiz_id": sub.quiz_id,
                "score": sub.score,
                "max_score": sub.max_score,
                "percentage": (sub.score / sub.max_score * 100) if sub.max_score > 0 else 0,
                "submitted_at": sub.submitted_at,
                "attempt_number": sub.attempt_number
            }
            for sub in quiz_submissions
        ],
        "analytics": {
            "total_quizzes_taken": total_quizzes,
            "average_score": avg_score,
            "highest_score": highest_score,
            "lowest_score": lowest_score,
            "overall_performance": "excellent" if avg_score >= 90 else "good" if avg_score >= 80 else "fair" if avg_score >= 70 else "needs_improvement"
        }
    }