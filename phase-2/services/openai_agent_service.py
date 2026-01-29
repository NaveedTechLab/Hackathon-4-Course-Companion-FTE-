import openai
from typing import List, Dict, Any, Optional
from config import settings
import logging
from utils.token_tracker import TokenTracker
from services.cost_calculator import CostCalculator

logger = logging.getLogger(__name__)

class OpenAIAgentService:
    """
    Service for interacting with OpenRouter API (supporting multiple LLM providers)
    All interactions are logged for cost tracking and usage analytics
    """

    def __init__(self):
        # Prioritize OpenRouter settings
        if settings.openrouter_api_key:
            self.client = openai.OpenAI(
                api_key=settings.openrouter_api_key,
                base_url=settings.openrouter_base_url
            )
            self.model = settings.llm_model
        elif settings.openai_api_key:
            self.client = openai.OpenAI(api_key=settings.openai_api_key)
            self.model = settings.openai_model
        else:
            raise ValueError("Either OPENROUTER_API_KEY or OPENAI_API_KEY environment variable must be set")

        self.token_tracker = TokenTracker()
        self.cost_calculator = CostCalculator()

    def create_completion(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
        max_tokens: int = 1000,
        temperature: float = 0.7,
        user_id: Optional[str] = None,
        feature_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a completion using OpenAI with cost tracking
        """
        try:
            # Prepare the API call parameters
            params = {
                "model": self.model,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "messages": messages
            }

            if system_prompt:
                # Add system prompt as the first message
                params["messages"] = [{"role": "system", "content": system_prompt}] + messages

            # Make the API call
            response = self.client.chat.completions.create(**params)

            # Extract token usage information
            input_tokens = response.usage.prompt_tokens
            output_tokens = response.usage.completion_tokens

            # Log the token usage for cost tracking
            if user_id and feature_type:
                from sqlalchemy.orm import Session
                # In a real implementation, you would have access to the database session
                # For now, we'll simulate the logging
                logger.info(
                    f"Token usage logged: user={user_id}, feature={feature_type}, "
                    f"input_tokens={input_tokens}, output_tokens={output_tokens}"
                )

            # Return the response with additional metadata
            return {
                "content": response.choices[0].message.content,
                "model": response.model,
                "finish_reason": response.choices[0].finish_reason,
                "usage": {
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                    "total_tokens": input_tokens + output_tokens
                },
                "cost_estimate": self.cost_calculator.calculate_cost(
                    input_tokens, output_tokens, self.model
                )
            }

        except Exception as e:
            logger.error(f"Error creating OpenAI completion: {e}")
            raise

    def create_streaming_completion(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
        max_tokens: int = 1000,
        temperature: float = 0.7,
        user_id: Optional[str] = None,
        feature_type: Optional[str] = None
    ):
        """
        Create a streaming completion using OpenAI
        """
        try:
            # Prepare the API call parameters
            params = {
                "model": self.model,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "messages": messages
            }

            if system_prompt:
                # Add system prompt as the first message
                params["messages"] = [{"role": "system", "content": system_prompt}] + messages

            # Create streaming response
            stream = self.client.chat.completions.create(**params, stream=True)

            full_response = ""
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    content_piece = chunk.choices[0].delta.content
                    full_response += content_piece
                    yield content_piece

            # After stream completion, get usage info
            # Note: For streaming, we'll need to estimate or track tokens differently
            # This is a simplified approach
            input_tokens = sum(len(msg.get("content", "")) for msg in params["messages"]) // 4
            output_tokens = len(full_response) // 4

            # Log the token usage for cost tracking
            if user_id and feature_type:
                logger.info(
                    f"Streaming token usage logged: user={user_id}, feature={feature_type}, "
                    f"input_tokens={input_tokens}, output_tokens={output_tokens}"
                )

        except Exception as e:
            logger.error(f"Error creating OpenAI streaming completion: {e}")
            raise

    def validate_api_access(self) -> bool:
        """
        Validate that the OpenAI API key is working properly
        """
        try:
            # Make a simple test call
            response = self.client.chat.completions.create(
                model=self.model,
                max_tokens=10,
                temperature=0.0,
                messages=[{"role": "user", "content": "Test"}]
            )

            return True
        except Exception as e:
            logger.error(f"API access validation failed: {e}")
            return False

    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the configured OpenAI model
        """
        return {
            "model_name": self.model,
            "provider": "OpenAI",
            "capabilities": [
                "text_generation",
                "analysis",
                "reasoning",
                "coding_assistance"
            ],
            "max_tokens": 128000,  # Most OpenAI models support up to 128K tokens
            "context_window": 128000
        }

    def count_tokens(self, text: str) -> int:
        """
        Count the number of tokens in a text string
        """
        try:
            # Use tiktoken to count tokens accurately
            import tiktoken
            encoding = tiktoken.encoding_for_model(self.model)
            return len(encoding.encode(text))
        except ImportError:
            # Fallback to rough estimation (4 chars per token)
            return max(1, len(text) // 4)
        except Exception as e:
            logger.error(f"Error counting tokens: {e}")
            # Fallback to rough estimation (4 chars per token)
            return max(1, len(text) // 4)

    def moderate_content(self, text: str) -> Dict[str, Any]:
        """
        Moderate content using OpenAI's moderation API
        """
        try:
            response = self.client.moderations.create(input=text)
            result = response.results[0]

            return {
                "flagged": result.flagged,
                "categories": dict(result.categories),
                "scores": dict(result.category_scores)
            }

        except Exception as e:
            logger.error(f"Error moderating content: {e}")
            # Return safe default
            return {
                "flagged": False,
                "categories": {},
                "scores": {}
            }

    def batch_process_requests(self, requests: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Process multiple requests in batch (simulated - OpenAI doesn't support true batching)
        """
        results = []
        for request in requests:
            try:
                result = self.create_completion(
                    messages=request.get("messages", []),
                    system_prompt=request.get("system_prompt"),
                    max_tokens=request.get("max_tokens", 1000),
                    temperature=request.get("temperature", 0.7),
                    user_id=request.get("user_id"),
                    feature_type=request.get("feature_type")
                )
                results.append(result)
            except Exception as e:
                logger.error(f"Error processing batch request: {e}")
                results.append({
                    "error": str(e),
                    "success": False
                })

        return results

    def get_cost_estimate(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
        max_tokens: int = 1000
    ) -> Dict[str, Any]:
        """
        Estimate the cost of a potential OpenAI API call
        """
        # Estimate token count
        total_text = ""
        if system_prompt:
            total_text += system_prompt + " "

        for msg in messages:
            total_text += msg.get("content", "") + " "

        estimated_tokens = self.count_tokens(total_text)
        # Assume roughly equal distribution between input and output
        estimated_input_tokens = estimated_tokens
        estimated_output_tokens = max_tokens // 2  # Rough estimate

        cost_estimate = self.cost_calculator.calculate_cost(
            estimated_input_tokens,
            estimated_output_tokens,
            self.model
        )

        return {
            "estimated_input_tokens": estimated_input_tokens,
            "estimated_output_tokens": estimated_output_tokens,
            "estimated_total_tokens": estimated_input_tokens + estimated_output_tokens,
            "estimated_cost_usd": float(cost_estimate),
            "model_used": self.model
        }

    def create_educational_completion(
        self,
        user_query: str,
        course_context: str,
        learning_objective: str,
        user_level: str = "intermediate",
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a completion specifically tailored for educational contexts
        """
        system_prompt = f"""
        You are an expert educational assistant helping students learn.
        Adapt your explanations to the student's level: {user_level}.
        Use clear examples and analogies to explain concepts.
        Focus on helping the student understand rather than just providing answers.
        """

        user_content = f"""
        Course Context: {course_context}
        Learning Objective: {learning_objective}
        Student Query: {user_query}

        Provide an educational response that helps the student understand the concept
        and guides them toward achieving the learning objective.
        """

        messages = [
            {"role": "user", "content": user_content}
        ]

        return self.create_completion(
            messages=messages,
            system_prompt=system_prompt,
            max_tokens=1500,
            temperature=0.5,  # Lower temperature for more consistent educational responses
            user_id=user_id,
            feature_type="educational_assistance"
        )

    def create_assessment_grading(
        self,
        question: str,
        correct_answer: str,
        student_response: str,
        rubric: Dict[str, Any],
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create an assessment grading using OpenAI
        """
        system_prompt = """
        You are an expert educational assessor. Grade the student's response based on the
        provided question, correct answer, rubric, and student response.
        Provide detailed feedback that helps the student understand their mistakes
        and how to improve. Be fair and consistent in your grading.
        """

        user_content = f"""
        QUESTION: {question}
        CORRECT ANSWER: {correct_answer}
        STUDENT RESPONSE: {student_response}
        RUBRIC: {str(rubric)}

        Grade the response and provide detailed feedback. Return your response as
        a JSON object with these fields:
        - score (numeric)
        - max_score (numeric)
        - feedback (string)
        - strengths (array of strings)
        - areas_for_improvement (array of strings)
        - misconceptions_identified (array of strings)
        - next_learning_recommendations (array of strings)
        """

        messages = [
            {"role": "user", "content": user_content}
        ]

        response = self.create_completion(
            messages=messages,
            system_prompt=system_prompt,
            max_tokens=2000,
            temperature=0.2,  # Very low temperature for consistency in grading
            user_id=user_id,
            feature_type="assessment_grading"
        )

        return response

    def create_adaptive_learning_path(
        self,
        user_profile: Dict[str, Any],
        course_content: List[Dict[str, Any]],
        learning_objectives: List[str],
        current_progress: Dict[str, Any],
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create an adaptive learning path using OpenAI
        """
        system_prompt = """
        You are an expert educational advisor. Analyze the student's profile, current progress,
        learning objectives, and available course content to recommend an optimal learning path.
        Consider their learning pace, strengths, weaknesses, and preferred learning style.
        Provide specific recommendations with clear reasoning.
        """

        user_content = f"""
        USER PROFILE: {str(user_profile)}
        COURSE CONTENT: {str(course_content[:10])}  # Limit to first 10 items to manage context
        LEARNING OBJECTIVES: {str(learning_objectives)}
        CURRENT PROGRESS: {str(current_progress)}

        Generate a personalized learning path with recommendations and reasoning.
        Return as JSON with these fields:
        - recommended_path (array of content IDs in order)
        - alternative_paths (array of alternative sequences)
        - focus_areas (array of areas needing attention)
        - reasoning (string explaining recommendations)
        """

        messages = [
            {"role": "user", "content": user_content}
        ]

        response = self.create_completion(
            messages=messages,
            system_prompt=system_prompt,
            max_tokens=3000,
            temperature=0.4,  # Low temperature for consistency
            user_id=user_id,
            feature_type="adaptive_learning_path"
        )

        return response