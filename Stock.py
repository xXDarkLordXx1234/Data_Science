import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing=.3)
    stock_data_specific = stock_data[stock_data.Date <= '2021--06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True),
                             y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True),
                             y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
                      height=900,
                      title=stock,
                      xaxis_rangeslider_visible=True)
    fig.show()


# TESLA
tesla = yf.Ticker("TSLA")
tesla_data = tesla.history(period="max")
tesla_data.reset_index(inplace=True)
tesla_url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm"
html_data = requests.get(tesla_url).text
tesla_soup = BeautifulSoup(html_data, 'html5lib')
tesla_revenue = pd.read_html(tesla_url, match="Tesla Quarterly Revenue", flavor='bs4')[0]
col_name = {'Tesla Quarterly Revenue (Millions of US $)': 'Date',
            'Tesla Quarterly Revenue (Millions of US $).1': 'Revenue'}
tesla_revenue.columns = tesla_revenue.columns.str.strip()
tesla_revenue = tesla_revenue.rename(columns=col_name)
tesla_revenue['Revenue'] = tesla_revenue['Revenue'].str.replace(',|\$', "")
# Execute the following lines to remove an null or empty strings in the Revenue column.
tesla_revenue.dropna(inplace=True)
tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]
#

# GME
game = yf.Ticker("GME")
gme_data = game.history(period="max")
gme_data.reset_index(inplace=True)
gme_url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN" \
          "-SkillsNetwork/labs/project/stock.html"
html_data = requests.get(gme_url).text
gme_soup = BeautifulSoup(gme_url, "html5lib")
gme_revenue = pd.read_html(gme_url, match="GameStop Quarterly Revenue", flavor='bs4')[0]
col_name = {'GameStop Quarterly Revenue (Millions of US $)': 'Date',
            'GameStop Quarterly Revenue (Millions of US $).1': 'Revenue'}

gme_revenue = gme_revenue.rename(columns=col_name)
gme_revenue['Revenue'] = gme_revenue['Revenue'].str.replace(',|\$',"")
print(gme_revenue.columns)

#Construction of Graph
make_graph(tesla_data, tesla_revenue, 'Tesla')
make_graph(gme_data,gme_revenue,'GameStop')
