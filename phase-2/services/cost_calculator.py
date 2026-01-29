import logging
from typing import Dict, Optional
from decimal import Decimal

logger = logging.getLogger(__name__)

class CostCalculator:
    """
    Service for calculating token usage costs based on model and token counts
    """

    def __init__(self):
        # Cost per 1,000 tokens (input and output)
        # These are approximate costs based on Claude 3 model pricing
        self.model_costs = {
            "claude-3-sonnet-20240229": {
                "input_cost_per_1k_tokens": Decimal("0.003"),  # $0.003 per 1K input tokens
                "output_cost_per_1k_tokens": Decimal("0.015")  # $0.015 per 1K output tokens
            },
            "claude-3-opus-20240229": {
                "input_cost_per_1k_tokens": Decimal("0.015"),  # $0.015 per 1K input tokens
                "output_cost_per_1k_tokens": Decimal("0.075")  # $0.075 per 1K output tokens
            },
            "claude-3-haiku-20240307": {
                "input_cost_per_1k_tokens": Decimal("0.00025"),  # $0.00025 per 1K input tokens
                "output_cost_per_1k_tokens": Decimal("0.00125")  # $0.00125 per 1K output tokens
            },
            # Default costs for unknown models
            "default": {
                "input_cost_per_1k_tokens": Decimal("0.003"),
                "output_cost_per_1k_tokens": Decimal("0.015")
            }
        }

    def calculate_cost(self, tokens_input: int, tokens_output: int, model_used: str) -> Decimal:
        """
        Calculate the estimated cost based on token counts and model used
        """
        try:
            model_cost = self.model_costs.get(model_used, self.model_costs["default"])

            # Calculate input cost
            input_cost = (Decimal(tokens_input) / Decimal(1000)) * model_cost["input_cost_per_1k_tokens"]

            # Calculate output cost
            output_cost = (Decimal(tokens_output) / Decimal(1000)) * model_cost["output_cost_per_1k_tokens"]

            # Total cost
            total_cost = input_cost + output_cost

            logger.debug(
                f"Cost calculation: model={model_used}, input_tokens={tokens_input}, "
                f"output_tokens={tokens_output}, total_cost=${total_cost}"
            )

            return total_cost

        except Exception as e:
            logger.error(f"Error calculating cost: {e}")
            # Return a default cost calculation in case of error
            default_model = self.model_costs["default"]
            input_cost = (Decimal(tokens_input) / Decimal(1000)) * default_model["input_cost_per_1k_tokens"]
            output_cost = (Decimal(tokens_output) / Decimal(1000)) * default_model["output_cost_per_1k_tokens"]
            return input_cost + output_cost

    def get_cost_breakdown(self, tokens_input: int, tokens_output: int, model_used: str) -> Dict[str, Decimal]:
        """
        Get detailed cost breakdown for input and output tokens
        """
        try:
            model_cost = self.model_costs.get(model_used, self.model_costs["default"])

            input_cost = (Decimal(tokens_input) / Decimal(1000)) * model_cost["input_cost_per_1k_tokens"]
            output_cost = (Decimal(tokens_output) / Decimal(1000)) * model_cost["output_cost_per_1k_tokens"]
            total_cost = input_cost + output_cost

            return {
                "input_cost": input_cost,
                "output_cost": output_cost,
                "total_cost": total_cost,
                "cost_per_1k_input": model_cost["input_cost_per_1k_tokens"],
                "cost_per_1k_output": model_cost["output_cost_per_1k_tokens"]
            }

        except Exception as e:
            logger.error(f"Error calculating cost breakdown: {e}")
            raise

    def estimate_average_cost_per_token(self, model_used: str = "default") -> Decimal:
        """
        Estimate average cost per token for a given model
        """
        try:
            model_cost = self.model_costs.get(model_used, self.model_costs["default"])

            # Average of input and output costs per token
            avg_input_cost_per_token = model_cost["input_cost_per_1k_tokens"] / Decimal(1000)
            avg_output_cost_per_token = model_cost["output_cost_per_1k_tokens"] / Decimal(1000)

            # Assuming equal distribution of input and output tokens
            avg_cost_per_token = (avg_input_cost_per_token + avg_output_cost_per_token) / Decimal(2)

            return avg_cost_per_token

        except Exception as e:
            logger.error(f"Error estimating average cost per token: {e}")
            raise

    def calculate_monthly_projection(
        self,
        daily_tokens_input: int,
        daily_tokens_output: int,
        model_used: str,
        days_in_month: int = 30
    ) -> Dict[str, Decimal]:
        """
        Calculate projected monthly costs based on daily usage
        """
        try:
            daily_cost = self.calculate_cost(daily_tokens_input, daily_tokens_output, model_used)
            monthly_cost = daily_cost * Decimal(days_in_month)

            return {
                "daily_cost": daily_cost,
                "monthly_cost": monthly_cost,
                "daily_tokens_input": Decimal(daily_tokens_input),
                "daily_tokens_output": Decimal(daily_tokens_output),
                "monthly_tokens_input": Decimal(daily_tokens_input * days_in_month),
                "monthly_tokens_output": Decimal(daily_tokens_output * days_in_month)
            }

        except Exception as e:
            logger.error(f"Error calculating monthly projection: {e}")
            raise

    def get_model_cost_info(self, model_used: str) -> Optional[Dict[str, Decimal]]:
        """
        Get cost information for a specific model
        """
        model_cost = self.model_costs.get(model_used)
        if model_cost:
            return {
                "input_cost_per_1k_tokens": model_cost["input_cost_per_1k_tokens"],
                "output_cost_per_1k_tokens": model_cost["output_cost_per_1k_tokens"],
                "model": model_used
            }
        return None

    def get_most_cost_effective_model(self, tokens_input: int, tokens_output: int) -> str:
        """
        Determine which model would be most cost-effective for the given token counts
        """
        min_cost = Decimal("999999")
        most_cost_effective_model = "default"

        for model, costs in self.model_costs.items():
            if model == "default":
                continue  # Skip default as it's a fallback

            cost = (Decimal(tokens_input) / Decimal(1000)) * costs["input_cost_per_1k_tokens"] + \
                   (Decimal(tokens_output) / Decimal(1000)) * costs["output_cost_per_1k_tokens"]

            if cost < min_cost:
                min_cost = cost
                most_cost_effective_model = model

        return most_cost_effective_model

    def apply_discount(self, cost: Decimal, discount_percentage: Decimal) -> Decimal:
        """
        Apply a discount percentage to a cost
        """
        if discount_percentage < 0 or discount_percentage > 100:
            raise ValueError("Discount percentage must be between 0 and 100")

        discount_multiplier = Decimal("1.0") - (discount_percentage / Decimal("100.0"))
        discounted_cost = cost * discount_multiplier

        return discounted_cost

    def calculate_cost_with_tier_pricing(
        self,
        tokens_input: int,
        tokens_output: int,
        model_used: str,
        user_tier: str = "standard"
    ) -> Decimal:
        """
        Calculate cost with potential tier-based discounts
        """
        try:
            # Calculate base cost
            base_cost = self.calculate_cost(tokens_input, tokens_output, model_used)

            # Apply tier discounts
            tier_discounts = {
                "free": Decimal("0"),      # No discount
                "premium": Decimal("5"),   # 5% discount
                "enterprise": Decimal("10")  # 10% discount
            }

            discount_percentage = tier_discounts.get(user_tier, Decimal("0"))

            if discount_percentage > 0:
                final_cost = self.apply_discount(base_cost, discount_percentage)
                logger.debug(f"Applied {discount_percentage}% discount for {user_tier} tier")
            else:
                final_cost = base_cost

            return final_cost

        except Exception as e:
            logger.error(f"Error calculating cost with tier pricing: {e}")
            # Fallback to base cost calculation
            return self.calculate_cost(tokens_input, tokens_output, model_used)