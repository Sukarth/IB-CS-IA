from .assignment import Assignment 
from .work_chunk import WorkChunk

class ProblemSet(Assignment):
  def __init__(self, id: int, classroom_id: int, title: str, description: str, deadline: datetime, effort_hours: int, difficulty: int, is_published: bool, number_of_problems: int, type: AssignmentType | None = None):
    super().__init__(id, classroom_id, title, description, deadline, effort_hours, difficulty, is_published, type)
    self.number_of_problems = number_of_problems
  
  @classmethod
  def create(cls, classroom_id: int, title: str, description: str, deadline: datetime, effort_hours: float, difficulty: int, number_of_problems: int, is_published: bool, type: AssignmentType | None = None):
      super().create(classroom_id, title, description, deadline, effort_hours, difficulty, is_published)
      
      if not number_of_problems:
            raise ValueError("Number of problems cannot be blank!")
            
      assignment_id = execute("INSERT INTO ASSIGNMENTS number_of_problems VALUES ?", (number_of_problems,))
      
      return cls.get_by_id(assignment_id)
      
  def get_type_specific_details(self):
    return {'work_chunk': self.WorkChunk, 'number_of_problems': self.number_of_problems}
