import logging
from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session
from datetime import datetime
from models.token_cost_log import TokenCostLog
from services.cost_calculator import CostCalculator

logger = logging.getLogger(__name__)

class TokenTracker:
    """
    Utility for tracking token usage and costs for premium features
    """

    def __init__(self):
        self.cost_calculator = CostCalculator()

    def log_token_usage(
        self,
        db: Session,
        user_id: UUID,
        feature_type: str,
        tokens_input: int,
        tokens_output: int,
        model_used: str,
        request_metadata: Optional[dict] = None
    ) -> TokenCostLog:
        """
        Log token usage for a specific request
        """
        try:
            # Calculate estimated cost
            estimated_cost = self.cost_calculator.calculate_cost(
                tokens_input, tokens_output, model_used
            )

            # Create token cost log entry
            token_log = TokenCostLog(
                user_id=user_id,
                feature_type=feature_type,
                request_id=self._generate_request_id(),
                tokens_input=tokens_input,
                tokens_output=tokens_output,
                total_tokens=tokens_input + tokens_output,
                estimated_cost_usd=estimated_cost,
                model_used=model_used,
                request_metadata=request_metadata
            )

            # Save to database
            db.add(token_log)
            db.commit()
            db.refresh(token_log)

            logger.info(
                f"Token usage logged: user={user_id}, feature={feature_type}, "
                f"input_tokens={tokens_input}, output_tokens={tokens_output}, "
                f"cost=${estimated_cost:.6f}"
            )

            return token_log

        except Exception as e:
            logger.error(f"Error logging token usage: {e}")
            db.rollback()
            raise

    def get_user_token_usage(
        self,
        db: Session,
        user_id: UUID,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> dict:
        """
        Get token usage summary for a user
        """
        try:
            query = db.query(TokenCostLog).filter(TokenCostLog.user_id == user_id)

            if start_date:
                query = query.filter(TokenCostLog.created_at >= start_date)
            if end_date:
                query = query.filter(TokenCostLog.created_at <= end_date)

            logs = query.all()

            total_tokens = sum(log.total_tokens for log in logs)
            total_cost = sum(float(log.estimated_cost_usd) for log in logs)
            usage_by_feature = {}

            for log in logs:
                feature = log.feature_type
                if feature not in usage_by_feature:
                    usage_by_feature[feature] = {
                        "total_tokens": 0,
                        "total_cost": 0.0,
                        "count": 0
                    }

                usage_by_feature[feature]["total_tokens"] += log.total_tokens
                usage_by_feature[feature]["total_cost"] += float(log.estimated_cost_usd)
                usage_by_feature[feature]["count"] += 1

            return {
                "user_id": user_id,
                "period_start": start_date,
                "period_end": end_date,
                "total_tokens": total_tokens,
                "total_cost": round(total_cost, 6),
                "request_count": len(logs),
                "usage_by_feature": usage_by_feature,
                "average_cost_per_request": round(total_cost / len(logs), 6) if logs else 0.0
            }

        except Exception as e:
            logger.error(f"Error getting user token usage: {e}")
            raise

    def get_feature_token_usage(
        self,
        db: Session,
        feature_type: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> dict:
        """
        Get token usage summary for a specific feature
        """
        try:
            query = db.query(TokenCostLog).filter(TokenCostLog.feature_type == feature_type)

            if start_date:
                query = query.filter(TokenCostLog.created_at >= start_date)
            if end_date:
                query = query.filter(TokenCostLog.created_at <= end_date)

            logs = query.all()

            total_tokens = sum(log.total_tokens for log in logs)
            total_cost = sum(float(log.estimated_cost_usd) for log in logs)
            unique_users = len(set(log.user_id for log in logs))

            return {
                "feature_type": feature_type,
                "period_start": start_date,
                "period_end": end_date,
                "total_tokens": total_tokens,
                "total_cost": round(total_cost, 6),
                "request_count": len(logs),
                "unique_users": unique_users,
                "average_cost_per_request": round(total_cost / len(logs), 6) if logs else 0.0,
                "average_tokens_per_request": round(total_tokens / len(logs), 2) if logs else 0.0
            }

        except Exception as e:
            logger.error(f"Error getting feature token usage: {e}")
            raise

    def is_within_usage_limit(
        self,
        db: Session,
        user_id: UUID,
        feature_type: str,
        daily_limit_tokens: int = 100000  # Default to 100K tokens per day
    ) -> bool:
        """
        Check if user is within daily token usage limit for a feature
        """
        try:
            from datetime import date

            today = date.today()
            start_of_day = datetime.combine(today, datetime.min.time())
            end_of_day = datetime.combine(today, datetime.max.time())

            usage_summary = self.get_user_token_usage(
                db, user_id, start_of_day, end_of_day
            )

            # Check if total tokens for this user today exceed the limit
            return usage_summary["total_tokens"] < daily_limit_tokens

        except Exception as e:
            logger.error(f"Error checking usage limit: {e}")
            # Fail safe - if we can't check, assume user is within limit
            return True

    def get_cost_projection(
        self,
        db: Session,
        user_id: UUID,
        feature_type: str,
        projected_tokens: int
    ) -> dict:
        """
        Project the cost for a potential request
        """
        try:
            # Get user's recent usage patterns to estimate costs
            usage_summary = self.get_user_token_usage(db, user_id)

            avg_cost_per_token = (
                usage_summary["total_cost"] / usage_summary["total_tokens"]
                if usage_summary["total_tokens"] > 0
                else self.cost_calculator.estimate_average_cost_per_token()
            )

            projected_cost = projected_tokens * avg_cost_per_token

            return {
                "user_id": user_id,
                "feature_type": feature_type,
                "projected_tokens": projected_tokens,
                "projected_cost": round(projected_cost, 6),
                "historical_avg_cost_per_token": round(avg_cost_per_token, 8),
                "message": f"Estimated cost for {projected_tokens} tokens: ${projected_cost:.6f}"
            }

        except Exception as e:
            logger.error(f"Error calculating cost projection: {e}")
            raise

    def _generate_request_id(self) -> str:
        """
        Generate a unique request ID for tracking
        """
        import uuid
        return str(uuid.uuid4())

    def get_token_cost_breakdown(self, db: Session, user_id: UUID, days: int = 30) -> dict:
        """
        Get detailed token cost breakdown for a user over a period
        """
        try:
            from datetime import datetime, timedelta

            start_date = datetime.utcnow() - timedelta(days=days)

            # Get all token logs for the user in the specified period
            logs = db.query(TokenCostLog).filter(
                TokenCostLog.user_id == user_id,
                TokenCostLog.created_at >= start_date
            ).order_by(TokenCostLog.created_at.desc()).all()

            # Group by date and feature
            daily_breakdown = {}
            feature_breakdown = {}

            total_tokens = 0
            total_cost = 0.0

            for log in logs:
                # Daily breakdown
                date_str = log.created_at.strftime("%Y-%m-%d")
                if date_str not in daily_breakdown:
                    daily_breakdown[date_str] = {
                        "total_tokens": 0,
                        "total_cost": 0.0,
                        "request_count": 0,
                        "logs": []
                    }

                daily_breakdown[date_str]["total_tokens"] += log.total_tokens
                daily_breakdown[date_str]["total_cost"] += float(log.estimated_cost_usd)
                daily_breakdown[date_str]["request_count"] += 1
                daily_breakdown[date_str]["logs"].append({
                    "feature": log.feature_type,
                    "tokens": log.total_tokens,
                    "cost": float(log.estimated_cost_usd),
                    "timestamp": log.created_at.isoformat()
                })

                # Feature breakdown
                feature = log.feature_type
                if feature not in feature_breakdown:
                    feature_breakdown[feature] = {
                        "total_tokens": 0,
                        "total_cost": 0.0,
                        "request_count": 0
                    }

                feature_breakdown[feature]["total_tokens"] += log.total_tokens
                feature_breakdown[feature]["total_cost"] += float(log.estimated_cost_usd)
                feature_breakdown[feature]["request_count"] += 1

                # Running totals
                total_tokens += log.total_tokens
                total_cost += float(log.estimated_cost_usd)

            return {
                "user_id": user_id,
                "period_days": days,
                "total_tokens": total_tokens,
                "total_cost": round(total_cost, 6),
                "request_count": len(logs),
                "daily_breakdown": daily_breakdown,
                "feature_breakdown": feature_breakdown,
                "average_daily_tokens": round(total_tokens / days, 2) if days > 0 else 0,
                "average_daily_cost": round(total_cost / days, 6) if days > 0 else 0.0
            }

        except Exception as e:
            logger.error(f"Error getting token cost breakdown: {e}")
            raise

    def apply_cost_optimization(
        self,
        input_tokens: int,
        output_tokens: int,
        model_used: str,
        optimization_level: str = "medium"  # low, medium, high
    ) -> dict:
        """
        Apply cost optimization strategies based on optimization level
        """
        optimization_strategies = {
            "low": {
                "max_output_tokens_ratio": 2.0,  # Output can be up to 2x input
                "min_compression_ratio": 0.9     # Minimal compression
            },
            "medium": {
                "max_output_tokens_ratio": 1.5,  # Output should be closer to input
                "min_compression_ratio": 0.7     # Moderate compression
            },
            "high": {
                "max_output_tokens_ratio": 1.2,  # Output close to input
                "min_compression_ratio": 0.5     # Aggressive compression
            }
        }

        strategy = optimization_strategies.get(optimization_level, optimization_strategies["medium"])

        # Calculate if current usage is within optimization bounds
        output_to_input_ratio = output_tokens / input_tokens if input_tokens > 0 else 0
        is_optimized = output_to_input_ratio <= strategy["max_output_tokens_ratio"]

        # Suggest optimizations if needed
        optimization_suggestions = []
        if not is_optimized:
            optimization_suggestions.append(
                f"Reduce output token count (currently {output_tokens}, aim for ~{int(input_tokens * strategy['max_output_tokens_ratio'])})"
            )

        # Calculate potential savings
        original_cost = self.cost_calculator.calculate_cost(input_tokens, output_tokens, model_used)
        optimized_output_tokens = min(output_tokens, int(input_tokens * strategy["max_output_tokens_ratio"]))
        optimized_cost = self.cost_calculator.calculate_cost(input_tokens, optimized_output_tokens, model_used)
        potential_savings = original_cost - optimized_cost

        return {
            "is_optimized": is_optimized,
            "current_ratio": round(output_to_input_ratio, 2),
            "recommended_max_ratio": strategy["max_output_tokens_ratio"],
            "optimization_suggestions": optimization_suggestions,
            "original_cost": round(original_cost, 6),
            "optimized_cost": round(optimized_cost, 6),
            "potential_savings": round(potential_savings, 6),
            "optimization_level": optimization_level
        }