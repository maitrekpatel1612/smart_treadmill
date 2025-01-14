# Smart Treadmill Project

## Overview

The Smart Treadmill project is designed to provide real-time analysis and post-workout statistics for treadmill workouts. It includes hardware integration, data processing, and a user interface for monitoring and visualizing workout data.

## Project Structure

smart_treadmill/
│
├── requirements.txt
├── config/
│   └── settings.py
├── data/
│   └── treadmill_training_data.csv
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

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/smart_treadmill.git
    cd smart_treadmill
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Configure the settings in `config/settings.py` as needed.

2. Run the application:
    ```sh
    python main.py
    ```

3. Use the command-line arguments for additional options:
    ```sh
    python main.py --config path/to/config.json --debug --simulate
    ```

## Features

- Real-time workout data analysis
- Post-workout statistics and summaries
- Hardware integration with treadmill and heart rate monitor
- User interface for monitoring and visualizing workout data
- Data export to CSV

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

### Abstract

Using treadmill and cycle ergometers are the best methods of endurance training and choosing best training intensity is very crucial in endurance exercise training. According to more than one decade of our research experiences, it is possible to determine optimum personal training intensity based on estimation of person's anaerobic threshold. A hardware and software has been developed to monitor the heart rate and control the treadmill speed and slope. Software provided utilities to record the individual information (e.g. name, age, gender, weight and maximum and resting heart rate) and graphical curves of treadmill (speed, slope, work, power) and real-time heart rate. In this method, heart rate was used to draw the heart rate-time curve during an exhaustive graded maximal intensity exercise to find the best treadmill speed and slope in his/her anaerobic threshold. In this study, ten male athletes (19.3±1.7 years; 88.50±4.43 kg; 182.0±3.7 cm) recruited. Validity and reliability of this method have been evaluated by gas analysis every 5 seconds to determine anaerobic threshold and compare it with the Heart Rate Deflection Point (HRDP) calculated by the software on a standard Treadmill protocol during two sessions with one week rest. Bland-Altman and Intraclass Correlation Coefficients (ICC) was used to find any agreement between the two methods and Test-Retest was used to prove the reliability of the method. There was a very high agreement between two methods (±1.96; 95% CI = -16.5 to +37.5 b/min) and calculate anaerobic threshold had a positive and significant correlation (r=0.932; p<0.001). Feasibility of design a hardware and software and validity and reliability of estimated individual anaerobic threshold ascertained. It is a reasonably low price hardware and software recommendable to implement in future treadmill manufacturing.
```
