
# SMT Performance Project
# Data Analysis and Visualization

## Table of Contents
- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Data](#data)
- [Usage](#usage)
- [Explanation of Files](#explanation-of-files)

## Introduction
This project aims to analyze relationships between movement parameters and errors across trial types using a dataset. The script cleans the data, visualizes relationships, and analyzes how response duration affects significant relationships.

## Prerequisites
Before running the script, ensure you have the following prerequisites installed:

- **Python 3.10+**
- **Pandas 2.2.2**
- **Numpy 1.26.4**
- **Scipy 1.13.1**
- **Matplotlib 3.10.0**
- **Seaborn 0.13.2**

## Data
The dataset required for this analysis can be downloaded from the following link:
[Sensory-Motor Timing Performance](https://www.kaggle.com/datasets/thedevastator/sensory-motor-timing-performance)
After downloading, save the dataset in the same directory as the script or update the file path accordingly.

## Usage
To run the analysis using the script, follow the steps below:
1. Clone or download this repository.
2. Ensure the dataset is available in the directory, or update the DATA_PATH variable when running the script.
3. Run the script using the command line interface (CLI):
python main.py

## Detailed Instructions:
1. **Data Loading and Cleaning**:
    - The script starts by loading the dataset using pandas and then proceeds to clean the data by handling missing values and removing outliers using the IQR method.
2. **Visualization**:
    - Various plots are created to visualize the relationships between movement parameters and errors. These include scatter plots with regression lines, box plots, and histograms.
3. **Correlation Analysis**:
    - The script calculates Pearson correlation coefficients for different movement and error pairs across trial types and stores significant relationships with p-values less than 0.05.
4. **Impact of Response Duration**:
    - For significant relationships, the impact of response duration is further analyzed and visualized using 2D scatter plots with color representation.
