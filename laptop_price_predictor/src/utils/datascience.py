"""
datascience.py

Author: Lander Combarro Exposito
Created: July 17, 2024
Last Modified: December 10, 2024

Description
-----------
Module for Data Analysis Utilities.

This module provides a set of utility functions for data analysis, including calculating 
the coefficient of variation, generating heatmaps of correlation matrices, and calculating 
cardinality statistics for DataFrame columns.
"""

import re

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def get_cardinality(df: pd.DataFrame, threshold_categorical=10, threshold_continuous=30):
    """
    Calculates and returns cardinality statistics for each column in a pandas DataFrame, 
    classifying the columns based on their cardinality.

    Parameters
    ----------
    df : pandas.DataFrame
        The input DataFrame for which cardinality statistics will be computed.
    
    threshold_categorical : int, optional (default=10)
        The threshold used to classify columns as 'Categoric' or 'Numeric - Discrete'. 
        Columns with a number of unique values less than this threshold are classified as 'Categoric'.
    
    threshold_continuous : int, optional (default=30)
        The threshold percentage used to classify columns as 'Numeric - Continuous'. 
        Columns where the percentage of unique values exceeds this threshold are classified as 'Numeric - Continuous'.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with the following columns:
        - 'Card': The number of unique values in each column.
        - '%_Card': The percentage of unique values relative to the total number of rows in each column.
        - 'NaN_Values': The number of missing (NaN) values in each column.
        - '%_NaN_Values': The percentage of missing values relative to the total number of rows in each column.
        - 'Type': The data type of each column.
        - 'Class': The classification of each column based on its cardinality.
    """
    print('pandas.DataFrame shape:', df.shape)
    
    df_out = pd.DataFrame([df.nunique(), df.nunique()/len(df) * 100, 
                           df.isna().sum(), df.isna().mean() * 100, df.dtypes])
    df_out = df_out.T.rename(columns={0: 'Card', 1: '%_Card', 
                                      2: 'NaN_Values', 3: '%_NaN_Values', 4: 'Type'})
    
    df_out.loc[df_out['Card'] < threshold_categorical, 'Class'] = 'Categoric'
    df_out.loc[df_out['Card'] == 2, 'Class'] = 'Binary'
    df_out.loc[df_out['Card'] >= threshold_categorical, 'Class'] = 'Numeric - Discrete'
    df_out.loc[df_out['%_Card'] > threshold_continuous, 'Class'] = 'Numeric - Continuous'
    
    return df_out


def coefficient_of_variation(df):
    """
    Returns a pandas DataFrame with the mean, standard deviation (std), 
    in the same units as the mean, and the coefficient of variation (CV) for each numerical column in the input DataFrame.

    Parameters
    ----------
    df : pandas.DataFrame
        A DataFrame containing numerical columns for which the mean, standard deviation, 
        and coefficient of variation are calculated.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with the following columns:
        - 'mean': The mean of each column.
        - 'std': The standard deviation of each column.
        - 'CV': The coefficient of variation, calculated as the ratio of standard deviation to mean.
        
    Notes
    -----
    The coefficient of variation (CV) is a normalized measure of the dispersion of a dataset, 
    which is useful for comparing the variability of different datasets with different units or scales.
    """
    df_var = df.describe().loc[['std', 'mean']].T
    df_var['CV'] = df_var['std'] / df_var['mean']
    return df_var


def split_by_uppercase(text) -> str:
    """
    Uses regular expressions to find uppercase letters, split a string at those points,
    and return a new string separated by spaces.
    
    Parameters
    ----------
    text : str
        Text to split.
        
    Returns
    -------
    str
        The modified string with spaces inserted before each uppercase letter.
    """
    strings = re.findall(r'[A-Z][^A-Z]*', text)
    return ' '.join(strings)


def correlation_heatmap(corr_matrix):
    """
    Generates and displays a heatmap for the given correlation matrix using seaborn.

    Parameters
    ----------
    corr_matrix : pandas.DataFrame
        A correlation matrix, typically generated using pandas' `DataFrame.corr()` method, 
        where the values represent the correlation coefficients between different variables.

    Returns
    -------
    None
        This function directly displays a heatmap using matplotlib.

    Notes
    -----
    - The `annot=True` argument in `sns.heatmap` annotates each cell with the numeric value of the correlation.
    - The `cmap="coolwarm"` argument defines the color palette used to represent the values, ranging from cool (blue) to warm (red) colors.
    - The heatmap is displayed with 45-degree rotated labels on both axes for better readability when needed.
    """
    plt.figure(figsize=(10, 8)) 
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", 
                cbar=True, square=True, linewidths=.5)

    plt.title('Correlation Matrix')
    plt.xticks(rotation=45)
    plt.yticks(rotation=45)
    plt.show()
