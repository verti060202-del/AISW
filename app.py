import streamlit as st
import openai
import os

# Streamlit Secrets에서 API 키 불러오기 (입력란 없음!)
openai.api_key = st.secrets["API_KEY"]

st.set_page_config(page_title="냉장고 속 재료로 만드는 레시피 추천기", page_icon="🍳")
st.title("🍳 냉장고 속 재료로 만드는 맞춤 레시피 추천기")


st.markdown("""
<div style="
    background-color:#E6F7FF;  /* 더 연한 하늘색 */
    padding:15px; 
    border-radius:10px; 
    margin-bottom:15px;
">
    <h2 style="color:#333; margin:0; font-size:24px;">🥕 냉장고 재료 기반 레시피 추천 서비스</h2>
    <p style="margin:5px 0 0; font-size:16px;">남은 재료로 똑똑하게 요리하세요!</p>
</div>
""", unsafe_allow_html=True)



st.write("입력한 재료를 기반으로 만들 수 있는 요리를 추천해주는 간단한 AI 레시피 앱입니다!")

# 3개 선택 옵션
col1, col2, col3 = st.columns(3)

with col1:
    difficulty = st.selectbox("난이도", ["상관 없음", "초급", "중급", "상급"])
with col2:
    meal_type = st.selectbox("식사 유형", ["상관 없음", "아침", "점심", "저녁", "간식"])
with col3:
    time_limit = st.selectbox("조리 시간", ["상관 없음", "10분 이내", "20분 이내", "30분 이내"])

# 재료 입력
ingredients = st.text_input("🥬 냉장고 속 재료를 입력하세요 (예: 계란, 당근, 우유)")

# 버튼 클릭 시 실행
if st.button("레시피 추천 받기"):
    if not ingredients:
        st.error("재료를 입력해주세요!")
    else:
        with st.spinner("AI가 레시피를 만드는 중입니다..."):
            try:
                prompt = f"""
                사용자가 입력한 재료: {ingredients}

                다음 형식으로 매우 현실적이고 꼼꼼하게 작성해줘.

                [재료 분석]
                - 입력된 재료로 가능한 기본 조합 설명 (간단히 3줄)

                [추천 요리 3가지]
                각 요리에 대해:
                1) 요리 이름
                2) 필요한 전체 재료 목록
                3) 부족한 재료 + 가능한 대체재
                4) 조리 난이도 (하/중/상)
                5) 예상 조리 시간
                6) 조리 단계 (최대 5단계, 간단하고 명확하게)

                현실적으로 만들 수 있는 요리만 제공해줘.
                과장하거나 지어내지 마.
                """

                response = openai.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}]
                )

                st.success("완료!")

                recipe_text = response.choices[0].message.content

                # ----------------------------
                # 카드 형태 출력 (간단 버전)
                # ----------------------------
                st.markdown(
                    f"""
                    <div style="
                        background-color: #f9f9f9; 
                        padding: 18px; 
                        border-radius: 12px; 
                        border: 1px solid #ddd;
                        margin-top: 12px;
                    ">
                        <h4>🍽️ 추천 레시피</h4>
                        <pre style="white-space: pre-wrap; font-size: 15px; margin: 0;">
{recipe_text}
                        </pre>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            except Exception as e:
                st.error(f"오류 발생: {e}")
