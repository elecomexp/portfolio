"""
functions.py

Author: Lander Combarro Exposito
Created: September 20, 2024
Last Modified: September 20, 2024

Description
-----------
This module provides utility functions for data analysis and feature extraction in datasets related 
to laptops and hardware specifications. The functions cover tasks such as feature extraction from 
GPU, CPU, storage, and screen resolution columns, as well as ensuring submission format compliance 
for Kaggle competitions.
"""

import re
import urllib.request

import numpy as np
import pandas as pd
from PIL import Image


def extract_gpu_features(gpu):
    """
    Extract features from the "Gpu" column, including brand, model, and whether it's an AMD or Intel GPU.
    """
    parts = gpu.split()
    is_amd = 1 if parts[0] == 'AMD' else 0
    is_intel = 1 if parts[0] == 'Intel' else 0
    model = ' '.join(parts[1:])

    return pd.Series([is_amd, is_intel, model], index=['Gpu_isAMD', 'Gpu_isIntel', 'Gpu_Model'])


def extract_cpu_features(cpu):
    """
    Extract features from the "Cpu" column, including brand, series, model, and frequency (GHz).
    """
    parts = cpu.split()
    brand = 1 if parts[0].lower() == 'amd' else 0
    frequency = float(parts[-1].replace('GHz', ''))
    series = ' '.join(parts[1:-2])
    model = parts[-2]
    
    return pd.Series([brand, series, model, frequency], index=['Cpu_isAMD', 'Cpu_Series', 'Cpu_Model', 'Cpu_GHz'])


def extract_screen_features(screen_resolution):
    """
    Extract features from the "ScreenResolution" column, including screen width, height,
    panel type (e.g., IPS), retina display, and touchscreen presence.
    """
    # Initialize values
    width = None
    height = None
    is_ips = 0
    is_retina = 0
    is_touchscreen = 0
    
    # Find width and height
    match = re.search(r'(\d+)x(\d+)', screen_resolution)
    if match:
        width = int(match.group(1))
        height = int(match.group(2))
    
    # Check if it's an IPS Panel
    if 'IPS Panel' in screen_resolution:
        is_ips = 1
    
    # Check if it's a Retina Display
    if 'Retina Display' in screen_resolution:
        is_retina = 1

    # Check if it has Touchscreen
    if 'Touchscreen' in screen_resolution:
        is_touchscreen = 1
    
    return pd.Series([width, height, is_ips, is_retina, is_touchscreen])


def extract_memory_by_type(storage):
    """
    Extract the storage capacities for different types (HDD, SSD, Flash Storage, Hybrid) from the "Storage" column.
    """
    # Initialize a dictionary to store capacities
    capacity_dict = {'HDD_GB': 0, 'SSD_GB': 0, 'Flash_Storage_GB': 0, 'Hybrid_GB': 0}
    
    for part in storage.split('+'):
        part = part.strip()
        # Check and sum capacities for each storage type
        for storage_type in capacity_dict.keys():
            if storage_type.replace('_GB', '').replace('_', ' ') in part:
                gb_match = re.search(r'(\d+)\s*GB', part)
                tb_match = re.search(r'(\d+(\.\d+)?)\s*TB', part)

                if gb_match:
                    capacity_dict[storage_type] += int(gb_match.group(1))  # Extraer valor en GB
                elif tb_match:
                    capacity_dict[storage_type] += int(float(tb_match.group(1)) * 1000)  # Convertir TB a GB

    return pd.Series(capacity_dict)


# Iván Cordero function
def kaggle_checker(df_to_submit, path, sample=pd.read_csv('../data/sample_submission.csv')):
    """
    Esta función se asegura de que tu submission tenga la forma requerida por Kaggle.
    
    Si es así, se guardará el dataframe en un `csv` y estará listo para subir a Kaggle.
    
    Si no, LEE EL MENSAJE Y HAZLE CASO.
    
    Si aún no:
    - apaga tu ordenador, 
    - date una vuelta, 
    - enciendelo otra vez, 
    - abre este notebook y 
    - leelo todo de nuevo. 
    Todos nos merecemos una segunda oportunidad. También tú.
    """
    if df_to_submit.shape == sample.shape:
        if df_to_submit.columns.all() == sample.columns.all():
            if df_to_submit.laptop_ID.all() == sample.laptop_ID.all():
                print("You're ready to submit!")
                df_to_submit.to_csv(path, index=False) #muy importante el index = False
                urllib.request.urlretrieve("https://www.mihaileric.com/static/evaluation-meme-e0a350f278a36346e6d46b139b1d0da0-ed51e.jpg", "../img/gfg.png")     
                img = Image.open("../img/gfg.png")
                img.show()   
            else:
                print("Check the ids and try again")
        else:
            print("Check the names of the columns and try again")
    else:
        print("Check the number of rows and/or columns and try again")
        print("\nMensaje secreto de Iván y Manuel: No me puedo creer que después de todo este notebook hayas hecho algún cambio en las filas de `laptops_test.csv`. Lloramos.")
        
