# ui/widgets/heart_rate_plot.py
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from collections import deque

class HeartRatePlot(tk.Frame):
    def _init_(self, parent, history_size: int = 60):
        super()._init_(parent)
        self.history_size = history_size
        self.heart_rate_history = deque(maxlen=history_size)
        self.time_history = deque(maxlen=history_size)
        
        # Create matplotlib figure
        self.figure = Figure(figsize=(8, 4), dpi=100)
        self.plot = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Initialize plot
        self.line, = self.plot.plot([], [], 'b-')
        self.plot.set_ylim(40, 200)
        self.plot.set_xlim(0, history_size)
        self.plot.set_title('Heart Rate Over Time')
        self.plot.set_xlabel('Time (s)')
        self.plot.set_ylabel('Heart Rate (BPM)')
        self.plot.grid(True)

    def update_plot(self, heart_rate: int):
        """Update the plot with new heart rate data"""
        self.heart_rate_history.append(heart_rate)
        self.time_history.append(len(self.time_history))
        
        self.line.set_data(list(self.time_history), list(self.heart_rate_history))
        self.canvas.draw()