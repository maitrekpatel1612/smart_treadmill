# ui/_init_.py
from .main_window import MainWindow
from .widgets.heart_rate_plot import HeartRatePlot
from .widgets.control_panel import ControlPanel

_all_ = ['MainWindow', 'HeartRatePlot', 'ControlPanel']