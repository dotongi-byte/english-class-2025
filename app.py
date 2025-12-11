import streamlit as st
from gtts import gTTS
from io import BytesIO

# 페이지 기본 설정 (제목, 레이아웃 등)
st.set_page_config(layout="wide", page_title="6th Grade English: Jobs")

# 학습할 단어 데이터 (단어, 뜻, 이미지 URL)
# *무료 이미지(Unsplash) 사용
vocab_list = [
    {"word": "cook", "mean": "요리사", "img": "https://images.unsplash.com/photo-1577219491135-ce391730fb2c?w=400"},
    {"word": "pilot", "mean": "비행기 조종사", "img": "https://images.unsplash.com/photo-1559627748-c81e74fbfd5f?w=400"},
    {"word": "doctor", "mean": "의사", "img": "https://images.unsplash.com/photo-1537368910025-700350fe46c7?w=400"},
    {"word": "scientist", "mean": "과학자", "img": "https://images.unsplash.com/photo-1507413245164-6160d8298b31?w=400"},
    {"word": "artist", "mean": "예술가", "img": "https://images.unsplash.com/photo-1513364776144-60967b0f800f?w=400"},
]

# 제목 및 소개
st.title("👩‍🍳 I want to be a cook! (직업 배우기) 👨‍✈️")
st.markdown("### 초등학교 6학년 필수 영단어 학습")
st.markdown("---")

# 화면을 2분할 (왼쪽: 학습 / 오른쪽: 퀴즈)
col1, col2 = st.columns([1, 1], gap="large")

# [왼쪽 컬럼] 단어 학습 존
with col1:
    st.subheader("📖 Vocabulary Learning")
    st.info("사진을 보고 발음을 들어보세요!")

    for idx, item in enumerate(vocab_list):
        # 각 단어를 구분하기 위한 컨테이너
        with st.container():
            sub_c1, sub_c2 = st.columns([1, 2])
            
            # 이미지 표시
            with sub_c1:
                st.image(item["img"], use_container_width=True)
            
            # 단어, 뜻, 발음 버튼 표시
            with sub_c2:
                st.markdown(f"### **{item['word']}**")
                st.write(f"뜻: {item['mean']}")
                
                # TTS 생성 및 재생 기능
                # 고유한 key를 주어 버튼 충돌 방지
                if st.button(f"🔊 듣기 ({item['word']})", key=f"btn_{idx}"):
                    tts = gTTS(text=item['word'], lang='en')
                    sound_file = BytesIO()
                    tts.write_to_fp(sound_file)
                    st.audio(sound_file)
            
            st.divider() # 구분선

# [오른쪽 컬럼] 퀴즈 존
with col2:
    st.subheader("✍️ Quiz Time")
    st.warning("왼쪽에서 배운 단어를 맞춰보세요! (소문자로 입력)")

    # 퀴즈 폼 생성 (한 번에 제출하여 정답 확인)
    with st.form("quiz_form"):
        score = 0
        user_answers = {}

        for item in vocab_list:
            # 입력창 생성
            user_answers[item['word']] = st.text_input(f"Q. '{item['mean']}' (은)는 영어로 무엇일까요?")

        # 제출 버튼
        submitted = st.form_submit_button("채점하기 💯")

        if submitted:
            all_correct = True
            for item in vocab_list:
                answer = user_answers[item['word']].strip().lower()
                if answer == item['word']:
                    st.success(f"✅ 정답입니다! ({item['mean']} -> {item['word']})")
                    score += 1
                else:
                    st.error(f"❌ 틀렸습니다. ({item['mean']})")
                    all_correct = False
            
            # 피드백 및 풍선 효과
            if score == len(vocab_list):
                st.balloons()
                st.markdown("### 🏆 대단해요! 모든 문제를 맞췄어요! You are a master!")
            elif score > 0:
                st.write(f"### 총 {len(vocab_list)}문제 중 {score}개를 맞췄어요. 다시 도전해보세요!")

# [하단] 유튜브 영상 임베드
st.markdown("---")
st.subheader("📺 Watch and Sing Along!")
# Jobs Song for Kids 관련 영상 (유튜브)
st.video("https://www.youtube.com/watch?v=CKjT5p2jXhE")
