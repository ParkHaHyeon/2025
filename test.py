import streamlit as st
import random

# 세션 상태 초기화
if 'pet_happiness' not in st.session_state:
    st.session_state.pet_happiness = 50
if 'game_result' not in st.session_state:
    st.session_state.game_result = ""
if 'pet_name' not in st.session_state:
    st.session_state.pet_name = "애완동물"
if 'user_name' not in st.session_state:
    st.session_state.user_name = "사용자"
# 화면 전환 상태(홈/게임)
if 'view' not in st.session_state:
    st.session_state.view = 'home'  # 'home' 또는 'game'

# 펫의 상태에 따른 이미지 URL
image_urls = {
    'happy': 'https://i.pinimg.com/736x/86/26/b3/8626b38f2f75408cc912f08c104bcfac.jpg',
    'neutral': 'https://i.pinimg.com/736x/c3/72/ae/c372ae91ad48a58fe556cb41a7250f3a.jpg',
    'sad': 'https://i.pinimg.com/736x/90/5e/f0/905ef0274ccdbb8779b73f30c78aece3.jpg'
}

def get_pet_state():
    if st.session_state.pet_happiness >= 100:
        return 'happy', f"{st.session_state.user_name}님 사랑해요! 🥰"
    elif st.session_state.pet_happiness > 70:
        return 'happy', f"{st.session_state.pet_name}은(는) 정말 행복해 보여요! 😊"
    elif st.session_state.pet_happiness < 30:
        return 'sad', f"{st.session_state.pet_name}은(는) 조금 슬퍼 보여요. 😥"
    else:
        return 'neutral', f"{st.session_state.pet_name}은(는) 기분이 좋아요! 😄"

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

# 페이지 제목
st.title('나만의 가상 펫🐾')

# 펫 이름 및 사용자 이름 입력 (두 화면에서 공통 사용)
st.session_state.pet_name = st.text_input("펫 이름을 지어주세요:", value=st.session_state.pet_name)
st.session_state.user_name = st.text_input("당신의 이름을 알려주세요:", value=st.session_state.user_name)

# 화면 렌더링 분기
if st.session_state.view == 'home':
    # 홈: 펫 상태 화면
    st.write(f'{st.session_state.pet_name}과(와) 함께 놀아주며 스트레스를 해소해 보세요!')

    state, message = get_pet_state()
    st.image(image_urls.get(state, 'https://via.placeholder.com/300?text=Image+Not+Found'), width=300)
    st.write(message)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button('쓰다듬기'):
            st.session_state.pet_happiness = min(100, st.session_state.pet_happiness + 15)
            st.session_state.game_result = ""
            st.rerun()
    with col2:
        if st.button('간식 주기'):
            st.session_state.pet_happiness = min(100, st.session_state.pet_happiness + 10)
            st.session_state.game_result = ""
            st.rerun()
    with col3:
        if st.button('가만히 두기'):
            st.session_state.pet_happiness = max(0, st.session_state.pet_happiness - 5)
            st.session_state.game_result = ""
            st.rerun()

    st.progress(st.session_state.pet_happiness / 100)
    st.write(f'{st.session_state.pet_name}의 현재 행복도: {st.session_state.pet_happiness}%')

    # 홈 → 게임 화면으로 이동 버튼
    st.markdown("<div style='height: 32px;'></div>", unsafe_allow_html=True)
    if st.button('게임하기 🎮'):
        st.session_state.view = 'game'
        st.rerun()

    # 펫에게 말 걸기 (홈에서 운영)
    user_text = st.text_input(f'{st.session_state.pet_name}에게 말을 걸어보세요:')
    if user_text:
        st.write(f'{st.session_state.pet_name}: "{user_text}라고요? 고마워요!"')

elif st.session_state.view == 'game':
    # 게임 화면
    st.subheader(f'{st.session_state.pet_name}과(와) 미니게임하기🎮')
    st.write(f'{st.session_state.pet_name}과(와) 동전 뒤집기 게임을 해보세요! 맞히면 행복도가 올라가요.')

    game_col1, game_col2 = st.columns(2)
    with game_col1:
        if st.button('앞면 선택'):
            coin_flip_game('앞면')
    with game_col2:
        if st.button('뒷면 선택'):
            coin_flip_game('뒷면')

    if st.session_state.game_result:
        st.write(st.session_state.game_result)

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
    # 게임 → 홈으로 돌아가기
    if st.button('← 뒤로가기 (펫 화면)'):
        st.session_state.view = 'home'
        st.rerun()
