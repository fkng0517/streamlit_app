import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

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

# メイン
st.title('防犯・安全レベル判定')
st.write('犯罪の統計データをもとに、地域の警戒レベルを可視化します')

filtered_df = df[(df['区分'] == selected_crime) & (df['都道府県'].isin(selected_pref))]

tab1, tab2 = st.tabs(['統計データ', 'アドバイス'])

with tab1:
    st.header(f'{selected_crime}の発生状況')

    for pref in selected_pref:
        # その都道府県のデータだけを抜き出す
        pref_data = df[(df['区分'] == selected_crime) & (df['都道府県'] == pref)].iloc[0]
        
        # 見やすくするために都道府県ごとに境界線を引く
        st.write(f"### {pref}")
        
        
        c1, c2, c3 = st.columns(3)
        c1.metric("2024年件数", f"{pref_data['24年件数']} 件")
        c2.metric("2023年件数", f"{pref_data['23年件数']} 件")
        
        # 増減を計算（deltaに件数差を入れる）
        delta_val = int(pref_data['24年件数']) - int(pref_data['23年件数'])
        # delta_color="inverse" をつけると「増えると赤」になる
        c3.metric("前年比", f"{delta_val} 件", delta=delta_val, delta_color="inverse")
        
        st.divider()


