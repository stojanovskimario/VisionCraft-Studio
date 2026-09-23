from dataclasses import dataclass


@dataclass
class ThemeStep:
    id: str
    question: str
    step_type: str