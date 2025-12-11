import streamlit as st

# 제목
st.title("🎈 선생님의 첫 번째 AI 앱")

# 텍스트 표시
st.write("교실 TV에서도, 학생 태블릿에서도 접속 가능합니다.")

# 비디오 (유튜브)
st.video("https://www.youtube.com/watch?v=M7lc1UVf-VE")

# TTS (음성 듣기 기능 테스트)
text = "Hello! This is a test for English class."
st.write(f"듣기 연습: {text}")
if st.button("원어민 발음 듣기"):
    # 실제로는 이 부분에 고품질 TTS 코드가 들어갑니다.
    # 지금은 기본 기능만 확인합니다.
    st.toast("🔊 소리가 재생됩니다 (설정 완료 후 구현 예정)")

st.success("축하합니다! 웹사이트 구축에 성공하셨습니다.")
