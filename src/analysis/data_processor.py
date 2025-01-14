# src/analysis/data_processor.py
import pandas as pd
import numpy as np
from typing import List, Dict, Optional
from datetime import datetime
import logging
from ..models.workout_session import WorkoutPoint

logger = logging.getLogger(_name_)

class DataProcessor:
    """
    Processes and analyzes workout data, including real-time analysis
    and post-workout statistics.
    """
    def _init_(self):
        self.workout_data: List[WorkoutPoint] = []
        self.current_session_id: Optional[int] = None
        self.session_start_time: Optional[datetime] = None

    def start_new_session(self, session_id: int):
        """Start a new workout session"""
        self.current_session_id = session_id
        self.session_start_time = datetime.now()
        self.workout_data = []
        logger.info(f"Started new workout session {session_id}")

    def add_workout_point(self, timestamp: float, heart_rate: int, 
                          speed: float, slope: float):
        """Add a new data point from the workout"""
        point = WorkoutPoint(
            timestamp=timestamp,
            heart_rate=heart_rate,
            speed=speed,
            slope=slope
        )
        self.workout_data.append(point)

    def load_dataset(self, filename: str) -> pd.DataFrame:
        """
        Load dataset from a CSV file.
        Args:
            filename: The name of the CSV file to load.
        Returns:
            A Pandas DataFrame containing the loaded dataset.
        """
        try:
            filepath = f"data/{filename}"  # Path to the data directory
            dataset = pd.read_csv(filepath)
            logger.info(f"Dataset {filename} loaded successfully")
            return dataset
        except Exception as e:
            logger.error(f"Error loading dataset: {str(e)}")
            raise

    def calculate_training_load(self, method: str = 'trimp') -> float:
        """
        Calculate training load using various methods
        Args:
            method: 'trimp' or 'hrr' (heart rate reserve)
        Returns: Training load value
        """
        if not self.workout_data:
            return 0.0

        try:
            df = pd.DataFrame([vars(p) for p in self.workout_data])
            duration_hours = (df['timestamp'].max() - df['timestamp'].min()) / 3600

            if method == 'trimp':
                # TRIMP calculation using Banister's formula
                avg_hr = df['heart_rate'].mean()
                return duration_hours * avg_hr * 0.64 * np.exp(1.92 * avg_hr / 200)
            else:
                # Simple heart rate reserve method
                avg_hr = df['heart_rate'].mean()
                return duration_hours * avg_hr

        except Exception as e:
            logger.error(f"Error calculating training load: {str(e)}")
            return 0.0

    def estimate_calories_burned(self, df: pd.DataFrame) -> float:
        """
        Estimate calories burned during workout
        Uses basic MET calculations based on speed and incline
        """
        try:
            mets = df.apply(lambda row: 
                           1.0 if row['speed'] == 0 else
                           2.0 if row['speed'] < 4 else
                           7.0 if row['speed'] < 8 else
                           10.0 if row['speed'] < 12 else
                           14.0, axis=1)
            mets = mets * (1 + df['slope'] * 0.1)
            calories_per_minute = mets * 3.5 * 70 / 200
            duration_minutes = (df['timestamp'].max() - df['timestamp'].min()) / 60
            return calories_per_minute.mean() * duration_minutes
        except Exception as e:
            logger.error(f"Error estimating calories burned: {str(e)}")
            return 0.0

    def get_workout_summary(self, df: pd.DataFrame) -> Dict:
        """Generate comprehensive workout summary statistics"""
        if df.empty:
            return {}

        try:
            hr_zones = {
                'recovery': (0.60, 0.70),
                'aerobic': (0.70, 0.80),
                'anaerobic': (0.80, 0.90),
                'maximum': (0.90, 1.00)
            }
            time_in_zones = {}
            total_time = (df['timestamp'].max() - df['timestamp'].min())

            for zone, (lower, upper) in hr_zones.items():
                mask = (df['heart_rate'] >= lower * 200) & (df['heart_rate'] < upper * 200)
                time_in_zones[zone] = (df[mask]['timestamp'].count() / 
                                     df['timestamp'].count() * 100)

            return {
                'duration_minutes': total_time / 60,
                'average_hr': df['heart_rate'].mean(),
                'max_hr': df['heart_rate'].max(),
                'min_hr': df['heart_rate'].min(),
                'average_speed': df['speed'].mean(),
                'max_speed': df['speed'].max(),
                'total_distance': (df['speed'] * (df['timestamp'].diff() / 3600)).sum(),
                'time_in_zones': time_in_zones,
                'training_load': self.calculate_training_load(),
                'calories_burned': self.estimate_calories_burned(df)
            }

        except Exception as e:
            logger.error(f"Error generating workout summary: {str(e)}")
            return {}

    def export_to_csv(self, filename: str):
        """Export workout data to CSV file"""
        try:
            df = pd.DataFrame([vars(p) for p in self.workout_data])
            df.to_csv(filename, index=False)
            logger.info(f"Workout data exported to {filename}")
        except Exception as e:
            logger.error(f"Error exporting workout data: {str(e)}")
            raise