import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random

# 페이지 기본 설정
st.set_page_config(
    page_title="고등 수학: 삼각함수 학습 및 퀴즈",
    page_icon="📐",
    layout="wide"
)

# 한글 및 마이너스 기호 깨짐 방지
plt.rcParams['axes.unicode_minus'] = False

# ==========================================
# 숫자를 깔끔한 수식 텍스트로 변환하는 함수
# ==========================================
def fmt_num(val):
    """정수면 소수점 제거, 소수면 필요 소수점만 표시"""
    val = round(val, 2)
    if val == int(val):
        return f"{int(val)}"
    return f"{val}"

def make_formula_str(func, a, b, c, d):
    """삼각함수를 깔끔한 LaTeX 수식 문장으로 조합 (계수 1은 그대로 표시)"""
    a_str = fmt_num(a)

    # x-c (x축 평행이동) 처리
    b_str = fmt_num(b)
    if c == 0:
        inner_str = f"{b_str}x"
    else:
        c_val = fmt_num(abs(c))
        c_sign = "-" if c > 0 else "+"
        c_text = f"\\pi" if c_val == "1" else f"{c_val}\\pi"
        
        if b == 1:
            inner_str = f"x {c_sign} {c_text}"
        elif b == -1:
            inner_str = f"-x {c_sign} {c_text}"
        else:
            inner_str = f"{b_str}(x {c_sign} {c_text})"

    # d (y축 평행이동) 처리
    if d == 0:
        d_str = ""
    elif d > 0:
        d_str = f" + {fmt_num(d)}"
    else:
        d_str = f" - {fmt_num(abs(d))}"

    return f"y = {a_str} \\cdot \\{func}({inner_str}){d_str}"


st.title("📐 고등학생을 위한 삼각함수 학습 & 퀴즈 인터랙티브 웹")
st.write("개념 학습 탭에서 원하는 값을 직접 입력해 그래프를 관찰하고, 퀴즈 탭에서 직접 실력을 점검해 보세요!")

# 탭 구성: 개념 학습 / 퀴즈
tab1, tab2 = st.tabs(["📊 개념 학습 & 그래프 시각화", "🧩 삼각함수 실력 점검 퀴즈"])

# ==========================================
# TAB 1: 개념 학습 & 그래프 시각화
# ==========================================
with tab1:
    st.sidebar.header("⚙️ 개념 학습 파라미터 입력")

    # 1. 삼각함수 선택
    func_choice = st.sidebar.selectbox(
        "학습할 삼각함수를 선택하세요",
        ["Sine (sin)", "Cosine (cos)", "Tangent (tan)"]
    )

    # 2. 파라미터 입력
    st.sidebar.subheader("파라미터 입력: $y = a \\cdot f(b(x - c)) + d$")

    a = st.sidebar.number_input("진폭/확대 (a)", value=1.0, step=0.5, key="a_input")
    b = st.sidebar.number_input("주기 조절 (b)", value=1.0, step=0.5, key="b_input")
    c = st.sidebar.number_input("x축 평행이동 (c: $\\pi$ 단위)", value=0.0, step=0.25, key="c_input")
    d = st.sidebar.number_input("y축 평행이동 (d)", value=0.0, step=0.5, key="d_input")

    # x 범위 설정 (-2π ~ 2π)
    x = np.linspace(-2 * np.pi, 2 * np.pi, 1000)

    # 선택한 함수명 정제
    func_name = "sin" if "sin" in func_choice.lower() else ("cos" if "cos" in func_choice.lower() else "tan")

    # 수식 라텍스 문자열 생성
    latex_formula = make_formula_str(func_name, a, b, c, d)

    # 삼각함수 계산
    if func_name == "sin":
        y_base = np.sin(x)
        y_mod = a * np.sin(b * (x - c * np.pi)) + d
        period = f"{fmt_num(2/abs(b))} $\\pi$" if b != 0 else "정의되지 않음 (b=0)"
        amplitude = f"{fmt_num(abs(a))}"
    elif func_name == "cos":
        y_base = np.cos(x)
        y_mod = a * np.cos(b * (x - c * np.pi)) + d
        period = f"{fmt_num(2/abs(b))} $\\pi$" if b != 0 else "정의되지 않음 (b=0)"
        amplitude = f"{fmt_num(abs(a))}"
    else:
        y_base = np.tan(x)
        y_mod = a * np.tan(b * (x - c * np.pi)) + d
        y_base[np.abs(y_base) > 10] = np.nan
        y_mod[np.abs(y_mod) > 10] = np.nan
        period = f"{fmt_num(1/abs(b))} $\\pi$" if b != 0 else "정의되지 않음 (b=0)"
        amplitude = "없음 (최대/최소값 없음)"

    # 레이아웃 분할
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("📊 그래프")
        
        # 식 크기를 크게 표시 (HTML font-size 활용)
        st.markdown(
            f"<h2 style='text-align: center; color: #333333;'>${latex_formula}$</h2>", 
            unsafe_allow_html=True
        )
        st.write("") # 약간의 여백
        
        fig, ax = plt.subplots(figsize=(10, 5))
        # 그래프 범례 한글 깨짐 방지를 위해 LaTeX 수식 표기 사용
        ax.plot(x, y_base, label=r"Base $y=f(x)$", color="gray", linestyle="--", alpha=0.6)
        ax.plot(x, y_mod, label=r"Modified $y=g(x)$", color="#007ACC", linewidth=2.5)
        
        ax.axhline(0, color='black', linewidth=1)
        ax.axvline(0, color='black', linewidth=1)
        
        y_limit = max(abs(a) + abs(d) + 2, 5)
        ax.set_ylim(-y_limit, y_limit)
        ax.set_xlim(-2 * np.pi, 2 * np.pi)
        
        xticks = [-2*np.pi, -1.5*np.pi, -np.pi, -0.5*np.pi, 0, 0.5*np.pi, np.pi, 1.5*np.pi, 2*np.pi]
        xtick_labels = [r'$-2\pi$', r'$-\frac{3}{2}\pi$', r'$-\pi$', r'$-\frac{1}{2}\pi$', r'$0$', 
                        r'$\frac{1}{2}\pi$', r'$\pi$', r'$\frac{3}{2}\pi$', r'$2\pi$']
        ax.set_xticks(xticks)
        ax.set_xticklabels(xtick_labels)
        
        ax.grid(True, linestyle=":", alpha=0.6)
        ax.legend(loc="upper right")
        
        st.pyplot(fig)

    with col2:
        st.subheader("💡 입력값 분석 정보")
        st.metric(label="현재 함수 주기 (Period)", value=period)
        st.metric(label="진폭 (Amplitude)", value=amplitude)
        
        st.markdown("---")
        st.markdown("### 📝 수식 핵심 규칙")
        st.latex(r"y = a \cdot f(b(x - c)) + d")
        
        st.markdown(f"""
        - **a = {fmt_num(a)}**: 진폭 조절 (절댓값 |a|)
        - **b = {fmt_num(b)}**: 주기 조절 (주기 = 기본주기 / |b|)
        - **c = {fmt_num(c)}**: x축 평행이동 (+{fmt_num(c)}π 만큼)
        - **d = {fmt_num(d)}**: y축 평행이동 (+{fmt_num(d)} 만큼)
        """)

# ==========================================
# TAB 2: 자율 퀴즈 모드
# ==========================================
with tab2:
    st.subheader("🧩 무작위 삼각함수 퀴즈")
    st.write("주어진 삼각함수 식을 보고 **진폭**, **주기(소수 둘째자리까지)**, **y축 평행이동 값**을 맞춰보세요!")

    # 세션 상태 초기화 (문제 세팅용)
    if "quiz_a" not in st.session_state:
        st.session_state.quiz_a = random.choice([1, 2, 3, 4, 5])
        st.session_state.quiz_b = random.choice([1, 2, 4])
        st.session_state.quiz_d = random.choice([-3, -2, -1, 1, 2, 3])
        st.session_state.quiz_func = random.choice(["sin", "cos"])

    q_a = st.session_state.quiz_a
    q_b = st.session_state.quiz_b
    q_d = st.session_state.quiz_d
    q_func = st.session_state.quiz_func

    # 문제 출력
    quiz_formula = make_formula_str(q_func, q_a, q_b, 0, q_d)
    st.info("### ❓ 문제: 아래 함수 식의 특성을 구하세요.")
    
    # 퀴즈 식 크기도 크게 변경
    st.markdown(
        f"<h2 style='text-align: center; color: #1E3A8A;'>${quiz_formula}$</h2>", 
        unsafe_allow_html=True
    )
    st.write("")

    col_q1, col_q2, col_q3 = st.columns(3)
    
    with col_q1:
        user_amp = st.number_input("1. 진폭 (Amplitude)", value=1.0, step=1.0, key="quiz_amp_input")
    with col_q2:
        user_period_coeff = st.number_input("2. 주기 (π 앞의 계수값, 예: 2π면 2 입력)", value=1.0, step=0.5, key="quiz_period_input")
    with col_q3:
        user_d = st.number_input("3. y축 평행이동 값 (d)", value=0.0, step=1.0, key="quiz_d_input")

    # 정답 계산
    ans_amp = float(q_a)
    ans_period_coeff = 2.0 / q_b  # 2π/b 이므로 π 앞의 계수
    ans_d = float(q_d)

    col_btn1, col_btn2 = st.columns([1, 4])
    
    with col_btn1:
        submit_btn = st.button("정답 확인 🎯")

    with col_btn2:
        if st.button("새 문제 생성 🔄"):
            st.session_state.quiz_a = random.choice([1, 2, 3, 4, 5])
            st.session_state.quiz_b = random.choice([1, 2, 4])
            st.session_state.quiz_d = random.choice([-3, -2, -1, 1, 2, 3])
            st.session_state.quiz_func = random.choice(["sin", "cos"])
            st.rerun()

    # 정답 제출 및 채점 결과/해설 출력
    if submit_btn:
        st.markdown("---")
        st.markdown("### 📋 채점 결과 및 상세 해설")

        correct_all = True

        # 1. 진폭 검증 및 해설
        if abs(user_amp - ans_amp) < 0.01:
            st.success(f"✅ **1. 진폭 (정답):** 입력값 `{fmt_num(user_amp)}`이(가) 맞습니다!")
        else:
            correct_all = False
            st.error(f"❌ **1. 진폭 (오답):** 입력값 `{fmt_num(user_amp)}`은(는) 오답입니다.")
            st.warning(f"""
            **💡 오답 원인 및 해설:**
            - 삼각함수 y = a · f(bx) + d에서 진폭은 삼각함수의 앞 계수인 **|a|**로 결정됩니다.
            - 이 문제에서 계수 a = {fmt_num(q_a)}이므로 진폭은 **{fmt_num(ans_amp)}**입니다.
            """)

        # 2. 주기 검증 및 해설
        if abs(user_period_coeff - ans_period_coeff) < 0.01:
            st.success(f"✅ **2. 주기 (정답):** 입력값 `{fmt_num(user_period_coeff)}`π가 맞습니다!")
        else:
            correct_all = False
            st.error(f"❌ **2. 주기 (오답):** 입력값 `{fmt_num(user_period_coeff)}`π은(는) 오답입니다.")
            st.warning(f"""
            **💡 오답 원인 및 해설:**
            - sin과 cos 함수 기본 주기는 2π이며, x 앞에 계수 b가 붙을 경우 주기는 **2π / |b|**가 됩니다.
            - 이 문제에서 x의 계수 b = {fmt_num(q_b)}이므로, 주기 공식은 2π / {fmt_num(q_b)} = {fmt_num(ans_period_coeff)}π 입니다.
            - 따라서 π 앞의 계수는 **{fmt_num(ans_period_coeff)}**이어야 합니다.
            """)

        # 3. y축 평행이동 검증 및 해설
        if abs(user_d - ans_d) < 0.01:
            st.success(f"✅ **3. y축 평행이동 (정답):** 입력값 `{fmt_num(user_d)}`이(가) 맞습니다!")
        else:
            correct_all = False
            st.error(f"❌ **3. y축 평행이동 (오답):** 입력값 `{fmt_num(user_d)}`은(는) 오답입니다.")
            st.warning(f"""
            **💡 오답 원인 및 해설:**
            - 수식 뒤에 더해지거나 빼지는 상수항 d는 그래프 전체를 위/아래로 이동시키는 **y축 평행이동량**입니다.
            - 이 문제에서 y축 방향 평행이동량은 **{fmt_num(ans_d)}**입니다.
            """)

        # 모두 맞췄을 때 이벤트
        if correct_all:
            st.balloons()
            st.success("🎉 축하합니다! 모든 항목을 정확하게 계산하셨습니다.")
