import pandas as pd
import streamlit as st

df = pd.read_csv("crime_data.csv")

# サイドバー
st.sidebar.header('🔎検索条件')

# 種別選択
crime_list = df['区分'].unique()
selected_crime = st.sidebar.selectbox('犯罪種別を選択してください', crime_list)

# 都道府県選択
pref_list = df['都道府県'].unique()
selected_pref = st.sidebar.multiselect('比較する都道府県・方面を選択してください,',
                                       pref_list,
                                       default=['東京都', '大阪府'])
