from ..models.teacher import Teacher
from ..models.help_request import HelpRequest
from ..models.assignment import Assignment
from .request_priority import calculate_priority
from ..adt.priority_queue import PriorityQueue
from datetime import datetime

def build_help_queue(teacher: Teacher):
    """Build a help queue for a teacher based on the priority of help requests."""
    help_requests = HelpRequest.get_unresolved_for_teacher(teacher.id)

    # Calculate priority for each help request
    now = datetime.now()
    prioritized_help_requests = PriorityQueue()
    for request in help_requests:
        assignment = Assignment.get_by_id(request.assignment_id)
        if assignment:
            priority = calculate_priority(request, assignment, now)
            prioritized_help_requests.enqueue(request, priority)

    return prioritized_help_requests