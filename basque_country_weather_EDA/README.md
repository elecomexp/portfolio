# Basque Country Weather EDA

This project focuses on the Exploratory Data Analysis (EDA) of weather data from the Basque Country in the last century. The main objective is to analyze metereological trends and relationship, particularly focusing on the increase in average temperatures and the frequency of extreme heat-days over the decades.

## Data Source

The data used in this analysis is obtained from the [AEMET OpenData API](https://opendata.aemet.es/), which provides access to a wide range of meteorological data collected by the Spanish Meteorological Agency (AEMET). The dataset includes historical weather records from various meteorological stations.


## Project Structure

The project is organized into the following main directories:

- `/docs`: Contains public presentations and the technical summary report.
- `/src` : Contains the source code and data for the analysis, organized as follows:

  - `/data`: Raw and processed data files.
  - `/img` : Images and figures used or generated during the analysis.
  - `/notebooks`: Jupyter Notebooks used for a first data exploration and analysis. **IMPORTANT:** This scripts may NOT work  properly as they were desingned just for the first studies, and some functions may be deprecated. All useful content is now presented in **get_aemet_data.ipynb** and **main.ipynb**.
  - `/utils`: Utility scripts and functions used in the project.
  - `get_aemet_data.ipynb` : Jupyter Notebook for accessing AEMET API REST data.
  - `main.ipynb` :  The main Jupyter Notebook for running the analysis.
  - `requirements.txt` : List of dependencies required to run the project.
  - `variables_spanish.py` : List of all weather variables contained in datasets (spanish). 

## Summary of the Analysis

- **Introduction**: The project aims to analyze weather data from various meteorological stations in the Basque Country, focusing on temperature and precipitation trends and extreme weather events.
- **Data Collection**: Data is obtained from the AEMET API, covering multiple decades of weather records.
- **Data Processing and Cleaning**: The data is cleaned, and missing values are handled. Stations or variables with insufficient data are filtered out.
- **EDA Techniques**: Various techniques are used to explore the data, including pandas.DataFrame manipulation, time series analysis, weather trend analysis, and visualizations using Seaborn and Matplotlib.
- **Key Findings**: 
  - The average temperature increases by 0.036°C per year in the Basque Country territory.
  - Over the past 50 years, temperatures have risen by approximately 1.8°C.
  - There are 30-40 more extreme-heat days per year compared to 100 years ago.
- **Challenges**: Challenges faced include accessing the data, handling missing data, ensuring data consistency, and visualizing long-term trends.

## Getting Started

1. Clone the repository.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Explore the data collection through the Jupyter Notebook `get_aemet_data.ipynb`.
4. Run `main.ipynb` to execute the complete data analysis.

## Conclusion

This EDA provides insights into the changing weather patterns in the Basque Country, highlighting significant trends in temperature increases and extreme heat events. The analysis serves as a foundation for further studies on climate change impacts in the region.

---

Feel free to explore the directories and files for a detailed understanding of the project and its findings. If you have any questions or suggestions, please feel free to reach out.
