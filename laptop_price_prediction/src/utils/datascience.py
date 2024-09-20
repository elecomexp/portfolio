import re

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

import scipy.stats

def get_cardinality(df: pd.DataFrame, threshold_categorical=10, threshold_continuous=30):
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



def coeficiente_variación(df):
    '''
    Devuelve un pandas.DataFrame con la media, la desviación estándar (ro), 
    en las mismas unidades que la media y su coeficiente de variación (CV)
    '''
    df_var = df.describe().loc[['std', 'mean']].T
    df_var['CV'] = df_var['std'] / df_var['mean']
    return df_var


def split_by_uppercase(text) -> str:
    '''
    Uses regular expressions to find uppercase letters, split a string at those points,
    and return a new string separated by spaces.
    
    Parameters:
    ----------
    text : str
        Text to split.
        
    Returns:
    -------
    str
        The modified string with spaces inserted before each uppercase letter.
    '''
    strings = re.findall(r'[A-Z][^A-Z]*', text)
    return ' '.join(strings)


# scipy.stats.mannwhitneyu()

# scipy.stats.f_oneway()

def mapa_calor(corr_matrix):
    '''
    Hay que introducir una matriz de correlación generada con pandas
    '''
    plt.figure(figsize=(10, 8))  # Ya lo veremos pero esto permite ajustar el tamaño de las gráficas
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", 
                cbar=True, square=True, linewidths=.5) # el cmap es el rango de colores usado para representar "el calor"

    plt.title('Matriz de Correlación')
    plt.xticks(rotation=45)  # Rota las etiquetas de las x si es necesario
    plt.yticks(rotation=45)  # Rota las etiquetas de las y si es necesario

    plt.show()
    
    








###########################################################################################
###     DEPRECATED      DEPRECATED      DEPRECATED      DEPRECATED      DEPRECATED      ###
###########################################################################################


def get_cardinality_class(df_in, threshold_categorical = 10, threshold_continuous = 30):
    '''
    Categorizes each column of `df_in` in a pandas.DataFrame based on its cardinality.

    Parameters
    ----------
    df_in : pandas.DataFrame
        The input DataFrame containing the data to be analyzed.
        
    threshold_categorical : int, optional
        The threshold for determining categorical variables. Columns with unique values 
        less than this threshold are considered categorical. Default is 10.
        
    threshold_continuous : int, optional
        The threshold percentage for determining continuous numerical variables. Columns with a 
        cardinality percentage higher than this threshold are considered continuous numerical. Default is 30.

    Returns
    -------
    pandas.DataFrame with columns:
        - 'Card': The cardinality of each column.
        - '%_Card': The percentage cardinality of each column relative to the total number of rows.
        - 'Tipo': The data type of each column.
        - 'Clase': The assigned variable class for each column based on the specified thresholds.

    Notes
    -----
    The function assigns variable classes as follows:
        - 'Categoric' for columns with cardinality less than `threshold_categorical`.
        - 'Binary' for columns with exactly 2 unique values.
        - 'Numeric - Discrete' for columns with cardinality greater than or equal to `threshold_categorical`.
        - 'Numeric - Continuous' for columns with a cardinality percentage greater than `threshold_continuous`.
    '''
    df_out = pd.DataFrame([df_in.nunique(), df_in.nunique()/len(df_in) * 100, df_in.dtypes])
    df_out = df_out.T.rename(columns = {0: "Card", 1: "%_Card", 2: "Tipo"})
    

    df_out.loc[df_out["Card"] < threshold_categorical, "Clase"] = "Categoric"    
    df_out.loc[df_out["Card"] == 2, "Clase"] = "Binary"
    df_out.loc[df_out["Card"] >= threshold_categorical, "Clase"] ="Numeric - Discrete"
    df_out.loc[df_out["%_Card"] > threshold_continuous, "Clase"] = "Numeric - Continuous"
    
    return df_out