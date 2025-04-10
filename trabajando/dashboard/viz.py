import os
import streamlit as st
import pandas as pd
import requests
import psycopg2
from dotenv import load_dotenv


# Set Streamlit layout
st.set_page_config(layout="wide")

# --- Database Connection ---
@st.cache_resource
def init_connection():
    conn_params = {
        'host': '127.0.0.1',
        'user': 'admin',
        'password': 'root',
        'dbname': 'modulo2',
        'port': 5432
    }
    return psycopg2.connect(**conn_params)

@st.cache_data
def get_data(query):
    with init_connection().cursor() as cur:
        cur.execute(query)
        columns = [desc[0] for desc in cur.description]
        data = cur.fetchall()
        return pd.DataFrame(data, columns=columns)

# --- Data Cleaning ---
def clean_data(df):
    df['date_published'] = df['date_published'].replace('not supported', '17-17-17')
    df['date_published'] = df['date_published'].apply(lambda x: str(x).split('T')[0] if 'T' in str(x) else x)
    df['date_published'] = pd.to_datetime(df['date_published'], errors='coerce')
    df['origin'] = df['origin'].str.strip()
    df['author'] = df['author'].str.strip()
    return df.dropna(subset=['date_published'])

# --- Currency API ---
def fetch_currency():
    params = {
        'included_tags': ['raiden-shogun'],
    }
    url = 'https://api.waifu.im/search'
    response = requests.get(url, params=params)
    # response = requests.get('https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/bob.json')
    if response.status_code == 200:
        data = response.json()
        print('++++++++++++++++++++++++++++++')
        print(data)
        print('++++++++++++++++++++++++++++++')
        images =data['images']

        for image in images:
            print(image)
            return image['url']
        # return data.get('bob', {}).get('1inch', '')
    return ''

# --- Load and Prepare Data ---
query = "SELECT * FROM job_data_refined"
df = clean_data(get_data(query))
# currency_val = fetch_currency()
waifu = fetch_currency()

# --- Header / Metrics ---
with st.container():
    _, main, _ = st.columns([1, 9, 1], vertical_alignment='center', gap='small')

with main:
    with st.container():
        col1, col2, _ = st.columns([1, 6, 0.8], vertical_alignment='center', gap='small')
        col1.markdown(
            f''' <h3>A waifu</h3><br /> <img src='{waifu}' />''',
            unsafe_allow_html=True)
        # col1.metric(label='Waifu', value=currency_val, delta=0.05)

        col2.markdown(
            "<h1 style='text-align: center; font-size: 35px;'>Demo Project Streamlit</h1>"
            f"<h3 style='text-align: center;'>Total Scraped: <span style='color: red'>{len(df)}</span></h3>",
            unsafe_allow_html=True
        )

    # --- Time Series Plot of Top 3 Job Types ---
    with st.container():
        _, col, _ = st.columns([1, 4, 1], vertical_alignment='center', gap='small')

        with col:
            jan_start, april_end = pd.Timestamp('2025-01-01'), pd.Timestamp('2025-04-30')
            df_april = df[(df['date_published'] >= jan_start) & (df['date_published'] <= april_end)]

            top_jobs = (
                df_april.groupby('author')
                .size()
                .sort_values(ascending=False)
                .head(3)
                .index.tolist()
            )

            top_df = df_april[df_april['author'].isin(top_jobs)].copy()
            top_df['month'] = top_df['date_published'].dt.to_period('M')
            monthly_counts = top_df.groupby(['month', 'author']).size().unstack(fill_value=0)
            monthly_counts.index = monthly_counts.index.to_timestamp()

            st.subheader('Top 3 Authors Over Time')
            st.line_chart(monthly_counts, height=500)

    st.markdown("###")

    # --- Left Column: Location Filter + Top Jobs ---
    col3, col4 = st.columns(2, vertical_alignment='top', gap='large')

    with col3:
        locations = sorted(df['origin'].unique().tolist())
        default_idx = locations.index('wired') if 'wired' in locations else 0
        selected_location = st.selectbox("Select a location to analyze:", options=locations, index=default_idx)

        loc_data = df_april[df_april['origin'] == selected_location]
        loc_data = loc_data[loc_data['author'].isin(top_jobs)].copy()

        if not loc_data.empty:
            rate = loc_data.groupby(loc_data['date_published'].dt.date).size().reset_index(name='count')
            rate['pct_change'] = rate['count'].pct_change()

            st.header(f"Publication Rate Change for {selected_location}")
            st.line_chart(rate.dropna(), x='date_published', y='pct_change')
        else:
            st.warning(f"No data available for {selected_location}")

        st.divider()

        st.header("Top 08 Authors Scraped")
        job_freq = df['author'].value_counts().reset_index()
        job_freq.columns = ['author', 'count']
        st.write(job_freq.head(8))

# --- Right Column: Location Frequency + Bernoulli Plot ---
    with col4:
        st.header("Info Frequencies")
        loc_freq = df['origin'].value_counts().reset_index()
        loc_freq.columns = ['origin', 'count']
        st.bar_chart(loc_freq, x='origin', y='count')

        st.divider()
        st.header("Bernoulli Distribution Of wired Over Time")
        df_bern_april = df[(df['date_published'] >= jan_start) & (df['date_published'] <= april_end)].copy()

        df_bern_april['is_santa_cruz'] = df_bern_april['origin'].apply(lambda x: 1 if x == 'wired' else 0)
        bernoulli = df_bern_april.groupby('date_published')['is_santa_cruz'].mean().reset_index(name='probability')
        bernoulli.set_index('date_published', inplace=True)

        st.subheader("Probability of wired Location Over Time")
        st.line_chart(bernoulli)
    


st.markdown("###")
_, col5, _ = st.columns([2,0.7, 2], vertical_alignment='center', gap='small')

with col5:
    st.markdown(
            '''<button style='padding: 10px; margin:8px; border-radius: 5px; background-color: #023047;'><a href='https://thenextweb.com/latest' style='color: #fff; text-decoration: none'>Thenextweb</a></button> 
            <button style='padding: 10px; margin:8px; border-radius: 5px; background-color: #023047;'><a href='https://www.wired.com/category/science/' style='color: #fff; text-decoration: none'>Wired</a></button>
            <button title='Agregaron una restriccion contra bots' style='padding: 10px; margin:8px; border-radius: 5px; background-color: #F44336;'><a href='https://parade.com/' style='color: #fff; text-decoration: none'>Parade</a></button>''',
            unsafe_allow_html=True
        )

