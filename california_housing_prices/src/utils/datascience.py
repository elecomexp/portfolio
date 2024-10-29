"""
datascience.py

Author: Lander Combarro Exposito
Created: 2024/10/23
Last Modified: 2024/10/23

Description
-----------
This module contains functions for data analysis and machine learning model processing.

Functions
---------
>>> get_cardinality()
>>> regression_report()
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from sklearn import metrics

def get_cardinality(df:pd.DataFrame, threshold_categorical=10, threshold_continuous=30):
    '''
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
    '''
    print('pandas.DataFrame shape: ', df.shape)
    
    df_out = pd.DataFrame([df.nunique(), df.nunique()/len(df) * 100, 
                           df.isna().sum(), df.isna().mean() * 100, df.dtypes])
    df_out = df_out.T.rename(columns={0: 'Card', 1: '%_Card', 
                                      2: 'NaN_Values', 3: '%_NaN_Values', 4: 'Type'})
    
    df_out.loc[df_out['Card'] < threshold_categorical, 'Class'] = 'Categoric'
    df_out.loc[df_out['Card'] == 2, 'Class'] = 'Binary'
    df_out.loc[df_out['Card'] >= threshold_categorical, 'Class'] = 'Numeric - Discrete'
    df_out.loc[df_out['%_Card'] > threshold_continuous, 'Class'] = 'Numeric - Continuous'
    
    return df_out


def regression_report(model, X_true, y_true):
    """
    Generates and prints a comprehensive regression performance report for a given model.

    Parameters
    ----------
    model : object
        A trained regression model (fitted with .fit()) that has a `predict` method.
    X_true : array-like or pandas DataFrame, shape (n_samples, n_features)
        The input data used for predictions, where each row is a sample and each column is a feature.
    y_true : array-like or pandas Series, shape (n_samples,)
        The true target values corresponding to the input data.

    Returns
    -------
    None
        Prints the following performance metrics:
        - MSE (Mean Squared Error): Measures the average squared difference between predicted and actual values.
        - RMSE (Root Mean Squared Error): The square root of MSE, providing an estimate of the prediction error standard deviation.
        - MAE (Mean Absolute Error): The average magnitude of the prediction errors.
        - MAPE (Mean Absolute Percentage Error): The average percentage difference between predicted and true values.
        - R2 (Coefficient of Determination): A measure of how well the model explains the variance in the target variable.

    Notes
    -----
    - MAE is less sensitive to outliers than RMSE, making it more robust when large errors are not as important.
    - MAPE may be unreliable when true values are close to zero, as it involves division by the true values.
    - RMSE is more sensitive to large errors and is useful when large deviations are particularly undesirable.
    - R² provides insight into how well the model fits the data, with a value of 1 indicating a perfect fit.
    """
    y_pred = model.predict(X_true)
    args = (y_true, y_pred)
    
    print('Regression Report:')
    print('MSE:', metrics.mean_squared_error(*args))
    print('RMSE:', metrics.root_mean_squared_error(*args))
    print('MAE:', metrics.mean_absolute_error(*args))
    print('MAPE:', metrics.mean_absolute_percentage_error(*args))
    print('R2:', model.score(X_true, y_true))
    
    return