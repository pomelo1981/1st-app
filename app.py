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

    # 2. 숫자 입력 방식(st.number_input) 파라미터 설정
    st.sidebar.subheader("파라미터 입력: $y = a \\cdot f(b(x - c)) + d$")

    a = st.sidebar.number_input("진폭/확대 (a)", value=1.0, step=0.1, format="%.2f", key="a_input")
    b = st.sidebar.number_input("주기 조절 (b)", value=1.0, step=0.1, format="%.2f", key="b_input")
    c = st.sidebar.number_input("x축 평행이동 (c: $\\pi$ 단위)", value=0.0, step=0.25, format="%.2f", key="c_input")
    d = st.sidebar.number_input("y축 평행이동 (d)", value=0.0, step=0.5, format="%.2f", key="d_input")

    # x 범위 설정 (-2π ~ 2π)
    x = np.linspace(-2 * np.pi, 2 * np.pi, 1000)

    # 함수 선택에 따른 처리
    if "sin" in func_choice.lower():
        y_base = np.sin(x)
        y_mod = a * np.sin(b * (x - c * np.pi)) + d
        title_str = f"$y = {a:.2f} \\cdot \\sin({b:.2f}(x - {c:.2f}\\pi)) + {d:.2f}$"
        period = f"{2/abs(b):.2f} $\\pi$" if b != 0 else "정의되지 않음 (b=0)"
        amplitude = f"{abs(a):.2f}"
    elif "cos" in func_choice.lower():
        y_base = np.cos(x)
        y_mod = a * np.cos(b * (x - c * np.pi)) + d
        title_str = f"$y = {a:.2f} \\cdot \\cos({b:.2f}(x - {c:.2f}\\pi)) + {d:.2f}$"
        period = f"{2/abs(b):.2f} $\\pi$" if b != 0 else "정의되지 않음 (b=0)"
        amplitude = f"{abs(a):.2f}"
    else:
        # 탄젠트 함수 불연속점 처리
        y_base = np.tan(x)
        y_mod = a * np.tan(b * (x - c * np.pi)) + d
        y_base[np.abs(y_base) > 10] = np.nan
        y_mod[np.abs(y_mod) > 10] = np.nan
        title_str = f"$y = {a:.2f} \\cdot \\tan({b:.2f}(x - {c:.2f}\\pi)) + {d:.2f}$"
        period = f"{1/abs(b):.2f} $\\pi$" if b != 0 else "정의되지 않음 (b=0)"
        amplitude = "없음 (최대/최소값 없음)"

    # 레이아웃 분할
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader(f"📊 그래프: {title_str}")
        
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(x, y_base, label="기본형 $y=f(x)$", color="gray", linestyle="--", alpha=0.6)
        ax.plot(x, y_mod, label="변형된 함수", color="#007ACC", linewidth=2.5)
        
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
        - **$a = {a}$**: 진폭 조절 ($|a|$)
        - **$b = {b}$**: 주기 조절 (주기 = 기본주기 / $|b|$)
        - **$c = {c}$**: x축 평행이동 ($+{c}\\pi$ 만큼)
        - **$d = {d}$**: y축 평행이동 ($+{d}$ 만큼)
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
    d_sign = f"+ {q_d}" if q_d > 0 else f"- {abs(q_d)}"
    st.info(f"### ❓ 문제: 함수 $y = {q_a} \\cdot \\{q_func}({q_b}x) {d_sign}$ 의 특성을 구하세요.")

    col_q1, col_q2, col_q3 = st.columns(3)
    
    with col_q1:
        user_amp = st.number_input("1. 진폭 (Amplitude)", value=1.0, step=1.0, key="quiz_amp_input")
    with col_q2:
        user_period_coeff = st.number_input("2. 주기 ($\pi$ 앞의 계수값, 예: 2$\pi$면 2 입력)", value=1.0, step=0.5, key="quiz_period_input")
    with col_q3:
        user_d = st.number_input("3. y축 평행이동 값 (d)", value=0.0, step=1.0, key="quiz_d_input")

    # 정답 계산
    ans_amp = float(q_a)
    ans_period_coeff = 2.0 / q_b  # 2π/b 이므로 π 앞의 계수
    ans_d = float(q_d)

    col_btn1, col_btn2 = st.columns([1, 4])
    
    with col_btn1:
        if st.button("정답 확인 🎯"):
            correct = True
            
            if abs(user_amp - ans_amp) < 0.01:
                st.success("1. 진폭 정답입니다! 🎉")
            else:
                st.error(f"1. 진폭 오답입니다. (정답: {ans_amp})")
                correct = False

            if abs(user_period_coeff - ans_period_coeff) < 0.01:
                st.success(f"2. 주기 정답입니다! ({ans_period_coeff:.2f}$\\pi$) 🎉")
            else:
                st.error(f"2. 주기 오답입니다. (정답: {ans_period_coeff:.2f}$\\pi$)")
                correct = False

            if abs(user_d - ans_d) < 0.01:
                st.success("3. y축 평행이동 정답입니다! 🎉")
            else:
                st.error(f"3. y축 평행이동 오답입니다. (정답: {ans_d})")
                correct = False

            if correct:
                st.balloons()

    with col_btn2:
        if st.button("새 문제 생성 🔄"):
            st.session_state.quiz_a = random.choice([1, 2, 3, 4, 5])
            st.session_state.quiz_b = random.choice([1, 2, 4])
            st.session_state.quiz_d = random.choice([-3, -2, -1, 1, 2, 3])
            st.session_state.quiz_func = random.choice(["sin", "cos"])
            st.rerun()
