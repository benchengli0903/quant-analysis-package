# get SP index historical data
def get_hist(ticker, start_date, end_date):
  hist = yf.download(ticker, start_date, end_date)
  hist["Date"] = hist.index
  hist = hist[['Date','Low','High','Open','Adj Close']]
  return hist

# visualize using plotly
import plotly.graph_objs as go
from plotly.subplots import make_subplots

def bollinger_plot(sp_hist, time):

  # find its typical price and compute upper and lower bollinger bound using 50 days

  sp_hist['SMA50'] = sp_hist['Adj Close'].rolling(time).mean()
  sp_hist['UB'] = ((sp_hist['Low'] + sp_hist['High'] + sp_hist['Adj Close'])/3).rolling(time).mean() + 2 * ((sp_hist['Low'] + sp_hist['High'] + sp_hist['Adj Close'])/3).rolling(time).std()
  sp_hist['LB'] = ((sp_hist['Low'] + sp_hist['High'] + sp_hist['Adj Close'])/3).rolling(time).mean() - 2 * ((sp_hist['Low'] + sp_hist['High'] + sp_hist['Adj Close'])/3).rolling(time).std()
  sp_hist['Abs Band'] = (sp_hist['UB'] - sp_hist['LB'])/sp_hist['SMA50']
  sp_hist.dropna(inplace = True)

  # Create a Plotly figure
  fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1)

  # Add the price chart
  fig.add_trace(go.Scatter(x=sp_hist.index, y=sp_hist['Adj Close'], mode='lines', name='Price'), row = 1, col = 1)

  # Add the Upper Bollinger Band (UB) and shade the area
  fig.add_trace(go.Scatter(x=sp_hist.index, y=sp_hist['UB'], mode='lines', name='Upper Bollinger Band', line=dict(color='red')), row = 1, col = 1)
  fig.add_trace(go.Scatter(x=sp_hist.index, y=sp_hist['LB'], fill='tonexty', mode='lines', name='Lower Bollinger Band', line=dict(color='green'), fillcolor = 'rgba(137, 196, 244, 0.3)'), row = 1, col = 1)

  # Add the Middle Bollinger Band (MA)
  fig.add_trace(go.Scatter(x=sp_hist.index, y=sp_hist['SMA50'], mode='lines', name='Middle Bollinger Band', line=dict(color='blue')), row = 1, col = 1)

  # Add the Absolute Bandwidth
  fig.add_trace(go.Scatter(x=sp_hist.index, y=sp_hist['Abs Band'], mode='lines', name = 'Absolute Bandwidth'), row=2, col=1)

  # Customize the chart layout
  fig.update_layout(title='Stock Price with Bollinger Bands',
                    xaxis_title='Date',
                    yaxis_title='Price',
                    showlegend=True)

  # Show the chart
  fig.show()
