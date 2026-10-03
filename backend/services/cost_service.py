from typing import List, Dict, Any
from backend.models.component import Component

def calculate_cost_summary(budget: float, components: List[Component]) -> Dict[str, Any]:
    """
    Calculate full cost metrics for a project:
    - total_spent = sum(quantity * unit_price)
    - remaining_budget = budget - total_spent
    - budget_used_percentage = (total_spent / budget * 100) if budget > 0 else 0.0
    - is_over_budget = total_spent > budget and budget > 0
    - over_budget_amount = (total_spent - budget) if is_over_budget else 0.0
    - is_warning = 80% <= budget_used_percentage <= 100% (when budget > 0)
    """
    total_spent = sum(c.total_price for c in components)
    safe_budget = budget if budget is not None else 0.0
    remaining = safe_budget - total_spent

    if safe_budget > 0:
        used_pct = round((total_spent / safe_budget) * 100.0, 1)
        is_over = total_spent > safe_budget
        over_amt = round(total_spent - safe_budget, 2) if is_over else 0.0
        is_warn = (used_pct >= 80.0) and not is_over
    else:
        used_pct = 0.0
        is_over = False
        over_amt = 0.0
        is_warn = False

    return {
        "budget": safe_budget,
        "total_spent": round(total_spent, 2),
        "remaining_budget": round(remaining, 2),
        "budget_used_percentage": used_pct,
        "is_over_budget": is_over,
        "over_budget_amount": over_amt,
        "is_warning": is_warn,
        "component_count": len(components)
    }
