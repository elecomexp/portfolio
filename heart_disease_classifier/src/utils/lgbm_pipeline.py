"""
lgbm_pipeline.py

Author: Lander Combarro Exposito
Created: 2024/11/18
Last Modified: 2024/11/18

Description
-----------
This script defines the complete pipeline for training a LightGBM (LGBMClassifier) model to predict heart disease. The pipeline includes the following components:

Usage
-----
The imbalanced-learn (library) Pipeline handles the preprocessing, class balancing, and model training in a unified manner.
The parameter grid allows for easy tuning of the LGBM classifier's hyperparameters.
This setup can be directly imported and used in a training script or Jupyter notebook. 
The user can enable or disable specific hyperparameter tuning options.
"""

from imblearn.pipeline import Pipeline
from imblearn.under_sampling import RandomUnderSampler
from lightgbm import LGBMClassifier
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import OrdinalEncoder

from utils.config import CAT_FEATURES, NUM_FEATURES

# preprocessing Pipeline definition
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='most_frequent')), 
            ('encoder', OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1))
        ]), CAT_FEATURES),
        ('num', SimpleImputer(strategy='median'), NUM_FEATURES)
    ],
    remainder='drop'
)

# default parameters for the LGBMClassifier model
default_params = {
    'objective': 'binary',
    'boosting_type': 'gbdt',
    'n_estimators': 200,
    'num_leaves': 60,
    'max_depth': 10,
    'learning_rate': 0.01,
    'min_child_samples': 20,
    'subsample': 0.8,
    'colsample_bytree': 0.8,
    'verbose': 1
}

# full Pipeline (imbalanced-learn) definition. Includes undersampling for class balance, preprocessing, and model training
pipeline = Pipeline([
    ('undersampling', RandomUnderSampler()),
    ('preprocessor', preprocessor),
    ('model', LGBMClassifier(**default_params))
])

# parameter grid for hyperparameter tuning in GridSearchCV
param_grid = {
    'model__num_leaves': [31, 45, 60],
    'model__max_depth': [4, 7, 10],
    'model__learning_rate': [0.01, 0.05, 0.1],
    'model__n_estimators': [100, 200, 400],
    'model__min_child_samples': [20, 40],
    'model__subsample': [0.8, 1.0],
    'model__colsample_bytree': [0.8, 1.0]
}

# arguments for the GridSearchCV function
kwargs = {
    'cv': StratifiedKFold(n_splits=5, shuffle=True),
    'scoring': 'recall',
    'n_jobs': -5,
    'verbose': 1
}
