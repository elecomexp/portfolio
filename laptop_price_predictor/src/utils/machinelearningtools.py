"""
machinelearningtools.py

Author: Lander Combarro Exposito
Created: September 20, 2024
Last Modified: September 20, 2024

Description
-----------
This function plots the predicted values against the actual values for regression tasks to visually 
assess the performance of a regression model. The plot includes a scatter plot of predicted vs actual 
values and a reference line (y=x) to indicate perfect predictions.
"""

import matplotlib.pyplot as plt

def plot_predictions_vs_actual(y_real, y_pred):
    """
    Plot the predicted values against the actual values for regression tasks.

    Parameters
    ----------
    y_real (array-like): Ground truth (actual) values of the target variable.
    y_pred (array-like): Predicted values of the target variable.
    
    Return
    -------
    None
    """
    plt.figure(figsize=(8, 6))
    plt.scatter(y_pred, y_real, alpha=0.5, edgecolor='k', s=50)
    plt.xlabel("Predicted Values", fontsize=12)
    plt.ylabel("Actual Values", fontsize=12)

    # Plotting y=x reference line
    max_value = max(max(y_real), max(y_pred))
    min_value = min(min(y_real), min(y_pred))
    plt.plot([min_value, max_value], [min_value, max_value], 'r', linestyle='--', linewidth=2, label="y = x")

    plt.title('Predictions vs Actual', fontsize=14)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
