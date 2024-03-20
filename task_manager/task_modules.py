from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict


@dataclass
class Task:
    name: str
    status: str = "Not started"
    input_time: datetime = datetime.now()
    due_to: datetime = datetime.now() + timedelta(days=7)

    def create_task(self) -> Dict:
        task = {
            "name": self.name,
            "status": self.status,
            "input_time": self.input_time,
            "due_to": self.due_to,
        }
        return task