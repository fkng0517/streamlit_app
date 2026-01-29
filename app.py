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

        # 件数折れ線グラフ
        st.subheader('1. 年度別の推移')
        
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(['2023', '2024'], [pref_data['23年件数'], pref_data['24年件数']], marker='o', color='blue')
        
        ax.set_ylabel('Cases') 
        ax.set_title('Year')
        
        st.pyplot(fig)

    # 増減率棒グラフ
    st.subheader('2. 選択した地域の増減比較')

    pref_map = {
    '札幌方面': 'Sapporo', '函館方面': 'Hakodate', '旭川方面': 'Asahikawa', '釧路方面': 'Kushiro', '北見方面': 'Kitami', '青森県': 'Aomori', '岩手県': 'Iwate', '宮城県': 'Miyagi', '秋田県': 'Akita', '山形県': 'Yamagata', '福島県': 'Fukushima',
    '東京都': 'Tokyo', '茨城県': 'Ibaraki', '栃木県': 'Tochigi', '群馬県': 'Gunma', '埼玉県': 'Saitama', '千葉県': 'Chiba', '神奈川県': 'Kanagawa', '新潟県': 'Nigata', '山梨県': 'Yamanashi', '長野県': 'Nagano',
    '静岡県': 'Shizuoka', '富山県': 'Toyama', '石川県': 'Ishikawa', '福井県': 'Fukui',  '岐阜県': 'Gifu', '愛知県': 'Aichi', '三重県': 'Mie',
    '滋賀県': 'Shiga', '京都府': 'Kyoto', '大阪府': 'Osaka', '兵庫県': 'Hyogo', '奈良県': 'Nara', '和歌山県': 'Wakayama',
    '鳥取県': 'Tottori', '島根県': 'Shimane', '岡山県': 'Okayama', '広島県': 'Hiroshima', '山口県': 'Yamaguchi',
    '徳島県': 'Tokushima', '香川県': 'Kagawa', '愛媛県': 'Ehime', '高知県': 'Kochi',
    '福岡県': 'Fukuoka', '佐賀県': 'Saga', '長崎県': 'Nagasaki', '熊本県': 'Kumamoto', '大分県': 'Oita', '宮崎県': 'Miyazaki', '鹿児島県': 'Kagoshima', '沖縄県': 'Okinawa',
    }
    
    filtered_df = filtered_df.copy()
    filtered_df['Pref_En'] = filtered_df['都道府県'].map(pref_map)
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    ax2.bar(filtered_df['Pref_En'], filtered_df['増減率'], color='khaki')
    
    ax2.set_ylabel('Change in cases')
    ax2.set_xlabel('Prefecture')
    plt.xticks(rotation=45) 
    ax2.grid(True, axis='y', linestyle='--') 
    
    st.pyplot(fig2)

with tab2:
    st.header('警戒レベル判定')
    for pref in selected_pref:
        p_data = df[(df['区分'] == selected_crime) & (df['都道府県'] == pref)].iloc[0]
        change = int(p_data['増減率'])

        with st.expander(f"{pref}の判定結果"):
            if change > 0:
                st.error(f"【警戒】{selected_crime}が前年より {change} 件増加しています。")
                st.write("夜間の外出や戸締まりに十分注意してください。")
            elif change < 0:
                st.success(f"【良好】{selected_crime}が前年より {-change} 件減少しています。")
                st.write("治安は改善傾向にありますが、防犯意識は維持しましょう。")
            else:
                st.info(f"【維持】{selected_crime}の発生数は昨年と変わりません。")

