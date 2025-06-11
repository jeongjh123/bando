import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# 제목
st.title("반도체 공정 시뮬레이터")

# 사이드바 - 공정 선택 및 조건 입력
st.sidebar.header("공정 조건 선택")
process = st.sidebar.selectbox("공정 선택", ["산화", "식각", "증착"])
temp = st.sidebar.slider("온도 (°C)", min_value=200, max_value=1000, value=600, step=50)
time = st.sidebar.slider("공정 시간 (분)", min_value=1, max_value=120, value=30)

# 선택 요약
st.write(f"선택한 공정: **{process}**, 온도: {temp}°C, 시간: {time}분")

# 산화 공정 시뮬레이션
if process == "산화":
    st.subheader("산화막 두께 시뮬레이션 (Deal-Grove 모델)")

    # Dry O2 기준 상수 (온도 고정: 예시값)
    A = 0.1       # μm
    B = 0.0117    # μm²/min

    # 시간 배열 생성
    times = np.linspace(0, time, 100)
    thicknesses = [(-A + np.sqrt(A**2 + 4 * B * t_i)) / 2 * 1000 for t_i in times]  # nm

    # 결과 출력
    final_thickness = thicknesses[-1]
    st.write(f"예상 산화막 두께: **{round(final_thickness, 2)} nm**")

    # 그래프 출력
    fig, ax = plt.subplots()
    ax.plot(times, thicknesses, color='green')
    ax.set_xlabel("Time (min)")
    ax.set_ylabel("Oxide Thickness (nm)")
    ax.set_title("산화막 두께 변화 (Deal-Grove Model)")
    ax.grid(True)
    st.pyplot(fig)

# 증착 공정 시뮬레이션
elif process == "증착":
    st.subheader("증착막 두께 시뮬레이션")

    deposition_rate = 0.08 * (temp / 100)  # nm/min
    deposited_thickness = deposition_rate * time
    st.write(f"예상 증착막 두께: **{round(deposited_thickness, 2)} nm**")

    fig, ax = plt.subplots()
    ax.plot([0, time], [0, deposited_thickness], color='blue')
    ax.set_xlabel("Time (min)")
    ax.set_ylabel("Deposited Thickness (nm)")
    ax.set_title("증착막 두께 변화")
    ax.grid(True)
    st.pyplot(fig)

# 식각 공정 시뮬레이션
elif process == "식각":
    st.subheader("식각 깊이 시뮬레이션 (예시)")

    etch_rate = 0.05 * (temp / 100)  # nm/min, 임의 값
    etched_depth = etch_rate * time
    st.write(f"예상 식각 깊이: **{round(etched_depth, 2)} nm**")

    fig, ax = plt.subplots()
    ax.plot([0, time], [0, etched_depth], color='red')
    ax.set_xlabel("Time (min)")
    ax.set_ylabel("Etched Depth (nm)")
    ax.set_title("식각 깊이 변화")
    ax.grid(True)
    st.pyplot(fig)

# 공정 이론 설명
st.markdown("---")
with st.expander("공정 이론 보기"):
    if process == "산화":
        st.markdown("""
        - **산화 공정**은 실리콘 표면에 산화막(SiO₂)을 형성하는 공정입니다.  
        - 고온에서 O₂ 또는 H₂O와 반응하여 이루어지며, **Dry 산화**와 **Wet 산화** 방식이 있습니다.  
        - Deal-Grove 모델은 산화막의 성장 속도를 예측하는 고전적 모델입니다.
        """)
    elif process == "식각":
        st.markdown("""
        - **식각 공정**은 특정 영역의 박막을 제거하는 공정입니다.  
        - **습식 식각 (Wet Etching)**: 화학 용액 사용, 공정이 간단하지만 방향성이 없음.  
        - **건식 식각 (Dry Etching)**: 플라즈마를 이용한 이방성 식각 가능, 고정밀 가공에 적합.
        """)
    elif process == "증착":
        st.markdown("""
        - **증착 공정**은 웨이퍼 표면에 물질을 얇게 쌓는 공정입니다.  
        - 대표적 방식은 **CVD (화학 기상 증착)**, **PVD (물리 기상 증착)**가 있습니다.  
        - 증착 속도는 온도와 공정 조건에 따라 달라집니다.
        """)

