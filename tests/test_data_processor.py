# tests/test_data_processor.py
import unittest
import numpy as np
from src.analysis.data_processor import DataProcessor

class TestDataProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = DataProcessor()
        self.sample_heart_rates = [120, 125, 130, 128, 135, 140, 138, 142, 145, 143]
        self.sample_timestamps = list(range(len(self.sample_heart_rates)))
        
    def test_moving_average(self):
        """Test moving average calculation"""
        window_size = 3
        expected = [
            np.mean(self.sample_heart_rates[i:i+window_size])
            for i in range(len(self.sample_heart_rates) - window_size + 1)
        ]
        
        result = self.processor.calculate_moving_average(
            self.sample_heart_rates,
            window_size
        )
        
        self.assertEqual(len(result), len(expected))
        for res, exp in zip(result, expected):
            self.assertAlmostEqual(res, exp)
            
    def test_heart_rate_variability(self):
        """Test heart rate variability calculation"""
        hrv = self.processor.calculate_hrv(self.sample_heart_rates)
        
        # HRV should be non-negative
        self.assertGreaterEqual(hrv, 0)
        
        # Test with constant heart rate (should have 0 variability)
        constant_hr = [70] * 10
        constant_hrv = self.processor.calculate_hrv(constant_hr)
        self.assertEqual(constant_hrv, 0)
        
    def test_calorie_estimation(self):
        """Test calorie burn estimation"""
        duration_minutes = 30
        user_weight_kg = 70
        average_hr = 140
        
        calories = self.processor.estimate_calories_burned(
            duration_minutes,
            user_weight_kg,
            average_hr
        )
        
        # Calories should be positive
        self.assertGreater(calories, 0)
        
        # Test with zero duration (should return 0 calories)
        zero_calories = self.processor.estimate_calories_burned(0, user_weight_kg, average_hr)
        self.assertEqual(zero_calories, 0)
        
    def test_detect_anomalies(self):
        """Test heart rate anomaly detection"""
        # Normal heart rates
        normal_data = self.sample_heart_rates.copy()
        anomalies = self.processor.detect_anomalies(normal_data)
        self.assertEqual(len(anomalies), 0)
        
        # Add some anomalies
        data_with_anomalies = normal_data + [50, 200]  # Add unlikely values
        anomalies = self.processor.detect_anomalies(data_with_anomalies)
        self.assertEqual(len(anomalies), 2)
        
    def test_workout_intensity_zones(self):
        """Test workout intensity zone classification"""
        max_hr = 190
        zones = self.processor.classify_intensity_zones(self.sample_heart_rates, max_hr)
        
        # Verify all heart rates are classified
        self.assertEqual(len(zones), len(self.sample_heart_rates))
        
        # Verify zone numbers are valid (1-5)
        for zone in zones:
            self.assertGreaterEqual(zone, 1)
            self.assertLessEqual(zone, 5)
            
    def test_invalid_inputs(self):
        """Test handling of invalid inputs"""
        # Test empty data
        with self.assertRaises(ValueError):
            self.processor.calculate_moving_average([], 3)
            
        # Test invalid window size
        with self.assertRaises(ValueError):
            self.processor.calculate_moving_average(self.sample_heart_rates, 0)
            
        # Test negative duration
        with self.assertRaises(ValueError):
            self.processor.estimate_calories_burned(-1, 70, 140)
            
        # Test negative weight
        with self.assertRaises(ValueError):
            self.processor.estimate_calories_burned(30, -70, 140)