# models/workout_session.py
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Optional
import json
import numpy as np

@dataclass
class WorkoutPoint:
    """Single point of workout data"""
    timestamp: float
    heart_rate: int
    speed: float
    slope: float
    power: Optional[float] = None
    cadence: Optional[int] = None
    stride_length: Optional[float] = None

    def calculate_power(self) -> float:
        """Calculate power output based on speed and slope"""
        # Power calculation formula based on speed and incline
        # This is a simplified version - could be made more sophisticated
        weight = 75  # Default weight in kg if not provided
        gravity = 9.81
        
        # Convert slope to angle in radians
        angle = np.arctan(self.slope / 100)
        
        # Calculate power components
        vertical_power = weight * gravity * np.sin(angle) * self.speed
        horizontal_power = 0.5 * weight * self.speed * self.speed * np.cos(angle)
        
        self.power = vertical_power + horizontal_power
        return self.power

@dataclass
class WorkoutSession:
    """Complete workout session data"""
    id: int
    user_id: int
    start_time: datetime = field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    name: str = "Workout Session"
    description: Optional[str] = None
    data_points: List[WorkoutPoint] = field(default_factory=list)
    anaerobic_threshold: Optional[int] = None
    summary: Dict = field(default_factory=dict)
    
    def add_data_point(self, heart_rate: int, speed: float, slope: float, 
                      cadence: Optional[int] = None) -> WorkoutPoint:
        """Add a new data point to the session"""
        point = WorkoutPoint(
            timestamp=datetime.now().timestamp(),
            heart_rate=heart_rate,
            speed=speed,
            slope=slope,
            cadence=cadence
        )
        point.calculate_power()
        self.data_points.append(point)
        return point

    def end_session(self):
        """End the workout session and calculate summary"""
        self.end_time = datetime.now()
        self._calculate_summary()

    def _calculate_summary(self):
        """Calculate workout summary statistics"""
        if not self.data_points:
            return

        hrs = [p.heart_rate for p in self.data_points]
        speeds = [p.speed for p in self.data_points]
        powers = [p.power for p in self.data_points if p.power is not None]

        duration = (self.end_time - self.start_time).total_seconds()
        
        self.summary = {
            'duration_minutes': duration / 60,
            'average_heart_rate': np.mean(hrs),
            'max_heart_rate': max(hrs),
            'average_speed': np.mean(speeds),
            'max_speed': max(speeds),
            'distance': np.sum(speeds) * (duration / 3600),  # km
            'average_power': np.mean(powers) if powers else 0,
            'max_power': max(powers) if powers else 0,
            'total_ascent': self._calculate_total_ascent(),
            'anaerobic_threshold': self.anaerobic_threshold
        }

    def _calculate_total_ascent(self) -> float:
        """Calculate total vertical ascent in meters"""
        total_ascent = 0
        if len(self.data_points) < 2:
            return total_ascent
            
        for i in range(1, len(self.data_points)):
            # Calculate height difference based on slope and distance
            time_diff = self.data_points[i].timestamp - self.data_points[i-1].timestamp
            distance = self.data_points[i-1].speed * (time_diff / 3600)  # km
            slope = self.data_points[i-1].slope / 100  # convert to decimal
            ascent = distance * 1000 * slope  # meters
            if ascent > 0:
                total_ascent += ascent
                
        return round(total_ascent, 2)

    def to_dict(self) -> Dict:
        """Convert session to dictionary format"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'name': self.name,
            'description': self.description,
            'anaerobic_threshold': self.anaerobic_threshold,
            'summary': self.summary,
            'data_points': [
                {
                    'timestamp': p.timestamp,
                    'heart_rate': p.heart_rate,
                    'speed': p.speed,
                    'slope': p.slope,
                    'power': p.power,
                    'cadence': p.cadence,
                    'stride_length': p.stride_length
                }
                for p in self.data_points
            ]
        }

    def to_json(self) -> str:
        """Convert session to JSON format"""
        return json.dumps(self.to_dict())

    def export_csv(self, filename: str):
        """Export session data to CSV file"""
        import pandas as pd
        df = pd.DataFrame([vars(p) for p in self.data_points])
        df.to_csv(filename, index=False)