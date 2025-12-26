import streamlit as st
import pandas as pd
import yfinance as yf
import altair as alt

st.set_page_config(page_title="株価表示", layout="wide")


days = st.sidebar.slider("表示する日数を選択", 5, 60, 20)

tickers = {
    'Apple': 'AAPL',
    'Microsoft': 'MSFT',
    'Amazon': 'AMZN',
    'Alphabet': 'GOOGL',
    'Meta': 'META',
}

selected_companies = [
    company for company in tickers.keys()
    if st.sidebar.checkbox(company, True)
]

price_min, price_max = st.sidebar.slider(
    "表示する株価の範囲 (USD)",
    min_value=0,
    max_value=3500,
    value=(0, 500),
    step=5,
    )



def get_data(days, tickers):
    df = pd.DataFrame()
    for company, symbol in tickers.items():
        tkr = yf.Ticker(symbol)
        hist = tkr.history(period="2mo").tail(days)
        hist.index = hist.index.strftime("%Y-%m-%d")
        hist = hist[['Close']]
        hist.columns = [company]
        df = pd.concat([df, hist], axis=1)
    df.index.name = 'Date'
    return df

df = get_data(days, tickers)
data = df.reset_index().melt('Date', var_name='Company', value_name='Closing Price')


filtered_data = data[
    (data['Company'].isin(selected_companies)) &
    (data['Closing Price'].between(price_min, price_max))
]


st.title("株価表示")
st.markdown(
    f"###株価範囲： **${price_min} ～ ${price_max} USD**"
)


chart = (
    alt.Chart(filtered_data)
    .mark_line(point=True)
    .encode(
        x=alt.X('Date:T', title='Date'),
        y=alt.Y(
            'Closing Price:Q',
            title='Closing Price (USD)',
            scale=alt.Scale(domain=[price_min, price_max])
        ),
        color=alt.Color('Company:N', title='Company'),
        tooltip=['Date', 'Company', 'Closing Price']
    )
    .properties(
        title=f'Stock Closing Prices (Last {days} Days)',
        width=800,
        height=400
    )
    .interactive()
)

st.altair_chart(chart, use_container_width=True)
st.dataframe(filtered_data)
