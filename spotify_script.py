import streamlit as st
import pandas as pd
import numpy as np
import matplotlib
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Spotify", page_icon="bar_chart",layout="wide")

st.title("Spotify Dashboard")
st.markdown('<style>div.block-container{padding-top:2rem;}</style>',unsafe_allow_html=True)


df = pd.read_csv("spotify.csv", encoding='latin1')
df = df.drop(columns=['key','in_shazam_charts'], axis=1)
df['streams'] = pd.to_numeric(df['streams'], errors='coerce')
df = df.dropna(subset=['streams'])
df['released_date'] = pd.to_datetime({
    'year': df['released_year'],
    'month': df['released_month'],
    'day': df['released_day']
})
df = df.drop(columns=['released_year','released_month','released_day'])
df = df.loc[~df.duplicated(subset = ['track_name','artist(s)_name'])].reset_index(drop=True).copy()


#Histogram- univariate analysis

def create_histogram(variable):
    fig, ax = plt.subplots(figsize=(15, 5))
    sns.histplot(df[variable], kde=True, ax=ax)

    if variable == 'in_apple_charts':
        ax.set_title('Apple chart distribution')
        ax.set_xlabel('Songs in Apple charts')
    elif variable == 'in_spotify_charts':
        ax.set_title('Spotify chart distribution')
        ax.set_xlabel('Songs in Spotify charts')

    ax.set_ylabel('Frequency')
    plt.tight_layout()
    return fig



st.title("Univariate Analysis")

variables = ['in_apple_charts', 'in_spotify_charts']
selected_variable = st.selectbox("Select a variable:", variables)

if selected_variable:
    fig = create_histogram(selected_variable)
    st.pyplot(fig)


st.title("Heatmap of various features in top 10 songs.")
top_10_songs = df.sort_values(by='streams', ascending=False).head(10)

st.subheader("Select Features for Heatmap")

features_list = ['danceability_%', 'valence_%', 'energy_%',
                 'acousticness_%','instrumentalness_%',
                 'liveness_%', 'speechiness_%']
selected_features = st.multiselect(
    "Choose features",
    options=features_list,
    default=features_list[:4]
)

if len(selected_features) > 0:
    features = top_10_songs[selected_features]
    fig, ax = plt.subplots(figsize=(15, 5))
    sns.heatmap(features.corr(), annot=True, cmap='coolwarm', square=True)
    st.pyplot(fig)
else:
    st.warning("Please select at least one feature.")