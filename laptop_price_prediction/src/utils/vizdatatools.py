'''
Author: Lander Combarro Exposito
Date: 2024-07-17

Module Functions:

Análisis  univariante
---------------------

    plot_multiple_categorical_distributions
    plot_multiple_histograms_KDEs_boxplots
    violinplot_multiple
    boxplot_multiple
    lineplot_multiple

Análisis bivariante
-------------------

    Categórica - Categórica
    
        plot_categorical_relationship
        plot_absolute_categorical_relationship_and_contingency_table

    Categórica - Numérica
    
        plot_categorical_numerical_relationship
        boxplots_grouped
        plot_histograms_by_categorical_numerical_relationship
        plot_histograms_grouped

    Numérica - Numérica
    
        scatterplot_with_correlation

Análisis multivariante
----------------------

    3 Categorical Variables
    
        plot_tricategorical_analysis

    2 Numerical, 1 Categorical Variables
    
        bubleplot
        scatterplot_3variables
    
    4 Variables
        scatterplot

'''

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import squarify

'''
###################################################################################################
#                                                                                                 #
#   Análisis UNIVARIANTE               Análisis UNIVARIANTE                Análisis UNIVARIANTE   #
#                                                                                                 #
###################################################################################################
'''


def plot_multiple_categorical_distributions(df, categorical_columns, *, relative = False, show_values = True, rotation = 45, palette = 'viridis') -> None:
    '''
    Plot a bar-graphs matrix, with 2 columns and the rows needed to plot the
    `absolute` or `relative` frequency from the categorical columns of `df`.
    
    Parameters
    ----------
    df : pandas.DataFrame
        pandas.DataFrame

    categorical_columns : list
        Categorical columns   

    relative : bool, optional
        If True, it plots Relative Frecuency.
        
    show_values : bool, optional
        If True, show numerical values over each bar.
        
    rotation : int, optional
        X-Tick label rotation.
        
    palette : None, palette name, list, or dict, optional
        Colors to use for the different levels of the hue variable. 
        Should be something that can be interpreted by color_palette(), 
        or a dictionary mapping hue levels to matplotlib colors. 
    '''
    num_columns = len(categorical_columns)
    num_rows = (num_columns // 2) + (num_columns % 2)

    if num_columns == 1:
        fig, ax = plt.subplots(1, 1, figsize=(7, 5))
    else:
        fig, axs = plt.subplots(num_rows, 2, figsize=(15, 5 * num_rows))
        axs = axs.flatten()     # Return a copy of the array collapsed into one dimension.

    for i, col in enumerate(categorical_columns):
        if num_columns > 1:
            ax = axs[i]
        if relative:    
            total = df[col].value_counts().sum()
            serie = df[col].value_counts().apply(lambda x: x / total)
            sns.barplot(x = serie.index, y = serie, ax = ax, palette = palette, hue = serie.index, legend = False)
            ax.set_ylabel('Relative Frequency')
        else:
            serie = df[col].value_counts()
            sns.barplot( x = serie.index, y = serie, ax = ax, palette = palette, hue = serie.index, legend = False)
            ax.set_ylabel('Frecuency')

        ax.set_title(f'{col}: Distribution')
        ax.set_xlabel('')
        ax.tick_params(axis = 'x', rotation = rotation)

        if show_values:
            for p in ax.patches:
                height = p.get_height()
                ax.annotate(f'{height:.2f}', (p.get_x() + p.get_width() / 2., height), 
                            ha='center', va='center', xytext=(0, 9), textcoords='offset points')

    for j in range(i + 1, num_rows * 2):
        if num_columns > 1:
            axs[j].axis('off')

    plt.tight_layout()
    plt.show()


def plot_multiple_histograms_KDEs_boxplots(df, columns, *, kde=True, boxplot = True, whisker_width = 1.5, bins = None) -> None:
    '''
    Plot histogram, KDE and Box-Plots in one figure, using `plt.subplots()` and `"Seaborn"`
    
    Parameters
    ----------
    df : pandas.DataFrame
        `pandas.DataFrame` to evaluate.
    
    columns : list
        Numerical columns from `df`

    kde : bool, optional
        If True, plot the KDE. Default is True.

    boxplot : bool, optional
        If True, plot the boxplot. Default is True.
                
    whisker_width : float, optional
        Width of the whiskers. Default is 1.5.
    
    bins : None or str, number, vector, or a pair of such values, optional
        Number of bins for the groups. Default is "auto".
    '''
    num_columns = len(columns)
    if num_columns:
        if boxplot:
            fig, axs = plt.subplots(num_columns, 2, figsize=(12, 5 * num_columns))
        else:
            fig, axs = plt.subplots(num_columns, 1, figsize=(6, 5 * num_columns))

        for i, column in enumerate(columns):
            if df[column].dtype in ['int64', 'float64']:
                # Histogram and KDE
                sns.histplot(df[column], kde=kde, ax=axs[i, 0] if boxplot and num_columns > 1 else axs[i], bins="auto" if not bins else bins[i])
                if boxplot:
                    if kde:
                        axs[i, 0].set_title(f'{column}: Histogram and KDE')
                    else:
                        axs[i, 0].set_title(f'{column}: Histogram')
                else:
                    if kde:
                        axs[i].set_title(f'{column}: Histogram and KDE')
                    else:
                        axs[i].set_title(f'{column}: Histogram')

                # Boxplot
                if boxplot:
                    sns.boxplot(x=df[column], ax=axs[i, 1] if num_columns > 1 else axs[i + num_columns], whis=whisker_width)
                    axs[i, 1].set_title(f'{column}: BoxPlot')

        plt.tight_layout()
        plt.show()


def violinplot_multiple(df, columnas_numericas) -> None:
    """
    Muestra una matriz de diagramas de violín para las columnas numéricas especificadas de un DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame que contiene los datos.
        
    columnas_numericas : list
        Lista de nombres de las columnas numéricas.
    """
    num_cols = len(columnas_numericas)

    # Configurar el tamaño de la figura
    plt.figure(figsize=(num_cols * 4, 4))

    # Crear un diagrama de violín para cada columna numérica
    for i, col in enumerate(columnas_numericas, 1):
        plt.subplot(1, num_cols, i)
        sns.violinplot(y=df[col])
        plt.title(col)

    # Mostrar la matriz de diagramas de violín
    plt.tight_layout()
    plt.show()


def boxplot_multiple(df, columns, dim_matriz_visual = 2) -> None:
    num_cols = len(columns)
    num_rows = num_cols // dim_matriz_visual + num_cols % dim_matriz_visual
    fig, axes = plt.subplots(num_rows, dim_matriz_visual, figsize=(12, 6 * num_rows))
    axes = axes.flatten()

    for i, column in enumerate(columns):
        if df[column].dtype in ['int64', 'float64']:
            sns.boxplot(data=df, x=column, ax=axes[i])
            axes[i].set_title(column)

    # Ocultar ejes vacíos
    for j in range(i+1, num_rows * 2):
        axes[j].axis('off')

    plt.tight_layout()
    plt.show()


def lineplot_multiple(df, numerical_serie_columns, *, all_together=False, start_date=None, end_date=None) -> None:
    '''
    Lineplots of serie-style columns in the DataFrame.

    Parameters
    ----------
    df : pandas.DataFrame
        pandas.DataFrame

    numerical_serie_columns : list
        These columns must be sorted and represent a serie (of dates for example)
    
    all_together : bool, optional
        If True, plot all lines in one plot with a legend. Default is False.

    start_date : str or pd.Timestamp, optional
        Start date for the plot. Default is None (use all data).

    end_date : str or pd.Timestamp, optional
        End date for the plot. Default is None (use all data).
    '''
    # Redefine dataframe
    if start_date:
        df = df[df.index >= pd.to_datetime(start_date)]
    if end_date:
        df = df[df.index <= pd.to_datetime(end_date)]

    num_columns = len(numerical_serie_columns)
    num_rows = (num_columns // 2) + (num_columns % 2)

    if all_together:
        fig, ax = plt.subplots(1, 1, figsize=(7, 5))
        for col in numerical_serie_columns:
            sns.lineplot(x = df.index, y = df[col], data = df, ax = ax, label = col)
        ax.set_title('All Columns: Line-Plot')
        ax.set_xlabel(f'{df.index.name}')
        ax.set_ylabel('Values')
        ax.legend()
    else:
        if num_columns == 1:
            fig, ax = plt.subplots(1, 1, figsize=(7, 5))
            sns.lineplot(x = df.index, y = df[numerical_serie_columns[0]], data = df, ax = ax)
            ax.set_title(f'{numerical_serie_columns[0]}: Line-Plot')
            ax.set_xlabel(f'{df.index.name}')
            ax.set_ylabel(f'{numerical_serie_columns[0]}')
        else:
            fig, axs = plt.subplots(num_rows, 2, figsize=(15, 5 * num_rows))
            axs = axs.flatten()  # Return a copy of the array collapsed into one dimension.

            for i, col in enumerate(numerical_serie_columns):
                ax = axs[i]
                sns.lineplot(x = df.index, y = df[col], data = df, ax = ax)
                ax.set_title(f'{col}: Line-Plot')
                ax.set_xlabel(f'{df.index.name}')
                ax.set_ylabel(f'{col}')

            for j in range(i + 1, num_rows * 2):
                axs[j].axis('off')

    plt.tight_layout()
    plt.show()


'''
###################################################################################################
#                                                                                                 #
#    Análisis BIVARIANTE                Análisis BIVARIANTE                 Análisis BIVARIANTE   #
#                                                                                                 #
###################################################################################################
'''

'''
##############################################
#          Dos variables CATEGÓRICAS         #
##############################################
'''

def plot_categorical_relationship(df, cat_col1, cat_col2, relative_freq=False, show_values=True, size_group = 5):
    # Prepara los datos
    count_data = df.groupby([cat_col1, cat_col2]).size().reset_index(name='count')
    total_counts = df[cat_col1].value_counts()
    
    # Convierte a frecuencias relativas si se solicita
    if relative_freq:
        count_data['count'] = count_data.apply(lambda x: x['count'] / total_counts[x[cat_col1]], axis=1)

    # Si hay más de size_group categorías en cat_col1, las divide en grupos de size_group
    unique_categories = df[cat_col1].unique()
    if len(unique_categories) > size_group:
        num_plots = int(np.ceil(len(unique_categories) / size_group))

        for i in range(num_plots):
            # Selecciona un subconjunto de categorías para cada gráfico
            categories_subset = unique_categories[i * size_group:(i + 1) * size_group]
            data_subset = count_data[count_data[cat_col1].isin(categories_subset)]

            # Crea el gráfico
            plt.figure(figsize=(10, 6))
            ax = sns.barplot(x=cat_col1, y='count', hue=cat_col2, data=data_subset, order=categories_subset)

            # Añade títulos y etiquetas
            plt.title(f'Relación entre {cat_col1} y {cat_col2} - Grupo {i + 1}')
            plt.xlabel(cat_col1)
            plt.ylabel('Frecuencia' if relative_freq else 'Conteo')
            plt.xticks(rotation=45)

            # Mostrar valores en el gráfico
            if show_values:
                for p in ax.patches:
                    ax.annotate(f'{p.get_height():.2f}', (p.get_x() + p.get_width() / 2., p.get_height()),
                                ha='center', va='center', fontsize=10, color='black', xytext=(0, size_group),
                                textcoords='offset points')

            # Muestra el gráfico
            plt.show()
    else:
        # Crea el gráfico para menos de size_group categorías
        plt.figure(figsize=(10, 6))
        ax = sns.barplot(x=cat_col1, y='count', hue=cat_col2, data=count_data)

        # Añade títulos y etiquetas
        plt.title(f'Relación entre {cat_col1} y {cat_col2}')
        plt.xlabel(cat_col1)
        plt.ylabel('Frecuencia' if relative_freq else 'Conteo')
        plt.xticks(rotation=45)

        # Mostrar valores en el gráfico
        if show_values:
            for p in ax.patches:
                ax.annotate(f'{p.get_height():.2f}', (p.get_x() + p.get_width() / 2., p.get_height()),
                            ha='center', va='center', fontsize=10, color='black', xytext=(0, size_group),
                            textcoords='offset points')

        # Muestra el gráfico
        plt.show()


def plot_absolute_categorical_relationship_and_contingency_table(df, col1, col2):
    '''
    This function takes a DataFrame and two categorical column names, then performs the following tasks:
    
    1. Draws a combination of graphs with the absolute frequencies of each categorical column using countplot.
    2. Creates a catplot with the second categorical column as the 'col' argument for comparison.
    3. Returns the contingency table of the two columns.
    
    Parameters
    -----------
    df : pd.DataFrame
        The input DataFrame containing the data.
        
    col1 : str
        The name of the first categorical column.
    
    col2 : str
        The name of the second categorical column.
    
    Returns
    --------
    pd.DataFrame: A contingency table showing the frequency distribution of the two categorical columns.
    
    Example
    --------
    df = pd.DataFrame({
        'Category1': ['A', 'B', 'A', 'C', 'B', 'A', 'C'],
        'Category2': ['X', 'Y', 'X', 'Y', 'X', 'X', 'Y']
    })
    
    result = plot_and_contingency_table(df, 'Category1', 'Category2')
    print(result)
    '''
    fig, axs = plt.subplots(1, 2, figsize = (15, 5))
    
    # Countplot for the first categorical column
    sns.countplot(data = df, x = col1, ax = axs[0])
    axs[0].set_title(f'Count of {col1}')
    
    # Countplot for the second categorical column
    sns.countplot(data=df, x=col2, ax=axs[1])
    axs[1].set_title(f'Count of {col2}')
    
    plt.tight_layout()
    
    # Create a catplot for the comparison of the two columns
    catplot_fig = sns.catplot(data = df, x = col1, col = col2, kind = 'count')
    
    plt.show()
    
    # Generate the contingency table
    contingency_table = pd.crosstab(df[col1], df[col2])
    
    return contingency_table


'''
##############################################
#    Dos Variables: CATEGÓRICA + NUMÉRICA    #
##############################################
'''

def plot_categorical_numerical_relationship(df, categorical_col, numerical_col, show_values=True, measure='mean', group_size=5):
    # Calcula la medida de tendencia central (mean o median)
    if measure == 'median':
        grouped_data = df.groupby(categorical_col)[numerical_col].median()
    else:
        # Por defecto, usa la media
        grouped_data = df.groupby(categorical_col)[numerical_col].mean()

    # Ordena los valores
    grouped_data = grouped_data.sort_values(ascending=False)

    # Si hay más de group_size categorías, las divide en grupos de group_size
    if grouped_data.shape[0] > group_size:
        unique_categories = grouped_data.index.unique()
        num_plots = int(np.ceil(len(unique_categories) / group_size))

        for i in range(num_plots):
            # Selecciona un subconjunto de categorías para cada gráfico
            categories_subset = unique_categories[i * group_size:(i + 1) * group_size]
            data_subset = grouped_data.loc[categories_subset]

            # Crea el gráfico
            plt.figure(figsize=(10, 6))
            ax = sns.barplot(x=data_subset.index, y=data_subset.values)

            # Añade títulos y etiquetas
            plt.title(f'Relación entre {categorical_col} y {numerical_col} - Grupo {i + 1}')
            plt.xlabel(categorical_col)
            plt.ylabel(f'{measure.capitalize()} de {numerical_col}')
            plt.xticks(rotation=45)

            # Mostrar valores en el gráfico
            if show_values:
                for p in ax.patches:
                    ax.annotate(f'{p.get_height():.2f}', (p.get_x() + p.get_width() / 2., p.get_height()),
                                ha='center', va='center', fontsize=10, color='black', xytext=(0, 5),
                                textcoords='offset points')

            # Muestra el gráfico
            plt.show()
    else:
        # Crea el gráfico para menos de group_size categorías
        plt.figure(figsize=(10, 6))
        ax = sns.barplot(x=grouped_data.index, y=grouped_data.values)

        # Añade títulos y etiquetas
        plt.title(f'Relación entre {categorical_col} y {numerical_col}')
        plt.xlabel(categorical_col)
        plt.ylabel(f'{measure.capitalize()} de {numerical_col}')
        plt.xticks(rotation=45)

        # Mostrar valores en el gráfico
        if show_values:
            for p in ax.patches:
                ax.annotate(f'{p.get_height():.2f}', (p.get_x() + p.get_width() / 2., p.get_height()),
                            ha='center', va='center', fontsize=10, color='black', xytext=(0, 5),
                            textcoords='offset points')

        # Muestra el gráfico
        plt.show()


def boxplots_grouped(df, cat_col, num_col, group_size = 5):
    unique_cats = df[cat_col].unique()
    num_cats = len(unique_cats)


    for i in range(0, num_cats, group_size):
        subset_cats = unique_cats[i:i+group_size]
        subset_df = df[df[cat_col].isin(subset_cats)]
        
        plt.figure(figsize=(10, 6))
        sns.boxplot(x=cat_col, y=num_col, data=subset_df)
        plt.title(f'Boxplots of {num_col} for {cat_col} (Group {i//group_size + 1})')
        plt.xticks(rotation=45)
        plt.show()


def plot_histograms_by_categorical_numerical_relationship(df, cat_column, num_column):
    '''
    Generate a grid of histograms to compare a categorical variable with a numerical variable.
    
    Parameters
    -----------
    df : pd.DataFrame
        The input DataFrame containing the data.
        
    cat_column : str
        The name of the categorical column in the DataFrame.
    
    num_column : str
        The name of the numerical column in the DataFrame.
    
    Returns
    --------
    None (displays plots)
    
    Example
    --------
    df = pd.DataFrame({
        'Category': ['A', 'B', 'A', 'C', 'B', 'A', 'C'],
        'Numeric': [10, 15, 8, 12, 9, 11, 13]
    })
    
    plot_histograms_by_categorical_numerical_relationship(df, 'Category', 'Numeric')
    '''
    # Get unique categories in the categorical column
    categories = df[cat_column].unique()
    num_categories = len(categories)
    
    # Calculate number of rows and columns for subplot grid
    num_rows = (num_categories + 2) // 3  # Ensure at least one row
    num_cols = min(num_categories, 3)
    
    # Create a grid of subplots
    fig, axs = plt.subplots(num_rows, num_cols, figsize=(15, 4 * num_rows))
    
    # Flatten the axis array if there's only one row or one column
    if num_rows == 1 and num_cols == 1:
        axs = np.array([axs])
    elif num_rows == 1:
        axs = axs.reshape(1, -1)
    elif num_cols == 1:
        axs = axs.reshape(-1, 1)
    
    # Iterate through each category and plot corresponding histograms
    for i, category in enumerate(categories):
        row = i // num_cols
        col = i % num_cols
        
        # Filter DataFrame rows based on category
        data_subset = df[df[cat_column] == category]
        
        # Plot histogram for the numerical column
        sns.histplot(data=data_subset, x=num_column, ax=axs[row, col])
        axs[row, col].set_title(f'Histogram of {num_column} for {cat_column} = {category}')
        axs[row, col].set_xlabel(num_column)
        axs[row, col].set_ylabel('Frequency')
    
    plt.tight_layout()
    plt.show()


def plot_histograms_grouped(df, cat_col, num_col, group_size = 3):
    """
    Plots grouped histograms for a numerical column based on unique categories from a categorical column.

    This function takes a dataframe and plots histograms of a specified numerical column (`num_col`) 
    for unique categories within a categorical column (`cat_col`). The histograms are grouped, where 
    each group contains a subset of categories, allowing for easier visualization if there are many 
    unique categories.

    Parameters:
    -----------
    df : pandas.DataFrame
        The input dataframe containing the data to be plotted.
    cat_col : str
        The name of the categorical column used to group the data.
    num_col : str
        The name of the numerical column for which the histograms are plotted.
    group_size : int, optional (default=3)
        The number of unique categories to display per group of histograms.

    Returns:
    --------
    None
        Displays the histograms for each group of categories in a series of plots.
    """    
    unique_cats = df[cat_col].unique()
    num_cats = len(unique_cats)

    for i in range(0, num_cats, group_size):
        subset_cats = unique_cats[i:i+group_size]
        subset_df = df[df[cat_col].isin(subset_cats)]
        
        plt.figure(figsize=(10, 6))
        for cat in subset_cats:
            sns.histplot(subset_df[subset_df[cat_col] == cat][num_col], kde=True, label=str(cat))
        
        plt.title(f'Histograms of {num_col} for {cat_col} (Group {i//group_size + 1})')
        plt.xlabel(num_col)
        plt.ylabel('Frequency')
        plt.legend()
        plt.show()


'''
##############################################
#           Dos Variables NUMÉRICAS          #
##############################################
'''


def scatterplot_with_correlation(df, columna_x, columna_y, tamano_puntos=50, mostrar_correlacion=True):
    """
    Crea un diagrama de dispersión entre dos columnas y opcionalmente muestra la correlación.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame que contiene los datos.
        
    columna_x : str
        Nombre de la columna para el eje X.
        
    columna_y : str
        Nombre de la columna para el eje Y.
        
    tamano_puntos : int, opcional
        Tamaño de los puntos en el gráfico. Por defecto es 50.
        
    mostrar_correlacion : bool, opcional
        Si es True, muestra la correlación en el gráfico. Por defecto es False.
    """

    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x=columna_x, y=columna_y, s=tamano_puntos)

    if mostrar_correlacion:
        correlacion = df[[columna_x, columna_y]].corr().iloc[0, 1]
        plt.title(f'Diagrama de Dispersión con Correlación: {correlacion:.2f}')
    else:
        plt.title('Diagrama de Dispersión')

    plt.xlabel(columna_x)
    plt.ylabel(columna_y)
    plt.grid(True)
    plt.show()


'''
###################################################################################################
#                                                                                                 #
#    Análisis MULTIVARIANTE           Análisis MULTIVARIANTE            Análisis MULTIVARIANTE    #
#                                                                                                 #
###################################################################################################
'''
'''
##############################################
#           3 Categorical Variables          #
##############################################
'''

# Función de Alberto. S07, U02, Práctica obligatoria
def plot_tricategorical_analysis(df, direct_cat_col, cat_col1, cat_col2, relative = False, show_values = True):
    '''   
    Example
    -------
    plot_tricategorical_analysis(df_titanic, "class", ["alive","who"])
    '''

    diccionario_multivariante = {}
    for valor in df[direct_cat_col].unique():
        diccionario_multivariante[valor] = df.loc[df[direct_cat_col] == valor,[cat_col2,cat_col1]] 

    for valor,df_datos in diccionario_multivariante.items():
        print(f"Respuesta {valor}:")
        plot_categorical_relationship(df_datos,cat_col2,cat_col1, relative_freq= relative, show_values= show_values)

'''
##############################################
#     2 Numeric, 1 Categorical Variables     #
##############################################
'''

def bubleplot(df, col_x, col_y, col_size, scale = 1000):
    """
    Crea un scatter plot usando dos columnas para los ejes X e Y,
    y una tercera columna para determinar el tamaño de los puntos.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame de pandas.
        
    col_x : str
        Nombre de la columna para el eje X.
        
    col_y : str
        Nombre de la columna para el eje Y.
        
    col_size : str
        Nombre de la columna para determinar el tamaño de los puntos.
    """

    # Asegúrate de que los valores de tamaño sean positivos
    sizes = (df[col_size] - df[col_size].min() + 1)/scale

    plt.scatter(df[col_x], df[col_y], s=sizes)
    plt.xlabel(col_x)
    plt.ylabel(col_y)
    plt.title(f'Burbujas de {col_x} vs {col_y} con Tamaño basado en {col_size}')
    plt.show()


def scatterplot_3variables(df, col_num1, col_num2, col_cat):
    """
    Genera scatter plots superpuestos de dos columnas numéricas, 
    agrupados y coloreados según una columna categórica.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame que contiene los datos.
        
    col_num1 : str
        Nombre de la primera columna numérica para el eje X.
        
    col_num2 : str
        Nombre de la segunda columna numérica para el eje Y.
        
    col_cat : str
        Nombre de la columna categórica para agrupar y colorear los datos.
    """
    # Configuración para mejorar la estética del gráfico
    sns.set(style="whitegrid")

    plt.figure(figsize=(10, 8))

    # Usar seaborn para generar los scatter plots agrupados y coloreados
    sns.scatterplot(x=col_num1, y=col_num2, hue=col_cat, data=df, palette="viridis")

    # Añadir título y etiquetas
    plt.title(f'{col_num1} vs {col_num2} Scatterplot, gruoped by {col_cat}')
    plt.xlabel(col_num1)
    plt.ylabel(col_num2)

    # Mostrar leyenda y gráfico
    plt.legend(title=col_cat)
    plt.show()

    # Uso de la función
    # df es tu DataFrame
    # scatter_plots_agrupados(df, 'nombre_columna_categoria', 'nombre_columna_num1', 'nombre_columna_num2')
    return


'''
##############################################
#                 4 Variables                #
##############################################
'''

def scatterplot(df, num_col1, num_col2, cat_col=None, point_size=50, scale=1, show_legend=True):
    """
    Plots a scatter diagram from `df` of `num_col1` vs `num_col2` using `cat_col` for coloring
    the points, and `point_size * scale` for determining the size of the points. If no `cat_col` is 
    provided, no color parameter is passed to the plotting function.
    `show_legend` doesn't work yet

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing the data.
        
    num_col1 : str
        Name of the numerical column for the X-axis.
        
    num_col2 : str
        Name of the numerical column for the Y-axis.
    
    cat_col : str, optional
        Name of the categorical column for coloring the points. Defaults to None.
    
    point_size : str or float
        Value or column name for the size of the points. Can be a numerical value or a string representing a column name. Default is 50.
    
    scale : float
        Scale factor for the point sizes if `point_size` is a column name. Default is 1.
    
    show_legend : bool
        Whether to show the legend for colors and sizes. Default is True.

    Example
    --------
        # Assume df is a DataFrame with appropriate columns
        df['log_population'] = np.log10(df['population_total'])
        scatterplot(
            df=df,
            num_col1='longitude',
            num_col2='latitude',
            cat_col='log_population',
            point_size='population_total',
            scale=1/10000,
            show_legend=True
        )
    """
    plt.figure(figsize=(10, 6))
    
    # Determine point sizes
    if isinstance(point_size, str):
        sizes = df[point_size] * scale
    else:
        sizes = point_size
    
    # Plot the scatter diagram
    if cat_col:
        scatter = sns.scatterplot(data = df, x = num_col1, y = num_col2,
                                  hue = cat_col, size = sizes, sizes = (20, 200), 
                                  palette = 'viridis', alpha = 0.6, legend = show_legend)
    else:
        scatter = sns.scatterplot(data=df, x=num_col1, y=num_col2, size=sizes, sizes=(20, 200), palette='viridis', alpha=0.6, legend=show_legend)
    
    if show_legend:
        plt.legend()
    else:
        plt.colorbar(scatter, ax=plt.gca(), label=cat_col if cat_col else '')
    
    plt.xlabel(num_col1)
    plt.ylabel(num_col2)
    plt.title(f'Scatter Plot of {num_col1} vs {num_col2}')
    plt.show()
    
    