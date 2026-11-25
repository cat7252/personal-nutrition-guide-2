
import streamlit as st

# --------------------------------
# 1. 페이지 기본 설정
# --------------------------------
st.set_page_config(
    page_title="영양제 추천 가이드",
    page_icon="💊",
    layout="centered"
)

st.title("💊 개인 증상별 맞춤 영양제 추천 가이드")
st.write("나이와 현재 증상을 입력하면 관련 영양 성분을 추천해 주는 프로그램입니다.")

st.divider()

# --------------------------------
# 2. 증상별 영양제 데이터 리스트
# --------------------------------
nutrition_data = [
    {
        "증상": "피로 및 무기력",
        "영양제": "비타민 B군",
        "이유": "에너지 대사에 관여하는 영양소입니다.",
        "개선 정보": "정상적인 에너지 대사에 도움을 줍니다.",
        "부작용": "과다 섭취 시 메스꺼움, 속쓰림 등이 나타날 수 있으며 비타민 B6를 장기간 과다 섭취하면 신경 손상이 발생할 수 있습니다."
    },
    {
        "증상": "눈의 피로",
        "영양제": "루테인",
        "이유": "눈 건강과 관련하여 알려진 성분입니다.",
        "개선 정보": "눈 건강 관리에 활용되는 성분입니다.",
        "부작용": "제품이나 개인에 따라 속 불편함 등 위장 증상이 나타날 수 있습니다."
    },
    {
        "증상": "수면 부족",
        "영양제": "마그네슘",
        "이유": "근육과 신경 기능에 필요한 영양소입니다.",
        "개선 정보": "정상적인 신경 및 근육 기능 유지에 필요합니다.",
        "부작용": "과다 섭취 시 설사, 메스꺼움, 복통 등이 나타날 수 있습니다."
    },
    {
        "증상": "면역력 관리",
        "영양제": "비타민 C",
        "이유": "항산화 작용과 정상적인 면역 기능에 관여합니다.",
        "개선 정보": "정상적인 면역 기능 유지에 도움을 줍니다.",
        "부작용": "과다 섭취 시 설사, 메스꺼움, 복통 등이 나타날 수 있습니다."
    },
    {
        "증상": "뼈 건강",
        "영양제": "칼슘",
        "이유": "뼈와 치아를 구성하는 주요 영양소입니다.",
        "개선 정보": "뼈와 치아의 형성 및 유지에 필요합니다.",
        "부작용": "과다 섭취 시 변비, 복부 팽만감 등이 나타날 수 있으며 일부 사람에게 신장 결석 위험이 높아질 수 있습니다."
    },
    {
        "증상": "근육 피로",
        "영양제": "마그네슘",
        "이유": "정상적인 근육 기능에 필요한 영양소입니다.",
        "개선 정보": "정상적인 근육 기능 유지에 필요합니다.",
        "부작용": "과다 섭취 시 설사, 메스꺼움, 복통 등이 나타날 수 있습니다."
    },
    {
        "증상": "피부 건강",
        "영양제": "비타민 C",
        "이유": "콜라겐 합성에 필요한 영양소입니다.",
        "개선 정보": "결합조직 형성과 기능 유지에 필요합니다.",
        "부작용": "과다 섭취 시 설사, 메스꺼움, 복통 등이 나타날 수 있습니다."
    }
]

# --------------------------------
# 3. 사용자 입력 받기
# --------------------------------
st.subheader("① 나이 입력")

age = st.number_input(
    "나이를 입력하세요.",
    min_value=1,
    max_value=120,
    value=20,
    step=1
)

st.divider()

st.subheader("② 증상 입력")
st.write("현재 개선하고 싶은 증상을 선택하세요.")

symptom_list = [
    "피로 및 무기력",
    "눈의 피로",
    "수면 부족",
    "면역력 관리",
    "뼈 건강",
    "근육 피로",
    "피부 건강"
]

selected_symptoms = []

for symptom in symptom_list:
    if st.checkbox(symptom, key=symptom):
        selected_symptoms.append(symptom)

# --------------------------------
# 4. 증상 강도 입력
# --------------------------------
st.divider()
st.subheader("③ 증상 강도 선택")

severity_data = {}

if selected_symptoms:
    for symptom in selected_symptoms:
        severity = st.slider(
            f"{symptom}의 증상 강도",
            min_value=1,
            max_value=5,
            value=3,
            key=f"severity_{symptom}"
        )

        severity_data[symptom] = severity

    st.caption("1 = 약함 / 2 = 조금 약함 / 3 = 보통 / 4 = 강함 / 5 = 매우 강함")
else:
    st.info("먼저 해당하는 증상을 선택해 주세요.")

st.divider()

# --------------------------------
# 5. 분석 함수 정의
# --------------------------------
def analyze_symptoms(age, severity_data):

    results = []
    supplement_scores = {}

    for symptom, severity in severity_data.items():

        for item in nutrition_data:

            if item["증상"] == symptom:

                results.append({
                    "증상": symptom,
                    "증상 강도": severity,
                    "추천 영양제": item["영양제"],
                    "추천 이유": item["이유"],
                    "관련 정보": item["개선 정보"],
                    "부작용": item["부작용"]
                })

                # 영양제별 점수 계산
                supplement = item["영양제"]

                if supplement not in supplement_scores:
                    supplement_scores[supplement] = 0

                supplement_scores[supplement] += severity

    return results, supplement_scores


# --------------------------------
# 6. 분석 버튼 및 결과 출력
# --------------------------------
if st.button("🔍 증상 분석하기", use_container_width=True):

    if len(selected_symptoms) == 0:

        st.warning("최소 한 가지 이상의 증상을 선택해 주세요.")

    else:

        results, scores = analyze_symptoms(
            age,
            severity_data
        )

        st.success("증상 분석이 완료되었습니다!")

        st.divider()

        # 나이별 안내
        st.subheader("👤 사용자 정보")
        st.write(f"입력한 나이: **{age}세**")
        st.write(f"선택한 증상: **{len(selected_symptoms)}개**")

        if age < 19:
            st.warning(
                "성장기에는 영양제 선택과 섭취에 특별한 주의가 필요합니다. "
                "보호자 및 의료 전문가와 상담하세요."
            )
        elif age >= 65:
            st.info(
                "고령자는 복용 중인 약이나 건강 상태를 고려하여 "
                "전문가와 상담하는 것이 좋습니다."
            )

        # 추천 영양제 출력
        st.subheader("💊 추천 영양제")

        sorted_scores = sorted(
            scores.items(),
            key=lambda x: x[1],
            reverse=True
        )

        for supplement, score in sorted_scores:

            st.markdown(
                f"### ⭐ {supplement}"
            )

            st.write(
                f"선택한 관련 증상의 강도 합계: {score}점"
            )

        # 결과 테이블
        st.divider()
        st.subheader("📊 증상별 분석 결과")

        st.dataframe(
            results,
            use_container_width=True,
            hide_index=True
        )

        # 결과 문장 출력
        st.divider()
        st.subheader("📝 맞춤 분석 결과")

        for result in results:

            st.write(
                f"**{result['증상']}** 증상의 강도는 "
                f"{result['증상 강도']}점이며, "
                f"관련 영양 성분으로 "
                f"**{result['추천 영양제']}**를 소개합니다."
            )

            st.caption(result["관련 정보"])

        # 영양제별 부작용 출력
        st.divider()
        st.subheader("⚠️ 영양제별 부작용 안내")

        for result in results:

            st.markdown(
                f"**{result['추천 영양제']} "
                f"({result['증상']})**"
            )

            st.warning(result["부작용"])

        st.divider()

        st.info(
            "※ 이 프로그램은 학습용 영양 정보 안내 프로그램입니다. "
            "증상만으로 영양 결핍이나 질환을 진단할 수 없으며, "
            "영양제의 복용 여부와 용량은 식사 상태, 건강 상태, "
            "복용 중인 약 등을 고려하여 전문가와 상담해야 합니다."
        )

else:
    st.info("증상을 선택하고 '증상 분석하기' 버튼을 눌러주세요.")
