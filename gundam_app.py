import streamlit as st
import pandas as pd
import plotly.express as px

st.title("ガンプラ中古価格可視化アプリ")

# データ読み込み（エンコーディング自動判定・エラー出ないようtry）
try:
    df = pd.read_csv('gundam_cleaned.csv', encoding='utf-8')
except UnicodeDecodeError:
    df = pd.read_csv('gundam_cleaned.csv', encoding='shift_jis')

# 列名を表示して動作確認
st.write("データの列名:", df.columns.tolist())

# モデル（機体名）選択
if '商品名' in df.columns:
    models = df['商品名'].unique().tolist()
    model = st.selectbox('モデル（機体名）を選択', ['全て'] + models)
else:
    st.error("商品名 列が見つかりません。csvの表頭を確認してください。")

# 組立状態選択
if '状態' in df.columns:
    status = st.selectbox('組立状態を選択', ['全て', '未組立', '組立済み'])
else:
    st.error("状態 列が見つかりません。csvの表頭を確認してください。")

# 価格列の存在チェック
if '価格' not in df.columns:
    st.error("価格 列が見つかりません。csvの表頭を確認してください。")
else:
    # 絞り込み
    filtered = df.copy()
    if '商品名' in df.columns and model != '全て':
        filtered = filtered[filtered['商品名'] == model]
    if '状態' in df.columns and status != '全て':
        filtered = filtered[filtered['状態'] == status]

    st.write(f"データ件数: {len(filtered)}")
    st.dataframe(filtered)

    # 価格ヒストグラム
    if len(filtered) > 0:
        fig = px.histogram(filtered, x='価格', nbins=20, title='価格分布')
        st.plotly_chart(fig)
    else:
        st.write("表示できるデータがありません。")
