# CorrEasy

CorrEasy is a simple data analysis tool built with Streamlit that allows users to analyze the correlation between two numerical variables in a CSV dataset. It also provides functionality for filtering data based on date ranges and visualizing scatter plots with regression lines.

## Features

- Upload a CSV file and display the data
- Filter data based on date ranges
- Choose numerical variables for X and Y axis
- Visualize scatter plot with regression line
- Calculate and display the correlation coefficient
- Analyze the strength and direction of the correlation

## Prerequisites

Before running the application, you need to have Python installed and the following libraries:

- Streamlit
- Pandas
- NumPy
- Matplotlib
- Seaborn
- python-dateutil
- Logging

You can install the required libraries using pip:

```bash
pip install streamlit pandas numpy matplotlib seaborn python-dateutil logging
```

## Usage
To run the application, simply navigate to the directory containing the script and execute the following command:

```bash
streamlit run app.py
```

This will start the Streamlit server and open the application in your default web browser.

## License
This project is licensed under the MIT License. See the LICENSE file for more information.
