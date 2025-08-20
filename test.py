import streamlit as st
import random

# 세션 상태 초기화
if 'pet_happiness' not in st.session_state:
    st.session_state.pet_happiness = 50
if 'game_result' not in st.session_state:
    st.session_state.game_result = ""
if 'pet_name' not in st.session_state:
    st.session_state.pet_name = ""
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""
# 화면 전환 상태: 'setup' | 'home' | 'game'
if 'view' not in st.session_state:
    # 이름이 비어 있으면 설정 화면부터, 있으면 홈부터
    st.session_state.view = 'setup' if not (st.session_state.pet_name and st.session_state.user_name) else 'home'

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

# 공통: 제목
st.title('나만의 가상 펫🐾')

# 화면 분기
if st.session_state.view == 'setup':
    st.subheader('이름 설정')
    st.caption('펫과 사용자 이름을 정한 뒤 시작하세요.')

    pet_name_input = st.text_input("펫 이름을 지어주세요:", value=st.session_state.pet_name, placeholder="예: 가나디")
    user_name_input = st.text_input("당신의 이름을 알려주세요:", value=st.session_state.user_name, placeholder="예: 홍길동")

    col_a, col_b = st.columns([1, 1])
    with col_a:
        if st.button('시작하기 ✅', use_container_width=True):
            # 공백 제거 후 검증
            p = (pet_name_input or "").strip()
            u = (user_name_input or "").strip()
            if not p or not u:
                st.warning("이름이 비어 있어요. 두 칸 모두 입력해 주세요.")
            else:
                st.session_state.pet_name = p
                st.session_state.user_name = u
                st.session_state.view = 'home'
                st.rerun()
    with col_b:
        if st.button('랜덤 이름 넣기 🎲', use_container_width=True):
            # 간단 랜덤 이름
            candidates = ["콩이", "희망이", "콜라", "겨울이", "동강이", "장군이", "네로", "나비", "식빵이", "연탄이", "초코초키"]
            st.session_state.pet_name = random.choice(candidates)
            st.session_state.user_name = st.session_state.user_name or "사용자"
            st.rerun()

elif st.session_state.view == 'home':
    st.write(f'{st.session_state.pet_name}를(을) 놀아주며 스트레스를 해소해 보세요!')

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

    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
    colh1, colh2 = st.columns([1,1])
    with colh1:
        if st.button('게임하기 🎮', use_container_width=True):
            st.session_state.view = 'game'
            st.rerun()
    with colh2:
        if st.button('이름 수정 ✏️', use_container_width=True):
            st.session_state.view = 'setup'
            st.rerun()

    # 펫에게 말 걸기
    user_text = st.text_input(f'{st.session_state.pet_name}에게 말을 걸어보세요:')
    if user_text:
        st.write(f'{st.session_state.pet_name}: "{user_text}라고요? 고마워요!"')

elif st.session_state.view == 'game':
    st.subheader(f'{st.session_state.pet_name}과(와) 미니게임하기🎮')
    
    state, message = get_pet_state()
    st.image(image_urls.get(state, 'https://via.placeholder.com/300?text=Image+Not+Found'), width=300)
    st.write(message)
    st.progress(st.session_state.pet_happiness / 100)
    st.write(f'{st.session_state.pet_name}의 현재 행복도: {st.session_state.pet_happiness}%')
    st.markdown("<div style='height: 48px;'></div>", unsafe_allow_html=True)
    
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
    if st.button('← 뒤로가기 (펫 화면)'):
        st.session_state.view = 'home'
        st.rerun()
