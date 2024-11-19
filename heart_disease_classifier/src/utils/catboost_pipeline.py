"""
catboost_pipeline.py

Author: Lander Combarro Exposito
Created: 2024/11/18
Last Modified: 2024/11/18

Description
-----------
This script defines the complete pipeline for training a CatBoost model (CatBoostClassifier) to predict heart disease.

Usage
-----
The imbalanced-learn (library) pipeline integrates preprocessing, class balancing, and model training into one unified workflow.
Hyperparameter tuning is set up using GridSearchCV to improve the model's recall score.
The CatBoost model can be configured to run on GPU for faster processing.
The user can enable or disable specific hyperparameter tuning options.
"""

from catboost import CatBoostClassifier
from imblearn.pipeline import Pipeline
from imblearn.under_sampling import RandomUnderSampler
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import StratifiedKFold

from utils.config import CAT_FEATURES, NUM_FEATURES

# default parameters for the LGBMClassifier model
default_params = {
    'iterations': 200,
    'learning_rate': 0.05,
    'depth': 10,
    'bagging_temperature': 0.0,
    'l2_leaf_reg': 5,
    'cat_features': list(range(0, 14)),
    # 'task_type': 'GPU',
    # 'devices': '0',
    'verbose': 1
}

# full Pipeline definition. Includes undersampling for class balance, preprocessing, and model training
pipeline = Pipeline([
    ('undersampling', RandomUnderSampler()),
    ('preprocessor', ColumnTransformer(
        transformers=[
            ('cat', SimpleImputer(strategy='most_frequent'), CAT_FEATURES),
            ('num', SimpleImputer(strategy='median'), NUM_FEATURES)
        ],
        remainder='drop'
    )),
    ('model', CatBoostClassifier(**default_params))
])

# parameter grid for hyperparameter tuning in GridSearchCV
param_grid = {
    'model__iterations': [100, 200],
    'model__learning_rate': [0.01, 0.05],
    'model__depth': [7, 10],
    'model__l2_leaf_reg': [1, 5],
    'model__bagging_temperature': [0.0, 1.0]
}

# arguments for the GridSearchCV function
kwargs = {
    'cv': StratifiedKFold(n_splits=5, shuffle=True),
    'scoring': 'recall',
    'n_jobs': -5,
    'verbose': 1
}
