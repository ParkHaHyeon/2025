import streamlit as st
import random
# from PIL import Image  # PIL 라이브러리는 로컬 파일이 있을 때만 필요하므로 주석 처리합니다.

# 펫의 상태를 관리하기 위한 세션 상태
if 'pet_happiness' not in st.session_state:
    st.session_state.pet_happiness = 50
if 'game_result' not in st.session_state:
    st.session_state.game_result = ""

# 펫의 상태에 따른 이미지 URL 설정 (인터넷 링크 사용)
image_urls = {
    'happy': 'https://i.imgur.com/GzB9oJ5.png',  # 행복한 펫 이미지 (예시)
    'neutral': 'https://i.imgur.com/H1J6M7J.png', # 보통 펫 이미지 (예시)
    'sad': 'https://i.imgur.com/vHq136M.png'    # 슬픈 펫 이미지 (예시)
}

# 펫의 상태에 따라 이미지와 메시지 결정
def get_pet_state():
    if st.session_state.pet_happiness > 70:
        return 'happy', "정말 행복해 보여요! 😊"
    elif st.session_state.pet_happiness < 30:
        return 'sad', "으음, 조금 슬퍼 보여요. 😥"
    else:
        return 'neutral', "기분이 좋아요! 😄"

# 동전 뒤집기 게임 함수
def coin_flip_game(user_choice):
    st.write('동전을 뒤집습니다...')
    coin_result = random.choice(['앞면', '뒷면'])
    
    if user_choice == coin_result:
        st.session_state.game_result = f'🎉 와! 맞혔어요! 동전은 "{coin_result}"이(가) 나왔어요.'
        st.session_state.pet_happiness = min(100, st.session_state.pet_happiness + 20)
    else:
        st.session_state.game_result = f'😅 아쉽네요... 동전은 "{coin_result}"이(가) 나왔어요.'
        st.session_state.pet_happiness = max(0, st.session_state.pet_happiness - 10)
    
    st.rerun()

# Streamlit 페이지 구성
st.title('나만의 가상 펫')
st.write('펫과 함께 놀아주며 스트레스를 해소해 보세요!')

# 펫의 상태 가져오기
state, message = get_pet_state()

# 펫 이미지 표시 (인터넷 링크 사용)
st.image(image_urls[state], width=300)
st.write(message)

# 펫과 상호작용하는 버튼
col1, col2, col3 = st.columns(3)

with col1:
    if st.button('쓰다듬기'):
        st.session_state.pet_happiness = min(100, st.session_state.pet_happiness + 15)
        st.session_state.game_result = ""  # 게임 결과 초기화
        st.rerun()

with col2:
    if st.button('간식 주기'):
        st.session_state.pet_happiness = min(100, st.session_state.pet_happiness + 10)
        st.session_state.game_result = ""  # 게임 결과 초기화
        st.rerun()

with col3:
    if st.button('냅두기'):
        st.session_state.pet_happiness = max(0, st.session_state.pet_happiness - 5)
        st.session_state.game_result = ""  # 게임 결과 초기화
        st.rerun()

# 현재 행복도 상태바 표시
st.progress(st.session_state.pet_happiness / 100)
st.write(f'현재 행복도: {st.session_state.pet_happiness}%')

st.subheader('펫과 미니게임하기')
st.write('펫과 동전 뒤집기 게임을 해보세요! 맞히면 행복도가 올라가요.')

game_col1, game_col2 = st.columns(2)
with game_col1:
    if st.button('앞면 선택'):
        coin_flip_game('앞면')

with game_col2:
    if st.button('뒷면 선택'):
        coin_flip_game('뒷면')

if st.session_state.game_result:
    st.write(st.session_state.game_result)

# 펫에게 말 걸기
user_text = st.text_input('펫에게 말을 걸어보세요:')
if user_text:
    st.write(f'펫: "{user_text}라고요? 고마워요!"')
