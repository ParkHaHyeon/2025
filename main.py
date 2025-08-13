import streamlit as st
import random
import time

# Set page configuration
st.set_page_config(page_title="나만의 동화 만들기", page_icon="📖")

# --- App Title and Description ---
st.title("📖✨ 나만의 동화 만들기")
st.write("---")
st.info("주인공 이름, 장소, 물건을 선택하면 여러분만의 특별한 동화가 만들어져요!")

# --- User Inputs ---
st.subheader("1. 주인공 이름을 정해주세요.")
character_name = st.text_input("주인공 이름:", "용감한 토끼")

st.subheader("2. 이야기의 배경을 골라주세요.")
place = st.selectbox(
    "장소:",
    ("신비로운 숲 속", "구름 위의 성", "반짝이는 수정 동굴", "깊은 바닷속 용궁")
)

st.subheader("3. 신기한 물건을 하나 골라주세요.")
item = st.selectbox(
    "물건:",
    ("말하는 요술봉", "하늘을 나는 양탄자", "모든 것을 아는 지도", "투명하게 만드는 모자")
)

# --- Generate Story Button ---
st.write("---")
if st.button("🚀 동화 만들기!", type="primary"):
    # --- Story Templates ---
    story_template_1 = (
        f"옛날 옛적, **{place}**에 **{character_name}**라는 이름의 주인공이 살고 있었어요. "
        f"어느 날, **{character_name}**은/는 우연히 **{item}**을/를 발견했답니다. "
        f"**{item}**의 신비한 힘으로, **{character_name}**은/는 아무도 상상하지 못했던 놀라운 모험을 떠나게 되었고, "
        f"그곳에서 새로운 친구들을 만나 행복하게 살았답니다."
    )

    story_template_2 = (
        f"**{character_name}**은/는 **{place}**에서 가장 호기심 많은 아이였어요. "
        f"그러던 어느 날, 반짝이는 **{item}**을/를 손에 넣게 되었죠. "
        f"**{character_name}**이/가 **{item}**을/를 사용하자, 세상이 온통 무지갯빛으로 변했어요! "
        f"그 후로 **{character_name}**은/는 **{item}**과 함께 매일매일 신나는 하루를 보냈답니다."
    )
    
    story_template_3 = (
        f"깊고 깊은 **{place}**에는 비밀이 하나 숨겨져 있었어요. 바로 전설의 **{item}**이었죠. "
        f"용감한 **{character_name}**은/는 마침내 그 **{item}**을/를 찾아냈어요. "
        f"**{item}** 덕분에 **{character_name}**은/는 어려움에 처한 친구들을 도와주는 멋진 영웅이 되었답니다. "
        f"모두가 **{character_name}**의 용기를 칭찬했어요."
    )

    # Randomly select a story template
    stories = [story_template_1, story_template_2, story_template_3]
    chosen_story = random.choice(stories)
    
    # --- Displaying the result with a loading spinner ---
    with st.spinner('동화를 만들고 있어요... 잠시만 기다려주세요!'):
        time.sleep(2) # Simulate generation time

    st.subheader("🎉 짜잔! 완성된 동화예요!")
    st.success(chosen_story)
    st.balloons()
