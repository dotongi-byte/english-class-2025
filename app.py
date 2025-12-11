import streamlit as st
from gtts import gTTS
import io

# --- 1. 페이지 설정 및 디자인 ---
st.set_page_config(
    page_title="Breadinator's Eco Class",
    page_icon="🤖",
    layout="wide"
)

# 커스텀 CSS (브레드 이발소 테마 색상 적용)
st.markdown("""
<style>
    .stApp {
        background-color: #FFF8E1; /* 연한 노랑 배경 */
    }
    .main-header {
        font-family: 'Helvetica Neue', sans-serif;
        color: #B45309; /* Amber 700 */
        text-align: center;
        font-weight: 800;
        padding: 20px;
        background-color: white;
        border-radius: 20px;
        border: 3px solid #FCD34D; /* Amber 300 */
        margin-bottom: 20px;
    }
    .character-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        border: 2px solid #FDE68A;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
    }
    .big-emoji {
        font-size: 60px;
    }
    /* 버튼 스타일링 */
    div.stButton > button {
        width: 100%;
        background-color: #F59E0B;
        color: white;
        border-radius: 10px;
        border: none;
        padding: 10px;
        font-weight: bold;
    }
    div.stButton > button:hover {
        background-color: #D97706;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. 데이터 준비 (선생님 HTML 내용 이식) ---
if 'page' not in st.session_state:
    st.session_state.page = 'Intro'

characters = [
    {"name": "Bread", "role": "Master Barber", "desc": "천재 이발사. 무뚝뚝하지만 의리파!", "icon": "🍞"},
    {"name": "Wilk", "role": "The Assistant", "desc": "열정 넘치는 직원. 긍정 에너지 뿜뿜!", "icon": "🥛"},
    {"name": "Choco", "role": "The Cashier", "desc": "시크한 반전 매력의 캐셔.", "icon": "🍫"},
    {"name": "Breadinator", "role": "Future Robot", "desc": "미래에서 온 환경 지킴이 로봇.", "icon": "🤖"}
]

words = [
    {"eng": "environment", "kor": "환경", "icon": "🌍", "ex": "We should save the environment."},
    {"eng": "disposable", "kor": "일회용의", "icon": "🥤", "ex": "Disposable cup should be terminated."},
    {"eng": "reusable", "kor": "재사용 가능한", "icon": "🥛", "ex": "Switch to reusable."},
    {"eng": "harmful", "kor": "해로운", "icon": "☠️", "ex": "Emissions can be very harmful."},
    {"eng": "efficiently", "kor": "효율적으로", "icon": "⚙️", "ex": "Use water more efficiently."},
    {"eng": "separate", "kor": "분리하다", "icon": "♻️", "ex": "Separate your recyclables."},
    {"eng": "electricity", "kor": "전기", "icon": "⚡", "ex": "Save electricity."},
    {"eng": "leftover", "kor": "남은 음식", "icon": "🍱", "ex": "Don't make leftover food."},
    {"eng": "pollution", "kor": "오염", "icon": "🏭", "ex": "Pollution is very serious."},
]

quizzes = [
    {
        "q": "Breadinator sees a disposable cup. What should he do?",
        "options": ["Use it", "Use a reusable cup", "Throw it away"],
        "answer": "Use a reusable cup",
        "tip": "Tip: 'Disposable'은 'Terminated' 되어야 해요!",
        "icon": "🥤"
    },
    {
        "q": "It's only a 3-minute walk. How should we go?",
        "options": ["Take a taxi", "Drive a car", "Walk"],
        "answer": "Walk",
        "tip": "Tip: 가까운 거리는 걷는 게 환경에 좋아요.",
        "icon": "🚶"
    },
    {
        "q": "Air conditioner uses too much energy. Use this instead:",
        "options": ["Fan", "Heater", "Open fridge"],
        "answer": "Fan",
        "tip": "Tip: 선풍기(Fan)가 전기를 덜 써요.",
        "icon": "💨"
    }
]

# --- 3. 기능 함수 (TTS) ---
def play_tts(text):
    """구글 TTS를 이용해 즉석에서 음성을 만들고 재생합니다."""
    try:
        tts = gTTS(text=text, lang='en')
        audio_fp = io.BytesIO()
        tts.write_to_fp(audio_fp)
        st.audio(audio_fp, format='audio/mp3', start_time=0)
    except Exception as e:
        st.error("음성 재생 중 오류가 발생했습니다.")

# --- 4. 사이드바 네비게이션 ---
with st.sidebar:
    st.title("🤖 메뉴")
    selection = st.radio("Go to", ["Intro", "Word Study", "Pattern Drill", "Video", "Quiz"])

# --- 5. 메인 화면 구성 ---

if selection == "Intro":
    st.markdown('<div class="main-header"><h1>Lesson 11. We Should Save the Earth</h1></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbm90eW54M3Y4Z3Y4Z3Y4Z3Y4Z3Y4Z3Y4Z3Y4/3o7TKSjRrfIPjeiVyM/giphy.gif", caption="Save the Earth!") # 환경 관련 움짤 예시
    with col2:
        st.markdown("### 🤖 Breadinator's Eco Class")
        st.info("오늘 에피소드에는 미래에서 온 로봇 **Breadinator**가 등장합니다! 환경 오염으로 파괴된 미래를 막기 위해 과거로 왔어요.")

    st.markdown("---")
    st.markdown("### ✨ Today's Characters")
    
    cols = st.columns(4)
    for idx, char in enumerate(characters):
        with cols[idx]:
            st.markdown(f"""
            <div class="character-card">
                <div class="big-emoji">{char['icon']}</div>
                <h3>{char['name']}</h3>
                <p>{char['role']}</p>
                <small>{char['desc']}</small>
            </div>
            """, unsafe_allow_html=True)

elif selection == "Word Study":
    st.markdown('<div class="main-header"><h2>📚 Word Study</h2></div>', unsafe_allow_html=True)
    
    # 단어 선택
    word_idx = st.slider("단어를 선택하세요", 0, len(words)-1, 0)
    current_word = words[word_idx]

    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown(f'<div style="font-size: 150px; text-align: center;">{current_word["icon"]}</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"# {current_word['eng']}")
        
        # 발음 듣기 버튼
        if st.button("🔊 발음 & 예문 듣기"):
            play_tts(f"{current_word['eng']}. {current_word['ex']}")
            
        with st.expander("의미 확인하기 (Click)", expanded=False):
            st.markdown(f"## {current_word['kor']}")
            st.success(f"Example: {current_word['ex']}")

elif selection == "Pattern Drill":
    st.markdown('<div class="main-header"><h2>🗣️ Pattern Drill</h2></div>', unsafe_allow_html=True)
    
    st.markdown("### 🎬 Scene 1: The Disposable Cup")
    
    col1, col2 = st.columns(2)
    with col1:
        st.warning("Before (문제 상황)")
        st.markdown("**Breadinator:** Disposable cup should be terminated.")
        st.markdown("(일회용 컵은 제거되어야 해.)")
        if st.button("🔊 Listen (Robot)"):
            play_tts("Disposable cup should be terminated.")

    with col2:
        st.success("After (올바른 행동)")
        st.markdown("**Correction:** We should use **reusable cups**.")
        st.markdown("(우리는 재사용 컵을 써야 해요.)")
        if st.button("🔊 Listen (Correct)"):
            play_tts("We should use reusable cups.")
            
    st.divider()
    
    st.markdown("### 🎬 Scene 2: Delivery Food")
    st.markdown("> **Problem:** Too much trash from delivery.")
    
    # 변환 연습
    if st.button("✨ 문장 바꾸기 (Transform!)"):
        st.balloons()
        st.markdown("## 👉 How about cooking homemade meals?")
        play_tts("How about cooking homemade meals?")
    else:
        st.markdown("## 👉 How about __________________?")

elif selection == "Video":
    st.markdown('<div class="main-header"><h2>📺 Video Time</h2></div>', unsafe_allow_html=True)
    # 유튜브 영상 (브레드 이발소 관련 영상이나 환경 관련 영상 링크로 교체 가능)
    st.video("https://www.youtube.com/watch?v=M7lc1UVf-VE") 
    st.info("영상을 보고 나서 퀴즈를 풀어봅시다!")

elif selection == "Quiz":
    st.markdown('<div class="main-header"><h2>🧩 Pop Quiz</h2></div>', unsafe_allow_html=True)
    
    for i, q in enumerate(quizzes):
        st.markdown(f"### Q{i+1}. {q['q']}")
        st.write(f"Situation: {q['icon']}")
        
        answer = st.radio(f"Select answer for Q{i+1}", q['options'], key=f"q{i}")
        
        if st.button(f"Submit Q{i+1}"):
            if answer == q['answer']:
                st.balloons()
                st.success("Ding Dong Dang! Correct!")
                play_tts("Great job!")
            else:
                st.error("Try again!")
                st.info(q['tip'])
        st.divider()
