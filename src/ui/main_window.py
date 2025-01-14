# ui/main_window.py
import tkinter as tk
from tkinter import ttk
from .widgets.heart_rate_plot import HeartRatePlot
from .widgets.control_panel import ControlPanel

class MainWindow(tk.Tk):
    def _init_(self):
        super()._init_()

        self.title("Smart Treadmill Control")
        self.geometry("800x600")

        # Create main containers
        self.top_frame = ttk.Frame(self)
        self.bottom_frame = ttk.Frame(self)
        
        self.top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # Initialize widgets
        self.heart_rate_plot = HeartRatePlot(self.top_frame)
        self.control_panel = ControlPanel(self.bottom_frame)

        self.heart_rate_plot.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.control_panel.pack(fill=tk.X, padx=10, pady=5)

        # Bind close event
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        """Handle cleanup when window is closed"""
        self.control_panel.cleanup()
        self.destroy()