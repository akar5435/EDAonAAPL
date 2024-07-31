import pandas as pd
import plotly.graph_objects as go
import numpy as np

# Load the dataset
df = pd.read_csv('C:/python/AppleEDA/AAPL.csv', parse_dates=['Date'], index_col='Date')

# Handle missing values (example: forward fill)
df.fillna(method='ffill', inplace=True)

# Ensure the data is sorted by date
df.sort_index(inplace=True)

# Create subsets of the data
df_before_covid = df[(df.index >= '2015-01-01') & (df.index < '2020-03-23')]  # Before the COVID-19 Market Crash
df_after_covid = df[df.index >= '2020-03-23']  # From the COVID-19 Market Crash onward

# List of events with distinct outline markers
events = [
    {'date': '2015-09-09', 'event': 'iPhone 6s Announcement', 'marker': 'circle-open', 'color': 'blue'},
    {'date': '2016-03-21', 'event': 'iPhone SE Announcement', 'marker': 'square-open', 'color': 'purple'},
    {'date': '2017-09-12', 'event': 'iPhone X Announcement', 'marker': 'diamond-open', 'color': 'orange'},
    {'date': '2018-09-12', 'event': 'iPhone XS and XR Announcement', 'marker': 'cross-open', 'color': 'green'},
    {'date': '2018-11-01', 'event': 'Q4 2018 Earnings Report', 'marker': 'x-open', 'color': 'red'},
    {'date': '2019-09-10', 'event': 'iPhone 11 Announcement', 'marker': 'star-open', 'color': 'pink'},
    {'date': '2020-03-23', 'event': 'COVID-19 Market Crash', 'marker': 'triangle-up-open', 'color': 'black'},
    {'date': '2020-09-15', 'event': 'Apple Watch Series 6 Announcement', 'marker': 'triangle-down-open', 'color': 'cyan'},
    {'date': '2020-11-10', 'event': 'M1 Chip Announcement', 'marker': 'hexagon-open', 'color': 'magenta'},
    {'date': '2021-03-23', 'event': 'iPad Pro 2021 Announcement', 'marker': 'octagon-open', 'color': 'brown'},
    {'date': '2021-09-14', 'event': 'iPhone 13 Announcement', 'marker': 'square-open', 'color': 'teal'},
    {'date': '2021-10-26', 'event': 'MacBook Pro 2021 Announcement', 'marker': 'diamond-open', 'color': 'grey'},
    {'date': '2022-03-08', 'event': 'Mac Studio and Studio Display Announcement', 'marker': 'circle-open', 'color': 'darkblue'},
    {'date': '2022-09-07', 'event': 'iPhone 14 Announcement', 'marker': 'star-open', 'color': 'orange'},
    {'date': '2023-09-12', 'event': 'iPhone 15 Announcement', 'marker': 'triangle-up-open', 'color': 'green'}
]

# Convert event dates to datetime
for event in events:
    event['date'] = pd.to_datetime(event['date'])

# Create the combined figure
fig = go.Figure()

# Add trace for data before March 2020
fig.add_trace(go.Scatter(
    x=df_before_covid.index,
    y=df_before_covid['Close'],
    mode='lines',
    name='Close Price up to March 2020',
    line=dict(color='blue')
))

# Add trace for data from March 2020 onward
fig.add_trace(go.Scatter(
    x=df_after_covid.index,
    y=df_after_covid['Close'],
    mode='lines',
    name='Close Price from March 2020 onward',
    line=dict(color='green')
))

# Helper function to adjust marker position
def adjust_position(date, value, offset=0.03, x_offset_days=10):
    # Adjust the position to avoid overlap with the trendline
    x_offset = pd.DateOffset(days=np.random.randint(-x_offset_days, x_offset_days))
    y_offset = np.random.uniform(-offset, offset)
    return date + x_offset, value + y_offset

# Add markers for events with enhanced visuals
for event in events:
    y_value = df.loc[event['date'], 'Close'] if event['date'] in df.index else df['Close'].asof(event['date'])
    x_adjusted, y_adjusted = adjust_position(event['date'], y_value)

    fig.add_trace(go.Scatter(
        x=[x_adjusted],
        y=[y_adjusted],
        mode='markers',
        name=event['event'],
        marker=dict(size=14, color=event['color'], symbol=event['marker'], opacity=0.8, line=dict(width=2, color='black')),
        hovertext=f"{event['event']}<br>Date: {event['date'].strftime('%Y-%m-%d')}<br>Close Price: ${y_value:.2f}",
        hoverinfo='text',
        showlegend=False
    ))

# Add legend entries for events
for event in events:
    fig.add_trace(go.Scatter(
        x=[None],  # Add an invisible trace for the legend entry
        y=[None],
        mode='markers',
        name=event['event'],
        marker=dict(size=14, color=event['color'], symbol=event['marker'], opacity=0.8, line=dict(width=2, color='black')),
        legendgroup=event['event'],
        showlegend=True
    ))

# Update layout with increased size and improved aesthetics
fig.update_layout(
    title='Apple Stock Close Price with Key Events (2015 - Present)',
    xaxis_title='Date',
    yaxis_title='Close Price (in USD)',
    yaxis_tickformat='$,.2f',
    height=800,  # Increase height
    width=1200,  # Increase width
    legend_title='Events',
    legend=dict(
        x=1.05,  # Position legend outside the plot
        y=1,
        traceorder='normal',
        orientation='v'
    ),
    plot_bgcolor='white',  # Set plot background color
    paper_bgcolor='lightgrey',  # Set paper background color
    xaxis=dict(
        gridcolor='lightgrey',
        showgrid=True,
        zeroline=False
    ),
    yaxis=dict(
        gridcolor='lightgrey',
        showgrid=True,
        zeroline=False
    )
)

# Show the figure
fig.show()
