import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 페이지 기본 설정
st.set_page_config(
    page_title="고등 수학: 삼각함수 학습용 웹",
    page_icon="📐",
    layout="wide"
)

# 한글 폰트 설정 (기본 폰트 사용 시 깨짐 방지 처리)
plt.rcParams['axes.unicode_minus'] = False

st.title("📐 고등학생을 위한 삼각함수 학습 파트너")
st.write("슬라이더를 조절하며 삼각함수 그래프의 변형(진폭, 주기, 평행이동)을 직관적으로 이해해 보세요!")

st.sidebar.header("⚙️ 함수 및 파라미터 설정")

# 1. 삼각함수 선택
func_choice = st.sidebar.selectbox(
    "학습할 삼각함수를 선택하세요",
    ["Sine (sin)", "Cosine (cos)", "Tangent (tan)"]
)

# 2. 일반식 표준형 파라미터 조절: y = a * f(b * (x - c)) + d
st.sidebar.subheader("파라미터 설정: $y = a \\cdot f(b(x - c)) + d$")

a = st.sidebar.slider("진폭/확대 (a)", min_value=0.1, max_value=5.0, value=1.0, step=0.1)
b = st.sidebar.slider("주기 조절 (b)", min_value=0.1, max_value=5.0, value=1.0, step=0.1)
c = st.sidebar.slider("x축 평행이동 (c: $\\pi$ 단위)", min_value=-2.0, max_value=2.0, value=0.0, step=0.25)
d = st.sidebar.slider("y축 평행이동 (d)", min_value=-5.0, max_value=5.0, value=0.0, step=0.5)

# x 범위 설정 (-2π ~ 2π)
x = np.linspace(-2 * np.pi, 2 * np.pi, 1000)

# 선택된 함수에 따른 값 계산
if "sin" in func_choice.lower():
    y_base = np.sin(x)
    y_mod = a * np.sin(b * (x - c * np.pi)) + d
    title_str = f"$y = {a:.1f} \\cdot \\sin({b:.1f}(x - {c:.2f}\\pi)) + {d:.1f}$"
    period = f"{2/b:.2f} $\\pi$" if b != 0 else "정의되지 않음"
    amplitude = f"{abs(a):.1f}"
elif "cos" in func_choice.lower():
    y_base = np.cos(x)
    y_mod = a * np.cos(b * (x - c * np.pi)) + d
    title_str = f"$y = {a:.1f} \\cdot \\cos({b:.1f}(x - {c:.2f}\\pi)) + {d:.1f}$"
    period = f"{2/b:.2f} $\\pi$" if b != 0 else "정의되지 않음"
    amplitude = f"{abs(a):.1f}"
else:
    # 탄젠트 함수 불연속점 처리
    y_base = np.tan(x)
    y_mod = a * np.tan(b * (x - c * np.pi)) + d
    # 큰 값 잘라내기 (그래프 왜곡 방지)
    y_base[np.abs(y_base) > 10] = np.nan
    y_mod[np.abs(y_mod) > 10] = np.nan
    title_str = f"$y = {a:.1f} \\cdot \\tan({b:.1f}(x - {c:.2f}\\pi)) + {d:.1f}$"
    period = f"{1/b:.2f} $\\pi$" if b != 0 else "정의되지 않음"
    amplitude = "없음 (최대/최소값 없음)"

# 레이아웃 분할 (왼쪽: 그래프, 오른쪽: 개념 설명)
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader(f"📊 그래프: {title_str}")
    
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # 기본 y = f(x) 그래프 (점선)
    ax.plot(x, y_base, label="기본형 $y=f(x)$", color="gray", linestyle="--", alpha=0.6)
    # 변형된 그래프
    ax.plot(x, y_mod, label="변형된 함수", color="#007ACC", linewidth=2.5)
    
    # 축 설정
    ax.axhline(0, color='black', linewidth=1)
    ax.axvline(0, color='black', linewidth=1)
    ax.set_ylim(-7, 7)
    ax.set_xlim(-2 * np.pi, 2 * np.pi)
    
    # x축 눈금을 라디안 표현으로 변경
    xticks = [-2*np.pi, -1.5*np.pi, -np.pi, -0.5*np.pi, 0, 0.5*np.pi, np.pi, 1.5*np.pi, 2*np.pi]
    xtick_labels = [r'$-2\pi$', r'$-\frac{3}{2}\pi$', r'$-\pi$', r'$-\frac{1}{2}\pi$', r'$0$', 
                    r'$\frac{1}{2}\pi$', r'$\pi$', r'$\frac{3}{2}\pi$', r'$2\pi$']
    ax.set_xticks(xticks)
    ax.set_xticklabels(xtick_labels)
    
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.legend(loc="upper right")
    
    st.pyplot(fig)

with col2:
    st.subheader("💡 함수 핵심 정보")
    
    st.metric(label="현재 함수 주기 (Period)", value=period)
    st.metric(label="진폭 (Amplitude)", value=amplitude)
    
    st.markdown("---")
    st.markdown("### 📝 변수별 수식 공식")
    st.latex(r"y = a \cdot f(b(x - c)) + d")
    st.markdown(f"""
    - **$|a|$ (진폭 조절):** 그래프를 y축 방향으로 확대/축소합니다.
    - **$b$ (주기 조절):** 기본 주기를 $b$로 나눕니다. (sin/cos 주기는 $\\frac{{2\\pi}}{{|b|}}$)
    - **$c$ (평행이동):** x축 방향으로 $+c\\pi$ 만큼 이동합니다.
    - **$d$ (평행이동):** y축 방향으로 $+d$ 만큼 이동합니다.
    """)

# 하단 퀴즈 코너
st.markdown("---")
st.subheader("🧩 자율 체크 퀴즈")
with st.expander("Q. 주기와 진폭 관련 질문 (클릭해서 정답 확인)"):
    st.markdown("""
    **질문:** $y = 3\sin(2x) + 1$ 함수의 진폭과 주기는 얼마일까요?
    
    - **진폭:** $|a| = 3$ (최대값 $4$, 최소값 $-2$)
    - **주기:** $\\frac{2\\pi}{2} = \\pi$
    """)
