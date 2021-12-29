import pandas as pd
import streamlit as st
import yfinance as yf
import datetime
import numpy as np
import matplotlib.pyplot as plt
import altair as alt

st.write("""
# Stock Price Visualization
Select a date range and stock below to view the stock's price and volume!
""")

#tickerSymbol = 'GOOGL'

st.sidebar.header('User Input Features: ')
#ask user for date input
today = datetime.date.today()
tomorrow = today + datetime.timedelta(days=1)
start_date = st.sidebar.date_input('Start date: ', today - datetime.timedelta(days=365))
end_date = st.sidebar.date_input('End date: ', tomorrow)
if start_date > end_date:
    st.error('Error: End date must fall after start date.')
#else:
    #st.success('Start date: `%s`\n\nEnd date: `%s`' % (start_date, end_date))
    
option = st.sidebar.selectbox(
  'Which stock would you like to explore?',
 ('Google', 'Apple', 'Amazon', 'Nike', 'Tesla'))
st.write('You selected:', option)

#getting the ticker symbol of the selected stock
ticker_dict = {'Google': 'GOOGL', 'Apple': 'AAPL', 'Amazon': 'AMZN', 'Nike': 'NKE', 'Tesla': 'TSLA'}
tickerSymbol = ticker_dict[option]

#getting data of selected tickerSymbol
tickerData = yf.Ticker(tickerSymbol)

tickerDf = tickerData.history(period='1d', start=start_date, end=end_date)
#Date | Open | High | Low | Close | Volume | Dividends | Stock Splits
print(tickerDf)

#plotting line chart
st.line_chart(tickerDf[['Volume']])

print(tickerDf.describe())

#need to reset the index of tickerDf to create custom plots
stock_data = tickerDf.reset_index()


base = alt.Chart(stock_data).mark_point().encode(
    alt.X('Date', axis=alt.Axis(title=None)),
    tooltip=['Date', 'Open:N', 'Close:N', 'Volume:N']
)

line1 = base.mark_line(color='#57A44C').encode(
    alt.Y('Close',
          axis=alt.Axis(title='Close Price', titleColor='#57A44C'))
)

line2 = base.mark_area(opacity=0.5, stroke='#5276A7', interpolate='monotone').encode(
    alt.Y('Volume',
          axis=alt.Axis(title='Volume', titleColor='#5276A7'))
)

c = alt.layer(line1, line2).resolve_scale(
    y = 'independent'
)
st.altair_chart(c, use_container_width=True)



# chart = alt.Chart(tickerDf[['Date', '']]).mark_line().encode(
#   alt.X('Open'),
#   alt.Y('Close')
# ).properties(title="Hello World")
# st.altair_chart(chart, use_container_width=True)

base2 = alt.Chart(stock_data).mark_point().encode(
    alt.X('Date', axis=alt.Axis(title=None)),
    tooltip=['Date', 'Open:N', 'Close:N']
)

open_price = base.mark_line(color='#57A44C').encode(
    alt.Y('Open',
          axis=alt.Axis(title='Open Price', titleColor='#57A44C'))
)

close_price = base.mark_line(stroke='#5276A7', interpolate='monotone').encode(
    alt.Y('Close',
          axis=alt.Axis(title='Close Price', titleColor='#5276A7'))
)

chart2 = alt.layer(open_price, close_price)
st.altair_chart(chart2, use_container_width=True)