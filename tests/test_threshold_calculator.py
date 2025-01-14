# tests/test_threshold_calculator.py
import unittest
from src.analysis.threshold_calculator import ThresholdCalculator

class TestThresholdCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = ThresholdCalculator()
        self.user_age = 30
        self.resting_heart_rate = 60
        
    def test_max_heart_rate_calculation(self):
        """Test the maximum heart rate calculation"""
        expected_max_hr = 220 - self.user_age  # Standard formula
        calculated_max_hr = self.calculator.calculate_max_heart_rate(self.user_age)
        self.assertEqual(calculated_max_hr, expected_max_hr)
        
    def test_heart_rate_zones(self):
        """Test heart rate training zones calculation"""
        zones = self.calculator.calculate_heart_rate_zones(self.user_age, self.resting_heart_rate)
        
        # Verify we have all five zones
        self.assertEqual(len(zones), 5)
        
        # Verify zones are in ascending order
        for i in range(1, len(zones)):
            self.assertGreater(zones[i][0], zones[i-1][0])
            self.assertGreater(zones[i][1], zones[i-1][1])
            
        # Verify zones are within possible heart rate range
        max_hr = 220 - self.user_age
        for zone_min, zone_max in zones:
            self.assertGreaterEqual(zone_min, self.resting_heart_rate)
            self.assertLessEqual(zone_max, max_hr)
            
    def test_anaerobic_threshold(self):
        """Test anaerobic threshold calculation"""
        threshold = self.calculator.estimate_anaerobic_threshold(self.user_age)
        max_hr = 220 - self.user_age
        
        # Threshold should be between 80-90% of max heart rate
        self.assertGreaterEqual(threshold, 0.80 * max_hr)
        self.assertLessEqual(threshold, 0.90 * max_hr)
        
    def test_invalid_inputs(self):
        """Test handling of invalid inputs"""
        # Test negative age
        with self.assertRaises(ValueError):
            self.calculator.calculate_max_heart_rate(-1)
            
        # Test unrealistic age
        with self.assertRaises(ValueError):
            self.calculator.calculate_max_heart_rate(150)
            
        # Test negative resting heart rate
        with self.assertRaises(ValueError):
            self.calculator.calculate_heart_rate_zones(30, -60)
            
        # Test unrealistic resting heart rate
        with self.assertRaises(ValueError):
            self.calculator.calculate_heart_rate_zones(30, 200)