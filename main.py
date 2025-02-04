from analysis import *

def main(data_path):
    """
    Run full analysis process
    """
    try:
        # Load data
        data = Data(data_path)
        # Analyze data
        analysis = Analysis(data)
        print(analysis)
        return analysis.relationships_results

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