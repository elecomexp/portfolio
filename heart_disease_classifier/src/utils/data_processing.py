"""
data_processing.py

Author: Lander Combarro Exposito
Created: 2024/11/18
Last Modified: 2024/11/18

Description
-----------
This module contains utility functions for loading training data and target encoding labels.
"""

import pandas as pd
from sklearn.preprocessing import LabelEncoder
from utils.config import TARGET, TRAIN_PATH

def load_data(train_path=TRAIN_PATH):
    """
    Loads the training data, splits it into features and target.
    
    Parameters
    ----------
    train_path : str, optional
        Path to the training dataset (default is TRAIN_PATH).
    
    Returns
    -------
    X_train : pd.DataFrame
        DataFrame containing the feature columns.
    
    y_train : pd.Series
        Series containing the target column.
    """
    train_set = pd.read_csv(train_path)
    X_train = train_set.drop(columns=[TARGET])  # Features
    y_train = train_set[TARGET]  # Target
    return X_train, y_train

def label_encoder(y_train):
    """
    Encodes target labels into numeric values.
    
    Parameters
    ----------
    y_train : pd.Series
        Series containing the target labels.
    
    Returns
    -------
    le : LabelEncoder
        Fitted LabelEncoder instance.
    
    y_train_encoded : np.ndarray
        Array of encoded target values.
    """
    le = LabelEncoder()
    y_train_encoded = le.fit_transform(y_train)  # Encode target labels
    return le, y_train_encoded
