import re

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from sklearn import metrics
from sklearn.model_selection import cross_val_score
from sklearn.neighbors import KNeighborsClassifier


def safe_log(column):
    """
    Aplicar el logaritmo de manera segura, para evitar hacer log(0) o de números negativos.
    """
    # Desplazar los valores si hay alguno <= 0
    min_val = column.min()
    if min_val <= 0:
        column = column - min_val + 1
    return np.log(column)


def remove_highly_correlated_features(train_set, num_features, threshold=0.7, visualize='none', verbose=False):
    """
    Removes numerical features that are highly correlated with each other based on a specified threshold.

    Parameters:
    -----------
    train_set : pd.DataFrame
        DataFrame containing the numerical features.
    num_features : list
        List of numerical feature column names to evaluate.
    threshold : float, optional
        Threshold for collinearity between features. If the absolute correlation is greater than or equal
        to this value, one of the features will be excluded. Default is 0.7.
    visualize : str, optional
        Defines how the correlation matrix between features will be visualized ('heatmap', 'dataframe', 'both', 'none').
        Default is 'none'.
    verbose : bool, optional
        If True, prints detailed messages during the process. Default is False.

    Returns:
    --------
    list
        List of remaining features after excluding highly collinear ones.
    """
    
    # Compute correlation matrix for numerical features
    corr_matrix = train_set[num_features].corr().abs()
    
    # Visualization of the correlation matrix
    if visualize in ['heatmap', 'both']:
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
        plt.title("Feature Correlation Matrix (Heatmap)")
        plt.show()
    
    if visualize in ['dataframe', 'both']:
        print("Feature Correlation Matrix (DataFrame):")
        display(corr_matrix)
    
    # List to hold the features to be removed
    excluded_features = set()
    
    # Iterate over the correlation matrix
    for i in range(len(corr_matrix.columns)):
        for j in range(i+1, len(corr_matrix.columns)):
            feature_1 = corr_matrix.columns[i]
            feature_2 = corr_matrix.columns[j]
            corr_value = corr_matrix.iloc[i, j]
            
            # If correlation exceeds the threshold, mark one of the features for removal
            if corr_value >= threshold:
                if verbose:
                    print(f"Correlation between {feature_1} and {feature_2} is {corr_value}. Excluding {feature_2}.")
                excluded_features.add(feature_2)
    
    # Create the list of remaining features after exclusion
    remaining_features = [feature for feature in num_features if feature not in excluded_features]
    
    if verbose:
        print("Excluded features:", excluded_features)
        print("Remaining features:", remaining_features)
    
    return remaining_features



def get_target_correlated_features(train_set, num_features, target, target_threshold=0.1, collinearity_threshold=0.7, visualize='none', verbose=False):
    """
    Detects collinearity between numerical features and the target, and excludes highly collinear features.
    The correlation matrix shown in the heatmap and DataFrame includes the target as the first row/column.
    
    Parameters:
    -----------
    train_set : pd.DataFrame
        DataFrame containing the numerical features and the target.
    num_features : list
        List of numerical feature column names to evaluate.
    target : str
        Name of the target column.
    target_threshold : float, optional
        Threshold for selecting features that correlate with the target. Default is 0.1.
    collinearity_threshold : float, optional
        Threshold for collinearity between features. If the absolute correlation is greater than or equal
        to this value, one of the features will be excluded. Default is 0.7.
    visualize : str, optional
        Defines how the correlation matrix between features will be visualized ('heatmap', 'dataframe', 'both', 'none').
        Default is 'none'.
    verbose : bool, optional
        If True, prints detailed messages during the process. Default is False.

    Returns:
    --------
    list
        List of columns that have been excluded due to high collinearity.
    list
        List of remaining columns after exclusion.
    """
    
    # Add the target to the list of features for correlation matrix computation
    all_features = [target] + num_features
    
    # Compute correlation matrix including the target
    corr_matrix = train_set[all_features].corr()
    
    # Filter features based on their correlation with the target
    target_correlations = corr_matrix[target].abs().drop(target)
    selected_features = target_correlations[target_correlations >= target_threshold].index.tolist()
    
    if verbose:
        print(f"Features selected by correlation with target (threshold={target_threshold}): {selected_features}")
    
    # Add target back to the selected features list
    selected_features = [target] + selected_features
    
    # Generate the correlation matrix for the selected features including the target
    filtered_corr_matrix = corr_matrix.loc[selected_features, selected_features]
    
    # Visualization of the correlation matrix
    if visualize in ['heatmap', 'both']:
        plt.figure(figsize=(10, 8))
        sns.heatmap(filtered_corr_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
        plt.title("Correlation Matrix (Heatmap)")
        plt.show()
    
    if visualize in ['dataframe', 'both']:
        print("Correlation Matrix (DataFrame):")
        display(filtered_corr_matrix)
    
    # Initialize list of excluded features
    excluded_features = []
    
    # Check collinearity among selected features (excluding the target)
    for col in selected_features[1:]:
        if verbose:
            print(f"Checking collinearity with {col}")
        # Check if the column has already been excluded
        if col not in excluded_features:
            for col_2, corr_value in filtered_corr_matrix[col].items():
                if verbose:
                    print(f"\t{col_2}:", end=' ')
                # Ensure it's not the same column and that col_2 is in the selected features (excluding the target)
                if col != col_2 and col_2 in selected_features[1:]:
                    # If the absolute correlation exceeds the threshold, exclude col_2
                    if np.abs(corr_value) >= collinearity_threshold:
                        if verbose:
                            print(f"\tCorrelation is {round(corr_value, 2)}, excluding {col_2}.")
                        excluded_features.append(col_2)
                    else:
                        if verbose:
                            print(f"\tCorrelation is below the threshold. Keeping {col_2}.")
                elif col == col_2:
                    if verbose:
                        print("\tThis is the same feature. Not excluding.")
                else:
                    if verbose:
                        print("\tNot in the original feature list. Doing nothing.")
    
    # Remove duplicates from the excluded features list
    excluded_features = list(set(excluded_features))
    
    # Create a reduced set of features excluding the collinear ones
    reduced_features = [col for col in selected_features[1:] if col not in excluded_features]
    
    if verbose:
        print("Excluded features: ", excluded_features)
        print("Reduced set of features:", reduced_features)
    
    return excluded_features, reduced_features



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


def find_best_k(X_train, y_train, k_range=20):
    """
    Find the optimal number of neighbors (k) for a KNeighborsClassifier using cross-validation
    based on the "balanced accuracy" metric.

    Parameters
    ----------
    X_train: array-like of shape (n_samples, n_features)
        Training data.
    y_train: array-like of shape (n_samples,)
        Target values.
    k_range: int, optional, default=20
        The maximum number of neighbors to try.

    Returns
    -------
    best_k: int
        The value of k that gives the best balanced accuracy.
    best_model: KNeighborsClassifier object
        The trained KNeighborsClassifier with the optimal k.
    best_score: float
        The best balanced accuracy score achieved during cross-validation.
    """
    metrics = []
    for k in range(1, k_range + 1):
        print(f"Evaluating for k = {k}, balanced accuracy =", end=" ")
        model = KNeighborsClassifier(n_neighbors=k)
        balanced_accuracy = np.mean(cross_val_score(model, X_train, y_train, cv=5, scoring="balanced_accuracy"))
        metrics.append(balanced_accuracy)
        print(balanced_accuracy)
    
    # Identify the best k
    best_k = np.argmax(metrics) + 1  # Add 1 because np.argmax returns the index (0-based)
    best_score = metrics[best_k - 1]
    print(f"Best k = {best_k}, with balanced accuracy = {best_score}")
    
    # Train the final model with the best k
    best_model = KNeighborsClassifier(n_neighbors=best_k)
    best_model.fit(X_train, y_train)
    
    return best_k, best_model, best_score




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
        - R² (Coefficient of Determination): A measure of how well the model explains the variance in the target variable.

    Notes
    -----
    - MAE is less sensitive to outliers than RMSE, making it more robust when large errors are not as important.
    - MAPE may be unreliable when true values are close to zero, as it involves division by the true values.
    - RMSE is more sensitive to large errors and is useful when large deviations are particularly undesirable.
    - R² provides insight into how well the model fits the data, with a value of 1 indicating a perfect fit.
    """
    y_pred = model.predict(X_true)
    args = (y_true, y_pred)
    
    print('MSE train', metrics.mean_squared_error(*args))
    print('RMSE train', metrics.root_mean_squared_error(*args))
    print('MAE train:', metrics.mean_absolute_error(*args))
    print('MAPE train:', metrics.mean_absolute_percentage_error(*args))
    print('R2 train', model.score(X_true, y_true))
    
    return


def show_regression_coefs(model_reg):
    '''
    Visualizes the coefficients of a fitted regression model, including binary and multiclass logistic regression models.

    This function creates horizontal bar plots of the regression model's coefficients.
    For multiclass models, it creates a subplot for each class showing the original coefficients,
    and another subplot showing the absolute values of the coefficients sorted in ascending order. 
    Additionally, it returns a DataFrame containing the coefficients.

    Parameters
    ----------
    model_reg : sklearn.base.ClassifierMixin or sklearn.base.RegressorMixin
        A fitted scikit-learn regression model. The model should have the attributes 
        `coef_` (the model's coefficients) and `feature_names_in_` (the names of the features).
    
    Returns
    -------
    df_coef : pandas.DataFrame
        A DataFrame containing the coefficients of the regression model. For multiclass models,
        the DataFrame has one column per class. The index consists of the feature names.
    
    Example
    -------
    >>> from sklearn.linear_model import LogisticRegression
    >>> model_logreg = LogisticRegression(multi_class='multinomial').fit(X_train, y_train)
    >>> show_regression_coefs(model_logreg)
    
    Notes
    -----
    This function is designed to handle both binary and multiclass logistic regression models.
    '''
    # Handle binary or multiclass coefficients
    if model_reg.coef_.shape[0] > 1:  # Multiclass case
        coef = model_reg.coef_.T  # Transpose to have features as rows, classes as columns
        columns = [f"Class {i}" for i in range(coef.shape[1])]
    else:  # Binary case
        coef = model_reg.coef_.flatten()  # Flatten to 1D array
        columns = ["coefs"]

    # Create DataFrame with coefficients
    df_coef = pd.DataFrame(coef, index=model_reg.feature_names_in_, columns=columns)
    
    # Determine the number of columns for subplots
    num_cols = len(columns)
    
    # Plotting the coefficients
    fig, axs = plt.subplots(2, num_cols, figsize=(15, 10))
    fig.suptitle(f"Regression Model Coefficients - {str(model_reg)}")

    # Ensure axs is a 2D array even if num_cols == 1
    if num_cols == 1:
        axs = axs.reshape(2, 1)

    for i, col in enumerate(df_coef.columns):
        df_coef[col].plot(kind="barh", ax=axs[0, i], legend=False, title=f"Original Coefs: {col}")
        df_coef[col].abs().sort_values().plot(kind="barh", ax=axs[1, i], legend=False, title=f"Absolute Coefs: {col}")

    fig.tight_layout()
    plt.show()

    return df_coef




# def show_regression_coefs(model_reg):
#     '''
#     Visualizes the coefficients of a fitted regression model, including multiclase logistic regression models.

#     This function creates horizontal bar plots of the regression model's coefficients.
#     For multiclase models, it creates a subplot for each class showing the original coefficients,
#     and another subplot showing the absolute values of the coefficients sorted in ascending order. 
#     Additionally, it returns a DataFrame containing the coefficients.

#     Parameters
#     ----------
#     model_reg : sklearn.base.ClassifierMixin or sklearn.base.RegressorMixin
#         A fitted scikit-learn regression model. The model should have the attributes 
#         `coef_` (the model's coefficients) and `feature_names_in_` (the names of the features).
    
#     Returns
#     -------
#     df_coef : pandas.DataFrame
#         A DataFrame containing the coefficients of the regression model. For multiclase models,
#         the DataFrame has one column per class. The index consists of the feature names.
    
#     Example
#     -------
#     >>> from sklearn.linear_model import LogisticRegression
#     >>> model_logreg = LogisticRegression(multi_class='multinomial').fit(X_train, y_train)
#     >>> show_regression_coefs(model_logreg)
    
#     Notes
#     -----
#     This function is designed to handle both binary and multiclase logistic regression models.
#     '''
#     # Handle binary or multiclass coefficients
#     if len(model_reg.coef_.shape[0]) > 1:
#         coef = model_reg.coef_.T  # Transpose to have features as rows, classes as columns
#         columns = [f"Class {i}" for i in range(coef.shape[1])]
#     else:
#         coef = model_reg.coef_.flatten()
#         columns = ["coefs"]

#     # Create DataFrame with coefficients
#     df_coef = pd.DataFrame(coef, index=model_reg.feature_names_in_, columns=columns)
    
#     # Plotting the coefficients
#     fig, axs = plt.subplots(2, coef.shape[1], figsize=(15, 10))
#     fig.suptitle(f"Regression Model Coefficients - {str(model_reg)}")

#     for i, col in enumerate(df_coef.columns):
#         df_coef[col].plot(kind="barh", ax=axs[0, i], legend=False, title=f"Original Coefs: {col}")
#         df_coef[col].abs().sort_values().plot(kind="barh", ax=axs[1, i], legend=False, title=f"Absolute Coefs: {col}")

#     fig.tight_layout()
#     plt.show()

#     return df_coef


## ###############
## S12, U02, Ejercicios workout tengo funciones interesantes
## ###############


def plot_roc_curve(model, X, y):
    '''
    Plots the Receiver Operating Characteristic (ROC) curve for a given model's predictions.
    Typically apply on test set.

    Parameters:
    -----------
    model : estimator object
        The fitted model from which to predict probabilities.
    
    X : array-like of shape (n_samples, n_features)
        The input samples to predict probabilities on.
    
    y : array-like of shape (n_samples,)
        True binary labels for X.

    Returns:
    --------
    None
        This function plots the ROC curve but does not return any value.
    '''
    
    # Predict probabilities
    scores = model.predict_proba(X)
    
    # Compute ROC curve and ROC area
    fpr, tpr, thresholds = roc_curve(y, scores[:, 1])
    roc_auc = auc(fpr, tpr)
    print("AUC: %.2f" %(roc_auc))
    
    # Plotting the ROC curve
    plt.figure(figsize=(6, 5))
    plt.plot(fpr, tpr, linewidth=2, color='blue', label=f'ROC (area = {roc_auc:0.2f})')
    plt.plot([0, 1], [0, 1], 'k:', label="Random classifier's ROC curve")
    plt.ylabel('True Positive Rate (Recall)')
    plt.xlabel('False Positive Rate')
    plt.title('ROC Curve')
    plt.grid()
    plt.axis([0, 1, 0, 1])
    plt.legend(loc='lower right', fontsize=13)
    plt.show()



def get_features_importance(model, X_train, top_n=5):
    '''
    Returns the top N most important features based on the absolute value of the coefficients
    from a fitted logistic regression model.

    Parameters:
    -----------
    model : estimator object
        The fitted logistic regression model (e.g., from sklearn's LogisticRegression).
    
    X_train : DataFrame
        The DataFrame containing the training features used to fit the model.
    
    top_n : int, optional, default=5
        The number of top features to return based on the absolute value of the coefficients.

    Returns:
    --------
    DataFrame
        A DataFrame containing the top N features with the highest absolute coefficients, sorted in descending order.
    '''
    
    # Extract the intercept and coefficients from the model
    intercept = model.intercept_
    coefs = model.coef_.ravel()
    
    # Create a DataFrame to hold the features and their corresponding coefficients
    features = pd.DataFrame(coefs, X_train.columns, columns=['coefficient']).copy()
    
    # Take the absolute value of the coefficients
    features['coefficient'] = np.abs(features['coefficient'])
    
    # Sort the features by the absolute value of the coefficients and return the top N
    top_features = features.sort_values('coefficient', ascending=False).head(top_n)
    
    return top_features



def plot_features_importance(model, X_train, y_train):
    '''
    Calculates and plots the standardized feature importance based on the absolute value of the coefficients
    from a fitted logistic regression model, adjusted for feature standard deviations.

    Parameters:
    -----------
    model : estimator object
        The fitted logistic regression model (e.g., from sklearn's LogisticRegression).
    
    X_train : DataFrame
        The DataFrame containing the training features used to fit the model.
    
    y_train : Series
        The Series containing the training target variable.
    
    Returns:
    --------
    None
        This function plots the standardized feature importance but does not return any value.
    '''
    
    # Extract the coefficients from the model
    coefs = model.coef_.ravel()
    
    # Create a DataFrame to hold the features and their corresponding coefficients
    features = pd.DataFrame(coefs, X_train.columns, columns=['coefficient']).copy()
    
    # Calculate the standard deviation of each feature
    stdevs = [X_train[i].std() for i in X_train.columns]
    features['stdev'] = np.array(stdevs).reshape(-1, 1)
    
    # Calculate the importance of each feature
    features['importance'] = features['coefficient'] * features['stdev']
    features['importance_standardized'] = features['importance'] / y_train.std()
    
    # Sort features by standardized importance
    features = features.sort_values('importance_standardized', ascending=True)
    
    # Plot the standardized importance of features
    plt.figure(figsize=(10, 8))
    plt.barh(features.index, features['importance_standardized'], color='skyblue')
    plt.xlabel('Standardized Importance')
    plt.ylabel('Features')
    plt.title('Feature Importance Standardized by Coefficient and Feature Std Dev')
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.show()



##############################################
# DEPRECATED        DEPRECATED      DEPRECATED
##############################################

def show_regression_coefs_OLD(model_reg):
    '''
    Visualizes the coefficients of a fitted regression model.

    This function creates a horizontal bar plot of the regression model's coefficients.
    It displays two subplots: one showing the original coefficients and the other
    showing the absolute values of the coefficients sorted in ascending order. 
    Additionally, it returns a DataFrame containing the coefficients.

    Parameters
    ----------
    model_reg : sklearn.base.RegressorMixin
        A fitted scikit-learn regression model. The model should have the attributes 
        `coef_` (the model's coefficients) and `feature_names_in_` (the names of the features).
    
    figsize : tuple, optional, default=(10, 5)
        The size of the figure for the bar plots. It is passed to `matplotlib.pyplot.subplots`.
    
    Returns
    -------
    df_coef : pandas.DataFrame
        A DataFrame containing the coefficients of the regression model. The index consists of the feature 
        names and the single column is labeled "coefs".
    
    Example
    -------
    >>> from sklearn.linear_model import Ridge
    >>> model_ridge = Ridge().fit(X_train, y_train)
    >>> show_coefs(model_ridge)
    
    Notes
    -----
    This function requires the regression model to have been trained on the dataset with the `coef_` 
    and `feature_names_in_` attributes, which are standard for linear models like 
    `Ridge`, `Lasso`, or `LinearRegression` in scikit-learn.
    '''
    df_coef = pd.DataFrame(model_reg.coef_, index=model_reg.feature_names_in_, columns=["coefs"])

    fig, ax = plt.subplots(1, 2, figsize=(10, 5))
    df_coef.plot(kind="barh", ax=ax[0], legend=False)
    df_coef.abs().sort_values(by="coefs").plot(kind="barh", ax=ax[1], legend=False)
    fig.suptitle(f"Regression Model Coefficients - {str(model_reg)}")

    fig.tight_layout()

    return df_coef