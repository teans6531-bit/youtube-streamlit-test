import streamlit as st
import numpy as np

st.set_page_config(page_title="迷路ゲーム", layout="centered")
st.title("🕹️ Streamlit迷路ゲーム（ボタン操作）")

# --- 迷路定義 ---
maze = np.array([
    [1,1,1,1,1,1,1],
    [1,0,0,0,1,0,1],
    [1,0,1,0,1,0,1],
    [1,0,1,0,0,0,1],
    [1,0,1,1,1,0,1],
    [1,0,0,0,0,2,1],
    [1,1,1,1,1,1,1],
])

# --- 状態保持 ---
if "player_pos" not in st.session_state:
    st.session_state.player_pos = [1, 1]

x, y = st.session_state.player_pos

# --- プレイヤー移動処理 ---
def move(dx, dy):
    new_x, new_y = x + dx, y + dy
    if maze[new_x, new_y] != 1:
        st.session_state.player_pos = [new_x, new_y]

# --- 迷路描画 ---
display = maze.copy()
px, py = st.session_state.player_pos
display[px, py] = 9

emoji = {0: "⬜️", 1: "⬛️", 2: "🏁", 9: "😀"}
maze_html = "<br>".join("".join(emoji[c] for c in row) for row in display)

st.markdown(
    f"""
    <div style="
        display:flex;
        justify-content:center;
        align-items:center;
        border:3px solid #666;
        width:260px;
        height:260px;
        margin:auto;
        background-color:#111;
        border-radius:10px;
        font-size:24px;
        font-family:monospace;
        line-height:1.1;
        color:white;
        text-align:center;
    ">
        <div>{maze_html}</div>
    </div>
    """,
    unsafe_allow_html=True
)

# --- ボタンUI（中央揃え＋スペース追加） ---
st.markdown("### 🎮 操作ボタン")

# ↑ボタン
col_center = st.columns([1, 1, 1, 1, 1])
with col_center[2]:
    if st.button("⬆️", use_container_width=True):
        move(-1, 0)

# ← → ボタン（間を広げた）
col_lr = st.columns([2, 1, 0.5, 1, 2])  # ←この「0.5」で間が広がる！
with col_lr[1]:
    if st.button("⬅️", use_container_width=True):
        move(0, -1)
with col_lr[3]:
    if st.button("➡️", use_container_width=True):
        move(0, 1)

# ↓ボタン
col_down = st.columns([1, 1, 1, 1, 1])
with col_down[2]:
    if st.button("⬇️", use_container_width=True):
        move(1, 0)

# --- ゴール判定 ---
if maze[px, py] == 2:
    st.success("🎉 ゴールしました！")
    if st.button("もう一度"):
        st.session_state.player_pos = [1, 1]
        st.rerun()


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
