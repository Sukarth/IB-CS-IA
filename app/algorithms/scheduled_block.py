class ScheduledBlock:
    def __init__(self, assignment_id: int, chunk_name: str, hours: float):
        self.assignment_id = assignment_id
        self.chunk_name = chunk_name
        self.hours = hours