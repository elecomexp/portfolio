# Heart Disease Classifier

This repository contains the implementation of a machine learning model to predict the likelihood of a heart attack using various features such as medical history, lifestyle habits, and demographics. The project emphasize the use of LightGBM and CatBoost classifiers, optimized through hyperparameter tuning, and is built to handle imbalanced data through under-sampling techniques. The model aims to provide accurate predictions to assist in the early detection of heart disease in patients.

## Abstract

According to the [U.S. Center for Disease Control and Prevention](https://www.cdc.gov/) (CDC), heart disease is one of the [primary causes of death](https://www.cdc.gov/heart-disease/data-research/facts-stats/index.html) across racial groups in the United States. Nearly half of all Americans (47%) live with at least one of the top [three risk factors](https://www.cdc.gov/heart-disease/risk-factors/?CDC_AAref_Val=https://www.cdc.gov/heartdisease/risk_factors.htm): high blood pressure, high cholesterol, or smoking. Other significant risk indicators include diabetes, obesity (high BMI), insufficient physical activity, and excessive alcohol consumption. Reducing these risk factors is crucial in healthcare, as they heavily influence heart disease rates. With advances in computing, machine learning offers powerful tools to analyze and detect "patterns" in health data that may help predict and manage heart conditions.

## Data Source

The CDC [Behavioral Risk Factor Surveillance System](https://www.cdc.gov/brfss/annual_data/annual_2022.html) (BRFSS) plays a significant role. This system conducts yearly telephone surveys to gather health data from U.S. residents. According to the CDC: "Initiated in 1984 with just 15 states, BRFSS now gathers data from all 50 states, the District of Columbia, and three U.S. territories. Each year, BRFSS completes over 400,000 interviews with adults, making it the world’s largest ongoing health survey system." 

Within this dataset, it can be identified numerous factors (survey questions) that influence heart disease, either directly or indirectly. Therefore, the most relevant variables for analysis have been selected in a [condensed version of the original BRFSS dataset](https://www.kaggle.com/datasets/kamilpytlak/personal-key-indicators-of-heart-disease/data). 

## Goal

For a classification problem focused on detecting potential **heart attacks**, the choice of metric is critical. In such medical applications, it’s essential to **minimize the likelihood of missing true cases** (i.e., actual heart attacks) because a missed detection could have severe health implications. Therefore, **optimizing for recall** (also known as sensitivity or true positive rate) will be the priority. Recall measures the proportion of actual positive cases (heart attacks) that are correctly identified by the model. **By maximizing recall, we aim to reduce the chances of false negatives, which in this context means failing to identify a patient at risk.**

## Project Structure

```bash
heart_disease_classifier/
│
├── docs/                 # Documentation files
├── src/                  # Source code for the project
│   ├── data/             # Data-related scripts
│   │   ├── processed/    # Processed data files
│   │   └── raw/          # Raw data files
│   ├── img/              # Images related to the project
│   ├── models/           # Trained models saved in .pkl (notebooks) or .joblib (train.py)
│   ├── notebooks/        # Jupyter Notebooks for analysis and experimentation (numbered)
│   └── utils/            # Utility functions (data processing, model setup, etc.)
│   └── train.py          # Main script for training models
│
├── README.md             # Main documentation for the project
└── requirements.txt      # Python dependencies
```

## Summary of the Analysis

This project follows a comprehensive process to develop a predictive model for a medical dataset, starting with data download and an in-depth exploration to understand its characteristics. An important aspect of this analysis was handling an **imbalanced target variable**, which is crucial to ensure fair detection of positive and negative cases. Each stage of the project is documented and can be followed step-by-step in the provided numbered [Jupyter Notebooks](./src/notebooks) (from nb00 to nb04), offering a clear guide from data preparation to final model evaluation.

Feature selection was guided a combination of an EDA, RFECV (Recursive Feature Elimination with Cross-Validation) and the expertise of the cardiologist [María Davó Jimémez](https://www.linkedin.com/in/mar%C3%ADa-dav%C3%B3-jim%C3%A9nez-b63371233/) from [Northwestern University](https://www.northwestern.edu/) (Chicago, IL)., ensuring that only the most relevant predictors for the target condition were retained. Many different models have been tested, but only two (with the highest initial performance metrics) were further optimized by hyperparameter tuning: [LGBMClassifier](https://lightgbm.readthedocs.io/en/latest/pythonapi/lightgbm.LGBMClassifier.html) and [CatBoostClassifier](https://catboost.ai/en/docs/concepts/python-reference_catboostclassifier).

In real-world healthcare, both True Positives (TP) and True Negatives (TN) are crucial:

- True Positives (TP): Correctly detecting heart attacks is critical for timely intervention, potentially saving lives.
- True Negatives (TN): Correctly identifying healthy patients is equally important, as false positives can cause unnecessary emotional distress, anxiety, and invasive tests.

Both models showed promising results with very similar performance metrics. The LightGBM model demonstrated efficiency with its gradient boosting framework, while CatBoost provided competitive results due to its handling of categorical features and GPU acceleration posibilities. Here are some of the results achieved in a test set:

```python
Heart Attack Classification Report:

              precision    recall  f1-score   support

          No       0.99      0.80      0.89     46518
         Yes       0.19      0.80      0.31      2687

    accuracy                           0.80     49205
   macro avg       0.59      0.80      0.60     49205
weighted avg       0.94      0.80      0.85     49205
```

All the steps from the Notebooks have been unified into the [train.py](./src/train.py) script, which provides a streamlined and efficient process for model training. This script is ready for future production deployment, encapsulating the entire workflow and enabling easy integration with other systems.

## Instalation

To get started with this project, you will need to install the necessary Python dependencies. You can do so by running:

```bash
pip install -r requirements.txt
```

## Usage

1. **Notebooks**:

The [Notebooks directory](./src/notebooks) contains Jupyter Notebooks for analysis, model validation, and visualizations. They can be followed step-by-step by the provided numeration (from nb00 to nb04).

2. **Training the model**.

To train a model, run the [train.py](./src/train.py) script. The script accepts command-line arguments to specify the model type (lgbm or catboost), whether to tune hyperparameters, and the output filename for the saved model.


```bash
Arguments
---------
--model   : Specify which model to use ('lgbm' or 'catboost').
--tune    : Flag to enable hyperparameter tuning via GridSearchCV.
--output  : The .joblib filename to save the trained model. If not specified, a default filename is used.
```

E.g., the following command will train a LightGBM model with hyperparameter tuning, via GridSearchCV, and save the trained model to `./models/lgbm_heart_model.joblib`.

```bash
python src/train.py --model lgbm --tune --output ./models/lgbm_heart_model.joblib
```

3. **Model Inference**:

After training, you can load the saved models from the models directory for inference or future predictions.

```python
import joblib
model = joblib.load('./models/lgbm_heart_model.joblib')
```

You can then use the `model.predict()` method to make predictions on new data.

## Contributing

Contributions are welcome! If you want to contribute, please follow these steps:

Fork the repository.
Create a new branch for your feature or bugfix.
Commit your changes.
Push to your fork.
Create a pull request with a description of the changes.

---

Feel free to explore the directories and files for a detailed understanding of the project and its findings. If you have any questions or suggestions, please feel free to reach out.