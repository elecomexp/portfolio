"""
config.py

Author: Lander Combarro Exposito
Created: 2024/11/18
Last Modified: 2024/11/18

Description
-----------
Configuration file for the heart disease prediction project.

This file contains the paths to the training dataset, the target variable, 
and the selected features (both categorical and numerical) used for model training. 
The feature selection was performed using Recursive Feature Elimination with Cross-Validation (RFECV) 
and expert knowledge provided by a cardiologist.
"""

# train dataset path
TRAIN_PATH = './data/processed/heart_disease_train.csv'

# classification target
TARGET = 'HadHeartAttack'

# categorical features selected by RFECV and cardiologist expertise
CAT_FEATURES = [
    'GeneralHealth',
    'RemovedTeeth',
    'HadDiabetes', 
    'SmokerStatus',
    'AgeCategory',
    'HadAngina',
    'HadStroke',
    'HadCOPD',
    'DeafOrHardOfHearing',
    'DifficultyWalking',
    'ChestScan',   
    'AlcoholDrinkers',
    'Sex',  
    'PhysicalActivities'
]

# numerical features selected by RFECV and cardiologist expertise
NUM_FEATURES = [    
    'SleepHours',
    'WeightInKilograms',
    'BMI'
]

# full features
FEATURES = CAT_FEATURES + NUM_FEATURES
