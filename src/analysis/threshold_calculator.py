# src/analysis/threshold_calculator.py
import numpy as np
from scipy.interpolate import interp1d
from scipy.signal import savgol_filter
from typing import Tuple, List, Optional
import logging

logger = logging.getLogger(__name__)

class ThresholdCalculator:
    """
    Implements the S.Dmax method for calculating the Heart Rate Deflection Point (HRDP)
    and estimating anaerobic threshold.
    """
    def __init__(self):
        self.heart_rates: List[int] = []
        self.timestamps: List[float] = []
        self.hrdp_time: Optional[float] = None
        self.hrdp_hr: Optional[int] = None

    def add_data_point(self, heart_rate: int, timestamp: float):
        """Add a new heart rate data point with its timestamp"""
        self.heart_rates.append(heart_rate)
        self.timestamps.append(timestamp)

    def clear_data(self):
        """Clear all stored data points"""
        self.heart_rates = []
        self.timestamps = []
        self.hrdp_time = None
        self.hrdp_hr = None

    def calculate_hrdp(self) -> Tuple[float, int]:
        """
        Calculate Heart Rate Deflection Point using S.Dmax method.
        Returns: (threshold_time, threshold_hr)
        """
        if len(self.heart_rates) < 10:
            raise ValueError("Insufficient data points for HRDP calculation")

        try:
            # Convert to numpy arrays
            hr_array = np.array(self.heart_rates)
            time_array = np.array(self.timestamps)

            # Smooth the heart rate data
            hr_smooth = savgol_filter(hr_array, 
                                    window_length=min(9, len(hr_array)-2), 
                                    polyorder=3)

            # Create third-order polynomial fit
            coeffs = np.polyfit(time_array, hr_smooth, 3)
            poly_fit = np.poly1d(coeffs)

            # Generate points along the curve
            x_new = np.linspace(time_array[0], time_array[-1], 1000)
            y_new = poly_fit(x_new)

            # Calculate first derivative
            dy_dx = np.gradient(y_new, x_new)

            # Calculate second derivative
            d2y_dx2 = np.gradient(dy_dx, x_new)

            # Find the point of maximum deflection
            deflection_idx = np.argmax(np.abs(d2y_dx2))

            self.hrdp_time = x_new[deflection_idx]
            self.hrdp_hr = int(y_new[deflection_idx])

            logger.info(f"HRDP calculated: Time={self.hrdp_time:.2f}s, HR={self.hrdp_hr}bpm")
            return self.hrdp_time, self.hrdp_hr

        except Exception as e:
            logger.error(f"Error calculating HRDP: {str(e)}")
            raise

    def estimate_anaerobic_threshold(self) -> int:
        """
        Estimate anaerobic threshold heart rate based on HRDP.
        Returns: Estimated anaerobic threshold heart rate
        """
        if self.hrdp_hr is None:
            self.calculate_hrdp()
        
        # Adjust HRDP to get anaerobic threshold
        # Based on research showing AT is typically slightly above HRDP
        at_hr = int(self.hrdp_hr * 1.02)  # 2% adjustment
        
        logger.info(f"Anaerobic threshold estimated at {at_hr}bpm")
        return at_hr

    def get_training_zones(self, max_hr: int) -> dict:
        """
        Calculate training zones based on anaerobic threshold
        Args:
            max_hr: Maximum heart rate
        Returns: Dictionary with training zone ranges
        """
        at_hr = self.estimate_anaerobic_threshold()
        
        return {
            'recovery': (int(0.60 * max_hr), int(0.70 * max_hr)),
            'aerobic': (int(0.70 * max_hr), int(at_hr * 0.90)),
            'threshold': (int(at_hr * 0.90), at_hr),
            'anaerobic': (at_hr, int(0.95 * max_hr)),
            'maximum': (int(0.95 * max_hr), max_hr)
        }