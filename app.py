import streamlit as st
import pandas as pd
from datetime import datetime
import os
import plotly.express as px

# 파일 저장 설정
FILE_NAME = "survey_data.csv"

# 페이지 설정
st.set_page_config(page_title="AI Literacy 역량 진단", layout="centered")

# --- 1. 진단 기간 설정 ---
START_DATE = datetime(2026, 1, 1)
END_DATE = datetime(2026, 1, 31)
current_time = datetime.now()

st.title("🤖 AI Literacy 역량 진단")
st.info(f"**진단 기간:** {START_DATE.strftime('%Y-%m-%d')} ~ {END_DATE.strftime('%Y-%m-%d')}")

# 기간 체크
if current_time < START_DATE:
    st.warning("아직 진단 기간이 아닙니다.")
    st.stop()
elif current_time > END_DATE:
    st.error("진단 기간이 종료되었습니다.")

# 데이터 로드 (중복 체크용)
if os.path.exists(FILE_NAME):
    existing_data = pd.read_csv(FILE_NAME)
else:
    existing_data = pd.DataFrame()

st.write("---")

# --- 2. 기본 정보 입력 ---
st.subheader("📋 기본 정보")
col1, col2 = st.columns(2)
with col1:
    name = st.text_input("성함", placeholder="홍길동")
    emp_no = st.text_input("사번", placeholder="8자리 입력")
with col2:
    dept = st.selectbox("소속 실", ["선택하세요", "경영지원실", "경영기획실", "서비스지원실", "안전보건실", "영업지원실", "대표직속", "Network운용본부", "수도권1본부", "수도권2본부", "중부본부", "서부본부", "부산본부", "대구본부"])
    position = st.selectbox("직책", ["선택하세요", "구성원(팀/지점)", "Staff(기획/HR/재무 등)", "리더(팀장/지점장/파트장)", "임원"])

# 🚫 중복 제출 체크
already_submitted = False
if not existing_data.empty and emp_no:
    if str(emp_no) in existing_data['사번'].astype(str).values:
        already_submitted = True
        st.warning(f"⚠️ 사번 {emp_no}는 이미 제출된 기록이 있습니다.")

# --- 진단 문항 영역 ---
# 5점 척도 옵션 (기본 선택값 방지를 위해 앞에 빈 값 추가)
rating_options = ["선택하세요", "1.전혀 그렇지 않다", "2.그렇지 않다", "3.보통이다", "4.그렇다", "5.매우 그렇다"]

if position != "선택하세요" and dept != "선택하세요" and not already_submitted:
    st.write("---")
    
    # 📢 5점 척도 안내 문구 (Formal 한 표현)
    st.markdown("""
    <div style="background-color: #f8f9fa; padding: 15px; border-left: 5px solid #007bff; border-radius: 5px;">
        <strong>[진단 응답 안내]</strong><br>
        본 진단 문항은 5점 척도로 구성되어 있습니다. 각 문항을 읽고 본인의 평소 생각 및 행동과 가장 일치하는 항목을 선택해 주시기 바랍니다.<br>
        (1: 전혀 그렇지 않다 ~ 5: 매우 그렇다)
    </div>
    """, unsafe_allow_html=True)
    st.write("")

    ans = {}
    
    # --- [공통 문항] ---
    st.subheader("🟦 [공통] AI 기본 이해 및 활용")
    ans['공통_A1'] = st.selectbox("1. 생성형 AI가 어떤 원리로 결과를 만들어내는지 개념적으로 이해하고 있다.", options=rating_options)
    ans['공통_A2'] = st.selectbox("2. 생성형 AI가 잘하는 영역과 한계가 무엇인지 알고 있다.", options=rating_options)
    ans['공통_A3'] = st.selectbox("3. AI 결과물은 항상 검증이 필요하다는 점을 인지하고 있다.", options=rating_options)
    ans['공통_B1'] = st.selectbox("4. 내 업무 중 AI로 보조하거나 대체할 수 있는 업무가 있다고 생각한다.", options=rating_options)
    ans['공통_B2'] = st.selectbox("5. AI 활용이 업무 효율을 높일 수 있다고 인식하고 있다.", options=rating_options)
    ans['공통_B3'] = st.selectbox("6. AI 활용 시 보안·정보 유출에 대한 기본적인 주의사항을 알고 있다.", options=rating_options)
    ans['공통_C1'] = st.selectbox("7. 원하는 결과를 얻기 위해 질문을 수정·보완해 본 경험이 있다.", options=rating_options)
    ans['공통_C2'] = st.selectbox("8. AI에게 역할, 조건, 출력 형식을 지정해 요청할 수 있다.", options=rating_options)
    ans['공통_C3'] = st.selectbox("9. AI의 첫 번째 결과가 만족스럽지 않을 경우 개선을 시도한다.", options=rating_options)

    # --- [직책별 추가 문항] --- (문장 변질 없이 유지)
    if position == "Staff(기획/HR/재무 등)":
        st.write("---")
        st.subheader("🟨 [Staff] 업무 자동화 및 도구 활용")
        ans['Staff_D1'] = st.selectbox("10. 내 업무 중 반복적이거나 정형적인 작업을 명확히 구분할 수 있다.", options=rating_options)
        ans['Staff_D2'] = st.selectbox("11. 반복 업무를 줄이기 위해 업무 방식을 바꿔본 경험이 있다.", options=rating_options)
        ans['Staff_D3'] = st.selectbox("12. AI를 활용해 업무 절차를 단순화할 수 있다고 생각한다.", options=rating_options)
        ans['Staff_E1'] = st.selectbox("13. AI를 엑셀, 문서, 보고자료 작성 등 기존 업무툴과 함께 활용해본 경험이 있다.", options=rating_options)
        ans['Staff_E2'] = st.selectbox("14. AI를 활용해 자료 정리, 요약, 초안 작성을 수행할 수 있다.", options=rating_options)
        ans['Staff_E3'] = st.selectbox("15. AI 결과물을 그대로 사용하는 것이 아니라, 업무에 맞게 수정·보완한다.", options=rating_options)

    elif position == "리더(팀장/지점장/파트장)":
        st.write("---")
        st.subheader("🟧 [리더] 조직 관리 및 의사결정")
        ans['리더_F1'] = st.selectbox("10. AI가 조직의 업무 방식에 미칠 영향을 이해하고 있다.", options=rating_options)
        ans['리더_F2'] = st.selectbox("11. 팀 내 업무 중 AI 적용이 가능한 영역을 식별할 수 있다.", options=rating_options)
        ans['리더_F3'] = st.selectbox("12. 팀원이 AI를 활용해 업무를 수행하는 것을 긍정적으로 인식한다.", options=rating_options)
        ans['리더_G1'] = st.selectbox("13. AI를 활용한 자료나 분석 결과를 의사결정 참고자료로 활용할 수 있다.", options=rating_options)
        ans['리더_G2'] = st.selectbox("14. AI 활용 시 발생할 수 있는 리스크(오류, 편향 등)를 인지하고 있다.", options=rating_options)

    elif position == "임원":
        st.write("---")
        st.subheader("🟥 [임원] 전략적 활용 및 의사결정")
        ans['임원_H1'] = st.selectbox("10. AI 활용이 조직의 경쟁력 강화에 기여할 수 있다고 판단한다.", options=rating_options)
        ans['임원_H2'] = st.selectbox("11. AI 도입 시 비용 대비 효과를 고려한 판단이 가능하다.", options=rating_options)
        ans['임원_H3'] = st.selectbox("12. AI 활용을 위한 조직 차원의 준비 과제를 인식하고 있다.", options=rating_options)

    # --- [주관식] ---
    st.write("---")
    st.subheader("📝 의견 수렴")
    ans['주관식_1'] = st.text_area("1. 현재 업무 중 AI로 가장 줄이고 싶은 반복 업무는 무엇입니까?")
    ans['주관식_2'] = st.text_area("2. AI 교육을 통해 가장 기대하는 점은 무엇입니까?")

    # 🛑 필수 항목 체크 (선택하세요가 하나라도 있으면 제출 방지)
    is_ready = all(value != "선택하세요" for value in ans.values())

    if st.button("✅ 진단 완료 및 제출하기", type="primary", use_container_width=True, disabled=not is_ready):
        if not name or not emp_no:
            st.error("성함과 사번을 입력해 주세요!")
        elif not is_ready:
            st.warning("아직 선택하지 않은 문항이 있습니다. 모든 문항을 체크해 주세요.")
        else:
            ans.update({
                '이름': name, '사번': emp_no, '소속': dept, '직책': position, 
                '제출시간': current_time.strftime('%Y-%m-%d %H:%M:%S'),
                '제출일자': current_time.strftime('%Y-%m-%d')
            })
            pd.DataFrame([ans]).to_csv(FILE_NAME, mode='a', header=not os.path.exists(FILE_NAME), index=False, encoding='utf-8-sig')
            st.success("제출이 완료되었습니다!")
            st.balloons()
            st.rerun()
    
    if not is_ready:
        st.caption("⚠️ 모든 문항에 대한 답변을 선택하셔야 제출 버튼이 활성화됩니다.")

# --- 3. 관리자 대시보드 (리포트 기능) ---
st.write("---")
with st.expander("🔐 관리자 전용 대시보드"):
    pw = st.text_input("관리자 비밀번호", type="password")
    if pw == "940930":
        if not existing_data.empty:
            st.subheader("📊 실시간 분석 리포트")
            daily_data = existing_data.groupby('제출일자').size().reset_index(name='참여자수')
            st.plotly_chart(px.line(daily_data, x='제출일자', y='참여자수', markers=True))
            
            # 요약 텍스트 분석
            total_count = len(existing_data)
            report_text = f"--- AI 역량 진단 요약 리포트 ---\n총 참여: {total_count}명\n부서수: {existing_data['소속'].nunique()}개"
            st.text_area("리포트 요약", report_text)
            
            st.download_button("📄 분석 결과 리포트(.txt) 내려받기", report_text, f"Report_{current_time.strftime('%m%d')}.txt", use_container_width=True)
            csv = existing_data.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')
            st.download_button("📥 전체 결과(Excel) 다운로드", csv, f"AI_Data_{current_time.strftime('%m%d')}.csv", use_container_width=True)
            st.dataframe(existing_data)
        else:
            st.warning("데이터가 없습니다.")