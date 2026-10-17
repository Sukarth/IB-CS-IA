from datetime import datetime
from ..models.help_request import HelpRequest
from ..models.assignment import Assignment

def _urgency_curve(value, half_point, steepness):
    """0 at value=0, exactly 0.5 at value=half_point, approaching 1 as value grows."""
    return value ** steepness / (half_point ** steepness + value ** steepness)

def calculate_priority(request: HelpRequest, assignment: Assignment, now=None):
    """Calculate the priority of a help request based on urgency, age, deadline, and assignment difficulty."""    
    now = now or datetime.now()
    AGE_HALF_POINT = 172800.0 # 2 days in seconds
    AGE_STEEPNESS  = 1.8
    DEADLINE_HALF_POINT = 86400.0 # 1 day in seconds
    DEADLINE_STEEPNESS = 1.9
    W_URGENT, W_AGE, W_DEADLINE, W_DIFFICULTY = 0.20, 0.15, 0.50, 0.15

    urgent = request.is_urgent
    requested_at = request.created_at
    deadline = assignment.deadline
    difficulty = assignment.difficulty
    
    if difficulty < 1 or difficulty > 5:
        raise ValueError("Difficulty must be between 1 and 5")

    urgency = 1.0 if urgent else 0.0
    difficulty_priority = difficulty/5.0

    seconds_waited = max((now - requested_at).total_seconds(), 0.0)
    time_priority = _urgency_curve(seconds_waited, AGE_HALF_POINT, AGE_STEEPNESS)

    seconds_remaining = max((deadline - now).total_seconds(), 0.0)
    deadline_priority = 1.0 - _urgency_curve(seconds_remaining, DEADLINE_HALF_POINT, DEADLINE_STEEPNESS)

    return W_URGENT * urgency + W_AGE * time_priority + W_DEADLINE * deadline_priority + W_DIFFICULTY * difficulty_priority
