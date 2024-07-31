'''
Author: Lander Combarro Exposito
Date: 2024-07-30

Module Functions
----------------
- show_AWS_info
- scatterplot_with_background
- fetch_data_aemet
- convert_coordinate
'''

import re
import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import requests


def show_AWS_info(df):
    '''
    Display information about each Automated Weather Station (AWS) in the DataFrame.

    This function iterates over the unique 'idema' values in the provided DataFrame and prints
    the idema, location name, and the service time (i.e., the range of dates for which data is available)
    for each AWS.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame containing AWS data. It is expected to have at least the following columns:
        - 'idema': A unique identifier for each AWS.
        - 'nombre': The name of the AWS location.
        - 'fecha': The dates for which data is available, in a datetime format.

    Returns
    -------
    None
        This function does not return any value. It only prints information to the console.
    '''
    for idema in df['idema'].unique():   
        AWS_name = df[df['idema'] == idema]['nombre'].unique()[0]
        min_date = df[df['idema'] == idema]['fecha'].min().strftime('%Y-%m')
        max_date = df[df['idema'] == idema]['fecha'].max().strftime('%Y-%m')
        print(f'{idema} : {AWS_name} --> Data from {min_date} to {max_date}.')   


def scatterplot_with_background(df, x, y, hue, size, image, year):
    """
    Create a scatter plot with a background image and annotate points with station names.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing the data to be plotted.
        
    x : str
        Name of the column in df to be used for the x-axis.
        
    y : str
        Name of the column in df to be used for the y-axis.
        
    hue : str
        Name of the column in df to be used for color coding the points.
        
    size : str
        Name of the column in df to be used for sizing the points.
        
    image : str or array-like
        Path to the background image or array representing the image to be displayed.
        
    year : int
        Year for which the data is being plotted. Used in the title of the plot.

    Returns
    -------
    None
        This function displays a scatter plot with a background image and annotations.
    """
    fig, ax = plt.subplots(figsize=(9, 7))

    # Add the background image, adjusting the values according to the data
    extent = [-3.55, -1.55, 42.47, 43.47]
    ax.imshow(image, extent=extent, aspect='auto', alpha=0.3)

    scatter = sns.scatterplot(data=df, x=x, y=y, hue=hue, size=size,
                            sizes=(20, 200), palette='viridis', alpha=0.6, legend=True, ax = ax)

    # Add station names as annotations, centered and above the points
    for i in range(df.shape[0]):
        ax.annotate(df.iloc[i]['nombre'], (df.iloc[i][x], df.iloc[i][y]), fontsize=8,
                    ha='center', va='bottom')

    ax.set_xlim([-3.55, -1.5])
    ax.set_ylim([42.45, 43.55])
    
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    ax.set_title(f'Year: {str(year)}')

    plt.show()


def fetch_data_aemet(url, headers, querystring, retries = 3, wait_time = 65):
    """
    Fetch data from the AEMET API with retry logic for rate limiting.

    This function sends a GET request to the specified AEMET API endpoint and handles the response. 
    If the request is rate limited (HTTP 429), it waits for a specified amount of time before 
    retrying. The function will retry the request up to the specified number of retries. If the
    request is successful, the data is returned as a pandas DataFrame.

    Parameters
    ----------
    url : str
        The URL of the AEMET API endpoint. 
        
    headers : dict
        A dictionary of HTTP headers to send with the request.
        
    querystring : dict      
        A dictionary of query parameters to send with the request.
        
    retries : int, optional     
        The number of times to retry the request if rate limited. Default is 3.
        
    wait_time : int, optional       
        The number of seconds to wait before retrying if rate limited. Default is 70.

    Returns
    -------
    pd.DataFrame : A pandas DataFrame containing the response data if the request is successful.

    Raises
    ------
    requests.exceptions.HTTPError : If an HTTP error other than rate limiting occurs.
    
    KeyError : If the 'datos' key is not found in the JSON response.
    """
    for attempt in range(retries):
        try:
            response = requests.request("GET", url, headers=headers, params=querystring)
            response.raise_for_status()  # Raise an exception for HTTP errors 4xx/5xx
            print('Request Status Code: ', response.status_code)
            # print('Request Info: ', response.json())
        
            response = requests.get(response.json()['datos'])
            print('Data Accessing Status code: ', response.status_code)
            # print('Data Info: ', response.json())
            
            return pd.DataFrame(response.json())
            
        except KeyError:
            print('Data Info: ', response.json())
            break
        
        except requests.exceptions.HTTPError as http_err:
            if response.status_code == 429:  # Requests limit exceeded
                print(f'Requests limit exceeded. Waiting {wait_time} seconds before retrying...')
                time.sleep(wait_time) 
            else:
                print(f'Error HTTP: {http_err}')  # Handle other HTTP errors
                break 
    


def convert_coordinate(coord):
    """
    Convert coordinate from string format (with N, S, E, W) to numeric format.

    Parameters
    ----------
    coord : str
        The coordinate in string format with a direction indicator (N, S, E, W).

    Returns
    -------
    float
        The numeric representation of the coordinate.
        
    Example
    -------
    data = [
    {'latitud': '394924N', 'indicativo': 'B013X', 'longitud': '025309E'},
    {'latitud': '394744N', 'indicativo': 'B051A', 'longitud': '024129E'},
    {'latitud': '394121N', 'indicativo': 'B087X', 'longitud': '023046E'},
    {'latitud': '393445N', 'indicativo': 'B103B', 'longitud': '021236E'}
    ]
    
    df = pd.DataFrame(data)
    
    df['latitud'] = df['latitud'].apply(convert_coordinate)
    df['longitud'] = df['longitud'].apply(convert_coordinate)
    """
    match = re.match(r"(\d{2})(\d{2})(\d{2})([NSEW])", coord)
    if match:
        degrees, minutes, seconds, direction = match.groups()
        value = float(degrees) + float(minutes) / 60 + float(seconds) / 3600
        if direction in ['S', 'W']:
            value = -value
        return value
    else:
        raise ValueError(f"Invalid coordinate format: {coord}")



