# ui/widgets/control_panel.py
import tkinter as tk
from tkinter import ttk
from typing import Callable

class ControlPanel(ttk.Frame):
    def _init_(self, parent):
        super()._init_(parent)
        
        # Speed control
        self.speed_frame = ttk.LabelFrame(self, text="Speed Control")
        self.speed_frame.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)
        
        self.speed_scale = ttk.Scale(
            self.speed_frame,
            from_=0,
            to=20,
            orient=tk.HORIZONTAL,
            command=self._on_speed_change
        )
        self.speed_scale.pack(fill=tk.X, padx=5, pady=5)
        
        self.speed_label = ttk.Label(self.speed_frame, text="0.0 km/h")
        self.speed_label.pack()

        # Incline control
        self.incline_frame = ttk.LabelFrame(self, text="Incline Control")
        self.incline_frame.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)
        
        self.incline_scale = ttk.Scale(
            self.incline_frame,
            from_=0,
            to=15,
            orient=tk.HORIZONTAL,
            command=self._on_incline_change
        )
        self.incline_scale.pack(fill=tk.X, padx=5, pady=5)
        
        self.incline_label = ttk.Label(self.incline_frame, text="0.0°")
        self.incline_label.pack()

        # Emergency stop button
        self.stop_button = ttk.Button(
            self,
            text="EMERGENCY STOP",
            style="Emergency.TButton",
            command=self._on_emergency_stop
        )
        self.stop_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Create emergency button style
        style = ttk.Style()
        style.configure("Emergency.TButton", background="red", foreground="white")

        # Callback handlers
        self.speed_callback: Callable[[float], None] = lambda x: None
        self.incline_callback: Callable[[float], None] = lambda x: None
        self.stop_callback: Callable[[], None] = lambda: None

    def set_callbacks(
        self,
        speed_callback: Callable[[float], None],
        incline_callback: Callable[[float], None],
        stop_callback: Callable[[], None]
    ):
        """Set callbacks for control events"""
        self.speed_callback = speed_callback
        self.incline_callback = incline_callback
        self.stop_callback = stop_callback

    def _on_speed_change(self, value):
        """Handle speed change events"""
        speed = float(value)
        self.speed_label.config(text=f"{speed:.1f} km/h")
        self.speed_callback(speed)

    def _on_incline_change(self, value):
        """Handle incline change events"""
        incline = float(value)
        self.incline_label.config(text=f"{incline:.1f}°")
        self.incline_callback(incline)

    def _on_emergency_stop(self):
        """Handle emergency stop button press"""
        self.speed_scale.set(0)
        self.stop_callback()

    def cleanup(self):
        """Perform any necessary cleanup"""
        pass