"""
train.py

Author: Lander Combarro Exposito
Created: 2024/11/18
Last Modified: 2024/11/18

Description
-----------
This script is responsible for training a heart-attack classfication machine learning model 
using either LightGBM (lgbm) or CatBoost (catboost).
The setup provides flexibility, allowing you to adapt the model to new data when necessary, use default 
parameters or include optional hyperparameter tuning via GridSearchCV.

The script performs the following steps:
1. Loads model configurations based on the selected model.
2. Optionally tunes hyperparameters if the '--tune' flag is provided.
3. Trains the model on the provided dataset.
4. Saves the trained model as a .joblib file for future use in production or evaluation.

Usage
-----
python train.py --model <model_name> --tune --output <output_filename>

Arguments
---------
--model   : Specify which model to use ('lgbm' or 'catboost').
--tune    : Flag to enable hyperparameter tuning via GridSearchCV.
--output  : The .joblib filename to save the trained model. If not specified, a default filename is used.

"""

import argparse
from importlib import import_module
from time import time

import joblib
from sklearn.model_selection import GridSearchCV
from utils.data_processing import label_encoder, load_data

def get_model_configs(model_name):
    """
    Dynamically loads model configurations based on the provided model name.
    
    Parameters
    ----------
    model_name : str
        Name of the model configuration to load ('lgbm' or 'catboost').
    
    Returns
    -------
    pipeline : Pipeline
        Model training pipeline.
    
    param_grid : dict
        Hyperparameter tuning grid.
    
    kwargs : dict
        Additional arguments for GridSearchCV.
    """
    module = import_module(f'utils.{model_name}_pipeline')
    return module.pipeline, module.param_grid, module.kwargs

def validate_output_filename(filename):
    """
    Validates that the output filename has a .joblib extension.
    
    Parameters
    ----------
    filename: str
        The filename to validate.
    
    Returns
    -------
    str
        A valid filename with .joblib extension.
    
    Raises
    ------
    ValueError
        If the filename does not have a .joblib extension.
    """
    if not filename.endswith('.joblib'):
        print("\033[93m>>> Warning: The specified filename does not have a .joblib extension. Adding it automatically.\033[0m")
        filename += '.joblib'
    return filename

if __name__ == "__main__":
    # parse command-line arguments
    parser = argparse.ArgumentParser(description='Train a model with optional hyperparameter tuning.')
    parser.add_argument('--model', type=str, default='lgbm', choices=['lgbm', 'catboost'], help='Specify the model to use ("lgbm" or "catboost").')
    parser.add_argument('--tune', action='store_true', help='Tune hyperparameters')
    parser.add_argument('--output', type=str, help='Filename for the saved model')
    args = parser.parse_args()
    
    # set a default output filename if none is provided, based on the model name
    if not args.output:
        args.output = f'./models/{args.model}_heart_model.joblib'

    # load model configurations
    pipeline, param_grid, kwargs = get_model_configs(args.model)

    # validate and adjust output filename if necessary
    output_filename = validate_output_filename(args.output)

    # load the data
    X_train, y_train = load_data()
    le, y_train_encoded = label_encoder(y_train)

    # fit time estimation
    time_init = time()
    # set up GridSearch if tuning is specified
    if args.tune:
        grid_search = GridSearchCV(estimator=pipeline, param_grid=param_grid, **kwargs)
        grid_search.fit(X_train, y_train_encoded)
        best_model = grid_search.best_estimator_
        print(f'>>> Best hyperparameters: {grid_search.best_params_}')
        print(f'>>> Best recall score: {grid_search.best_score_}.')
        print(f'>>> Model training completed with GridSearchCV.')
    else:
        # train with default parameters
        pipeline.fit(X_train, y_train_encoded)
        best_model = pipeline
        print('>>> Model training completed with default parameters.')     
         
    time_end = (time() - time_init) / 60 
    print(f'>>> Fitting time: {round(time_end, 2)} minutes.')

    # save the trained model
    joblib.dump(best_model, output_filename)
    print(f'>>> Model saved as {output_filename}.')
