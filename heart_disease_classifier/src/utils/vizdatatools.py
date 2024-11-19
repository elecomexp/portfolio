"""
vizdatatools.py

Author: Lander Combarro Exposito
Created: 2024/07/17
Last Modified: 2024/11/18

Description
-----------
Module for Data Visualization Utilities

This module provides a comprehensive set of visualization functions for univariate, 
bivariate, and multivariate analysis, as well as deep learning image processing. 
The functions cover a range of plot types including categorical, numerical, and 
combinations of both, designed to support various types of data analysis.

Functions
---------
vizdatatools
│
├── univariate_analysis
│   │
│   ├── plot_multiple_categorical_distributions
│   ├── plot_multiple_histograms_KDEs_boxplots
│   ├── violinplot_multiple
│   ├── boxplot_multiple
│   └── lineplot_multiple
│
├── bivariate_analysis
│   │
│   ├── categorical_categorical
│   │   ├── plot_categorical_relationship
│   │   └── plot_absolute_categorical_relationship_and_contingency_table
│   │
│   ├── categorical_numerical
│   │   ├── plot_categorical_numerical_relationship
│   │   ├── boxplots_grouped
│   │   ├── plot_histograms_by_categorical_numerical_relationship
│   │   └── plot_histograms_grouped
│   │
│   └── numerical_numerical
│       └── scatterplot_with_correlation
│
├── multivariate_analysis
│   │
│   ├── three_categorical_variables
│   │   └── plot_tricategorical_analysis
│   │
│   ├── two_numerical_one_categorical
│   │   ├── bubbleplot
│   │   └── scatterplot_3_variables
│   │
│   └── four_variables
│       └── scatterplot
│
└── deep_learning_image_processing
    │
    └── show_images_batch
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

"""
###################################################################################################
#   UNIVARIATE Analysis                UNIVARIATE Analysis                 UNIVARIATE Analysis    #
###################################################################################################
"""


def plot_multiple_categorical_distributions(df, categorical_columns, *, relative=False, show_values=True, rotation=45, palette='viridis') -> None:
    """
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
    """
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


def plot_multiple_histograms_KDEs_boxplots(df, columns, *, kde=True, boxplot=True, whisker_width=1.5, bins=None) -> None:
    """
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
    """
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


def violinplot_multiple(df, numerical_columns) -> None:
    """
    Displays a matrix of violin plots for the specified numerical columns of a DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame containing the data.
        
    numerical_columns : list
        A list of numerical column names.
    """
    num_cols = len(numerical_columns)

    # Configure the figure size
    plt.figure(figsize=(num_cols * 4, 4))

    # Create a violin plot for each numerical column
    for i, col in enumerate(numerical_columns, 1):
        plt.subplot(1, num_cols, i)
        sns.violinplot(y=df[col])
        plt.title(col)

    # Show the matrix of violin plots
    plt.tight_layout()
    plt.show()


def boxplot_multiple(df, columns, plot_per_row=2) -> None:
    """
    Generate a series of boxplots for specified numerical columns in a DataFrame.

    This function displays multiple boxplots for a set of specified columns, 
    organizing them in a grid format to enable easy visual comparison. The grid 
    dimensions are determined by `dim_matriz_visual`, with each row containing 
    up to this many plots.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame containing the data to be plotted.
    columns : list of str
        List of column names to plot. Only columns with numerical data types 
        ('int64' or 'float64') will be plotted.
    plot_per_row : int, optional, default=2
        Number of plots per row in the grid.

    Returns
    -------
    None
        Displays the boxplots as a matplotlib figure but does not return any value.

    Notes
    -----
    - Empty subplots are hidden if the grid is larger than the number of columns.
    - This function is designed for exploratory data analysis, providing a quick 
      way to assess the distribution and presence of outliers in multiple columns.
    """
    num_cols = len(columns)
    num_rows = num_cols // plot_per_row + num_cols % plot_per_row
    fig, axes = plt.subplots(num_rows, plot_per_row, figsize=(12, 6 * num_rows))
    axes = axes.flatten()

    for i, column in enumerate(columns):
        if df[column].dtype in ['int64', 'float64']:
            sns.boxplot(data=df, x=column, ax=axes[i])
            axes[i].set_title(column)

    # Hide empty axes
    for j in range(i + 1, num_rows * plot_per_row):
        axes[j].axis('off')

    plt.tight_layout()
    plt.show()


def lineplot_multiple(df, numerical_serie_columns, *, all_together=False, start_date=None, end_date=None) -> None:
    """
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
    """
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


"""
###################################################################################################
#    BIVARIATE Analysis                 BIVARIATE Analysis                  BIVARIATE Analysis    #
###################################################################################################

##############################################
#          Categorical - Categorical         #
##############################################
"""

def plot_categorical_relationship(df, cat_col1, cat_col2, relative_freq=False, show_values=True, size_group=5):
    """
    Plots the relationship between two categorical variables using bar charts, optionally displaying relative frequencies 
    and grouping categories if one of the variables has many levels.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame containing the data to plot.
    cat_col1 : str
        The name of the first categorical column (x-axis) to analyze.
    cat_col2 : str
        The name of the second categorical column (hue) to analyze.
    relative_freq : bool, optional, default=False
        If True, the function will plot relative frequencies instead of counts.
    show_values : bool, optional, default=True
        If True, the function will display the values on the bars.
    size_group : int, optional, default=5
        Number of unique categories of `cat_col1` to include in each plot if there are many categories.

    Notes
    -----
    - If `cat_col1` has more than `size_group` unique categories, the function splits the data into multiple plots 
      to improve readability.
    - The function automatically adjusts between displaying counts and relative frequencies based on `relative_freq`.

    Returns
    -------
    None
        Displays one or multiple bar plots showing the relationship between `cat_col1` and `cat_col2`.
    """
    # Prepare the data
    count_data = df.groupby([cat_col1, cat_col2]).size().reset_index(name='count')
    total_counts = df[cat_col1].value_counts()
    
    # Convert to relative frequencies if requested
    if relative_freq:
        count_data['count'] = count_data.apply(lambda x: x['count'] / total_counts[x[cat_col1]], axis=1)

    # Split into groups if `cat_col1` has more than `size_group` categories
    unique_categories = df[cat_col1].unique()
    if len(unique_categories) > size_group:
        num_plots = int(np.ceil(len(unique_categories) / size_group))

        for i in range(num_plots):
            # Select a subset of categories for each plot
            categories_subset = unique_categories[i * size_group:(i + 1) * size_group]
            data_subset = count_data[count_data[cat_col1].isin(categories_subset)]

            # Create the plot
            plt.figure(figsize=(10, 6))
            ax = sns.barplot(x=cat_col1, y='count', hue=cat_col2, data=data_subset, order=categories_subset)

            # Add titles and labels
            plt.title(f'Relationship between {cat_col1} and {cat_col2} - Group {i + 1}')
            plt.xlabel(cat_col1)
            plt.ylabel('Relative Frequency' if relative_freq else 'Count')
            plt.xticks(rotation=45)

            # Show values on the bars
            if show_values:
                for p in ax.patches:
                    ax.annotate(f'{p.get_height():.2f}', (p.get_x() + p.get_width() / 2., p.get_height()),
                                ha='center', va='center', fontsize=10, color='black', xytext=(0, size_group),
                                textcoords='offset points')

            # Display the plot
            plt.show()
    else:
        # Create the plot for fewer categories
        plt.figure(figsize=(10, 6))
        ax = sns.barplot(x=cat_col1, y='count', hue=cat_col2, data=count_data)

        # Add titles and labels
        plt.title(f'Relationship between {cat_col1} and {cat_col2}')
        plt.xlabel(cat_col1)
        plt.ylabel('Relative Frequency' if relative_freq else 'Count')
        plt.xticks(rotation=45)

        # Show values on the bars
        if show_values:
            for p in ax.patches:
                ax.annotate(f'{p.get_height():.2f}', (p.get_x() + p.get_width() / 2., p.get_height()),
                            ha='center', va='center', fontsize=10, color='black', xytext=(0, size_group),
                            textcoords='offset points')

        # Display the plot
        plt.show()


def plot_absolute_categorical_relationship_and_contingency_table(df, col1, col2):
    """
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
    """
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


"""
##############################################
#          Categorical - Numerical           #
##############################################
"""

def plot_categorical_numerical_relationship(df, categorical_col, numerical_col, show_values=True, measure='mean', group_size=5):
    """
    Displays a bar plot of the relationship between a categorical column and a numerical column, 
    grouped by a specified measure of central tendency (mean or median). If there are more than 
    a specified number of categories, plots will be divided into multiple groups.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame containing the data.
    
    categorical_col : str
        The name of the categorical column.
    
    numerical_col : str
        The name of the numerical column.
    
    show_values : bool, optional (default=True)
        If True, displays the values on top of each bar in the plot.
    
    measure : str, optional (default='mean')
        The measure of central tendency to use for the plot. Options are 'mean' or 'median'.
    
    group_size : int, optional (default=5)
        The maximum number of categories to display per plot. If the number of categories 
        exceeds this, multiple plots will be created, each containing up to group_size categories.
    """
    # Calculate central tendency measure (mean or median)
    if measure == 'median':
        grouped_data = df.groupby(categorical_col)[numerical_col].median()
    else:
        # Default to mean
        grouped_data = df.groupby(categorical_col)[numerical_col].mean()

    # Sort values
    grouped_data = grouped_data.sort_values(ascending=False)

    # If there are more than group_size categories, split into groups of group_size
    if grouped_data.shape[0] > group_size:
        unique_categories = grouped_data.index.unique()
        num_plots = int(np.ceil(len(unique_categories) / group_size))

        for i in range(num_plots):
            # Select a subset of categories for each plot
            categories_subset = unique_categories[i * group_size:(i + 1) * group_size]
            data_subset = grouped_data.loc[categories_subset]

            # Create the plot
            plt.figure(figsize=(10, 6))
            ax = sns.barplot(x=data_subset.index, y=data_subset.values)

            # Add titles and labels
            plt.title(f'Relationship between {categorical_col} and {numerical_col} - Group {i + 1}')
            plt.xlabel(categorical_col)
            plt.ylabel(f'{measure.capitalize()} of {numerical_col}')
            plt.xticks(rotation=45)

            # Display values on the plot
            if show_values:
                for p in ax.patches:
                    ax.annotate(f'{p.get_height():.2f}', (p.get_x() + p.get_width() / 2., p.get_height()),
                                ha='center', va='center', fontsize=10, color='black', xytext=(0, 5),
                                textcoords='offset points')

            # Show the plot
            plt.show()
    else:
        # Create the plot for fewer than group_size categories
        plt.figure(figsize=(10, 6))
        ax = sns.barplot(x=grouped_data.index, y=grouped_data.values)

        # Add titles and labels
        plt.title(f'Relationship between {categorical_col} and {numerical_col}')
        plt.xlabel(categorical_col)
        plt.ylabel(f'{measure.capitalize()} of {numerical_col}')
        plt.xticks(rotation=45)

        # Display values on the plot
        if show_values:
            for p in ax.patches:
                ax.annotate(f'{p.get_height():.2f}', (p.get_x() + p.get_width() / 2., p.get_height()),
                            ha='center', va='center', fontsize=10, color='black', xytext=(0, 5),
                            textcoords='offset points')

        # Show the plot
        plt.show()


def boxplots_grouped(df, cat_col, num_col, group_size=5):
    """
    Displays grouped boxplots for a numerical column across subsets of a categorical column, 
    divided into groups based on a specified group size.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame containing the data to be plotted.
        
    cat_col : str
        The name of the categorical column used to group the data.
        
    num_col : str
        The name of the numerical column for which the boxplots will be generated.
        
    group_size : int, optional (default=5)
        The maximum number of unique categories to include in each plot. 
        If the number of unique values in the categorical column exceeds this size, 
        multiple boxplots will be created in separate groups.

    Returns
    -------
    None
        This function does not return any value. It displays grouped boxplots.
        
    Notes
    -----
    - This function is useful when the categorical column has many unique values, 
      allowing for visualization in manageable subsets.
    - Each plot will contain up to `group_size` categories, with the total number 
      of plots dependent on the number of unique categories in `cat_col`.
      
    Example
    -------
    >>> boxplots_grouped(df=data, cat_col='Category', num_col='Value', group_size=4)
    This will display boxplots of 'Value' for each subset of 4 unique values in 'Category'.
    """
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
    """ 
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
    """
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


def plot_histograms_grouped(df, cat_col, num_col, group_size=3):
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


"""
##############################################
#           Numerical - Numerical            #
##############################################
"""


def scatterplot_with_correlation(df, x_column, y_column, point_size=50, show_correlation=True):
    """
    Creates a scatter plot between two columns and optionally displays the correlation coefficient.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing the data.
        
    x_column : str
        Name of the column for the X-axis.
        
    y_column : str
        Name of the column for the Y-axis.
        
    point_size : int, optional
        Size of the points in the plot. Default is 50.
        
    show_correlation : bool, optional
        If True, displays the correlation coefficient on the plot. Default is False.
    """

    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x=x_column, y=y_column, s=point_size)

    if show_correlation:
        correlation = df[[x_column, y_column]].corr().iloc[0, 1]
        plt.title(f'Scatter Plot with Correlation: {correlation:.2f}')
    else:
        plt.title('Scatter Plot')

    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.grid(True)
    plt.show()


"""
###################################################################################################
#    MULTIVARIATE Analysis            MULTIVARIATE Analysis             MULTIVARIATE Analysis     #
###################################################################################################

##############################################
#         Three Categorical Variables        #
##############################################
"""

# Alberto Romero Vázquez function. From DS Bootcamp, Sprint 7, Unit 2.
def plot_tricategorical_analysis(df, direct_cat_col, cat_col1, cat_col2, relative=False, show_values=True):
    """ 
    Analyzes and plots the relationship among three categorical variables.

    This function creates a dictionary to separate the DataFrame into subsets based on unique values 
    in the specified `direct_cat_col` column. It then plots the relationship between two other categorical columns 
    (`cat_col1` and `cat_col2`) within each subset.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame containing the data.
        
    direct_cat_col : str
        The main categorical column used to separate the data into subsets.
        
    cat_col1 : str
        The first categorical column to plot within each subset.
        
    cat_col2 : str
        The second categorical column to plot within each subset.
        
    relative : bool, optional
        If True, shows relative frequencies in the plot. Default is False.
        
    show_values : bool, optional
        If True, displays values on the plot. Default is True.

    Example
    -------
    plot_tricategorical_analysis(df_titanic, "class", "alive", "who")
    """
    tricategorical_dict = {}
    for value in df[direct_cat_col].unique():
        tricategorical_dict[value] = df.loc[df[direct_cat_col] == value, [cat_col2, cat_col1]]

    for value, df_subset in tricategorical_dict.items():
        print(f"Category {value}:")
        plot_categorical_relationship(df_subset, cat_col2, cat_col1, relative_freq=relative, show_values=show_values)


"""
##############################################
#  Two Numerical, One Categorical Variables  #
##############################################
"""

def bubbleplot(df, col_x, col_y, col_size, scale=1000):
    """
    Creates a scatter plot using two columns for the X and Y axes, 
    and a third column to determine the size of the points.

    Parameters
    ----------
    df : pd.DataFrame
        Pandas DataFrame containing the data.
        
    col_x : str
        Name of the column for the X-axis.
        
    col_y : str
        Name of the column for the Y-axis.
        
    col_size : str
        Name of the column that determines the size of the points.
        
    scale : int, optional
        Scaling factor to adjust the size of the bubbles. Default is 1000.
    """
    
    # Ensure that size values are positive
    sizes = (df[col_size] - df[col_size].min() + 1) / scale

    plt.scatter(df[col_x], df[col_y], s=sizes)
    plt.xlabel(col_x)
    plt.ylabel(col_y)
    plt.title(f'Bubble Plot of {col_x} vs {col_y} with Size based on {col_size}')
    plt.show()


def scatterplot_3_variables(df, col_num1, col_num2, col_cat):
    """
    Generates scatter plots of two numerical columns, grouped and colored by a categorical column.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing the data.
        
    col_num1 : str
        Name of the first numerical column for the X-axis.
        
    col_num2 : str
        Name of the second numerical column for the Y-axis.
        
    col_cat : str
        Name of the categorical column used to group and color the data.
    """
    # Setting to improve the aesthetics of the plot
    sns.set(style="whitegrid")

    plt.figure(figsize=(10, 8))

    # Using seaborn to generate grouped and colored scatter plots
    sns.scatterplot(x=col_num1, y=col_num2, hue=col_cat, data=df, palette="viridis")

    # Add title and labels
    plt.title(f'{col_num1} vs {col_num2} Scatter Plot, grouped by {col_cat}')
    plt.xlabel(col_num1)
    plt.ylabel(col_num2)

    # Show legend and plot
    plt.legend(title=col_cat)
    plt.show()


"""
##############################################
#               Four Variables               #
##############################################
"""

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
    
 
"""
###################################################################################################
#    DL Image Processing                DL Image Processing                 DL Image Processing   #
###################################################################################################
"""
 
 
def show_images_batch(images, titles=[], n_cols=5, size_scale=2, cmap="Greys"):
    """
    Displays a batch of images in a grid layout using matplotlib.

    Parameters:
    -----------
    images : list or array-like
        A list or array containing image data to be displayed. Each element
        should be an individual image (2D or 3D array depending on the image type).
    
    titles : list, optional (default=[])
        A list of titles for each image. If provided, each image will be displayed
        with its corresponding title. The length of this list should match the
        number of images. If no titles are provided, no titles will be shown.
    
    n_cols : int, optional (default=5)
        The number of columns in the grid. This determines how many images will
        be displayed per row. The total number of rows will be computed automatically.
    
    size_scale : float, optional (default=2)
        Scaling factor for the size of the images. Larger values will increase the
        size of each individual image in the grid.
    
    cmap : str, optional (default='Greys')
        The color map to use when displaying the images. Useful when showing grayscale
        images. You can change it to other colormaps like 'viridis', 'plasma', etc.
    
    Returns:
    --------
    None
        This function displays a plot of the images but does not return any values.

    Examples:
    ---------
    >>> show_images_batch([image1, image2, image3], titles=['Image 1', 'Image 2', 'Image 3'], n_cols=3)
    """
    
    n_rows = (len(images) - 1) // n_cols + 1
    plt.figure(figsize=(n_cols * size_scale, n_rows * 1.1 * size_scale))
    
    for index, image in enumerate(images):
        plt.subplot(n_rows, n_cols, index + 1)
        plt.imshow(image, cmap=cmap)
        plt.axis("off")
        if len(titles):
            plt.title(titles[index])
    plt.show()

    