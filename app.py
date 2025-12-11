import streamlit as st
from gtts import gTTS
import io
import os

# --- 1. 페이지 설정 및 디자인 ---
st.set_page_config(
    page_title="Why Should I Recycle?",
    page_icon="♻️",
    layout="wide"
)

# 커스텀 CSS (HTML 파일의 스타일을 Streamlit에 이식)
st.markdown("""
<style>
    /* 전체 폰트 및 배경 설정 */
    .stApp {
        background-color: #F0FDF4; /* 연한 에메랄드색 배경 */
    }
    
    /* 윗주(Ruby) 스타일 - 단어 뜻 표시 */
    ruby { ruby-position: over; }
    rt { 
        font-family: 'Gulim', sans-serif; 
        color: #059669; /* Emerald-600 */
        font-size: 0.6em; 
        font-weight: bold;
        transform: translateY(-5px);
    }
    
    /* 활성화된 문장 (읽고 있는 문장) 스타일 */
    .active-line {
        background-color: #FEF3C7; /* 연한 노란색 강조 */
        border-left: 5px solid #F59E0B;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    .active-text {
        font-size: 2.2rem; /* 글자 아주 크게 */
        font-weight: 800;
        color: #111827;
        line-height: 1.6;
        font-family: 'Helvetica', sans-serif;
    }
    .active-trans {
        font-size: 1.4rem;
        color: #047857;
        margin-top: 10px;
        font-weight: 600;
    }

    /* 비활성화된 문장 스타일 */
    .inactive-line {
        padding: 10px 20px;
        margin-bottom: 10px;
        opacity: 0.6; /* 흐리게 처리 */
        border-left: 5px solid transparent;
    }
    .inactive-text {
        font-size: 1.2rem;
        color: #4B5563;
    }

    /* 이미지 컨테이너 */
    .img-container {
        border-radius: 20px;
        border: 4px solid #D1FAE5;
        overflow: hidden;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. 데이터 준비 (선생님 HTML 내용 완벽 이식) ---

# 단어 데이터 (윗주 달기용)
vocab_map = {
    "recycle": "재활용하다", "garbage": "쓰레기", "return": "돌려주다",
    "used": "사용된", "throw": "버리다", "away": "멀리",
    "special": "특별한", "cans": "캔", "bottles": "병", "gate": "대문",
    "explain": "설명하다", "contained": "포함했다", "useful": "유용한",
    "separate": "분리된", "containers": "용기", "broken": "부서진",
    "melted": "녹은", "metal": "금속", "shredded": "찢겨진",
    "comics": "만화책", "waste": "낭비하다", "buried": "묻힌",
    "dumps": "매립지", "spoil": "망치다", "countryside": "시골",
    "secondhand": "중고의", "packages": "포장", "compost": "퇴비",
    "heap": "더미", "nature": "자연", "plastic": "플라스틱"
}

# 스토리 데이터 (페이지별 이미지와 문장)
story_data = [
    {
        "img": "1.png", # 이미지 파일명 (images 폴더 내)
        "lines": [
            {"eng": "In my family, we recycle our garbage.", "kor": "우리 가족은 쓰레기를 재활용해요."},
            {"eng": "We return things so they can be used again.", "kor": "우리는 물건들을 돌려줘서 다시 사용할 수 있어요."},
            {"eng": "We didn't always recycle.", "kor": "우리는 항상 재활용한 것은 아니에요."},
            {"eng": "We used to throw everything away!", "kor": "우리는 모든 것을 버렸어요!"}
        ]
    },
    {
        "img": "2.png",
        "lines": [
            {"eng": "On our way to school, we always pass Mr. Jones's house.", "kor": "학교 가는 길에, 우리는 항상 Jones 선생님 집을 지나가요."},
            {"eng": "Mr. Jones is our teacher.", "kor": "Jones 선생님은 우리 선생님이에요."},
            {"eng": "One day, we saw him putting a special box with cans, bottles, and papers by the gate.", "kor": "어느 날, 선생님이 문 앞에 캔, 병, 종이가 든 특별한 상자를 두는 것을 봤어요."},
            {"eng": "\"This box is for recycling. All these things are taken away and used again,\" said Mr. Jones.", "kor": "\"이 상자는 재활용용이야. 이것들은 수거되어 다시 사용된단다,\" 선생님이 말했어요."}
        ]
    },
    {
        "img": "3.png",
        "lines": [
            {"eng": "In class, Mr. Jones asked us what we did with our trash.", "kor": "수업 시간에, 선생님은 우리에게 쓰레기를 어떻게 하는지 물었어요."},
            {"eng": "\"We put it in the garbage can.\" \"It's just old garbage!\"", "kor": "\"우리는 쓰레기통에 넣어요.\" \"그냥 오래된 쓰레기예요!\""},
            {"eng": "Mr. Jones said garbage contained lots of useful things that can be recycled, or used again.", "kor": "선생님은 쓰레기에 재활용되거나 다시 쓸 수 있는 유용한 것들이 많다고 말했어요."},
            {"eng": "\"Why should I recycle?\"", "kor": "\"왜 제가 재활용해야 하나요?\""}
        ]
    },
    {
        "img": "4.png",
        "lines": [
            {"eng": "Mr. Jones took the class to a recycling center.", "kor": "Jones 선생님은 우리 반을 재활용 센터로 데려갔어요."},
            {"eng": "It had separate containers for bottles, cans, plastic, clothes, and paper.", "kor": "그곳에는 병, 캔, 플라스틱, 옷, 종이를 위한 분리된 용기들이 있었어요."},
            {"eng": "\"What do you think happens to all the glass that goes in here?\"", "kor": "\"여기에 들어가는 모든 유리가 어떻게 된다고 생각하니?\""},
            {"eng": "\"It all gets broken down to make new shiny bottles!\"", "kor": "\"전부 분해되어 새로운 반짝이는 병이 돼요!\""}
        ]
    },
    {
        "img": "5.png",
        "lines": [
            {"eng": "\"The paper gets shredded and used to make new books and comics.\"", "kor": "\"종이는 잘게 찢어져서 새로운 책과 만화책을 만드는 데 사용돼요.\""},
            {"eng": "\"All these things come from garbage we just throw away?\"", "kor": "\"이 모든 것들이 우리가 그냥 버린 쓰레기에서 나온 거예요?\""},
            {"eng": "\"This plastic can be used to make all kinds of things, including clothes.\"", "kor": "\"이 플라스틱은 옷을 포함한 모든 종류의 것들을 만드는 데 사용될 수 있어요.\""},
            {"eng": "\"So why waste waste?\"", "kor": "\"그러니 왜 쓰레기를 낭비하나요?\""}
        ]
    },
     {
        "img": "6.png",
        "lines": [
            {"eng": "\"Most of the garbage we put in the trash can gets buried in dumps that spoil the countryside.\"", "kor": "\"쓰레기통에 버린 대부분의 쓰레기는 시골을 망치는 매립지에 묻혀요.\""},
            {"eng": "\"It's good to recycle as much as you can!\" said Mr. Jones.", "kor": "\"가능한 한 많이 재활용하는 것이 좋아요!\" Jones 선생님이 말했어요."},
            {"eng": "\"So what else can we recycle?\"", "kor": "\"그럼 우리가 또 무엇을 재활용할 수 있나요?\""},
            {"eng": "\"Clothes, books, and toys that you don't want can all be taken to the secondhand store.\"", "kor": "\"원하지 않는 옷, 책, 장난감은 모두 중고 가게로 가져갈 수 있어요.\""}
        ]
    }
]

# --- 3. 함수 정의 ---

def play_tts(text):
    """gTTS로 음성 생성 및 재생"""
    try:
        tts = gTTS(text=text, lang='en')
        audio_fp = io.BytesIO()
        tts.write_to_fp(audio_fp)
        st.audio(audio_fp, format='audio/mp3', start_time=0)
    except Exception as e:
        st.error("음성 재생 오류")

def annotate_text(text):
    """영어 문장의 단어를 확인하여 윗주(Ruby) HTML 태그를 입힘"""
    words = text.split(' ')
    annotated_html = ""
    for word in words:
        # 구두점 제거하고 소문자로 단어 확인
        clean_word = word.lower().replace('.', '').replace(',', '').replace('"', '').replace('?', '').replace('!', '')
        if clean_word in vocab_map:
            meaning = vocab_map[clean_word]
            # HTML Ruby 태그 적용
            annotated_html += f"<ruby>{word}<rt>{meaning}</rt></ruby> "
        else:
            annotated_html += f"{word} "
    return annotated_html

# --- 4. 세션 상태 관리 (현재 페이지, 현재 문장) ---
if 'current_page' not in st.session_state:
    st.session_state.current_page = 0
if 'current_line' not in st.session_state:
    st.session_state.current_line = 0

# --- 5. UI 구성 ---

# 사이드바 (페이지 이동)
with st.sidebar:
    st.title("📚 책장 넘기기")
    
    # 페이지 이동 버튼
    col_prev, col_next = st.columns(2)
    with col_prev:
        if st.button("⬅️ 이전 쪽"):
            if st.session_state.current_page > 0:
                st.session_state.current_page -= 1
                st.session_state.current_line = 0
                st.rerun()
    with col_next:
        if st.button("다음 쪽 ➡️"):
            if st.session_state.current_page < len(story_data) - 1:
                st.session_state.current_page += 1
                st.session_state.current_line = 0
                st.rerun()

    st.markdown("---")
    st.info(f"현재 페이지: {st.session_state.current_page + 1} / {len(story_data)}")
    
    # 전체 초기화
    if st.button("🔄 처음으로 돌아가기"):
        st.session_state.current_page = 0
        st.session_state.current_line = 0
        st.rerun()

# 메인 화면
page_data = story_data[st.session_state.current_page]

# 1) 상단: 이미지 표시
col_img, col_text = st.columns([1, 1])

with col_img:
    st.markdown('<div class="img-container">', unsafe_allow_html=True)
    # 이미지가 있으면 표시, 없으면 안내 문구
    image_path = f"images/{page_data['img']}"
    if os.path.exists(image_path):
        st.image(image_path, use_container_width=True)
    else:
        st.warning(f"⚠️ 이미지를 찾을 수 없습니다.\n\n'{image_path}' 위치에 파일을 넣어주세요.")
        # 임시 플레이스홀더 이미지 (테스트용)
        st.image("https://via.placeholder.com/600x400?text=Please+Upload+Image", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 2) 하단(또는 우측): 텍스트 및 컨트롤
with col_text:
    st.title(f"Page {st.session_state.current_page + 1}")
    
    # 문장 네비게이션 (재생 컨트롤)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c1:
        if st.button("🔼 이전 문장"):
            if st.session_state.current_line > 0:
                st.session_state.current_line -= 1
                st.rerun()
    with c3:
        if st.button("다음 문장 🔽"):
            if st.session_state.current_line < len(page_data['lines']) - 1:
                st.session_state.current_line += 1
                st.rerun()
    
    st.markdown("---")

    # 문장 출력 루프
    for idx, line in enumerate(page_data['lines']):
        is_active = (idx == st.session_state.current_line)
        
        # HTML 생성 (Ruby 태그 포함)
        ruby_text = annotate_text(line['eng'])
        
        if is_active:
            # 활성화된 문장 (크고 강조됨, 음영 처리)
            st.markdown(f"""
            <div class="active-line">
                <div class="active-text">{ruby_text}</div>
                <div class="active-trans">{line['kor']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # 자동 재생 (현재 활성화된 문장만 읽기)
            # 매번 리로드될 때마다 읽으면 시끄러울 수 있으므로, 
            # '듣기' 버튼을 눌렀을 때만 읽게 하거나, 아래 주석을 풀면 자동 재생됩니다.
            # play_tts(line['eng']) 
            
            # 수동 듣기 버튼
            if st.button("🔊 소리 듣기", key=f"btn_{st.session_state.current_page}_{idx}"):
                play_tts(line['eng'])

        else:
            # 비활성화된 문장 (작고 흐림)
            # 클릭하면 해당 문장으로 이동하는 로직은 Streamlit 구조상 버튼으로 구현해야 함
            if st.button(f"{line['eng'][:20]}...", key=f"nav_{st.session_state.current_page}_{idx}", help="이 문장으로 이동"):
                 st.session_state.current_line = idx
                 st.rerun()
                 
            st.markdown(f"""
            <div class="inactive-line">
                <div class="inactive-text">{line['eng']}</div>
            </div>
            """, unsafe_allow_html=True)
