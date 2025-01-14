# models/user.py
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional

@dataclass
class User:
    """User model representing a treadmill user"""
    id: int
    username: str
    email: str
    age: int
    weight: float  # in kg
    height: float  # in cm
    gender: str
    max_heart_rate: Optional[int] = None
    resting_heart_rate: Optional[int] = None
    created_at: datetime = datetime.now()
    last_login: datetime = datetime.now()
    preferences: Dict = None

    def __post_init__(self):
        if self.preferences is None:
            self.preferences = {}
        if self.max_heart_rate is None:
            self.calculate_max_heart_rate()

    def calculate_max_heart_rate(self) -> int:
        """Calculate theoretical maximum heart rate based on age"""
        self.max_heart_rate = 220 - self.age
        return self.max_heart_rate

    def calculate_target_heart_rate_zones(self) -> Dict[str, tuple]:
        """Calculate heart rate training zones"""
        if not self.max_heart_rate:
            self.calculate_max_heart_rate()
            
        hrr = self.max_heart_rate - (self.resting_heart_rate or 60)
        
        return {
            'recovery': (
                int(hrr * 0.50 + (self.resting_heart_rate or 60)),
                int(hrr * 0.60 + (self.resting_heart_rate or 60))
            ),
            'aerobic': (
                int(hrr * 0.60 + (self.resting_heart_rate or 60)),
                int(hrr * 0.70 + (self.resting_heart_rate or 60))
            ),
            'anaerobic_threshold': (
                int(hrr * 0.70 + (self.resting_heart_rate or 60)),
                int(hrr * 0.80 + (self.resting_heart_rate or 60))
            ),
            'vo2_max': (
                int(hrr * 0.80 + (self.resting_heart_rate or 60)),
                int(hrr * 0.90 + (self.resting_heart_rate or 60))
            ),
            'maximum': (
                int(hrr * 0.90 + (self.resting_heart_rate or 60)),
                self.max_heart_rate
            )
        }

    def calculate_bmi(self) -> float:
        """Calculate Body Mass Index"""
        height_m = self.height / 100
        return round(self.weight / (height_m * height_m), 2)