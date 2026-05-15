import streamlit as st
import re
import io

# ページ設定
st.set_page_config(
    page_title="YMxT - Script Generator",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# カスタムCSS
st.markdown("""
<style>
    * {
        font-family: 'Segoe UI', 'Hiragino Sans', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        min-height: 100vh;
    }
    
    .header-container {
        text-align: center;
        padding: 40px 20px 30px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        margin-bottom: 30px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    .header-title {
        color: white;
        font-size: 3em;
        font-weight: 800;
        margin: 0;
        letter-spacing: -1px;
    }
    
    .header-subtitle {
        color: rgba(255,255,255,0.9);
        font-size: 1.1em;
        margin-top: 10px;
        font-weight: 300;
    }
    
    .input-section {
        background: white;
        padding: 30px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        margin-bottom: 25px;
    }
    
    .settings-section {
        display: flex;
        gap: 20px;
        margin-bottom: 25px;
        flex-wrap: wrap;
    }
    
    .settings-item {
        flex: 1;
        min-width: 200px;
    }
    
    .button-container {
        display: flex;
        gap: 15px;
        margin-top: 25px;
        justify-content: center;
    }
    
    .button-generate {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 12px 40px;
        border-radius: 8px;
        border: none;
        font-size: 1.1em;
        font-weight: 600;
        cursor: pointer;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
    }
    
    .button-generate:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    .success-box {
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
        color: #2d5016;
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
        font-weight: 500;
    }
    
    .info-box {
        background: rgba(102, 126, 234, 0.1);
        color: #667eea;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin-top: 30px;
    }
    
    .footer {
        text-align: center;
        margin-top: 40px;
        color: #666;
        font-size: 0.95em;
    }
    
    .stTextArea textarea {
        border-radius: 8px !important;
        border: 2px solid #e0e0e0 !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }
    
    .stTextInput input {
        border-radius: 8px !important;
        border: 2px solid #e0e0e0 !important;
    }
    
    .stTextInput input:focus {
        border-color: #667eea !important;
    }
</style>
""", unsafe_allow_html=True)

# ヘッダー
st.markdown("""
<div class="header-container">
    <h1 class="header-title">✨ YMxT</h1>
    <p class="header-subtitle">YMM4 Script Generator - 台本を自動生成</p>
</div>
""", unsafe_allow_html=True)

# メインコンテナ
st.markdown('<div class="input-section">', unsafe_allow_html=True)

st.markdown("### 📝 台本を入力")
input_text = st.text_area(
    "台本テキスト",
    placeholder="ここに台本を貼り付けてください...",
    height=280,
    label_visibility="collapsed"
)

st.markdown("### ⚙️ 設定")
col1, col2, col3 = st.columns([2, 2, 1])

with col1:
    chara_name = st.text_input("キャラクター名", value="霊夢", label_visibility="collapsed")

with col2:
    split_mode = st.toggle("AI推奨：自動分割モード", value=True)

st.markdown('</div>', unsafe_allow_html=True)

# 関数定義
def ai_like_split(text):
    text = text.replace('\n', ' ')
    pattern = r'([^。！？、]{15,30}?[、])|([^。！？]+?[。！？])|([^。！？、]+)'
    result = re.findall(pattern, text)
    
    lines = []
    for r in result:
        line = r[0] or r[1] or r[2]
        if line and line.strip():
            lines.append(line.strip())
    return lines

# ボタン
st.markdown('<div style="text-align: center; margin: 30px 0;">', unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    generate_button = st.button("🚀 生成してダウンロード", use_container_width=True, key="generate")
st.markdown('</div>', unsafe_allow_html=True)

# 処理
if generate_button:
    if not input_text:
        st.error("⚠️ 台本を入力してください")
    else:
        # 分割処理
        if split_mode:
            lines = ai_like_split(input_text)
        else:
            lines = [l.strip() for l in input_text.split('\n') if l.strip()]

        # YMM4形式に整形
        formatted_text = ""
        for line in lines:
            clean_text = re.sub(r'^.*?[:：]', '', line).strip()
            formatted_text += f"{chara_name}「{clean_text}」\n"

        # ダウンロード準備 (UTF-16)
        output = io.BytesIO()
        output.write(formatted_text.encode('utf-16'))
        
        st.markdown(f"""
        <div class="success-box">
            ✅ {len(lines)}個のブロックに分割しました！
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            st.download_button(
                label="📥 ファイルを保存",
                data=output.getvalue(),
                file_name="ymm4_script.txt",
                mime="text/plain",
                use_container_width=True
            )

# フッター情報
st.markdown("""
<div class="info-box">
    <strong>💡 使い方：</strong><br>
    生成されたファイルをYMM4の <code>[ファイル] > [台本読み込み]</code> から開いてください。
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="footer">
    <p>YMxT v1.0 | YMM4 Script Generator</p>
</div>
""", unsafe_allow_html=True)
