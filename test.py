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
 
# 반응속도 테스트용 상태값
if 'rt_now' not in st.session_state:
    st.session_state.rt_now = False
if 'rt_ready' not in st.session_state:
    st.session_state.rt_ready = False
if 'rt_go_time' not in st.session_state:
    st.session_state.rt_go_time = None
if 'rt_result' not in st.session_state:
    st.session_state.rt_result = None
    
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
    import random, time

    st.subheader(f'{st.session_state.pet_name}과(와) 미니게임하기🎮')
    st.caption('원하는 게임을 골라 즐겨보세요. 성적에 따라 행복도가 변합니다!')

    game = st.selectbox('게임 선택', ['동전 뒤집기', '가위바위보', '숫자 맞히기', '반응속도 테스트'])
    st.session_state.game_type = game

    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

    # 1) 동전 뒤집기
    if game == '동전 뒤집기':
        st.write('맞히면 행복도 +20, 틀리면 -10')
        col1, col2 = st.columns(2)
        with col1:
            if st.button('앞면 선택', use_container_width=True):
                coin = random.choice(['앞면', '뒷면'])
                if coin == '앞면':
                    st.success(f'정답! 동전은 {coin} 🎉 (행복도 +20)')
                    st.session_state.pet_happiness = min(100, st.session_state.pet_happiness + 20)
                else:
                    st.warning(f'아쉽네요… 동전은 {coin} 😅 (행복도 -10)')
                    st.session_state.pet_happiness = max(0, st.session_state.pet_happiness - 10)
        with col2:
            if st.button('뒷면 선택', use_container_width=True):
                coin = random.choice(['앞면', '뒷면'])
                if coin == '뒷면':
                    st.success(f'정답! 동전은 {coin} 🎉 (행복도 +20)')
                    st.session_state.pet_happiness = min(100, st.session_state.pet_happiness + 20)
                else:
                    st.warning(f'아쉽네요… 동전은 {coin} 😅 (행복도 -10)')
                    st.session_state.pet_happiness = max(0, st.session_state.pet_happiness - 10)

    # 2) 가위바위보
    elif game == '가위바위보':
        st.write('이기면 +15, 비기면 0, 지면 -10')
        choices = ['가위', '바위', '보']

        def rps_once(user_pick):
            bot_pick = random.choice(choices)
            st.write(f'{st.session_state.pet_name}의 선택: {bot_pick}')
            win = (user_pick == '가위' and bot_pick == '보') or \
                  (user_pick == '바위' and bot_pick == '가위') or \
                  (user_pick == '보' and bot_pick == '바위')
            draw = (user_pick == bot_pick)
            if win:
                st.success('이겼어요! 🎉 (행복도 +15)')
                st.session_state.pet_happiness = min(100, st.session_state.pet_happiness + 15)
            elif draw:
                st.info('비겼어요! 🙂 (변화 없음)')
            else:
                st.warning('졌어요! 😅 (행복도 -10)')
                st.session_state.pet_happiness = max(0, st.session_state.pet_happiness - 10)

        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button('가위 ✂️', use_container_width=True):
                rps_once('가위')
        with c2:
            if st.button('바위 ✊', use_container_width=True):
                rps_once('바위')
        with c3:
            if st.button('보 ✋', use_container_width=True):
                rps_once('보')

    # 3) 숫자 맞히기
    elif game == '숫자 맞히기':
        st.write('1~5 사이 숫자를 맞히면 +12, 틀리면 -6')
        if 'target_num' not in st.session_state:
            st.session_state.target_num = random.randint(1, 5)
            st.session_state.last_guess_msg = ''

        c_top1, c_top2 = st.columns([1,1])
        with c_top1:
            if st.button('새 라운드 시작 🔄', use_container_width=True):
                st.session_state.target_num = random.randint(1, 5)
                st.session_state.last_guess_msg = ''
                st.rerun()
        with c_top2:
            pass

        guess = st.number_input('숫자를 고르세요 (1~5)', min_value=1, max_value=5, step=1)
        if st.button('확인', use_container_width=True):
            if guess == st.session_state.target_num:
                st.session_state.last_guess_msg = '정답! 🎉 (행복도 +12)'
                st.session_state.pet_happiness = min(100, st.session_state.pet_happiness + 12)
            else:
                st.session_state.last_guess_msg = f'아쉬워요… 정답은 {st.session_state.target_num} 😅 (행복도 -6)'
                st.session_state.pet_happiness = max(0, st.session_state.pet_happiness - 6)
        if st.session_state.get('last_guess_msg'):
            st.write(st.session_state.last_guess_msg)

    # 4) 반응속도 테스트
    elif game == '반응속도 테스트':
        st.write('“시작” 후 랜덤 타이밍에 나타나는 “지금 클릭!” 버튼을 누르세요.')
        st.caption('1.0초 미만: +15 / 1.0~2.0초: +8 / 2.0초 이상: +0 / 성급한 클릭: -5')

        # 준비/시작
        if not st.session_state.rt_now:
            colA, colB = st.columns([1,1])
            with colA:
                if st.button('시작 ▶️', use_container_width=True):
                    st.session_state.rt_result = None
                    st.session_state.rt_ready = True
                    delay = random.uniform(1.5, 3.0)
                    st.info('준비...')
                    time.sleep(delay)
                    st.session_state.rt_go_time = time.perf_counter()
                    st.session_state.rt_now = True
                    st.rerun()
            with colB:
                if st.button('리셋 ♻️', use_container_width=True):
                    st.session_state.rt_now = False
                    st.session_state.rt_ready = False
                    st.session_state.rt_go_time = None
                    st.session_state.rt_result = None
                    st.rerun()

        # 클릭 단계
        if st.session_state.rt_now:
            if st.button('지금 클릭! 🖱️', type='primary', use_container_width=True):
                if st.session_state.rt_go_time is None:
                    # 너무 성급한 클릭(지시 전에 누름) — 이론상 방지용
                    st.warning('너무 빨랐어요! (행복도 -5)')
                    st.session_state.pet_happiness = max(0, st.session_state.pet_happiness - 5)
                else:
                    rt = time.perf_counter() - st.session_state.rt_go_time
                    st.session_state.rt_result = rt
                    if rt < 1.0:
                        st.success(f'대단해요! {rt:.3f}초 (행복도 +15)')
                        st.session_state.pet_happiness = min(100, st.session_state.pet_happiness + 15)
                    elif rt < 2.0:
                        st.info(f'좋아요! {rt:.3f}초 (행복도 +8)')
                        st.session_state.pet_happiness = min(100, st.session_state.pet_happiness + 8)
                    else:
                        st.write(f'다음엔 더 빠르게! {rt:.3f}초 (변화 없음)')
                # 라운드 종료
                st.session_state.rt_now = False
                st.session_state.rt_go_time = None

        # 성급한 클릭 방지용 안내
        if st.session_state.rt_ready and not st.session_state.rt_now and st.session_state.rt_result is None:
            st.caption('잠시 뒤 “지금 클릭!” 버튼이 나타나면 눌러주세요.')

        # 결과 표시
        if st.session_state.rt_result is not None:
            st.write(f'최근 기록: {st.session_state.rt_result:.3f}초')

    # 공통: 현재 행복도
    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
    st.progress(st.session_state.pet_happiness / 100)
    st.write(f'현재 행복도: {st.session_state.pet_happiness}%')

  


    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
    if st.button('← 뒤로가기 (펫 화면)'):
        st.session_state.view = 'home'
        st.rerun()
