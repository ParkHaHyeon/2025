# app.py (수정본)
import streamlit as st
import time
import json
from datetime import datetime
import os

st.set_page_config(page_title="생각의 전환 - 독서 타이머", layout="centered")

DATA_FILE = "reading_data.json"

# ---------- 유틸: 데이터 저장/불러오기 ----------
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return {"users": {}, "logs": [], "surveys": []}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

data = load_data()

# ---------- 사용자 설정 처리 (간단하고 안전한 방식) ----------
def set_user():
    user_input = st.session_state.get("user_input", "").strip()
    if user_input:
        st.session_state.user = user_input
        # 사용자 데이터가 없으면 초기화
        if user_input not in data["users"]:
            data["users"][user_input] = {
                "xp": 0,
                "level": 1,
                "evolution_stage": 1,
                "total_minutes": 0,
                "total_pages": 0,
                "items": []
            }
            save_data(data)
        # st.experimental_rerun() 호출 제거 — 세션 상태만 변경하면 다음 렌더링에서 반영됩니다

# 사이드바에 닉네임 입력 위젯 배치(한 번만 생성)
st.sidebar.title("사용자 설정")
st.sidebar.text_input("닉네임을 입력하세요 (예: 친구A)", key="user_input", on_change=set_user)
st.sidebar.write("닉네임을 입력하면 앱이 로드됩니다. 익명으로 사용하세요.")

# 닉네임이 세션에 없으면 안내 후 종료
if "user" not in st.session_state:
    st.title("생각의 전환 - 독서 타이머 (프로토타입)")
    st.write("사이드바에 닉네임을 입력해 주세요. 입력 후 엔터 또는 확인을 누르면 앱이 시작됩니다.")
    st.stop()

# 이제 안전하게 user 사용
user = st.session_state.user

# 캐릭터 설정(간단)
THRESHOLDS = {
    "small_feed": 5,    # 분
    "med_feed": 20,     # 분
    "complete_book_pages": 100  # 기본 완독 페이지 기준
}

# ---------- 상단: 캐릭터 상태 요약 ----------
st.title("생각의 전환 - 독서 타이머 (프로토타입)")
st.markdown(f"안녕하세요, **{user}** 님. 아래에서 오늘의 목표를 정하고 타이머를 시작하세요.")

user_data = data["users"][user]
col1, col2 = st.columns(2)
with col1:
    st.subheader("캐릭터 상태")
    st.write(f"레벨: {user_data['level']}")
    st.write(f"진화단계: {user_data['evolution_stage']}")
    st.write(f"누적 독서 시간(분): {user_data['total_minutes']}")
    st.write(f"누적 페이지 수: {user_data['total_pages']}")
with col2:
    st.subheader("오늘 목표")
    goal_type = st.selectbox("목표 타입 선택", ["시간(분)", "페이지 수"])
    if goal_type == "시간(분)":
        today_goal = st.number_input("오늘 목표(분)", min_value=1, value=5, step=1, key="today_goal_min")
    else:
        today_goal = st.number_input("오늘 목표(페이지)", min_value=1, value=10, step=1, key="today_goal_page")

# ---------- 타이머 로직 ----------
st.markdown("---")
st.subheader("타이머")

if "timer_running" not in st.session_state:
    st.session_state.timer_running = False
if "timer_start" not in st.session_state:
    st.session_state.timer_start = None
if "accum_today" not in st.session_state:
    st.session_state.accum_today = 0  # 분 단위

start_col, stop_col, reset_col = st.columns([1,1,1])
with start_col:
    if st.button("타이머 시작"):
        if not st.session_state.timer_running:
            st.session_state.timer_running = True
            st.session_state.timer_start = time.time()
            st.success("타이머가 시작되었습니다. 집중해서 읽어보세요!")
            # 재실행 없이 상태만 변경하고 다음 렌더링에서 반영되도록 함
with stop_col:
    if st.button("타이머 중지"):
        if st.session_state.timer_running and st.session_state.timer_start is not None:
            elapsed = time.time() - st.session_state.timer_start
            minutes = int(elapsed // 60)
            st.session_state.accum_today += minutes
            st.session_state.timer_running = False
            st.session_state.timer_start = None
            now = datetime.now().isoformat()
            data["logs"].append({
                "user": user,
                "timestamp": now,
                "minutes": minutes,
                "pages": 0,
                "goal_type": "manual_stop"
            })
            user_data["total_minutes"] += minutes
            save_data(data)
            st.success(f"{minutes}분이 기록되었습니다.")

with reset_col:
    if st.button("오늘 누적 초기화"):
        st.session_state.accum_today = 0
        st.info("오늘 누적 시간이 초기화되었습니다.")
        # 재실행은 필요 없음

# 타이머 표시 (간단 방식)
timer_placeholder = st.empty()
if st.session_state.timer_running:
    elapsed = int(time.time() - st.session_state.timer_start)
    mins = elapsed // 60
    secs = elapsed % 60
    timer_placeholder.markdown(f"진행 중: {mins}분 {secs}초")
    st.info("실시간 초단위 갱신은 제한됩니다. '타이머 중지'를 눌러 기록하세요.")
else:
    timer_placeholder.markdown(f"오늘 누적 독서 시간(앱 내 기록): {st.session_state.accum_today}분")

# ---------- 페이지 수 입력 ----------
st.markdown("---")
st.subheader("페이지 수 입력(선택)")
pages_today = st.number_input("오늘 읽은 페이지 수를 입력하세요", min_value=0, value=0, step=1, key="pages_input")
if st.button("페이지 수 등록"):
    if pages_today > 0:
        now = datetime.now().isoformat()
        data["logs"].append({
            "user": user,
            "timestamp": now,
            "minutes": 0,
            "pages": pages_today,
            "goal_type": "pages_manual"
        })
        user_data["total_pages"] += int(pages_today)
        save_data(data)
        st.success(f"{pages_today}페이지가 기록되었습니다.")
    else:
        st.warning("0보다 큰 값을 입력해 주세요.")

# ---------- 행동(먹이/목욕 등) 잠금·해제 ----------
st.markdown("---")
st.subheader("캐릭터와 상호작용")

today_minutes_for_actions = st.session_state.accum_today
st.write(f"오늘 누적 시간: {today_minutes_for_actions}분 (앱에 기록된 시간만 포함)")

col_a, col_b, col_c = st.columns(3)
with col_a:
    if today_minutes_for_actions >= THRESHOLDS["small_feed"]:
        if st.button("먹이 주기 (소)"):
            gained = 10
            user_data["xp"] += gained
            save_data(data)
            st.success(f"먹이 주기 완료! XP +{gained}")
    else:
        st.button(f"먹이 주기 (소) - {THRESHOLDS['small_feed']}분 필요", disabled=True)
with col_b:
    if today_minutes_for_actions >= THRESHOLDS["med_feed"]:
        if st.button("먹이 주기 (중)"):
            gained = 40
            user_data["xp"] += gained
            save_data(data)
            st.success(f"먹이 주기 완료! XP +{gained}")
    else:
        st.button(f"먹이 주기 (중) - {THRESHOLDS['med_feed']}분 필요", disabled=True)
with col_c:
    book_pages = st.number_input("현재 읽는 책 전체 페이지 수", min_value=1, value=THRESHOLDS["complete_book_pages"], step=1, key="book_pages_input")
    if st.button("완독 표시 (완독 시 캐릭터 진화)"):
        if user_data["total_pages"] >= book_pages:
            user_data["evolution_stage"] += 1
            user_data["xp"] += 200
            save_data(data)
            st.success("축하합니다! 캐릭터가 진화했습니다. XP +200")
        else:
            st.warning("완독 조건을 충족하지 못했습니다. 먼저 페이지 수를 기록해 주세요.")

# 간단 레벨업 로직
leveled_up = False
while user_data["xp"] >= 100 * user_data["level"]:
    user_data["xp"] -= 100 * user_data["level"]
    user_data["level"] += 1
    leveled_up = True
if leveled_up:
    save_data(data)
    st.balloons()
    st.success("레벨업! 축하합니다.")

# ---------- 사전/사후 설문 ----------
# --- 간단 링크 방식 (붙여넣기용) ---
pre_url = "https://docs.google.com/forms/d/e/1FAIpQLSdlxENEMM31eK2Er-QpgQEej2Mz0azUnWXC2YDF4DuEkPp83g/viewform?usp=header"
post_url = "https://docs.google.com/forms/d/e/1FAIpQLSepOCxzVENWLuSaabe5N-Tu8RgX5BPLElnpXGVynwO8CTY0HA/viewform?usp=header"

st.markdown("### 사전 설문")
st.markdown(f"- [사전 설문지 열기]({pre_url})  (새 탭에서 열립니다)")

st.markdown("### 사후 설문")
st.markdown(f"- [사후 설문지 열기]({post_url})  (새 탭에서 열립니다)")

# ---------- 로그 보기(개인용) ----------
st.markdown("---")
st.subheader("내 기록 보기 (최근 10개)")
user_logs = [l for l in data["logs"] if l["user"] == user]
if user_logs:
    for log in user_logs[-10:]:
        st.write(f"{log['timestamp'][:19]} — 분: {log['minutes']}, 페이지: {log['pages']}")
else:
    st.write("기록이 없습니다.")

st.markdown("---")
st.caption("프로토타입입니다. 데이터는 로컬 파일에 저장됩니다. 실제 파일럿에서는 외부 저장 연동과 개인정보 최소화 절차를 권장합니다.")
