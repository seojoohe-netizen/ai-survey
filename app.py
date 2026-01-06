import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 파일 저장 설정
FILE_NAME = "survey_data.csv"

# 페이지 설정
st.set_page_config(page_title="AI Literacy 역량 진단", layout="centered")

# --- 진단 목적 및 안내 (Comment) ---
st.title("🤖 AI Literacy 역량 진단")
st.info("""
**본 진단은 임직원의 AI 활용 역량을 파악하여 맞춤형 교육 및 지원 체계를 수립하기 위해 실시됩니다.** 응답해주신 내용은 전사 AI 역량 강화 전략 수립 및 직무별 AI 교육 과정 설계의 소중한 기초 자료로 활용됩니다.  
귀하의 솔직한 답변은 조직의 디지털 전환을 앞당기는 큰 힘이 됩니다. (소요 시간: 약 5분)
""")

st.write("---")

# 1. 기본 정보 입력
st.subheader("📋 기본 정보")
col1, col2 = st.columns(2)
with col1:
    name = st.text_input("성함", placeholder="홍길동")
with col2:
    # 요청하신 대로 '일반 직원'을 '구성원(팀/지점)'으로 변경했습니다.
    position = st.selectbox("직책 (대상 구분에 따라 문항이 달라집니다)", 
                          ["선택하세요", "구성원(팀/지점)", "Staff(기획/HR/재무 등)", "리더(팀장/지점장/파트장)", "임원"])

# 5점 척도 옵션
options = ["1.전혀 그렇지 않다", "2.그렇지 않다", "3.보통이다", "4.그렇다", "5.매우 그렇다"]

# 답변을 담을 사전
ans = {}

if position != "선택하세요":
    st.write("---")
    
    # --- 1️⃣ 공통 문항 (전 대상 필수) ---
    st.subheader("🟦 [공통] AI 기본 이해 및 활용")
    ans['공통_A1'] = st.select_slider("1. 생성형 AI가 어떤 원리로 결과를 만들어내는지 개념적으로 이해하고 있다.", options=options, value="3.보통이다")
    ans['공통_A2'] = st.select_slider("2. 생성형 AI가 잘하는 영역과 한계가 무엇인지 알고 있다.", options=options, value="3.보통이다")
    ans['공통_A3'] = st.select_slider("3. AI 결과물은 항상 검증이 필요하다는 점을 인지하고 있다.", options=options, value="3.보통이다")
    
    st.write("")
    ans['공통_B1'] = st.select_slider("4. 내 업무 중 AI로 보조하거나 대체할 수 있는 업무가 있다고 생각한다.", options=options, value="3.보통이다")
    ans['공통_B2'] = st.select_slider("5. AI 활용이 업무 효율을 높일 수 있다고 인식하고 있다.", options=options, value="3.보통이다")
    ans['공통_B3'] = st.select_slider("6. AI 활용 시 보안·정보 유출에 대한 기본적인 주의사항을 알고 있다.", options=options, value="3.보통이다")

    st.write("")
    ans['공통_C1'] = st.select_slider("7. 원하는 결과를 얻기 위해 질문(프롬프트)을 수정·보완해 본 경험이 있다.", options=options, value="3.보통이다")
    ans['공통_C2'] = st.select_slider("8. AI에게 역할, 조건, 출력 형식을 지정해 요청할 수 있다.", options=options, value="3.보통이다")
    ans['공통_C3'] = st.select_slider("9. AI의 첫 번째 결과가 만족스럽지 않을 경우 개선을 시도한다.", options=options, value="3.보통이다")

    # --- 2️⃣ Staff 직무 대상 추가 문항 ---
    if position == "Staff(기획/HR/재무 등)":
        st.write("---")
        st.subheader("🟨 [Staff] 업무 자동화 및 도구 활용")
        ans['Staff_D1'] = st.select_slider("10. 내 업무 중 반복적이거나 정형적인 작업을 명확히 구분할 수 있다.", options=options, value="3.보통이다")
        ans['Staff_D2'] = st.select_slider("11. 반복 업무를 줄이기 위해 업무 방식을 바꿔본 경험이 있다.", options=options, value="3.보통이다")
        ans['Staff_D3'] = st.select_slider("12. AI를 활용해 업무 절차를 단순화할 수 있다고 생각한다.", options=options, value="3.보통이다")
        ans['Staff_E1'] = st.select_slider("13. AI를 엑셀, 문서, 보고자료 작성 등 기존 업무툴과 함께 활용해본 경험이 있다.", options=options, value="3.보통이다")
        ans['Staff_E2'] = st.select_slider("14. AI를 활용해 자료 정리, 요약, 초안 작성을 수행할 수 있다.", options=options, value="3.보통이다")

    # --- 3️⃣ 리더 대상 추가 문항 ---
    elif position == "리더(팀장/지점장/파트장)":
        st.write("---")
        st.subheader("🟧 [리더] 조직 관리 및 의사결정")
        ans['리더_F1'] = st.select_slider("10. AI가 조직의 업무 방식에 미칠 영향을 이해하고 있다.", options=options, value="3.보통이다")
        ans['리더_F2'] = st.select_slider("11. 팀 내 업무 중 AI 적용이 가능한 영역을 식별할 수 있다.", options=options, value="3.보통이다")
        ans['리더_F3'] = st.select_slider("12. 팀원이 AI를 활용해 업무를 수행하는 것을 긍정적으로 인식한다.", options=options, value="3.보통이다")
        ans['리더_G1'] = st.select_slider("13. AI를 활용한 자료나 분석 결과를 의사결정 참고자료로 활용할 수 있다.", options=options, value="3.보통이다")
        ans['리더_G2'] = st.select_slider("14. AI 활용 시 발생할 수 있는 리스크(오류, 편향 등)를 인지하고 있다.", options=options, value="3.보통이다")

    # --- 4️⃣ 임원 대상 추가 문항 ---
    elif position == "임원":
        st.write("---")
        st.subheader("🟥 [임원] 전략적 활용 및 의사결정")
        ans['임원_H1'] = st.select_slider("10. AI 활용이 조직의 경쟁력 강화에 기여할 수 있다고 판단한다.", options=options, value="3.보통이다")
        ans['임원_H2'] = st.select_slider("11. AI 도입 시 비용 대비 효과를 고려한 판단이 가능하다.", options=options, value="3.보통이다")
        ans['임원_H3'] = st.select_slider("12. AI 활용을 위한 조직 차원의 준비 과제를 인식하고 있다.", options=options, value="3.보통이다")

    # --- 5️⃣ 주관식 문항 ---
    st.write("---")
    st.subheader("📝 의견 수렴")
    ans['주관식_1'] = st.text_area("1. 현재 업무 중 AI로 가장 줄이고 싶은 반복 업무는 무엇입니까?")
    ans['주관식_2'] = st.text_area("2. AI 교육을 통해 가장 기대하는 점은 무엇입니까?")

    # 제출 버튼
    st.write("")
    if st.button("✅ 진단 완료 및 제출하기", type="primary", use_container_width=True):
        if not name:
            st.error("성함을 입력해 주세요!")
        else:
            # 최종 데이터 정리
            ans.update({
                '이름': name, 
                '직책': position, 
                '제출시간': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            df = pd.DataFrame([ans])
            
            # 저장 (엑셀 호환을 위해 utf-8-sig 사용)
            df.to_csv(FILE_NAME, mode='a', header=not os.path.exists(FILE_NAME), index=False, encoding='utf-8-sig')
            
            st.success(f"{name}님, 소중한 응답 감사합니다! 제출이 완료되었습니다.")
            st.balloons()
else:
    st.warning("위에서 성함을 입력하고 직책을 선택하시면 진단 문항이 나타납니다.")