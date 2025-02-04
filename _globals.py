"""
Global variables and constants used in the data analysis and visualization.
"""

DATA_PATH = 'The_role_of_consciously_timed_movements_in_shaping_and_improving_auditory_timing_(All_Subject_Data).csv'
"""str: Path to the main dataset CSV file."""

VARS_TO_PRINT = {
    'movdist': 'Movement Distance',
    'force': 'Force',
    'stoplatency': 'Stop Latency',
    'repduration': 'Response Duration',
    'error': 'Error',
    'abserror': 'Absolute Error',
    'trialtype': 'Trial Type',
}
"""dict: Mapping of variable names to their readable labels for plotting and display."""

MOVEMENT_COLS = ['movdist', 'force', 'stoplatency']
"""list: List of column names representing movement parameters."""
ERROR_COLS = ['error']
"""list: List of column names representing error measures."""

NUMERIC_COLS = ['movdist', 'force', 'stoplatency', 'repduration', 'error', 'abserror']
"""list: List of column names containing numeric data."""
OBJECT_COLS = []  # Currently empty, but included for potential future use.
"""list: List of column names containing categorical/object data."""
TRIALTYPE_COL = 'trialtype'
"""str: Name of the column representing the trial type."""
REQUIRED_COLS = NUMERIC_COLS + OBJECT_COLS + [TRIALTYPE_COL]
"""list: List of all required columns in the dataset.  Used for data validation."""