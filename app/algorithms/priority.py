from datetime import datetime
import math

def calculate_priority(urgent: bool, HelpRequest_created_at: datetime, Assignment_created_at: datetime, deadline: datetime, difficulty: int):
    AGE_HALF_POINT = 172800.0 # 2 days in seconds
    AGE_STEEPNESS  = 1.8
    DEADLINE_STEEPNESS = 3.5
    W_URGENT, W_AGE, W_DEADLINE, W_DIFFICULTY = 0.20, 0.15, 0.50, 0.15

    urgency = 1.0 if urgent else 0.0

    hours_waited = max((datetime.now() - HelpRequest_created_at).total_seconds(), 0.0)
    time_priority = _urgency_curve(hours_waited, AGE_HALF_POINT, AGE_STEEPNESS)

    hours_remaining = max((deadline - datetime.now()).total_seconds(), 0.0)
    deadline_priority = 1.0 - _urgency_curve(hours_remaining, 0.5, DEADLINE_STEEPNESS)

    if difficulty < 1 or difficulty > 5:
        raise ValueError("Difficulty must be between 1 and 5") 

    difficulty_priority = difficulty/5.0

    return W_URGENT * urgency + W_AGE * time_priority + W_DEADLINE * deadline_priority + W_DIFFICULTY * difficulty_priority

def _urgency_curve(value, half_point, steepness):
    """0 at value=0, exactly 0.5 at value=half_point, approaching 1 as value grows."""
    return value ** steepness / (half_point ** steepness + value ** steepness)