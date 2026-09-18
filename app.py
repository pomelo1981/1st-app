import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 페이지 기본 설정
st.set_page_config(
    page_title="고등 수학: 삼각함수 학습용 웹",
    page_icon="📐",
    layout="wide"
)

# 한글 폰트 및 마이너스 기호 깨짐 방지
plt.rcParams['axes.unicode_minus'] = False

st.title("📐 고등학생을 위한 삼각함수 학습 파트너")
st.write("원하는 숫자를 직접 입력하여 삼각함수 그래프의 변형(진폭, 주기, 평행이동)을 확인해 보세요!")

st.sidebar.header("⚙️ 함수 및 파라미터 입력")

# 1. 삼각함수 선택
func_choice = st.sidebar.selectbox(
    "학습할 삼각함수를 선택하세요",
    ["Sine (sin)", "Cosine (cos)", "Tangent (tan)"]
)

# 2. 숫자 입력 방식(st.number_input)으로 파라미터 설정: y = a * f(b * (x - c)) + d
st.sidebar.subheader("파라미터 입력: $y = a \\cdot f(b(x - c)) + d$")

a = st.sidebar.number_input("진폭/확대 (a)", value=1.0, step=0.1, format="%.2f")
b = st.sidebar.number_input("주기 조절 (b)", value=1.0, step=0.1, format="%.2f")
c = st.sidebar.number_input("x축 평행이동 (c: $\\pi$ 단위)", value=0.0, step=0.25, format="%.2f")
d = st.sidebar.number_input("y축 평행이동 (d)", value=0.0, step=0.5, format="%.2f")

# x 범위 설정 (-2π ~ 2π)
x = np.linspace(-2 * np.pi, 2 * np.pi, 1000)

# 선택된 함수에 따른 값 계산
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
    # 탄젠트 함수 계산 및 불연속점 처리
    y_base = np.tan(x)
    y_mod = a * np.tan(b * (x - c * np.pi)) + d
    
    # 큰 값 잘라내기 (탄젠트 발산으로 인한 그래프 왜곡 방지)
    y_base[np.abs(y_base) > 10] = np.nan
    y_mod[np.abs(y_mod) > 10] = np.nan
    
    title_str = f"$y = {a:.2f} \\cdot \\tan({b:.2f}(x - {c:.2f}\\pi)) + {d:.2f}$"
    period = f"{1/abs(b):.2f} $\\pi$" if b != 0 else "정의되지 않음 (b=0)"
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
    
    # y축 범위 자동/수동 조절 지원
    y_limit = max(abs(a) + abs(d) + 2, 5)
    ax.set_ylim(-y_limit, y_limit)
    ax.set_xlim(-2 * np.pi, 2 * np.pi)
    
    # x축 눈금을 라디안 기호로 표현
    xticks = [-2*np.pi, -1.5*np.pi, -np.pi, -0.5*np.pi, 0, 0.5*np.pi, np.pi, 1.5*np.pi, 2*np.pi]
    xtick_labels = [r'$-2\pi$', r'$-\frac{3}{2}\pi$', r'$-\pi$', r'$-\frac{1}{2}\pi$', r'$0$', 
                    r'$\frac{1}{2}\pi$', r'$\pi$', r'$\frac{3}{2}\pi$', r'$2\pi$']
    ax.set_xticks(xticks)
    ax.set_xticklabels(xtick_labels)
    
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.legend(loc="upper right")
    
    st.pyplot(fig)

with col2:
    st.subheader("💡 입력값 기반 핵심 분석")
    
    st.metric(label="현재 함수 주기 (Period)", value=period)
    st.metric(label="진폭 (Amplitude)", value=amplitude)
    
    st.markdown("---")
    st.markdown("### 📝 파라미터 역할 정리")
    st.latex(r"y = a \cdot f(b(x - c)) + d")
    st.markdown(f"""
    - **$a = {a}$**: y축 방향 확대/축소 (진폭 = $|a|$)
    - **$b = {b}$**: 주기 변경 (변화된 주기 = 기본주기 / $|b|$)
    - **$c = {c}$**: x축 평행이동 ($+{c}\\pi$ 만큼 이동)
    - **$d = {d}$**: y축 평행이동 ($+{d}$ 만큼 이동)
    """)

# 하단 자율학습 안내
st.markdown("---")
st.subheader("🧩 확인해보기")
st.info("사이드바에 임의의 값을 직접 입력해보면서 주기와 이동량이 어떻게 변화하는지 확인해보세요!")
