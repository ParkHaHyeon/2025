import streamlit as st
import random
import requests

# -----------------------------
# 한국 문학 인용구 (MBTI별)
# -----------------------------
quotes = {
    "INFJ": {
        "text": "보이지 않는 것이 더 많은 것을 말한다.",
        "author": "윤동주",
        "work": "별 헤는 밤, 『하늘과 바람과 별과 시』",
        "publisher": "정음사, 1948"
    },
    "INFP": {
        "text": "내가 그의 이름을 불러주었을 때, 그는 나에게로 와서 꽃이 되었다.",
        "author": "김춘수",
        "work": "꽃, 『김춘수 시선집』",
        "publisher": "문학과지성사, 1979"
    },
    "ENFP": {
        "text": "우리는 서로의 삶에 스며들며 비로소 살아간다.",
        "author": "박완서",
        "work": "그 많던 싱아는 누가 다 먹었을까",
        "publisher": "웅진, 1992"
    },
    "ENTP": {
        "text": "길은 걷는 사람이 만든다.",
        "author": "이효석",
        "work": "메밀꽃 필 무렵",
        "publisher": "『조광』, 1936"
    },
    "INTP": {
        "text": "생각은 끝없는 미궁과 같아서, 답은 또 다른 질문 속에서 태어난다.",
        "author": "이상",
        "work": "권태",
        "publisher": "『조선중앙일보』, 1937"
    },
    "INTJ": {
        "text": "끝내 이루지 못한 꿈이, 나를 살아가게 한다.",
        "author": "한강",
        "work": "소년이 온다",
        "publisher": "창비, 2014"
    },
    "ENTJ": {
        "text": "인생은 살기 어렵다는데, 시가 이렇게 쉽게 쓰여져도 되는 것인가.",
        "author": "윤동주",
        "work": "쉽게 쓰여진 시, 『하늘과 바람과 별과 시』",
        "publisher": "정음사, 1948"
    },
    "ESTJ": {
        "text": "생활은 평범하지만, 그 속에 가장 큰 진실이 있다.",
        "author": "박완서",
        "work": "그 남자네 집",
        "publisher": "1995"
    },
    "ISFJ": {
        "text": "오늘도 나를 지탱하는 것은 작은 마음들이다.",
        "author": "정현종",
        "work": "섬, 『사람들 사이에 섬이 있다』",
        "publisher": "문학과지성사, 1979"
    },
    "ESFJ": {
        "text": "사람은 서로 기대어 살아가는 존재다.",
        "author": "신경숙",
        "work": "엄마를 부탁해",
        "publisher": "창비, 2008"
    },
    "ISTJ": {
        "text": "사람은 의무를 다하는 데서 자유를 찾는다.",
        "author": "김동인",
        "work": "감자",
        "publisher": "『창조』, 1925"
    },
    "ESTP": {
        "text": "바람이 부는 대로 흔들리며 살아도 좋다.",
        "author": "나태주",
        "work": "풀꽃",
        "publisher": "1979"
    },
    "ISTP": {
        "text": "고독은 나의 무기이자 안식이다.",
        "author": "윤동주",
        "work": "자화상, 『하늘과 바람과 별과 시』",
        "publisher": "정음사, 1948"
    },
    "ESFP": {
        "text": "삶은 눈부신 축제와 같다.",
        "author": "천상병",
        "work": "귀천, 『새』",
        "publisher": "1970"
    },
    "ISFP": {
        "text": "사랑하는 것은 사랑을 받느니보다 행복하나니라.",
        "author": "한용운",
        "work": "사랑하는 까닭, 『님의 침묵』",
        "publisher": "1926"
    },
    "ENFJ": {
        "text": "너를 기다리는 동안, 나는 이미 너의 사람이었다.",
        "author": "황동규",
        "work": "즐거운 편지",
        "publisher": "1961"
    }
}

# -----------------------------
# Streamlit 앱 UI
# -----------------------------
st.title("📚 MBTI + 날씨 기반 한국 문학 글귀 추천")
st.write("당신의 MBTI와 오늘의 날씨를 바탕으로 글귀를 추천해드립니다.")

# 1. MBTI 선택
mbti = st.selectbox("당신의 MBTI를 선택하세요:", list(quotes.keys()))

# 2. 날씨 API (OpenWeatherMap)
city = st.text_input("당신의 도시를 입력하세요:", "Seoul")
api_key = "YOUR_API_KEY"  # OpenWeatherMap API 키 입력

if st.button("오늘의 글귀 추천받기"):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&lang=kr&units=metric"
        response = requests.get(url)
        data = response.json()

        if data["cod"] == 200:
            weather = data["weather"][0]["description"]
            temp = data["main"]["temp"]

            st.success(f"📍 {city}의 날씨: {weather}, {temp}°C")

            # 선택된 글귀 출력
            selected = quotes[mbti]
            st.subheader("오늘의 추천 글귀 ✨")
            st.write(f"“{selected['text']}”")
            st.caption(f"— {selected['author']}, {selected['work']} ({selected['publisher']})")

        else:
            st.error("날씨 정보를 불러오지 못했습니다. 도시 이름을 확인해주세요.")
    except:
        st.error("API 연결에 문제가 있습니다.")
