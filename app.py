import streamlit as st
import pandas as pd
from datetime import datetime
import os
import plotly.express as px

# 파일 저장 설정
FILE_NAME = "survey_data.csv"

# 페이지 설정
st.set_page_config(page_title="AI Literacy 역량 진단", layout="centered")

# --- 1. 설정 ---
# 내부적인 로직(기간 체크)을 위해 날짜 정보는 유지하되 화면 출력만 제거했습니다.
START_DATE = datetime(2026, 1, 1)
END_DATE = datetime(2026, 1, 31)
current_time = datetime.now()

st.title("🤖 AI Literacy 역량 진단")

# [진단 기간] 관련 텍스트 삭제, [진단 목적]만 유지
st.markdown(f"""
### **[진단 목적]**
본 진단은 임직원의 **AI 활용 역량 수준을 객관적으로 파악**하고, 향후 **개인별/직무별 맞춤형 AI 교육 커리큘럼을 수립**하기 위한 기초 자료로 활용됩니다. 
정확한 진단은 회사와 개인의 AI 경쟁력을 높이는 첫걸음입니다. 솔직한 응답 부탁드립니다.
---
""")

# 기간 체크 (화면에는 안 보이지만 기간 외 접속은 차단됨)
if current_time < START_DATE:
    st.warning("아직 진단 기간이 아닙니다.")
    st.stop()
elif current_time > END_DATE:
    st.error("진단 기간이 종료되었습니다.")

# 데이터 로드
if os.path.exists(FILE_NAME):
    existing_data = pd.read_csv(FILE_NAME)
else:
    existing_data = pd.DataFrame()

# --- 2. 기본 정보 입력 ---
st.subheader("📋 기본 정보")
col1, col2 = st.columns(2)
with col1:
    name = st.text_input("성함", placeholder="홍길동")
    emp_no = st.text_input("사번", placeholder="7자리 숫자 입력", max_chars=7)
with col2:
    dept = st.selectbox("소속 실", ["선택하세요", "경영지원실", "경영기획실", "서비스지원실", "안전보건실", "영업지원실", "대표직속", "Network운용본부", "수도권1본부", "수도권2본부", "중부본부", "서부본부", "부산본부", "대구본부"])
    position = st.selectbox("직책", ["선택하세요", "구성원(팀/지점)", "Staff(기획/HR/재무 등)", "리더(팀장/지점장/파트장)", "임원"])

# 중복 체크
already_submitted = False
if not existing_data.empty and emp_no:
    if str(emp_no) in existing_data['사번'].astype(str).values:
        already_submitted = True
        st.warning(f"⚠️ 사번 {emp_no}는 이미 제출된 기록이 있습니다.")

# --- 진단 문항 영역 ---
rating_options = ["1.전혀 그렇지 않다", "2.그렇지 않다", "3.보통이다", "4.그렇다", "5.매우 그렇다"]

if position != "선택하세요" and dept != "선택하세요" and not already_submitted:
    st.write("---")
    
    # 질문 서식 디자인 함수
    def question_style(text):
        st.markdown(f"""
            <div style="background-color: #eef2ff; padding: 10px 15px; border-radius: 5px; border-left: 5px solid #818cf8; margin-bottom: 10px; margin-top: 15px;">
                <span style="font-size: 1.02em; font-weight: 600; color: #374151;">{text}</span>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("##### 📢 진단 응답 안내")
    st.caption("모든 문항을 읽고 본인의 생각과 가장 가까운 점수를 선택해 주세요. (5점 만점)")
    st.write("")

    ans = {}
    
    # --- [공통 문항] ---
    st.subheader("🟦 [공통] AI 기본 이해 및 활용")
    
    question_style("1. 생성형 AI가 어떤 원리로 결과를 만들어내는지 개념적으로 이해하고 있다.")
    ans['공통_A1'] = st.radio("Q1", rating_options, horizontal=True, label_visibility="collapsed", index=None)
    
    question_style("2. 생성형 AI가 잘하는 영역과 한계가 무엇인지 알고 있다.")
    ans['공통_A2'] = st.radio("Q2", rating_options, horizontal=True, label_visibility="collapsed", index=None)
    
    question_style("3. AI 결과물은 항상 검증이 필요하다는 점을 인지하고 있다.")
    ans['공통_A3'] = st.radio("Q3", rating_options, horizontal=True, label_visibility="collapsed", index=None)
    
    question_style("4. 내 업무 중 AI로 보조하거나 대체할 수 있는 업무가 있다고 생각한다.")
    ans['공통_B1'] = st.radio("Q4", rating_options, horizontal=True, label_visibility="collapsed", index=None)
    
    question_style("5. AI 활용이 업무 효율을 높일 수 있다고 인식하고 있다.")
    ans['공통_B2'] = st.radio("Q5", rating_options, horizontal=True, label_visibility="collapsed", index=None)
    
    question_style("6. AI 활용 시 보안·정보 유출에 대한 기본적인 주의사항을 알고 있다.")
    ans['공통_B3'] = st.radio("Q6", rating_options, horizontal=True, label_visibility="collapsed", index=None)
    
    question_style("7. 원하는 결과를 얻기 위해 질문을 수정·보완해 본 경험이 있다.")
    ans['공통_C1'] = st.radio("Q7", rating_options, horizontal=True, label_visibility="collapsed", index=None)
    
    question_style("8. AI에게 역할, 조건, 출력 형식을 지정해 요청할 수 있다.")
    ans['공통_C2'] = st.radio("Q8", rating_options, horizontal=True, label_visibility="collapsed", index=None)
    
    question_style("9. AI의 첫 번째 결과가 만족스럽지 않을 경우 개선을 시도한다.")
    ans['공통_C3'] = st.radio("Q9", rating_options, horizontal=True, label_visibility="collapsed", index=None)

    # --- [직책별 추가 문항] ---
    if position == "Staff(기획/HR/재무 등)":
        st.write("---")
        st.subheader("🟨 [Staff] 업무 자동화 및 도구 활용")
        question_style("10. 내 업무 중 반복적이거나 정형적인 작업을 명확히 구분할 수 있다.")
        ans['Staff_D1'] = st.radio("S10", rating_options, horizontal=True, label_visibility="collapsed", index=None)
        question_style("11. 반복 업무를 줄이기 위해 업무 방식을 바꿔본 경험이 있다.")
        ans['Staff_D2'] = st.radio("S11", rating_options, horizontal=True, label_visibility="collapsed", index=None)
        question_style("12. AI를 활용해 업무 절차를 단순화할 수 있다고 생각한다.")
        ans['Staff_D3'] = st.radio("S12", rating_options, horizontal=True, label_visibility="collapsed", index=None)
        question_style("13. AI를 엑셀, 문서, 보고자료 작성 등 기존 업무툴과 함께 활용해본 경험이 있다.")
        ans['Staff_E1'] = st.radio("S13", rating_options, horizontal=True, label_visibility="collapsed", index=None)
        question_style("14. AI를 활용해 자료 정리, 요약, 초안 작성을 수행할 수 있다.")
        ans['Staff_E2'] = st.radio("S14", rating_options, horizontal=True, label_visibility="collapsed", index=None)
        question_style("15. AI 결과물을 그대로 사용하는 것이 아니라, 업무에 맞게 수정·보완한다.")
        ans['Staff_E3'] = st.radio("S15", rating_options, horizontal=True, label_visibility="collapsed", index=None)

    elif position == "리더(팀장/지점장/파트장)":
        st.write("---")
        st.subheader("🟧 [리더] 조직 관리 및 의사결정")
        question_style("10. AI가 조직의 업무 방식에 미칠 영향을 이해하고 있다.")
        ans['리더_F1'] = st.radio("L10", rating_options, horizontal=True, label_visibility="collapsed", index=None)
        question_style("11. 팀 내 업무 중 AI 적용이 가능한 영역을 식별할 수 있다.")
        ans['리더_F2'] = st.radio("L11", rating_options, horizontal=True, label_visibility="collapsed", index=None)
        question_style("12. 팀원이 AI를 활용해 업무를 수행하는 것을 긍정적으로 인식한다.")
        ans['리더_F3'] = st.radio("L12", rating_options, horizontal=True, label_visibility="collapsed", index=None)
        question_style("13. AI를 활용한 자료나 분석 결과를 의사결정 참고자료로 활용할 수 있다.")
        ans['리더_G1'] = st.radio("L13", rating_options, horizontal=True, label_visibility="collapsed", index=None)
        question_style("14. AI 활용 시 발생할 수 있는 리스크(오류, 편향 등)를 인지하고 있다.")
        ans['리더_G2'] = st.radio("L14", rating_options, horizontal=True, label_visibility="collapsed", index=None)

    elif position == "임원":
        st.write("---")
        st.subheader("🟥 [임원] 전략적 활용 및 의사결정")
        question_style("10. AI 활용이 조직의 경쟁력 강화에 기여할 수 있다고 판단한다.")
        ans['임원_H1'] = st.radio("E10", rating_options, horizontal=True, label_visibility="collapsed", index=None)
        question_style("11. AI 도입 시 비용 대비 효과를 고려한 판단이 가능하다.")
        ans['임원_H2'] = st.radio("E11", rating_options, horizontal=True, label_visibility="collapsed", index=None)
        question_style("12. AI 활용을 위한 조직 차원의 준비 과제를 인식하고 있다.")
        ans['임원_H3'] = st.radio("E12", rating_options, horizontal=True, label_visibility="collapsed", index=None)

    st.write("---")
    st.subheader("📝 의견 수렴")
    question_style("1. 현재 업무 중 AI로 가장 줄이고 싶은 반복 업무는 무엇입니까?")
    ans['주관식_1'] = st.text_area("주관식1", label_visibility="collapsed")
    
    st.write("")
    question_style("2. AI 교육을 통해 가장 기대하는 점은 무엇입니까?")
    ans['주관식_2'] = st.text_area("주관식2", label_visibility="collapsed")

    is_ready = all(v is not None for k, v in ans.items() if k not in ['주관식_1', '주관식_2'])

    if st.button("✅ 진단 완료 및 제출하기", type="primary", use_container_width=True, disabled=not is_ready):
        if not name or len(emp_no) < 7:
            st.error("성함과 사번(7자리)을 정확히 입력해 주세요!")
        else:
            ans.update({'이름': name, '사번': emp_no, '소속': dept, '직책': position, 
                        '제출시간': current_time.strftime('%Y-%m-%d %H:%M:%S'), '제출일자': current_time.strftime('%Y-%m-%d')})
            pd.DataFrame([ans]).to_csv(FILE_NAME, mode='a', header=not os.path.exists(FILE_NAME), index=False, encoding='utf-8-sig')
            st.success("제출이 완료되었습니다!")
            st.balloons()
            st.rerun()