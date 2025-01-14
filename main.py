# main.py
import sys
import logging
import argparse
from datetime import datetime
from pathlib import Path
from PyQt6.QtWidgets import QApplication

from src.ui.main_window import MainWindow
from src.models.user import User
from config.settings import Settings
from src.hardware.treadmill_controller import TreadmillController
from src.hardware.heart_rate_monitor import HeartRateMonitor

def setup_logging(settings):
    """Configure logging for the application"""
    log_file = Path(settings['LOGS_DIR']) / f"smart_treadmill_{datetime.now():%Y%m%d_%H%M%S}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    return logging.getLogger('smart_treadmill')

def check_hardware():
    """Check if required hardware is connected and functioning"""
    try:
        treadmill = TreadmillController()
        hr_monitor = HeartRateMonitor()
        
        # Test treadmill connection
        if not treadmill.is_connected():
            raise ConnectionError("Treadmill not connected")
            
        # Test heart rate monitor connection
        if not hr_monitor.is_connected():
            raise ConnectionError("Heart rate monitor not connected")
            
        # Cleanup
        treadmill.close()
        hr_monitor.close()
        
        return True
        
    except Exception as e:
        logging.error(f"Hardware check failed: {e}")
        return False

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Smart Treadmill Application')
    parser.add_argument('--config', type=str, help='Path to config file')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--simulate', action='store_true', help='Run in simulation mode (no hardware required)')
    return parser.parse_args()

def create_data_directories(settings):
    """Create necessary data directories if they don't exist"""
    Path(settings['DATA_DIR']).mkdir(parents=True, exist_ok=True)
    Path(settings['LOGS_DIR']).mkdir(parents=True, exist_ok=True)

def main():
    # Parse command line arguments
    args = parse_arguments()
    
    # Load settings
    settings = Settings.load(args.config)
    
    # Set up logging
    logger = setup_logging(settings)
    logger.info("Starting Smart Treadmill application")
    
    # Create necessary directories
    create_data_directories(settings)
    
    # Check hardware connections (skip if in simulation mode)
    if not args.simulate:
        if not check_hardware():
            logger.error("Hardware check failed. Please check connections and try again.")
            logger.info("To run in simulation mode, use --simulate flag")
            sys.exit(1)
    
    try:
        # Initialize Qt application
        app = QApplication(sys.argv)
        
        # Create and show main window
        window = MainWindow(
            settings=settings,
            simulation_mode=args.simulate,
            debug_mode=args.debug
        )
        window.show()
        
        # Set up exception handling
        sys.excepthook = lambda type, value, traceback: handle_exception(type, value, traceback, logger)
        
        # Start Qt event loop
        sys.exit(app.exec())
        
    except Exception as e:
        logger.error(f"Application failed to start: {e}", exc_info=True)
        sys.exit(1)

def handle_exception(exc_type, exc_value, exc_traceback, logger):
    """Handle uncaught exceptions"""
    if issubclass(exc_type, KeyboardInterrupt):
        # Handle Ctrl+C gracefully
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    
    logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

def cleanup():
    """Cleanup function to be called on program exit"""
    logging.info("Shutting down Smart Treadmill application")
    # Additional cleanup code can be added here

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nShutting down gracefully...")
        cleanup()
    finally:
        cleanup()