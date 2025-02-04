import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
from data_preprocessing import *

class Analysis:
    """
    A class for analyzing relationships between movement parameters and errors in preprocessed data.

    Attributes:
        data (Data): The preprocessed data (an instance of the `Data` class).
        df (pd.DataFrame): The cleaned DataFrame from the `Data` object.
        relationships_results (dict): A dictionary containing the correlation and p-value for each analyzed pair of variables and trial type.
        significant_pairs (list): A list of variable pairs (and trial types) with statistically significant relationships (p-value < 0.05).

    Raises:
        TypeError: If the provided `data` is not an instance of the `Data` class.
        ValueError: If the cleaned DataFrame is empty.
    """
    def __init__(self, data):
        """
        Initializes the Analysis object.

        Args:
            data (Data): The preprocessed data.
        """
        if not isinstance(data, Data):
            print("Only Data class is supported")
            return

        self.data = data
        self.df = self.data.df_clean
        if self.df.empty:
            print("No data to analyze")
            return

        self.relationships_results = self.analyze_relationships()
        self.significant_pairs = [pair for pair, res in self.relationships_results.items() if res['p_value'] < 0.05]
        self.analyze_response_time_impact()

    def __str__(self):
        return str(self.relationships_results)

    def check_col(self, col):
        """
        Checks if a column exists in the DataFrame.

        Args:
            col (str): The name of the column to check.

        Returns:
            bool: True if the column exists, False otherwise.
        """
        return col in self.df.columns

    def create_plots(self, mov_var, err_var):
        """
        Creates and displays plots to visualize the relationship between two variables,
        separated by trial type.

        Args:
            mov_var (str): The name of the movement variable column.
            err_var (str): The name of the error variable column.

        Returns:
            bool: True if plots were created successfully, False otherwise (e.g., if a column is missing).
        """
        if not (self.check_col(mov_var) and self.check_col(err_var)):
            print(f"One of the specified variables '{mov_var}' or '{err_var}' is not present in the DataFrame.")
            return False

        fig, axes = plt.subplots(1, 2, figsize=(15, 3))
        sns.scatterplot(data=self.df, x=mov_var, y=err_var, hue=TRIALTYPE_COL, ax=axes[0])
        for trial in self.df[TRIALTYPE_COL].unique():
            trial_data = self.df[self.df[TRIALTYPE_COL] == trial]
            sns.regplot(data=trial_data, x=mov_var, y=err_var, scatter=False, ax=axes[0])
        axes[0].set_xlabel(VARS_TO_PRINT[mov_var])
        axes[0].set_ylabel(VARS_TO_PRINT[err_var])
        axes[0].set_title(f'{VARS_TO_PRINT[mov_var]} vs {VARS_TO_PRINT[err_var]} by Trial Type')
        axes[0].legend(title=None)

        sns.boxplot(data=self.df, x=TRIALTYPE_COL, y=err_var, hue=TRIALTYPE_COL, ax=axes[1])
        axes[1].set_xlabel(VARS_TO_PRINT[TRIALTYPE_COL])
        axes[1].set_ylabel(VARS_TO_PRINT[err_var])
        axes[1].set_title(f'{VARS_TO_PRINT[err_var]} by Trial Type')
        plt.show()

        trial_types = self.df[TRIALTYPE_COL].unique()
        fig, axes = plt.subplots(1, len(trial_types), figsize=(15, 3), constrained_layout=True)
        fig.suptitle(f'{VARS_TO_PRINT[mov_var]} by Trial Type', y=1.05)
        if len(trial_types) == 1:
            axes = [axes]  # Handle the case of a single trial type
        for i, trial in enumerate(trial_types):
            trial_data = self.df[self.df[TRIALTYPE_COL] == trial]
            sns.histplot(data=trial_data, x=mov_var, ax=axes[i])
            axes[i].set_title(f'{trial}')
            axes[i].set_ylabel(VARS_TO_PRINT[err_var] + ' Index')
        plt.show()
        return True

    def get_correlation(self, trial_type, mov_var, err_var):
        """
        Computes the Pearson correlation coefficient and p-value between two variables for a specific trial type.

        Args:
            trial_type (str): The trial type to analyze.
            mov_var (str): The name of the movement variable column.
            err_var (str): The name of the error variable column.

        Returns:
            tuple: A tuple containing the Pearson correlation coefficient and the p-value.
        """
        trial_data = self.df[self.df[TRIALTYPE_COL] == trial_type]
        return stats.pearsonr(trial_data[mov_var], trial_data[err_var])

    def analyze_relationships(self):
        """
        Analyzes the relationships between movement parameters and error variables across different trial types.

        Returns:
            dict: A dictionary where keys are strings representing the combination of movement variable, error variable, and trial type (e.g., "amplitude_constant_A"), and values are dictionaries containing the 'correlation' and 'p_value'.
        """
        results = {}

        for mov_var in MOVEMENT_COLS:
            for err_var in ERROR_COLS:
                if self.create_plots(mov_var, err_var): # Only calculate correlations if plots are created
                    for trial_type in self.df[TRIALTYPE_COL].unique():
                        correlation = self.get_correlation(trial_type, mov_var, err_var)
                        results[f'{mov_var}_{err_var}_{trial_type}'] = {
                            'correlation': correlation[0],
                            'p_value': correlation[1]
                        }
        return results

    def analyze_response_time_impact(self):
        """
        Analyzes and visualizes the impact of response duration on significant relationships. Creates scatter plots of significant variable pairs, colored by response duration.

        Returns:
            bool: True if the analysis and visualization were successful.
        """
        for pair in self.significant_pairs:
            mov_var, err_var, trial_type = pair.split('_')
            trial_data = self.df[self.df[TRIALTYPE_COL] == trial_type]

            plt.figure(figsize=(12, 8))
            scatter = plt.scatter(
                trial_data[mov_var],
                trial_data[err_var],
                c=trial_data['repduration'],  # Color by response duration
                cmap='viridis',
                s=50,
                alpha=0.7,
                edgecolor='k'
            )
            plt.colorbar(scatter, label='Response Duration')
            plt.xlabel(VARS_TO_PRINT[mov_var])
            plt.ylabel(VARS_TO_PRINT[err_var])
            plt.title(f'{VARS_TO_PRINT[mov_var]} vs {VARS_TO_PRINT[err_var]} (colored by Response Duration)\nTrial Type: {trial_type}')
            plt.grid(True, linestyle='--', alpha=0.6)
            plt.tight_layout()
            plt.show()
        return True