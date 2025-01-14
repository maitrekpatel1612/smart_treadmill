## Project Structue

smart_treadmill/
│
├── requirements.txt
├── config/
│   └── settings.py
├── src/
│   ├── _init_.py
│   ├── hardware/
│   │   ├── _init_.py
│   │   ├── treadmill_controller.py
│   │   └── heart_rate_monitor.py
│   ├── analysis/
│   │   ├── _init_.py
│   │   ├── threshold_calculator.py
│   │   └── data_processor.py
│   ├── models/
│   │   ├── _init_.py
│   │   ├── user.py
│   │   └── workout_session.py
│   └── ui/
│       ├── _init_.py
│       ├── main_window.py
│       └── widgets/
│           ├── _init_.py
│           ├── heart_rate_plot.py
│           └── control_panel.py
├── tests/
│   ├── _init_.py
│   ├── test_threshold_calculator.py
│   └── test_data_processor.py
└── main.py
