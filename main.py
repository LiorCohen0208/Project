import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np

DATA_PATH = 'The_role_of_consciously_timed_movements_in_shaping_and_improving_auditory_timing_(All_Subject_Data).csv'

VARS_TO_PRINT = {
    'movdist': 'Movement Distance',
    'force': 'Force',
    'stoplatency': 'Stop Latency',
    'repduration': 'Response Duration',
    'error': 'Error',
    'abserror': 'Absolute Error',
    'trialtype': 'Trial Type',
}

def no_missing_columns(df):
    """
    Check if the dataframe contains the required columns
    """
    required_columns = ['movdist', 'force', 'stoplatency', 'repduration', 'error', 'abserror', 'trialtype']
    missing_columns = [col for col in required_columns if col not in df.columns]
    return len(missing_columns)==0

def no_data_missmatches(df):
    """
    Check that all numeric columns are actually numeric
    """
    for col in ['movdist', 'force', 'stoplatency', 'repduration', 'error', 'abserror']:
        try:
            df[col].astype(float)
        except:
            return False
    return True

def no_missing_values(df):
    """
    Check if any column contains missing values more than 30%
    """
    for col in ['movdist', 'force', 'stoplatency', 'repduration', 'error', 'abserror']:
        if df[col].isnull().sum()>0.3*len(df[col]):
            return False
    return True

def is_valid_df(df):
    """
    Check if the dataframe is valid
    """
    return no_missing_columns(df) and no_data_missmatches(df) and no_missing_values(df)

def clean_data(df):
    """
    Clean the dataset by handling missing values and removing outliers
    """
    # Create a copy of the dataframe
    df_clean = df.copy()

    # 1. Handle missing values
    # Fill missing values with median for numeric columns
    numeric_columns = df_clean.select_dtypes(include=[np.number]).columns
    for col in numeric_columns:
        df_clean[col] = df_clean[col].fillna(df_clean[col].median())
    # Fill missing values in categorical columns with mode
    categorical_columns = df_clean.select_dtypes(include=['object']).columns
    for col in categorical_columns:
        if col != 'trialtype':  # Specifically check for non-numeric categories
            df_clean[col] = df_clean[col].fillna(df_clean[col].mode()[0])

    # 2. Remove outliers using IQR method
    for col in ['movdist', 'force', 'stoplatency', 'repduration', 'error', 'abserror']:
        if col in df_clean.columns:
            # Calculate Q1, Q3, and IQR
            Q1 = df_clean[col].quantile(0.25)
            Q3 = df_clean[col].quantile(0.75)
            IQR = Q3 - Q1
            # Define bounds
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            # Remove outliers
            df_clean = df_clean[(df_clean[col] >= lower_bound) & (df_clean[col] <= upper_bound)]

    # Print cleaning summary
    print("Data Cleaning Summary:")
    print(f"Original rows: {len(df)}")
    print(f"Rows after cleaning: {len(df_clean)}")
    print(f"Removed rows: {len(df) - len(df_clean)}")
    return df_clean

def create_plots(df, mov_var, err_var):
    """
    Create plots to visualize relationships between movement parameters and errors
    """
    if mov_var not in df.columns or err_var not in df.columns:
        print(f"One of the specified variables '{mov_var}' or '{err_var}' is not present in the DataFrame.")
        return
    if df.empty:
        print("The DataFrame is empty. Plotting cannot be performed.")
        return

    fig, axes = plt.subplots(1, 2, figsize=(15, 3))
    sns.scatterplot(data=df, x=mov_var, y=err_var, hue='trialtype', ax=axes[0])
    for trial in df['trialtype'].unique():
        trial_data = df[df['trialtype'] == trial]
        sns.regplot(data=trial_data, x=mov_var, y=err_var, scatter=False, ax=axes[0])
    axes[0].set_xlabel(VARS_TO_PRINT[mov_var])
    axes[0].set_ylabel(VARS_TO_PRINT[err_var])
    axes[0].set_title(f'{VARS_TO_PRINT[mov_var]} vs {VARS_TO_PRINT[err_var]} by Trial Type')
    axes[0].legend(title=None)

    sns.boxplot(data=df, x='trialtype', y=err_var, hue='trialtype', ax=axes[1])
    axes[1].set_xlabel(VARS_TO_PRINT['trialtype'])
    axes[1].set_ylabel(VARS_TO_PRINT[err_var])
    axes[1].set_title(f'{VARS_TO_PRINT[err_var]} by Trial Type')
    plt.show()

    trial_types = df['trialtype'].unique()
    fig, axes = plt.subplots(1, len(trial_types), figsize=(15, 3), constrained_layout=True)
    fig.suptitle(f'{VARS_TO_PRINT[mov_var]} by Trial Type', y=1.05)
    if len(trial_types) == 1:
        axes = [axes]
    for i, trial in enumerate(trial_types):
        trial_data = df[df['trialtype'] == trial]
        sns.histplot(data=trial_data, x=mov_var, ax=axes[i])
        axes[i].set_title(f'{trial}')
        axes[i].set_ylabel(VARS_TO_PRINT[err_var]+' Index')
    plt.show()
    return True

def get_correlation(df, mov_var, err_var):
    """
    Compute Pearson correlation
    """
    if df.empty:
        print("The DataFrame is empty. Correlation cannot be computed.")
        return (np.nan, np.nan)
    return stats.pearsonr(df[mov_var], df[err_var])

def analyze_relationships(df):
    """
    Analyze relationships between movement parameters and errors across trial types
    """
    # List of comparisons to make
    movement_vars = ['movdist', 'force', 'stoplatency']
    error_vars = ['error']

    # corr. placeholder
    results = {}

    if df.empty:
        print("The DataFrame is empty. No relationships to analyze.")
        return results

    # Create plots
    for mov_var in movement_vars:
        for err_var in error_vars:
            if create_plots(df, mov_var, err_var):
                # Calculate correlations
                for trial in df['trialtype'].unique():
                    trial_data = df[df['trialtype'] == trial]
                    correlation = get_correlation(trial_data, mov_var, err_var)
                    # Store results
                    results[f'{mov_var}_{err_var}_{trial}'] = {
                        'correlation': correlation[0],
                        'p_value': correlation[1]
                    }
    return results

def analyze_response_time_impact(df, significant_pairs):
    """
    Analyze how response duration affects significant relationships (improved visualization)
    """
    if df.empty:
        print("The DataFrame is empty. Analysis cannot be performed.")
        return

    for pair in significant_pairs:
        mov_var, err_var, trial_type = pair.split('_')
        trial_data = df[df['trialtype'] == trial_type]
        # Create a 2D scatter plot with color representing response duration
        plt.figure(figsize=(12, 8))
        scatter = plt.scatter(
            trial_data[mov_var],
            trial_data[err_var],
            c=trial_data['repduration'],
            cmap='viridis',
            s=50,  # Point size
            alpha=0.7,  # Transparency
            edgecolor='k'  # Black edges for clarity
        )
        plt.colorbar(scatter, label='Response Duration')
        plt.xlabel(VARS_TO_PRINT[mov_var])
        plt.ylabel(VARS_TO_PRINT[err_var])
        plt.title(f'{VARS_TO_PRINT[mov_var]} vs {VARS_TO_PRINT[err_var]} (colored by Response Duration)\nTrial Type: {trial_type}')
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.tight_layout()
        plt.show()
    return True

def main(data_path):
    """
    Run full analysis process
    """
    try:
        # Load data
        df = pd.read_csv(data_path)
        if not is_valid_df(df):
            print("No data found in the CSV file.")
            return
        # Clean data
        df_clean = clean_data(df)
        # Perform analysis on cleaned data
        results = analyze_relationships(df_clean)
        # Find significant relationships (p < 0.05)
        significant_pairs = [pair for pair, res in results.items() if res['p_value'] < 0.05]
        # Analyze impact of response time on significant relationships
        analyze_response_time_impact(df_clean, significant_pairs)
        return results

    except FileNotFoundError:
        print(f"File not found: {data_path}")
        return
    except pd.errors.EmptyDataError:
        print("No data found in the CSV file.")
        return
    except pd.errors.ParserError:
        print("Error parsing the CSV file. Please check the file format.")
        return
    except ValueError as ve:
        print(f"ValueError occurred: {ve}")
        return
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return

main(DATA_PATH)