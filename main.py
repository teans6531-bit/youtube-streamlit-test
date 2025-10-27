import streamlit as st
import numpy as np

st.title("🧱 Streamlit 迷路ゲーム")

# --- セッション状態を利用して位置を記憶 ---
if "player_pos" not in st.session_state:
    st.session_state.player_pos = [1, 1]

# --- 迷路データを定義（1=壁, 0=道, 2=ゴール） ---
maze = np.array([
    [1,1,1,1,1,1,1],
    [1,0,0,0,1,0,1],
    [1,0,1,0,1,0,1],
    [1,0,1,0,0,0,1],
    [1,0,1,1,1,0,1],
    [1,0,0,0,0,2,1],
    [1,1,1,1,1,1,1],
])

# --- プレイヤーの位置取得 ---
x, y = st.session_state.player_pos

# --- 表示用の文字マップを作成 ---
display_maze = maze.copy()
display_maze[x, y] = 9  # 9=プレイヤー

emoji_map = {
    0: "⬜",  # 通路
    1: "⬛",  # 壁
    2: "🏁",  # ゴール
    9: "😀",  # プレイヤー
}

maze_display = "\n".join("".join(emoji_map[cell] for cell in row) for row in display_maze)
st.markdown(f"<pre style='font-size:20px'>{maze_display}</pre>", unsafe_allow_html=True)

# --- 移動ボタン ---
col1, col2, col3 = st.columns(3)
with col2:
    if st.button("⬆️ 上"):
        if maze[x-1, y] != 1:
            st.session_state.player_pos[0] -= 1
with col1:
    if st.button("⬅️ 左"):
        if maze[x, y-1] != 1:
            st.session_state.player_pos[1] -= 1
with col3:
    if st.button("➡️ 右"):
        if maze[x, y+1] != 1:
            st.session_state.player_pos[1] += 1
_, col_down, _ = st.columns(3)
with col_down:
    if st.button("⬇️ 下"):
        if maze[x+1, y] != 1:
            st.session_state.player_pos[0] += 1

# --- ゴール判定 ---
x, y = st.session_state.player_pos
if maze[x, y] == 2:
    st.success("🎉 ゴールしました！！")
    if st.button("もう一度あそぶ"):
        st.session_state.player_pos = [1, 1]



# import streamlit as st
# import time

# st.title("streamlit 入門")

# st.write('プログレスバーの表示')

# 'Start!!'
# latest_iteration = st.empty()
# bar = st.progress(0)

# for i in range(100):
#     latest_iteration.text(f'Iteration {i+1}')
#     bar.progress(i + 1)
#     time.sleep(0.1)

# 'Done!!!'


# left_column, right_column = st.columns(2)
# button = left_column.button('左カラムのボタン')
# if button:
#     right_column.write('右カラムに表示')

# expander = st.expander('問い合わせ')
# expander.write('問い合わせ内容を書く')

# text = st.text_input('あなたの趣味を教えて下さい。',)
# condition = st.slider('あなたの今の調子は？', 0, 100, 50)

# 'あなたの趣味は、', text, 'です。'
# 'コンディション', condition



# if st.checkbox('Show Image'):
#     img = Image.open('okumono_m_zatsu3_68.png')
#     st.image(img, caption='雑談')


# df = pd.DataFrame(
#     np.random.rand(100, 2) / [50, 50] + [35.69, 139.70],
#     columns=['lat', 'lon']
# )

# st.map(df)
# st.line_chart(df)








# df = pd.DataFrame({
#     '1列目': [1, 2, 3, 4],
#     '2列目': [10, 20, 30, 40]
# })

# st.dataframe(df.style.highlight_max(axis=0))

# """
# # 章
# ## 節
# ### 項

# ```python
# import streamlit as st
# import numpy as np
# import pandas as pd
# ```
# """
