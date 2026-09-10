from .assignment import Assignment 
from .work_chunk import WorkChunk

class Essay(Assignment):
  def __init__(self, id: int, classroom_id: int, title: str, description: str, deadline: datetime, effort_hours: int, difficulty: int, is_published: bool, word_limit: int, type: AssignmentType | None = None):
    super().__init__(id, classroom_id, title, description, deadline, effort_hours, difficulty, is_published, type)
    self.word_limit = word_limit
  
  @classmethod
  def create(cls, classroom_id: int, title: str, description: str, deadline: datetime, effort_hours: float, difficulty: int, word_limit: int, is_published: bool, type: AssignmentType | None = None):
      super().create(classroom_id, title, description, deadline, effort_hours, difficulty, is_published)
      
      if not word_limit:
            raise ValueError("Word limit cannot be blank!")
            
      assignment_id = execute("INSERT INTO ASSIGNMENTS word_limit VALUES ?", (word_limit,))
      
      return cls.get_by_id(assignment_id)
      
  def get_type_specific_details(self):
    return {'work_chunk': self.WorkChunk, 'word_limit': self.word_limit}

