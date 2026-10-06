from app.database import execute, query_one

class StudentSettings:
    def __init__(self, student_id: int, procrastination_factor: float = 1.0, exclude_overdue: bool = True, hours_free_monday: float = 0.0, hours_free_tuesday: float = 0.0, hours_free_wednesday: float = 0.0, hours_free_thursday: float = 0.0, hours_free_friday: float = 0.0, hours_free_saturday: float = 0.0, hours_free_sunday: float = 0.0):
        self.student_id = student_id
        self.procrastination_factor = procrastination_factor
        self.exclude_overdue = exclude_overdue
        self.hours_free_monday = hours_free_monday
        self.hours_free_tuesday = hours_free_tuesday
        self.hours_free_wednesday = hours_free_wednesday
        self.hours_free_thursday = hours_free_thursday
        self.hours_free_friday = hours_free_friday
        self.hours_free_saturday = hours_free_saturday
        self.hours_free_sunday = hours_free_sunday

    @classmethod
    def create(cls, student_id: int, procrastination_factor: float = 1.0, exclude_overdue: bool = True, hours_free_monday: float = 0.0, hours_free_tuesday: float = 0.0, hours_free_wednesday: float = 0.0, hours_free_thursday: float = 0.0, hours_free_friday: float = 0.0, hours_free_saturday: float = 0.0, hours_free_sunday: float = 0.0):
        cls._validate(procrastination_factor, exclude_overdue, hours_free_monday, hours_free_tuesday, hours_free_wednesday, hours_free_thursday, hours_free_friday, hours_free_saturday, hours_free_sunday)
        execute("INSERT INTO STUDENT_SETTINGS (student_id, procrastination_factor, exclude_overdue, hours_free_monday, hours_free_tuesday, hours_free_wednesday, hours_free_thursday, hours_free_friday, hours_free_saturday, hours_free_sunday) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (student_id, procrastination_factor, exclude_overdue, hours_free_monday, hours_free_tuesday, hours_free_wednesday, hours_free_thursday, hours_free_friday, hours_free_saturday, hours_free_sunday))
        
        return cls.get_by_student_id(student_id)

    def update_settings(self, procrastination_factor: float = 1.0, exclude_overdue: bool = True, hours_free_monday: float = 0.0, hours_free_tuesday: float = 0.0, hours_free_wednesday: float = 0.0, hours_free_thursday: float = 0.0, hours_free_friday: float = 0.0, hours_free_saturday: float = 0.0, hours_free_sunday: float = 0.0):
        self._validate(procrastination_factor, exclude_overdue, hours_free_monday, hours_free_tuesday, hours_free_wednesday, hours_free_thursday, hours_free_friday, hours_free_saturday, hours_free_sunday)

        execute("UPDATE STUDENT_SETTINGS SET procrastination_factor = ?, exclude_overdue = ?, hours_free_monday = ?, hours_free_tuesday = ?, hours_free_wednesday = ?, hours_free_thursday = ?, hours_free_friday = ?, hours_free_saturday = ?, hours_free_sunday = ? WHERE student_id = ?", (procrastination_factor, exclude_overdue, hours_free_monday, hours_free_tuesday, hours_free_wednesday, hours_free_thursday, hours_free_friday, hours_free_saturday, hours_free_sunday, self.student_id))
        
        if procrastination_factor is not None:
            self.procrastination_factor = procrastination_factor
        if exclude_overdue is not None:
            self.exclude_overdue = exclude_overdue
        if hours_free_monday is not None:
            self.hours_free_monday = hours_free_monday
        if hours_free_tuesday is not None:
            self.hours_free_tuesday = hours_free_tuesday
        if hours_free_wednesday is not None:
            self.hours_free_wednesday = hours_free_wednesday
        if hours_free_thursday is not None:
            self.hours_free_thursday = hours_free_thursday
        if hours_free_friday is not None:
            self.hours_free_friday = hours_free_friday
        if hours_free_saturday is not None:
            self.hours_free_saturday = hours_free_saturday
        if hours_free_sunday is not None:
            self.hours_free_sunday = hours_free_sunday

        return self

    @classmethod
    def get_by_student_id(cls, student_id: int):
        row = query_one("SELECT * FROM STUDENT_SETTINGS WHERE student_id = ?", (student_id,))

        if not row:
            return None
        
        return cls(row['student_id'], row['procrastination_factor'], bool(row['exclude_overdue']), row['hours_free_monday'], row['hours_free_tuesday'], row['hours_free_wednesday'], row['hours_free_thursday'], row['hours_free_friday'], row['hours_free_saturday'], row['hours_free_sunday'])

    def get_hours_for_day(self, day: int):
        match day:
            case 0:
                return self.hours_free_monday
            case 1:
                return self.hours_free_tuesday
            case 2:
                return self.hours_free_wednesday
            case 3:
                return self.hours_free_thursday
            case 4:
                return self.hours_free_friday
            case 5:
                return self.hours_free_saturday
            case 6:
                return self.hours_free_sunday
            case _:
                raise ValueError("Day must be an integer between 0 (Monday) and 6 (Sunday).")
    
    @staticmethod
    def _validate(procrastination_factor: float, exclude_overdue: bool, hours_free_monday: float, hours_free_tuesday: float, hours_free_wednesday: float, hours_free_thursday: float, hours_free_friday: float, hours_free_saturday: float, hours_free_sunday: float):
        if procrastination_factor < 0:
            raise ValueError("Procrastination factor must be non-negative.")
        if not isinstance(exclude_overdue, bool):
            raise ValueError("Exclude overdue must be True or False.")
        if any(hour < 0 for hour in [hours_free_monday, hours_free_tuesday, hours_free_wednesday, hours_free_thursday, hours_free_friday, hours_free_saturday, hours_free_sunday]):
            raise ValueError("Hours free must be non-negative.")