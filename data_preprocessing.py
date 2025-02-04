import pandas as pd
from _globals import *

class Data:
    """
    A class for loading, validating, and preprocessing data from a CSV file.

    Attributes:
        file_path (str): The path to the CSV file.
        df (pd.DataFrame): The original DataFrame loaded from the file.
        df_clean (pd.DataFrame): A copy of the DataFrame after preprocessing.

    Raises:
        FileNotFoundError: If the specified file path does not exist.
        pd.errors.EmptyDataError: If the CSV file is empty or contains no data after preprocessing.
    """
    def __init__(self, file_path):
        """
        Initializes a Data object by loading, validating, and preprocessing the data.

        Args:
            file_path (str): The path to the CSV file.
        """
        self.file_path = file_path
        self.df = pd.DataFrame()
        self.df_clean = self.df.copy()
        try:
             self.load_file(self.file_path)
             if self.df.empty:
                 raise pd.errors.EmptyDataError()
             self.is_valid_df()
             self.preprocess()
             if self.df_clean.empty:
                 raise pd.errors.EmptyDataError()
             self.preprocess_summary()

        except FileNotFoundError:
            print(f"File not found: {self.file_path}")

        except pd.errors.EmptyDataError:
            print("No data found in the CSV file.")


    def load_file(self, file_path):
        """
        Loads data from the specified CSV file into a pandas DataFrame.

        Args:
            file_path (str): The path to the CSV file.
        """
        self.df = pd.read_csv(file_path)

    def no_missing_columns(self):
        """
        Checks if the DataFrame contains all the required columns.

        Returns:
            bool: True if all required columns are present, False otherwise.
        """
        missing_columns = [col for col in REQUIRED_COLS if col not in self.df.columns]
        return len(missing_columns)==0

    def no_data_mismatches(self):
        """
        Checks if all numeric columns contain only numeric data.

        Returns:
            bool: True if all numeric columns contain valid numeric data, False otherwise.
        """
        for col in NUMERIC_COLS:
            try:
                self.df[col].astype(float)
            except:
                return False
        return True

    def no_missing_values(self):
        """
        Checks if any required column has more than 30% missing values.

        Returns:
            bool: True if no required column exceeds the missing value threshold, False otherwise.
        """
        for col in REQUIRED_COLS:
            if self.df[col].isnull().sum()>0.3*len(self.df[col]):
                return False
        return True

    def is_valid_df(self):
        """
        Checks if the DataFrame is valid by verifying the presence of required columns,
        correct data types in numeric columns, and acceptable missing value percentages.

        Returns:
            bool: True if the DataFrame is valid, False otherwise.
        """
        return self.no_missing_columns() and self.no_data_mismatches() and self.no_missing_values()

    def fill_na(self, col, how):
        """
        Fills missing values in a specified column using either the mode or median.

        Args:
            col (str): The name of the column to fill missing values in.
            how (str): The method to use for filling missing values ('mode' or 'median').

        Returns:
            pd.Series: The column with missing values filled.  Returns the modified column.
        """
        if how == 'mode':
            self.df[col] = self.df[col].fillna(self.df[col].mode()[0])
        if how == 'median':
            self.df[col] = self.df[col].fillna(self.df[col].median())
        return self.df[col]

    def remove_outliers(self, col):
        """
        Removes outliers from a specified column using the IQR method.

        Args:
            col (str): The name of the column to remove outliers from.

        Returns:
            pd.DataFrame: A new DataFrame with outliers removed from the specified column.
        """
        q1 = self.df[col].quantile(0.25)
        q3 = self.df[col].quantile(0.75)
        iqr = q3 - q1
        # Define bounds
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        return self.df[(self.df[col] >= lower_bound) & (self.df[col] <= upper_bound)]

    def preprocess(self):
        """
        Preprocesses the DataFrame by handling missing values and removing outliers
        for numeric and object type columns.  Stores the cleaned data in `self.df_clean`.
        """
        df_clean = self.df.copy()  # Start with a copy for the cleaned data
        for col in df_clean:
            if col in NUMERIC_COLS:
                self.fill_na(col,'median')
                self.df = self.remove_outliers(col)  # Note: modifies self.df
            if col in OBJECT_COLS:
                self.fill_na(col,'mode')
        self.df_clean = df_clean # Assign the cleaned data to df_clean

    def preprocess_summary(self):
        """
        Prints a summary of the preprocessing steps, including the number of rows
        before and after cleaning.
        """
        # Print preprocess summary
        print("Data Cleaning Summary:")
        print(f"Original rows: {len(self.df)}")
        print(f"Rows after cleaning: {len(self.df_clean)}")
        print(f"Removed rows: {len(self.df) - len(self.df_clean)}")