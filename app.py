import pandas as pd
import yfinance as yf
import altair as alt
import streamlit as st


st.title("株価表示")


st.sidebar.header("設定")

# スライダーで日数を選択（5〜60日の範囲）
days = st.sidebar.slider("表示する日数を選択", min_value=5, max_value=60, value=20, step=5)


tickers = {
    'apple': 'AAPL',
    'microsoft': 'MSFT',
    'amazon': 'AMZN',
    'alphabet': 'GOOGL',
    'meta': 'META',
}


st.sidebar.subheader("表示する企業を選択")
selected_companies = [
    company for company in tickers.keys()
    if st.sidebar.checkbox(company.capitalize(), True)
]


@st.cache_data
def get_data(days, tickers):
    df = pd.DataFrame()
    for company, symbol in tickers.items():
        tkr = yf.Ticker(symbol)
        hist = tkr.history(period="3mo").tail(days)
        hist.index = hist.index.strftime("%Y-%m-%d")
        hist = hist[['Close']]
        hist.columns = [company]
        df = pd.concat([df, hist], axis=1)
    df.index.name = 'Date'
    return df



df = get_data(days, tickers)
data = df.reset_index().melt('Date', var_name='Company', value_name='Closing Price')
filtered_data = data[data["Company"].isin(selected_companies)]


chart = (
    alt.Chart(filtered_data)
    .mark_line(point=True)
    .encode(
        x=alt.X('Date:T', title='Date'),
        y=alt.Y('Closing Price:Q', title='Closing Price (USD)'),
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


st.write("データプレビュー")
st.dataframe(filtered_data)
