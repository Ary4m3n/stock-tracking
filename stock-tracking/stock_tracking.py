"""Stock Price Tracking and Analysis Project

This project will provide working functions by which the stock prices for different stocks can be
tracked and analysed by comparing the trendlines with other stocks over a period of time.

To plot the data for one stock call plot_scatter_plot_1stock(time_period: str, stock_name1: str) in
the Python Console, where time period can be 'max', '5_years', '2_years', '1_year', '1_month', or
'15_days'.

To plot the data for two stocks call plot_scatter_plot_2stocks(time_period: str, stock_name1: str)
in the Python Console, where time period can be 'max', '5_years', '2_years', '1_year', '1_month', or
'15_days'.

To plot the data for three stocks call plot_scatter_plot_3stocks(time_period: str, stock_name1: str)
in the Python Console, where time period can be 'max', '5_years', '2_years', '1_year', '1_month', or
'15_days'.

NOTE: the file locations can vary so in order to prevent the program from not working, save the
stock information csv files in the same source folder for the project. Also, the file should be
named in the following format, stock_name + '.csv'. Not all stock data has been added to the file.
In order to add the desired stock data, download the data from "https://finance.yahoo.com/". The
data should be downloaded to the same folder as the stock_tracking.py file. When downloading the
file, set time_period to MAX and the frequency to Daily.

Copyright and Usage Information
===============================

This file is Copyright (c) 2022 Aryaman Sharma.
"""
import datetime
from datetime import date
import plotly.offline as pyo
import plotly.graph_objs as go


###################################################################################################
# Creating a Stock Tracking Class
###################################################################################################
# First we create a stock tracking class named "StockTracking" with an intialiser and a method
# called add_stock_price_info.

class StockTracking:
    """A custom data type that represents the stock price for a specific stock on different days.

    Instance Attributes:
      - stock_name: the name of the specific stock
      - stock_price_close: the closing stock price for a specific stock on a specific date

    Representation Invariants:
      - all(data[1] >= 0 for data in self.stock_price_close)
      - len(stock_name) == 4
    """
    stock_name: str
    stock_price_close: list[tuple[datetime, float]]

    def __init__(self, stock_name: str) -> None:
        """Initialize a new StockTracking object."""
        self.stock_name = stock_name
        self.stock_price_close = []

    def add_stock_price_info(self, stock_close_price: tuple[datetime, float]) -> None:
        """Add the tuple stock_close_price, containing a datetime object and a corresponding stock
        price, to the instance attribute of stock_price_close which is a list of similar tuples.

        Preconditions:
            - all(stock_close_price[0] in dates[0] for dates in self.stock_price_close)
        """
        self.stock_price_close.append(stock_close_price)


###################################################################################################
# Data Processing
###################################################################################################
# Next we move onto extracting and processing data from the csv file. We start with extracting the
# datetime from the file by using the function extract_date.

def extract_date(original_date: str) -> date:
    """Return an extracted datetime.date from original_date.

    NOTE: original_date is in the format (YEAR-MONTH-DATE) which matches the format in the CSV file.

    Preconditions:
        - len(original_date.split('-')[0]) == 4
        - 1 <= int(original_date.split('-')[1]) <= 12
        - 1 <= int(original_date.split('-')[2]) <= 31

    >>> extract_date('2010-06-29')
    datetime.date(2010, 6, 29)
    >>> extract_date('2010-07-09')
    datetime.date(2010, 7, 9)
    """
    # First the original_date which is in the form YEAR-MONTH-DATE is split into 3 parts, which are
    # stored in a list. These parts are the year, month and date respectively.
    lst_of_split_dates = original_date.split('-')
    # As the year is the first element in the list it can be obtained by indexing the list at the
    # first position.
    year = int(lst_of_split_dates[0])
    month_original = lst_of_split_dates[1]
    if month_original[0] == '0':
        month = int(month_original[1])
    else:
        month = int(month_original)
    day_original = lst_of_split_dates[2]
    if day_original[0] == '0':
        day = int(day_original[1])
    else:
        day = int(day_original)
    return date(year, month, day)

# Next we use the function extract_stock_close_price to extract the stock close price from the
# stock data of each line of the csv line.


def extract_stock_close_price(stock_data: str) -> float:
    """Return a list of extracted city_codes from the list of city_data.

    >>> data = '2010-06-29,3.800000,5.000000,3.508000,4.778000,4.778000,93831500'
    >>> extract_stock_close_price(data)
    4.778
    """
    return float(stock_data.split(',')[4])

# Next, we use the function add_city_stock_data to return a dictionary of the stock name to the
# respective StockTracking class which contains all the data of the stock close price to its
# respective datetime.


def add_city_stock_data(stock_name: str, stock_data: list[str]) -> dict[str, StockTracking]:
    """Return a dictionary mapping the stock_name to the StockTracking object for a specific stock.

    stock_data is a list of str from the csv data file.
    """
    dict_so_far = {}
    stock = StockTracking(stock_name)
    for i in range(len(stock_data)):
        day = extract_date(stock_data[i].split(',')[0])
        stock_close_price = extract_stock_close_price(stock_data[i])
        stock.add_stock_price_info((day, stock_close_price))
    dict_so_far[stock_name] = stock
    return dict_so_far


###################################################################################################
# Reading Data
###################################################################################################
# In the final steps, we first read the data in the csv file using the function read_data which
# returns a dictionary of the stock name to the respective StockTracking class containing all the
# data, which is added by using the function add_city_stock_data.

def read_data(stock_name: str, filename: str) -> dict[str, StockTracking]:
    """Return an organised dictionary mapping city to the respective RTLBCIData object when the
    filename is called in the function.
    """
    with open(filename, 'r', encoding='utf-8') as file:
        stock_data = file.readlines()

    return add_city_stock_data(stock_name, stock_data[1:])


###################################################################################################
# Data Representation as Scatterplot
###################################################################################################
# This final part of the project introduces 3 new functions plot_scatter_plot_1stock,
# plot_scatter_plot_2stocks and plot_scatter_plot_3stocks along with a helper function _extract_data
# which will allow us to finally plot scatterplots with the desired number of stocks and the
# desired time period.

def plot_scatter_plot_1stock(time_period: str, stock_name1: str) -> None:
    """Plot a scatterplot for 1 stock, i.e. stock_name1 over a fixed time_period.

    NOTE: Ensure that there is a corresponding csv file for stock_name1 in the main folder of the
    project. In case there is no existent csv file in the folder, follow the instruction in the main
    description of the project to download the csv file from "https://finance.yahoo.com/".

    Preconditions:
        - time_period == any('max', '5_years', '2_years', '1_year', '1_month', '15_days')
    """
    extracted_data1 = _extract_data(stock_name1)

    x_stock1, y_stock1 = ([], [])

    if time_period == 'max':
        x_stock1, y_stock1 = extracted_data1
    elif time_period == '5_years':
        x_stock1, y_stock1 = extracted_data1[0][len(extracted_data1) - (365 * 5):], \
                             extracted_data1[1][len(extracted_data1) - (365 * 5):]
    elif time_period == '4_years':
        x_stock1, y_stock1 = extracted_data1[0][len(extracted_data1) - (365 * 4):], \
                             extracted_data1[1][len(extracted_data1) - (365 * 4):]
    elif time_period == '3_years':
        x_stock1, y_stock1 = extracted_data1[0][len(extracted_data1) - (365 * 3):], \
                             extracted_data1[1][len(extracted_data1) - (365 * 3):]
    elif time_period == '2_years':
        x_stock1, y_stock1 = extracted_data1[0][len(extracted_data1) - (365 * 2):], \
                             extracted_data1[1][len(extracted_data1) - (365 * 2):]
    elif time_period == '1_year':
        x_stock1, y_stock1 = extracted_data1[0][len(extracted_data1) - 365:], \
                             extracted_data1[1][len(extracted_data1) - 365:]
    elif time_period == '1_month':
        x_stock1, y_stock1 = extracted_data1[0][len(extracted_data1) - 30:], \
                             extracted_data1[1][len(extracted_data1) - 30:]
    elif time_period == '15_days':
        x_stock1, y_stock1 = extracted_data1[0][len(extracted_data1) - 15:], \
                             extracted_data1[1][len(extracted_data1) - 15:]

    line_stock1 = go.Scatter(
        x=x_stock1,
        y=y_stock1,
        mode='lines',
        name=stock_name1
    )

    layout_stocks = go.Layout(
        title='Stock Close Price vs Time',
        xaxis=dict(title='Time', autorange=True),
        yaxis=dict(title='USD $', autorange=True)
    )

    figure = go.Figure(data=[line_stock1], layout=layout_stocks)

    pyo.plot(figure)


def plot_scatter_plot_2stocks(time_period: str, stock_name1: str, stock_name2: str) -> None:
    """Plot a scatterplot for 2 stocks, i.e. stock_name1 and stock_name2 over a fixed time_period.
    This scatterplot will show a direct comparison of the performance of the stocks over the
    time_period on the same set of axes for better analysis.

    NOTE: Ensure that there is a corresponding csv file for stock_name1 and stock_name2 in the main
    folder of the project. In case there is no existent csv file in the folder, follow the
    instructions in the main description of the project to download the csv file from
    "https://finance.yahoo.com/".

    Preconditions:
        - time_period == any('max', '5_years', '2_years', '1_year', '1_month', '15_days')
    """
    extracted_data1 = _extract_data(stock_name1)
    extracted_data2 = _extract_data(stock_name2)

    x_stock1, y_stock1 = ([], [])
    x_stock2, y_stock2 = ([], [])

    if time_period == 'max':
        x_stock1, y_stock1 = extracted_data1
        x_stock2, y_stock2 = extracted_data2
    elif time_period == '5_years':
        x_stock1, y_stock1 = extracted_data1[0][len(extracted_data1) - (365*5):], \
                             extracted_data1[1][len(extracted_data1) - (365 * 5):]
        x_stock2, y_stock2 = extracted_data2[0][len(extracted_data2) - (365 * 5):], \
                             extracted_data2[1][len(extracted_data2) - (365 * 5):]
    elif time_period == '4_years':
        x_stock1, y_stock1 = extracted_data1[0][len(extracted_data1) - (365 * 4):], \
                             extracted_data1[1][len(extracted_data1) - (365 * 4):]
        x_stock2, y_stock2 = extracted_data2[0][len(extracted_data2) - (365 * 4):], \
                             extracted_data2[1][len(extracted_data2) - (365 * 4):]
    elif time_period == '3_years':
        x_stock1, y_stock1 = extracted_data1[0][len(extracted_data1) - (365 * 3):], \
                             extracted_data1[1][len(extracted_data1) - (365 * 3):]
        x_stock2, y_stock2 = extracted_data2[0][len(extracted_data2) - (365 * 3):], \
                             extracted_data2[1][len(extracted_data2) - (365 * 3):]
    elif time_period == '2_years':
        x_stock1, y_stock1 = extracted_data1[0][len(extracted_data1) - (365 * 2):], \
                             extracted_data1[1][len(extracted_data1) - (365 * 2):]
        x_stock2, y_stock2 = extracted_data2[0][len(extracted_data2) - (365 * 2):], \
                             extracted_data2[1][len(extracted_data2) - (365 * 2):]
    elif time_period == '1_year':
        x_stock1, y_stock1 = extracted_data1[0][len(extracted_data1) - 365:], \
                             extracted_data1[1][len(extracted_data1) - 365:]
        x_stock2, y_stock2 = extracted_data2[0][len(extracted_data2) - 365:], \
                             extracted_data2[1][len(extracted_data2) - 365:]
    elif time_period == '1_month':
        x_stock1, y_stock1 = extracted_data1[0][len(extracted_data1) - 30:], \
                             extracted_data1[1][len(extracted_data1) - 30:]
        x_stock2, y_stock2 = extracted_data2[0][len(extracted_data2) - 30:], \
                             extracted_data2[1][len(extracted_data2) - 30:]
    elif time_period == '15_days':
        x_stock1, y_stock1 = extracted_data1[0][len(extracted_data1) - 15:], \
                             extracted_data1[1][len(extracted_data1) - 15:]
        x_stock2, y_stock2 = extracted_data2[0][len(extracted_data2) - 15:], \
                             extracted_data2[1][len(extracted_data2) - 15:]

    line_stock1 = go.Scatter(
        x=x_stock1,
        y=y_stock1,
        mode='lines',
        name=stock_name1
    )

    line_stock2 = go.Scatter(
        x=x_stock2,
        y=y_stock2,
        mode='lines',
        name=stock_name2
    )

    layout_stocks = go.Layout(
        title='Stock Close Price vs Time',
        xaxis=dict(title='Time', autorange=True),
        yaxis=dict(title='USD $', autorange=True)
    )

    figure = go.Figure(data=[line_stock1, line_stock2], layout=layout_stocks)

    pyo.plot(figure)


def plot_scatter_plot_3stocks(time_period: str, stock_name1: str, stock_name2: str,
                              stock_name3: str) -> None:
    """Plot a scatterplot for 3 stocks, i.e. stock_name1, stock_name2 and stock_name3 over a fixed
    time_period. This scatterplot will show a direct comparison of the performance of the 3 stocks
    over the time_period on the same set of axes for better analysis.

    NOTE: Ensure that there is a corresponding csv file for stock_name1, stock_name2 and stock_name3
    in the main folder of the project. In case there is no existent csv file in the folder, follow
    the instructions in the main description of the project to download the csv file from
    "https://finance.yahoo.com/".

    Preconditions:
        - time_period == any('max', '5_years', '2_years', '1_year', '1_month', '15_days')
    """
    extracted_data1 = _extract_data(stock_name1)
    extracted_data2 = _extract_data(stock_name2)
    extracted_data3 = _extract_data(stock_name3)

    x_stock1, y_stock1 = ([], [])
    x_stock2, y_stock2 = ([], [])
    x_stock3, y_stock3 = ([], [])

    if time_period == 'max':
        x_stock1, y_stock1 = extracted_data1
        x_stock2, y_stock2 = extracted_data2
        x_stock3, y_stock3 = extracted_data3
    elif time_period == '5_years':
        x_stock1, y_stock1 = extracted_data1[0][len(extracted_data1) - (365 * 5):], \
                             extracted_data1[1][len(extracted_data1) - (365 * 5):]
        x_stock2, y_stock2 = extracted_data2[0][len(extracted_data2) - (365 * 5):], \
                             extracted_data2[1][len(extracted_data2) - (365 * 5):]
        x_stock3, y_stock3 = extracted_data3[0][len(extracted_data3) - (365 * 5):], \
                             extracted_data3[1][len(extracted_data3) - (365 * 5):]
    elif time_period == '4_years':
        x_stock1, y_stock1 = extracted_data1[0][len(extracted_data1) - (365 * 4):], \
                             extracted_data1[1][len(extracted_data1) - (365 * 4):]
        x_stock2, y_stock2 = extracted_data2[0][len(extracted_data2) - (365 * 4):], \
                             extracted_data2[1][len(extracted_data2) - (365 * 4):]
        x_stock3, y_stock3 = extracted_data3[0][len(extracted_data3) - (365 * 4):], \
                             extracted_data3[1][len(extracted_data3) - (365 * 4):]
    elif time_period == '3_years':
        x_stock1, y_stock1 = extracted_data1[0][len(extracted_data1) - (365 * 3):], \
                             extracted_data1[1][len(extracted_data1) - (365 * 3):]
        x_stock2, y_stock2 = extracted_data2[0][len(extracted_data2) - (365 * 3):], \
                             extracted_data2[1][len(extracted_data2) - (365 * 3):]
        x_stock3, y_stock3 = extracted_data3[0][len(extracted_data3) - (365 * 3):], \
                             extracted_data3[1][len(extracted_data3) - (365 * 3):]
    elif time_period == '2_years':
        x_stock1, y_stock1 = extracted_data1[0][len(extracted_data1) - (365 * 2):], \
                             extracted_data1[1][len(extracted_data1) - (365 * 2):]
        x_stock2, y_stock2 = extracted_data2[0][len(extracted_data2) - (365 * 2):], \
                             extracted_data2[1][len(extracted_data2) - (365 * 2):]
        x_stock3, y_stock3 = extracted_data3[0][len(extracted_data3) - (365 * 2):], \
                             extracted_data3[1][len(extracted_data3) - (365 * 2):]
    elif time_period == '1_year':
        x_stock1, y_stock1 = extracted_data1[0][len(extracted_data1) - 365:], \
                             extracted_data1[1][len(extracted_data1) - 365:]
        x_stock2, y_stock2 = extracted_data2[0][len(extracted_data2) - 365:], \
                             extracted_data2[1][len(extracted_data2) - 365:]
        x_stock3, y_stock3 = extracted_data3[0][len(extracted_data3) - 365:], \
                             extracted_data3[1][len(extracted_data3) - 365:]
    elif time_period == '1_month':
        x_stock1, y_stock1 = extracted_data1[0][len(extracted_data1) - 30:], \
                             extracted_data1[1][len(extracted_data1) - 30:]
        x_stock2, y_stock2 = extracted_data2[0][len(extracted_data2) - 30:], \
                             extracted_data2[1][len(extracted_data2) - 30:]
        x_stock3, y_stock3 = extracted_data3[0][len(extracted_data3) - 30:], \
                             extracted_data3[1][len(extracted_data3) - 30:]
    elif time_period == '15_days':
        x_stock1, y_stock1 = extracted_data1[0][len(extracted_data1) - 15:], \
                             extracted_data1[1][len(extracted_data1) - 15:]
        x_stock2, y_stock2 = extracted_data2[0][len(extracted_data2) - 15:], \
                             extracted_data2[1][len(extracted_data2) - 15:]
        x_stock3, y_stock3 = extracted_data3[0][len(extracted_data3) - 15:], \
                             extracted_data3[1][len(extracted_data3) - 15:]

    line_stock1 = go.Scatter(
        x=x_stock1,
        y=y_stock1,
        mode='lines',
        name=stock_name1
    )

    line_stock2 = go.Scatter(
        x=x_stock2,
        y=y_stock2,
        mode='lines',
        name=stock_name2
    )

    line_stock3 = go.Scatter(
        x=x_stock3,
        y=y_stock3,
        mode='lines',
        name=stock_name3
    )

    layout_stocks = go.Layout(
        title='Stock Close Price vs Time',
        xaxis=dict(title='Time', autorange=True),
        yaxis=dict(title='USD $', autorange=True)
    )

    figure = go.Figure(data=[line_stock1, line_stock2, line_stock3], layout=layout_stocks)

    pyo.plot(figure)


def _extract_data(stock_name: str) -> tuple[list[datetime], list[float]]:
    """Return a tuple containing two lists, first containing all the dates in the data for the
    specific stock_name and the second list containing the corresponding stock close price values.
    """
    file = stock_name + '.csv'
    data = read_data(stock_name, file)
    lst_of_day = []
    lst_of_stock_price = []

    stock_data = data[stock_name]
    for i in range(len(stock_data.stock_price_close)):
        day = stock_data.stock_price_close[i][0]
        stock_close_price = stock_data.stock_price_close[i][1]
        lst_of_day.append(day)
        lst_of_stock_price.append(stock_close_price)

    return (lst_of_day, lst_of_stock_price)
