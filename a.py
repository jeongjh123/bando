import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# 제목
st.title("반도체 공정 시뮬레이터")

# 사이드바 입력
st.sidebar.header("공정 조건 선택")
process = st.sidebar.selectbox("공정 선택", ["산화", "식각", "증착"])
model_type = st.sidebar.radio("모델 선택", ["이론적", "현실적(실험적)"])
temp = st.sidebar.slider("온도 (°C)", 200, 1000, 600, step=50)
time = st.sidebar.slider("공정 시간 (분)", 1, 120, 30)

# 출력 요약
st.write(f"**{process}** 공정 / **{model_type}** 모델")
st.write(f"온도: **{temp}°C**, 시간: **{time}분**")

# 시간 배열
times = np.linspace(0, time, 100)

# ---- 공정별 모델 ----
if process == "산화":
    st.subheader("Oxide Thickness")

    A = 0.1       # μm
    B = 0.0117    # μm²/min

    # Deal-Grove 모델
    thickness_deal_grove = [(-A + np.sqrt(A**2 + 4 * B * t)) / 2 * 1000 for t in times]  # nm

    if model_type == "이론적":
        thickness = thickness_deal_grove
    else:
        # 현실적 모델: 포화형 (exponential saturation)
        saturation_thickness = 500  # nm
        rate = 0.05  # 1/min
        thickness = saturation_thickness * (1 - np.exp(-rate * times))

    # 결과 출력
    st.write(f"Estimated Oxide Thickness: **{round(thickness[-1], 2)} nm**")

    # 그래프
    fig, ax = plt.subplots()
    if model_type == "이론적":
        ax.plot(times, thickness, label="Theoretical Model", color='green')
    else:
        ax.plot(times, thickness, label="Exponential Saturation Model", color='green')
        ax.plot(times, thickness_deal_grove, '--', label="Theoretical Deal-Grove Model", color='gray')
    ax.set_xlabel("Time (min)")
    ax.set_ylabel("Oxide Thickness (nm)")
    ax.set_title("Change in Oxide Thickness")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

elif process == "증착":
    st.subheader("Deposition Thickness")

    deposition_rate = 0.08 * (temp / 100)  # nm/min
    thickness_linear = deposition_rate * times

    if model_type == "이론적":
        thickness = thickness_linear
    else:
        # 현실적: 초기 빠르다가 포화되는 모델 (예: 공급 제한형)
        max_thickness = deposition_rate * time * 1.1
        rate = 0.03
        thickness = max_thickness * (1 - np.exp(-rate * times))

    st.write(f"Estimated Deposition Thickness: **{round(thickness[-1], 2)} nm**")

    fig, ax = plt.subplots()
    if model_type == "이론적":
        ax.plot(times, thickness, label="Theoretical Model", color='blue')
    else:
        ax.plot(times, thickness, label="Exponential Saturation Model", color='blue')
        ax.plot(times, thickness_linear, '--', label="Theoretical Model", color='gray')
    ax.set_xlabel("Time (min)")
    ax.set_ylabel("Deposited Thickness (nm)")
    ax.set_title("Change in Deposition Thickness")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

elif process == "식각":
    st.subheader("Etch Depth")

    etch_rate = 0.05 * (temp / 100)  # nm/min
    depth_linear = etch_rate * times

    if model_type == "이론적":
        depth = depth_linear
    else:
        # 현실적: 반응 부산물/농도 감소 고려한 속도 감소형 모델
        decay_rate = 0.03
        depth = (etch_rate / decay_rate) * (1 - np.exp(-decay_rate * times))

    st.write(f"Estimated Etch Depth: **{round(depth[-1], 2)} nm**")

    fig, ax = plt.subplots()
    if model_type == "이론적":
        ax.plot(times, depth, label="Theoretical Model", color='red')
    else:
        ax.plot(times, depth, label="Decay Saturation Model", color='red')
        ax.plot(times, depth_linear, '--', label="Theoretical Model", color='gray')
    ax.set_xlabel("Time (min)")
    ax.set_ylabel("Etched Depth (nm)")
    ax.set_title("Change in Etch Depth")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

# 공정 이론 설명
st.markdown("---")
with st.expander("공정 이론 설명"):
    if process == "산화":
        st.markdown("""
        - **산화 공정**은 실리콘에 산화막(SiO₂)을 형성하는 공정입니다.  
        - **Deal-Grove 모델**은 시간에 따라 산화 속도가 느려지는 현상을 설명합니다.  
        - 현실에서는 포화, 확산 제한 등으로 더 복잡한 거동을 보입니다.
        """)
    elif process == "식각":
        st.markdown("""
        - **식각 공정**은 박막을 제거하는 공정입니다.  
        - 일정한 식각 속도를 가정하면 선형 증가하지만,  
        - 현실에서는 반응 부산물 누적이나 반응물 부족으로 속도가 감소할 수 있습니다.
        """)
    elif process == "증착":
        st.markdown("""
        - **증착 공정**은 박막을 쌓는 공정입니다.  
        - 이론적으로는 일정한 속도이지만,  
        - 현실에서는 반응물 농도 감소나 표면 반응 포화로 증착률이 줄어들기도 합니다.
        """)
